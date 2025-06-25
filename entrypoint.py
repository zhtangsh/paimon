import datetime
import time

from utils import sys_utils
from core.engine import V2DynamicPriceEngine
from utils import trading_utils, email_utils
import logging
import exchange_calendars as xcals

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sys_utils.logging_config()
    strategy_name = 'daily_v1'
    FILENAME_PREFIX = sys_utils.get_env('FILENAME_PREFIX',
                                        'http://192.168.1.50:9000/cbond-strategy/trade_order/trade_order_ref_v10_')
    SPREAD_TOLERANCE = sys_utils.get_env('SPREAD_TOLERANCE', '0.1')
    DATA_FEED = sys_utils.get_env('DATA_FEED', 'qmt')
    QMT_HOST = sys_utils.get_env('QMT_HOST', '192.168.1.57')
    QMT_PORT = sys_utils.get_env('QMT_PORT', '6000')
    POSITION_TYPE = sys_utils.get_env("POSITION_TYPE", "v2")
    host = QMT_HOST
    port = int(QMT_PORT)
    data_feed = DATA_FEED
    spread_tolerance = float(SPREAD_TOLERANCE)
    receiver = "wangdongli0102@163.com"
    xshg = xcals.get_calendar("XSHG")
    if not xshg.is_session(datetime.date.today()):
        logger.info("非交易日，退出")
        exit(0)
    if data_feed == 'rqdata':
        logger.info('data feed is rq, initialize it')
        import rqdatac as rq

        rq.init()
    trade_date = trading_utils.latest_trading_date()
    filename_prefix = FILENAME_PREFIX
    engine = V2DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance, data_feed=data_feed,
                                  strategy_name=strategy_name)
    filename = f"{filename_prefix}{trade_date.strftime('%Y%m%d')}.csv"
    target_order_list = engine.build_target_order_csv(filename=filename)
    order_list = engine.submit_target_order(target_order_list, check_period=1)
    time.sleep(10)
    target_order_list = engine.build_target_order_csv(filename=filename)
    order_list2 = engine.submit_target_order(target_order_list, check_period=1)
    order_list = order_list + order_list2
    message = ""
    for order in order_list:
        message += f"股票ID:{order.stock_code}\t交易方向:{'买入' if order.order_type == 23 else '卖出'}\t交易量:{order.volume}\n"
    email_utils.send_mail_163(recv=receiver, title=f"{trade_date}可转债交易交易简报", content=message, file_path=None)
    if engine.error_order_list:
        message = f"下单引擎有错误，请人工查看{engine.error_order_list}"
        logger.info(message)
        email_utils.send_mail_163(recv=receiver, title="下单引擎有错误,请检查交易软件", content=message, file_path=None)
