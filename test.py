from utils import sys_utils
from core.engine import VanillaEngine
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sys_utils.logging_config()
    host = '192.168.1.60'
    port = 5000
    engine = VanillaEngine(host=host, port=port)

    filename = 'static/trade_order_20231027.csv'
    target_order_list = engine.build_target_order_csv(filename=filename)
    engine.submit_target_order_v2(target_order_list)
