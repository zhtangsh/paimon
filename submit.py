from adapter.db.datasource import DbEngineFactory
import pandas as pd


def build_trade_report(stock_code, trade_last_month):
    sql = f"SELECT * FROM trade_data where strategy_name ='' and stock_code='{stock_code}'"
    name = '唐子涵'
    sh_account = 'A123921115'
    sz_account = '0366728350'
    if stock_code.endswith('SZ'):
        account = sz_account
    else:
        account = sh_account
    df = pd.read_sql(sql, con=DbEngineFactory.engine_paimon())
    res = []
    for _, row in df.iterrows():
        traded_time = row['traded_time']
        traded_volume = row['traded_volume']
        order_type = row['order_type']
        traded_price = row['traded_price']
        buy_info = ''
        sell_info = ''
        if order_type == '股票买入':
            buy_info = f"买入时间={traded_time},买入价格={traded_price},买入数量={traded_volume}"
        else:
            sell_info = f"卖出时间={traded_time},卖出价格={traded_price},卖出数量={traded_volume}"
        data = {
            'account': account,
            'name': name,
            'date': traded_time.date(),
            'note': '',
            'stock_code': stock_code,
            'volume': traded_volume,
            'trade_last_month': trade_last_month,
            'buy_info': buy_info,
            'sell_info': sell_info,
        }
        res.append(data)
    return pd.DataFrame(res)


if __name__ == '__main__':
    stock_code = '511090.SH'
    df = build_trade_report(stock_code, trade_last_month='否', )
    df.to_sql('daily_trade_report', con=DbEngineFactory.engine_paimon(), if_exists='append', index=False)
    print('hi')
