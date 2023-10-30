import datetime
import logging
from utils import sys_utils
from trade.qmt.client import *

dummy_target_order = {
    "date": datetime.date(2023, 10, 27),
    "deadline_second": 60 * 5,
    "expected_position": [
        {
            "order_book_id": "123096.XSHE",
            "amount": 10,
        },
        {
            "order_book_id": "123044.XSHE",
            "amount": 10,
        },
        {
            "order_book_id": "128132.XSHE",
            "amount": 10,
        },
    ]
}

logger = logging.getLogger(__name__)

client = QmtGrpcClient('192.168.1.60', 5000)


def check_current_position():
    stock_position_list = client.get_stock_positions()
    for stock_position in stock_position_list:
        print(stock_position)
    return [
        {
            "order_book_id": "123096.XSHE",
            "amount": 5,
        },
        {
            "order_book_id": "123044.XSHE",
            "amount": 20,
        }
    ]


def generate_order(current_position, expected_position):
    """
    通过现有持仓和期望持仓的对比，生成需要进行的操作
    :param current_position: 当前持仓
    :param expected_position: 期望持仓
    :return:
    """
    logger.info(f"generate_order:current_position={current_position},expected_position={expected_position}")
    current_balance_ref = {ele.get('order_book_id'): ele.get('amount') for ele in current_position}
    expect_balance_ref = {ele.get('order_book_id'): ele.get('amount') for ele in expected_position}
    res = []
    for position in current_position:
        order_book_id = position['order_book_id']
        cur_amount = position['amount']
        if order_book_id not in expect_balance_ref:
            logger.info(f"close position: order_book_id={order_book_id},amount={cur_amount}")
            res.append({
                'order_book_id': position['order_book_id'],
                'type': 'sell',
                'amount': position['amount']
            })
            continue
    for position in expected_position:
        order_book_id = position['order_book_id']
        cur_amount = current_balance_ref.get(order_book_id, 0)
        expected_amount = position['amount']
        if cur_amount == expected_amount:
            continue
        if cur_amount < expected_amount:
            logger.info(f"open position: order_book_id={order_book_id},amount={expected_amount - cur_amount}")
            res.append({
                'order_book_id': order_book_id,
                'type': 'buy',
                'amount': expected_amount - cur_amount
            })
        else:
            logger.info(f"close position: order_book_id={order_book_id},amount={cur_amount - expected_amount}")
            res.append({
                'order_book_id': order_book_id,
                'type': 'buy',
                'amount': cur_amount - expected_amount
            })
    return res


def execute_order(order_list):
    logger.info(f"execute_order: order_list={order_list}")
    qmt_order_list = []
    qmt_order_status_ref = {}
    for order in order_list:
        logger.info(f"submit order: order={order}")
    return None


def place_order(target_order):
    date = target_order.get("date")
    expected_position = target_order.get("expected_position")
    if date < datetime.date.today():
        logger.info(f"过去日期，跳过:{target_order}")
        return
    current_position = check_current_position()
    logger.info(f"current_position:{current_position}")
    logger.info(f"expected_position:{expected_position}")
    order_list = generate_order(current_position, expected_position)
    logger.info(f"order_list:{order_list}")
    execute_order(order_list)


if __name__ == '__main__':
    sys_utils.logging_config()
    place_order(dummy_target_order)
