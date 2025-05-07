import pandas as pd
from adapter.db.datasource import DbEngineFactory
from utils import email_utils


def check_table(engine, table_name: str, date_col: str, record_time_col: str = 'record_time'):
    sql = f'SELECT * FROM {table_name} WHERE DATE({date_col}) != DATE({record_time_col})'
    df = pd.read_sql(sql, con=engine)
    if df is None or df.empty:
        return None
    return f"表名={table_name},存在异常数据，请人工查看，异常数据尺寸={str(df.shape)}"


def entrypoint():
    engine = DbEngineFactory.engine_paimon()
    error = check_table(engine, 'trade_data', 'traded_time')
    receiver = "zhtangsh@163.com"
    if error:
        message = error
        email_utils.send_mail_163(recv=receiver, title="paimon数据库的trade_data有误,请人工查看", content=message, file_path=None)


if __name__ == '__main__':
    entrypoint()
