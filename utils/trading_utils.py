import pandas as pd
from adapter.db.datasource import DbEngineFactory


def latest_trading_date():
    engine = DbEngineFactory.engine_rqdata()
    sql = "SELECT * FROM trading_date " \
          "ORDER BY trading_date desc " \
          "LIMIT 10"
    df = pd.read_sql(sql, con=engine)
    if df is None or df.empty:
        raise ValueError('no trading date data')
    return df['trading_date'].to_list()[0]


if __name__ == '__main__':
    latest_trading_date()
