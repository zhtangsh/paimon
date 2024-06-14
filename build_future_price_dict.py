import pandas as pd
import re
from adapter.db.datasource import DbEngineFactory


def fetch_data(engine):
    sql = "SELECT s_info_code,s_info_mfprice FROM CFuturesContPro"
    df = pd.read_sql(sql=sql, con=engine)
    return df


def test():
    engine = DbEngineFactory.engine_by_key('wind_fofstar')
    engine2 = DbEngineFactory.engine_by_key('paimondev')
    df = fetch_data(engine)
    s_info_mfprice_list = df['s_info_mfprice'].unique().tolist()
    res = []
    pattern = '(^0\.\d{1,})|(^[1-9]\d{0,})'
    for s_info_mfprice in s_info_mfprice_list:
        re_result = re.findall(pattern, s_info_mfprice)[0]
        mfprice = re_result[0] if re_result[0] != '' else re_result[1]
        df_search = df[df['s_info_mfprice'] == s_info_mfprice]
        s_info_code_list = df_search['s_info_code'].unique().tolist()
        for s_info_code in s_info_code_list:
            res.append({
                's_info_code': s_info_code,
                'mfprice': mfprice
            })
    df = pd.DataFrame(res)
    df.to_sql(name='future_min_price', con=engine2, if_exists='append', index=False)


if __name__ == '__main__':
    test()
