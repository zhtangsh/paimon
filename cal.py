import pandas as pd
from utils import rq_utils
from adapter.rqdata import convertible
import rqdatac as rq

rq.init()


def slippage(x):
    order_type = x['order_type']
    traded_price = x['traded_price']
    open_price = x['open']
    direction = 1 if order_type == 23 else -1
    return direction * (traded_price - open_price)


trade_df = pd.read_excel('trade.xlsx', index_col=0)
mask = (trade_df['account_id'] != 55010000) & (trade_df['order_id'] != 0)
trade_df = trade_df[mask]
start_date = '2023-11-07'
end_date = '2023-11-10'
trade_df['order_book_id'] = trade_df['stock_code'].apply(lambda x: rq_utils.id_convert(x))
trade_df['trade_date'] = pd.to_datetime(trade_df['traded_time']).dt.date
order_book_id_list = trade_df['order_book_id'].drop_duplicates().to_list()
mkt_price_df = convertible.get_price(order_book_ids=order_book_id_list, start_date=start_date,
                                     end_date=end_date).reset_index()
mkt_price_df['trade_date'] = mkt_price_df['date'].dt.date
merged = trade_df.merge(mkt_price_df, how='left', on=['order_book_id', 'trade_date'])
filterer_column = ['order_id', 'order_type', 'stock_code', 'traded_price', 'traded_volume', 'traded_id', 'open',
                   'traded_time']
df_filtered = merged[filterer_column].copy()
df_filtered['slippage'] = df_filtered.apply(lambda x: slippage(x), axis=1)
df_filtered.to_excel('trade_ana.xlsx')
