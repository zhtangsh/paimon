from utils import sys_utils
from core.engine import DynamicPriceEngine
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    import rqdatac as rq

    rq.init()
    sys_utils.logging_config()
    host = '192.168.1.60'
    port = 5000
    spread_tolerance = 0.02
    engine = DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance)

    filename = 'static/trade_order_new_20231103.csv'
    target_order_list = engine.build_target_order_csv(filename=filename)
    engine.submit_target_order(target_order_list, check_period=1)
