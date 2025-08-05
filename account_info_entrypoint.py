import datetime
import logging

import exchange_calendars as xcals
import pandas as pd
from adapter.db.datasource import DbEngineFactory
from trade.qmt.client import QmtGrpcClient
from utils import sys_utils

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sys_utils.logging_config()
    host = '192.168.1.57'
    port = 6000
    xshg = xcals.get_calendar("XSHG")
    if not xshg.is_session(datetime.date.today()):
        logger.info("非交易日，退出")
        exit(0)
    client = QmtGrpcClient(host=host, port=port)
    asset = client.get_stock_asset()
    data = [
        {
            'account_id': asset.account_id,
            'balance': asset.total_asset,
            'dt': datetime.date.today(),
        }
    ]
    engine = DbEngineFactory.engine_paimon()
    df = pd.DataFrame(data)
    df.to_sql("qmt_account_info", con=engine, if_exists='append',index=False)
