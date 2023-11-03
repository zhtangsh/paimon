from trade.qmt import QmtGrpcClient
from trade.qmt import QmtOrder
from typing import List
import pandas as pd


def to_order_statistic(order_list: List[QmtOrder]):
    res = []
    for order in order_list:
        res.append({
            'order_volume': order.order_volume,
            'stock_code': order.stock_code,
            'order_time': order.order_time,
            'order_price': order.price,
            'traded_price': order.traded_price,
            'traded_volume': order.traded_volume,
        })
    df = pd.DataFrame(res)
    df.to_excel('order.xlsx')
    return res


if __name__ == '__main__':
    host = '192.168.1.60'
    port = 5000
    qmt_client = QmtGrpcClient(host=host, port=port)
    order_list = qmt_client.get_stock_orders(cancelable_only=False)
    to_order_statistic(order_list)
