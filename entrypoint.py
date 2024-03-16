from utils import sys_utils
from core.engine import V2DynamicPriceEngine
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    import rqdatac as rq

    rq.init()
    sys_utils.logging_config()
    host = '192.168.1.60'
    port = 6000
    spread_tolerance = 0.1
    data_feed = 'qmt'
    strategy_name = 'daily_v1'
    engine = V2DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance, data_feed=data_feed,
                                  strategy_name=strategy_name)
    filename = 'http://192.168.1.50:9000/cbond-strategy/trade_order/trade_order_ref_v3__20240314.csv'
    target_order_list = engine.build_target_order_csv(filename=filename)
    engine.submit_target_order(target_order_list, check_period=1)
