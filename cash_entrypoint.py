import datetime
import logging

import exchange_calendars as xcals
from core.engine import V2DynamicPriceEngine
from utils import sys_utils
from utils import trading_utils

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sys_utils.logging_config()
    host = '192.168.1.57'
    port = 6000
    data_feed = 'qmt'
    strategy_name = 'cash_management'
    FILENAME_PREFIX = sys_utils.get_env('FILENAME_PREFIX',
                                        'http://192.168.1.50:9000/cbond-strategy/trade_order/trade_order_ref_v6_')
    SPREAD_TOLERANCE = sys_utils.get_env('SPREAD_TOLERANCE', '0.1')
    spread_tolerance = float(SPREAD_TOLERANCE)
    receiver = "wangdongli0102@163.com"
    xshg = xcals.get_calendar("XSHG")
    if not xshg.is_session(datetime.date.today()):
        logger.info("非交易日，退出")
        exit(0)
    trade_date = trading_utils.latest_trading_date()
    filename_prefix = FILENAME_PREFIX
    engine = V2DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance, data_feed=data_feed,
                                  strategy_name=strategy_name)
    engine.close_cash()
