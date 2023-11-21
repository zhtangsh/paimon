from trade.qmt import QmtGrpcClient
from utils import rq_utils
from typing import List
import pandas as pd

host = '192.168.1.60'
port = 5000
client = QmtGrpcClient(host, port)


def latest_tick_slice(order_book_ids: List[str]) -> pd.DataFrame:
    stock_code_list = [rq_utils.reverse_id_convert(order_book_id) for order_book_id in order_book_ids]
    res = client.live_tick_data(stock_code_list)
    df = pd.DataFrame(res)
    df['order_book_id'] = df['stock_code'].apply(lambda x: rq_utils.id_convert(x))
    return df


if __name__ == '__main__':
    order_book_id_list = ['123113.XSHE', '113519.XSHG']
    df = latest_tick_slice(order_book_id_list)
    print(df)
