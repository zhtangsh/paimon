import time
from dataclasses import dataclass
from core.factory import from_qmt_position_list, from_csv_position
from trade.qmt import QmtGrpcClient
from core.model import Position, Order, OrderType
from typing import List
import datetime
import pandas as pd

import logging

from trade.qmt.constant import QmtOrderType, QmtPriceType

logger = logging.getLogger(__name__)


@dataclass
class VanillaEngine:
    qmt_client: QmtGrpcClient

    def __init__(self, host, port):
        self.qmt_client = QmtGrpcClient(host=host, port=port)

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
            cur_volume = cp.volume
            if cur_volume == 0:
                continue
            if stock_code not in expect_balance_ref:
                order = Order(stock_code=stock_code, volume=cur_volume, order_type=OrderType.STOCK_SELL)
                logger.info(f"close position: order={order}")
                res.append(order)
                continue
        for ep in expected_position:
            stock_code = ep.stock_code
            cur_volume = current_balance_ref.get(stock_code, 0)
            expected_volume = ep.volume
            if cur_volume == expected_volume:
                continue
            if cur_volume < expected_volume:
                order = Order(stock_code=stock_code, volume=expected_volume - cur_volume,
                              order_type=OrderType.STOCK_BUY)
                logger.info(f"open position: order={order}")
                res.append(order)
            else:
                order = Order(stock_code=stock_code, volume=cur_volume - expected_volume,
                              order_type=OrderType.STOCK_SELL)
                logger.info(f"close position: stock_code={stock_code},amount={cur_volume - expected_volume}")
                res.append(order)
        return res

    def execute_order(self, order_list: List[Order]):
        """
        执行Order
        :param order_list: order列表
        :return:
        """
        logger.info(f"execute_order: order_list={order_list}")
        qmt_order_id_list = []
        for order in order_list:
            logger.info(f"submit order: order={order}")
            stock_code = order.stock_code
            volume = order.volume
            order_type = QmtOrderType.STOCK_BUY if order.order_type == OrderType.STOCK_BUY else QmtOrderType.STOCK_SELL
            if stock_code.endswith("SZ"):
                price_type = QmtPriceType.MARKET_SZ_CONVERT_5_CANCEL
            else:
                price_type = QmtPriceType.MARKET_SH_CONVERT_5_CANCEL
            order_id = self.qmt_client.order_stock(
                stock_code=stock_code, order_type=order_type, order_volume=volume, price_type=price_type,
                price=0, strategy_name='test', order_remark='test')
            qmt_order_id_list.append(order_id)
        logger.info(f"qmt_order_id_list:{qmt_order_id_list}")
        return None

    def execute_order_v2(self, order_list: List[Order]):
        """
        执行Order
        :param order_list: order列表
        :return:
        """
        logger.info(f"execute_order_v2: order_list={order_list}")
        qmt_order_id_list = []
        for order in order_list:
            logger.info(f"submit order: order={order}")
            stock_code = order.stock_code
            volume = order.volume
            order_type = QmtOrderType.STOCK_BUY if order.order_type == OrderType.STOCK_BUY else QmtOrderType.STOCK_SELL
            price_type = QmtPriceType.LATEST_PRICE
            order_id = self.qmt_client.order_stock(
                stock_code=stock_code, order_type=order_type, order_volume=volume, price_type=price_type,
                price=0, strategy_name='test', order_remark='test')
            qmt_order_id_list.append(order_id)
        logger.info(f"qmt_order_id_list:{qmt_order_id_list}")
        return None

    def submit_target_order(self, target_order):
        date = target_order.get("date")
        expected_position = target_order.get("expected_position")
        if date < datetime.date.today():
            logger.info(f"过去日期，跳过:{target_order}")
            return
        current_position = self.check_current_position()
        logger.info(f"current_position:{current_position}")
        logger.info(f"expected_position:{expected_position}")
        order_list = self.generate_order(current_position, expected_position)
        logger.info(f"order_list:{order_list}")
        self.execute_order(order_list)

    def submit_target_order_v2(self, target_order, sleep_second: int = 1):
        """
        下单版本2
        1. 以最新价下单，每个1s进行check，如果未成交则撤单，然后重新下单
        :param target_order: 目标Order
        :param sleep_second: 下单查询间隔
        :return:
        """
        date = target_order.get("date")
        expected_position = target_order.get("expected_position")
        if date < datetime.date.today():
            logger.info(f"过去日期，跳过:{target_order}")
            return
        count = 0
        today = datetime.date.today()
        open_datetime = datetime.datetime(today.year, today.month, today.day, 9, 30)
        while True:
            now = datetime.datetime.now()
            if now < open_datetime:
                time.sleep(0.5)
                logger.info(f"submit_target_order_v2: 未到开盘时间，sleep")
                continue
            order_list = self.place_order_for_loop(expected_position)
            if len(order_list) == 0:
                logger.info("submit_target_order_v2: order_list为空，退出循环")
                break
            count += 1
            time.sleep(sleep_second * (count // 10 + 1))

    def place_order_for_loop(self, expected_position: List[Position]) -> List[Order]:
        """
        for loop中的下单逻辑
        :param expected_position: 期望仓位
        :return:
        """
        # 检查可撤单
        cancelable_order_list = self.qmt_client.get_stock_orders(cancelable_only=True)
        for cancelable_order in cancelable_order_list:
            self.qmt_client.cancel_order_stock(cancelable_order.order_id)
            logger.info(f"place_order_for_loop:撤单{cancelable_order.order_id}")
        current_position = self.check_current_position()
        logger.info(f"place_order_for_loop: current_position:{current_position},expected_position:{expected_position}")
        order_list = self.generate_order(current_position, expected_position)
        self.execute_order_v2(order_list)
        return order_list

    def close_cash(self):
        asset = self.qmt_client.get_stock_asset()
        cash = float(asset.cash)
        order_volume = int(cash // 1000)
        stock_code = '204001.SH'
        price_type = QmtPriceType.LATEST_PRICE
        self.qmt_client.order_stock(stock_code=stock_code, order_type=OrderType.STOCK_SELL, order_volume=order_volume,
                                    price_type=price_type, price=0, strategy_name='test', order_remark='国债逆回购')
