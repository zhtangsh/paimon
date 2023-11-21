from typing import List
import pandas as pd
from adapter.rqdata import general

tick_column = ['order_book_id', 'open', 'last', 'high', 'low', 'volume', 'a1', 'a2', 'a3', 'a4', 'a5', 'a1_v', 'a2_v',
               'a3_v', 'a4_v', 'a5_v', 'b1', 'b2', 'b3', 'b4', 'b5', 'b1_v', 'b2_v', 'b3_v', 'b4_v', 'b5_v']


def latest_tick_slice(order_book_ids: List[str]) -> pd.DataFrame:
    df = general.get_live_ticks(order_book_ids=order_book_ids)
    if df is None:
        return pd.DataFrame()
    return df.reset_index().groupby('order_book_id').last().reset_index()[tick_column].copy()


if __name__ == '__main__':
    import rqdatac as rq

    rq.init()
    order_book_id_list = ['123113.XSHE', '113519.XSHG']
    df = latest_tick_slice(order_book_id_list)
    print(df)
