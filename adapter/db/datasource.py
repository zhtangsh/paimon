from sqlalchemy import create_engine
from utils import sys_utils

MYSQL_HOST = sys_utils.get_env('MYSQL_HOST', '192.168.1.60')
MYSQL_PORT = sys_utils.get_env('MYSQL_PORT', '3306')
CLICKHOUSE_HOST = sys_utils.get_env('CLICKHOUSE_HOST', '192.168.1.60')
CLICKHOUSE_PORT = sys_utils.get_env('CLICKHOUSE_PORT', '9000')


class DbEngineFactory:
    cached_engine_ref = {}

    @staticmethod
    def url():
        return f'mysql+pymysql://root:Thanatos%40mysql_0102@{MYSQL_HOST}:{MYSQL_PORT}'

    @staticmethod
    def clickhouse_url():
        return f'clickhouse+native://default:Kitten_dongli_0102@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}'

    @staticmethod
    def engine_by_key(key):
        if key not in DbEngineFactory.cached_engine_ref:
            # build cached engine
            if key == 'mktdata_intraday':
                engine = create_engine(
                    DbEngineFactory.url() + '/mktdata_intraday',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'mktdata':
                engine = create_engine(
                    DbEngineFactory.url() + '/mktdata',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'TBF':
                engine = create_engine(
                    DbEngineFactory.url() + '/TBF',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'rqdata':
                engine = create_engine(
                    DbEngineFactory.url() + '/rqdata_cbonds',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'databus':
                engine = create_engine(
                    DbEngineFactory.url() + '/databus',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'strategy_tbf':
                engine = create_engine(
                    DbEngineFactory.url() + '/strategy_tbf',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'paimon':
                engine = create_engine(
                    DbEngineFactory.url() + '/paimon',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'clickhouse_rqdata':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/rqdata_cbond',
                    pool_recycle=3600,
                    echo=False
                )
            elif key == 'clickhouse_strategy_tbf':
                engine = create_engine(
                    DbEngineFactory.clickhouse_url() + '/strategy_tbf',
                    pool_recycle=3600,
                    echo=False
                )
            else:
                raise ValueError('不支持的数据库Engine')
            DbEngineFactory.cached_engine_ref[key] = engine
        return DbEngineFactory.cached_engine_ref[key]

    @staticmethod
    def engine_mktdata_intraday():
        return DbEngineFactory.engine_by_key('mktdata_intraday')

    @staticmethod
    def engine_mktdata():
        return DbEngineFactory.engine_by_key('mktdata')

    @staticmethod
    def engine_rqdata():
        return DbEngineFactory.engine_by_key('rqdata')

    @staticmethod
    def engine_databus():
        return DbEngineFactory.engine_by_key('databus')

    @staticmethod
    def engine_clickhouse_rqdata():
        return DbEngineFactory.engine_by_key('clickhouse_rqdata')

    @staticmethod
    def engine_clickhouse_strategy_tbf():
        return DbEngineFactory.engine_by_key('clickhouse_strategy_tbf')

    @staticmethod
    def engine_strategy_tbf():
        return DbEngineFactory.engine_by_key('strategy_tbf')

    @staticmethod
    def engine_paimon():
        return DbEngineFactory.engine_by_key('paimon')

    @staticmethod
    def engine_cal_inds():
        return DbEngineFactory.engine_by_key('cal_inds')
