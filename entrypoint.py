import datetime

from utils import sys_utils
from core.engine import V2DynamicPriceEngine
from utils import trading_utils, email_utils
import logging
import exchange_calendars as xcals

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sys_utils.logging_config()
    host = '192.168.1.57'
    port = 6000
    spread_tolerance = 0.1
    data_feed = 'qmt'
    strategy_name = 'daily_v1'
    FILENAME_PREFIX = sys_utils.get_env('FILENAME_PREFIX',
                                        'http://192.168.1.50:9000/cbond-strategy/trade_order/trade_order_ref_v6_')
    receiver = "wangdongli0102@163.com"
    xshg = xcals.get_calendar("XSHG")
    if not xshg.is_session(datetime.date.today()):
        logger.info("非交易日，退出")
        exit(0)
    trade_date = trading_utils.latest_trading_date()
    filename_prefix = FILENAME_PREFIX
    engine = V2DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance, data_feed=data_feed,
                                  strategy_name=strategy_name)
    filename = f"{filename_prefix}{trade_date.strftime('%Y%m%d')}.csv"
    target_order_list = engine.build_target_order_csv(filename=filename)
    order_list = engine.submit_target_order(target_order_list, check_period=1)
    message = ""
    for order in order_list:
        message += f"股票ID:{order.stock_code}\t交易方向:{'买入' if order.order_type == 23 else '卖出'}\t交易量:{order.volume}\n"
    email_utils.send_mail_163(recv=receiver, title=f"{trade_date}可转债交易交易简报", content=message, file_path=None)
