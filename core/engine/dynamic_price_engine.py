import time
from dataclasses import dataclass
from core.factory import from_qmt_position_list, from_csv_position
from trade.qmt import QmtGrpcClient, QmtOrder
from core.model import Position, Order, OrderType
from utils import rq_utils
from typing import List, Dict
import datetime
import pandas as pd

import logging

from trade.qmt.constant import QmtOrderType, QmtPriceType
from adapter.rqdata import std as rq_std
from adapter.qmt import std as qmt_std

logger = logging.getLogger(__name__)


@dataclass
class DynamicPriceEngine:
    """
    使用动态价格来下Limit Order的交易引擎
    1. 使用micro price进行下单
    2. 动态检测micro price的变化，进而优化下单价格
    """
    qmt_client: QmtGrpcClient
    price_df: pd.DataFrame
    spread_tolerance: float

    def __init__(self, host, port, spread_tolerance=0.01, strategy_name: str = 'test', data_feed: str = 'rqdata'):
        self.qmt_client = QmtGrpcClient(host=host, port=port)
        self.spread_tolerance = spread_tolerance
        self.current_order_list = []
        self.strategy_name = strategy_name
        self.data_feed = data_feed
        # 待确认委托列表
        self.to_verify_order_list: List[Order] = []
        # 委托列表
        self.limit_order_queue: List[Order] = []
        # 异常委托列表，需手动确认
        self.error_order_list: List[Order] = []

    def check_current_position(self) -> List[Position]:
        """
        检查当前账户的仓位信息
        :return: 仓位信息列表
        """
        stock_position_list = self.qmt_client.get_stock_positions()
        return from_qmt_position_list(stock_position_list)

    def build_target_order_csv(self, filename: str, order_date: datetime.date = None, deadline_second: int = 60 * 5):
        """
        从csv生成订单列表
        :param filename: csv输入数据
        :param order_date: 下单日期
        :param deadline_second: 期待完成的deadline
        :return:
        """
        if order_date is None:
            order_date = datetime.date.today()
        df = pd.read_csv(filename, index_col=0)
        df = df[df['order_status'] == 'normal']
        col_mask = ['order_book_id', 'order_int']
        values = df[col_mask].to_dict("records")
        expected_position = [from_csv_position(value) for value in values]
        return {
            "date": order_date,
            "deadline_second": deadline_second,
            "expected_position": expected_position
        }

    def generate_order(self, current_position: List[Position], expected_position: List[Position]) -> List[Order]:
        """
        通过现有持仓和期望持仓的对比，生成需要进行的操作
        :param current_position: 当前持仓
        :param expected_position: 期望持仓
        :return:
        """
        logger.info(f"generate_order:current_position={current_position},expected_position={expected_position}")
        current_balance_ref = {ele.stock_code: ele.volume for ele in current_position}
        expect_balance_ref = {ele.stock_code: ele.volume for ele in expected_position}
        res = []
        for cp in current_position:
            stock_code = cp.stock_code
            order_book_id = rq_utils.id_convert(stock_code)
            cur_volume = cp.volume
            if cur_volume == 0:
                continue
            if stock_code not in expect_balance_ref:
                order = Order(stock_code=stock_code, volume=cur_volume, order_type=OrderType.STOCK_SELL,
                              order_book_id=order_book_id)
                logger.info(f"generate_order: close position, order={order}")
                res.append(order)
                continue
        for ep in expected_position:
            stock_code = ep.stock_code
            order_book_id = rq_utils.id_convert(stock_code)
            cur_volume = current_balance_ref.get(stock_code, 0)
            expected_volume = ep.volume
            if cur_volume == expected_volume:
                continue
            if cur_volume < expected_volume:
                order = Order(stock_code=stock_code, volume=expected_volume - cur_volume,
                              order_type=OrderType.STOCK_BUY, order_book_id=order_book_id)
                logger.info(f"generate_order: open position, order={order}")
                res.append(order)
            else:
                order = Order(stock_code=stock_code, volume=cur_volume - expected_volume,
                              order_type=OrderType.STOCK_SELL, order_book_id=order_book_id)
                logger.info(
                    f"generate_order: close position, stock_code={stock_code},amount={cur_volume - expected_volume}")
                res.append(order)
        return res

    def query_current_price(self, order_book_id_list) -> None:
        """
        获得当前价格信息
        :param order_book_id_list: 债券列表
        """
        if not order_book_id_list or len(order_book_id_list) == 0:
            self.price_df = pd.DataFrame()
            return
        if self.data_feed == 'rqdata':
            self.price_df = rq_std.latest_tick_slice(order_book_ids=order_book_id_list)
        else:
            self.price_df = qmt_std.latest_tick_slice(order_book_ids=order_book_id_list)
        self.price_df['micro_price'] = (self.price_df['a1'] * self.price_df['a1_v'] + self.price_df['b1'] *
                                        self.price_df['b1_v']) / (self.price_df['a1_v'] + self.price_df['b1_v'])

    def cancel_order(self, order: Order) -> bool:
        """
        调用qmt接口进行撤单操作
        :param order: 待撤的委托
        :return: 是否取消成功
        """
        qmt_order_id = order.qmt_order_id
        # ok:0:成功,  -1:委托已完成撤单失败, -2:未找到对应委托编号撤单失败, -3:账号未登陆撤单失败
        ok = self.qmt_client.cancel_order_stock(qmt_order_id)
        if ok == -2 or ok == -3:
            # 撤单失败，或许已成
            return False
        # 订单已撤，更新已交易信息
        full_order_ref = self.full_order_ref()
        canceled_order = full_order_ref[qmt_order_id]
        order.traded_volume = order.traded_volume + canceled_order.traded_volume
        return True

    def execute_order(self, order: Order) -> None:
        """
        执行委托
        1. 使用micro price下单
        2. 如果当前的micro price与订单的micro price大于阈值，则调整委托
        3. 如果当前的micro price与订单的micro price小于阈值，则不做调整
        4. 如果委托未在qmt下单，则直接以当前micro price下单
        :param order: order
        """
        logger.info(f"execute_order: 开始执行订单, order={order}")
        stock_code = order.stock_code
        order_book_id = order.order_book_id
        cur_micro_price = self.price_df[self.price_df['order_book_id'] == order_book_id].iloc[-1]['micro_price']
        if order.qmt_submitted():
            price_diff = abs(cur_micro_price - order.price)
            if price_diff > self.spread_tolerance:
                logger.info(f"execute_order: price_diff={price_diff},micro price的价差大于阈值，调整委托")
                ok = self.cancel_order(order)
                if not ok:
                    logger.info(f"execute_order: 撤单异常,res={ok}，待确认.order={order}")
                    self.to_verify_order_list.append(order)
                    return
                else:
                    logger.info(f"execute_order: 撤单成功, res={ok},下个循环再下单")
                    order.qmt_order_id = -1
                    self.limit_order_queue.append(order)
                    return
            else:
                logger.info(f"execute_order: price_diff={price_diff},micro price的价差小于阈值，继续持有委托")
                return
        price = round(cur_micro_price, 3)
        volume = order.volume_to_trade()
        # 如果是买单，检查余额是否够用，不够则在下一个tick再下单
        if order.order_type == OrderType.STOCK_BUY:
            asset = self.qmt_client.get_stock_asset()
            if price * volume > asset.cash:
                logger.info(f"execute_order: 余额不足,order={order}放回队列，下一tick再进行下单.")
                self.limit_order_queue.append(order)
                return
        order_type = QmtOrderType.STOCK_BUY if order.order_type == OrderType.STOCK_BUY else QmtOrderType.STOCK_SELL
        price_type = QmtPriceType.FIX_PRICE
        qmt_order_id = self.qmt_client.order_stock(
            stock_code=stock_code, order_type=order_type, order_volume=volume, price_type=price_type,
            price=price, strategy_name=self.strategy_name, order_remark='test')
        order.qmt_order_id = qmt_order_id
        order.price = price
        order.order_create_ts = time.time_ns() // 1000
        logger.info(f"execute_order: 结束执行订单, order={order}")

    def order_execution_pool_tick(self) -> None:
        """
        执行Order
        """
        self.prune_limit_order_pool()
        self.verify_order()
        order_book_id_list = [order.order_book_id for order in self.limit_order_queue]
        self.query_current_price(order_book_id_list)
        order_snapshot = [order for order in self.limit_order_queue]
        for order in order_snapshot:
            self.execute_order(order)

    def verify_order(self) -> None:
        """
        验证Order
        :return:
        """
        if len(self.to_verify_order_list) == 0:
            return
        full_order_ref = self.full_order_ref()
        for to_verify_order in self.to_verify_order_list:
            qmt_order_id = to_verify_order.qmt_order_id
            if qmt_order_id not in full_order_ref:
                logger.info(f"order not found in order history {to_verify_order}")
                self.error_order_list.append(to_verify_order)
                continue
            qmt_order = full_order_ref[qmt_order_id]
            if qmt_order.traded_volume + to_verify_order.traded_volume == to_verify_order.volume:
                continue
            else:
                self.error_order_list.append(to_verify_order)
        self.to_verify_order_list.clear()

    def full_order_ref(self) -> Dict[int, QmtOrder]:
        return {order.order_id: order for order in self.qmt_client.get_stock_orders(cancelable_only=False)}

    def cancellable_order_ref_tick(self) -> Dict[str, QmtOrder]:
        return {order.stock_code: order for order in self.qmt_client.get_stock_orders(cancelable_only=True)}

    def prune_limit_order_pool(self):
        # 获得可撤单的委托列表
        cancellable_order_ref = self.cancellable_order_ref_tick()
        next_limit_order_queue = []
        for order in self.limit_order_queue:
            if order.qmt_order_id == -1:
                # 初始订单，还未在qmt下单
                next_limit_order_queue.append(order)
                continue
            if order.stock_code not in cancellable_order_ref:
                # qmt订单不可撤销，默认该订单已成
                self.to_verify_order_list.append(order)
                continue
            next_limit_order_queue.append(order)
        logger.info(f"prune_limit_order_pool: 调整后的limit_order_queue={next_limit_order_queue}")
        self.limit_order_queue = next_limit_order_queue

    def submit_target_order(self, target_order, check_period: int = 0.01) -> None:
        """
        - 以micro price下单
        - 实时监控当前价格与订单价格的偏差，及时调整订单
        :param target_order: 目标Order
        :param check_period: 下单查询间隔
        """
        date = target_order.get("date")
        expected_position = target_order.get("expected_position")
        if date < datetime.date.today():
            logger.info(f"过去日期，跳过:{target_order}")
            return
        today = datetime.date.today()
        open_datetime_phase1 = datetime.datetime(today.year, today.month, today.day, 9, 30)
        close_datetime_phase1 = datetime.datetime(today.year, today.month, today.day, 11, 30)
        open_datetime_phase2 = datetime.datetime(today.year, today.month, today.day, 13, 00)
        close_datetime_phase2 = datetime.datetime(today.year, today.month, today.day, 15, 00)
        # 检查当前持仓
        current_position = self.check_current_position()
        # 生成当前订单列表: order_list
        order_list = self.generate_order(current_position, expected_position)
        # 依据订单列表生成订单池
        self.limit_order_queue = [order for order in order_list]
        # 循环执行订单
        while True:
            now = datetime.datetime.now()
            # 检查当前时间，是否未开盘
            is_open_phase1 = open_datetime_phase1 < now < close_datetime_phase1
            is_open_phase2 = open_datetime_phase2 < now < close_datetime_phase2
            if not (is_open_phase1 or is_open_phase2):
                time.sleep(0.5)
                logger.info(f"submit_target_order: 未到开盘时间，sleep")
                continue
            # 如果当前订单池为空，退出循环
            if len(self.limit_order_queue) == 0:
                logger.info("submit_target_order: limit_order_pool为空，退出循环")
                logger.info(f"submit_target_order: 推出时的error_order_list{self.error_order_list}")
                break
            self.order_execution_pool_tick()
            time.sleep(check_period)

    def close_cash(self):
        asset = self.qmt_client.get_stock_asset()
        cash = float(asset.cash)
        order_volume = int(cash // 1000)
        stock_code = '204001.SH'
        price_type = QmtPriceType.LATEST_PRICE
        self.qmt_client.order_stock(stock_code=stock_code, order_type=OrderType.STOCK_SELL, order_volume=order_volume,
                                    price_type=price_type, price=0, strategy_name='test', order_remark='国债逆回购')
