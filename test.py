from core.engine import V2DynamicPriceEngine

if __name__ == '__main__':
    from utils import sys_utils

    sys_utils.logging_config()
    host = '192.168.1.60'
    port = 6000
    spread_tolerance = 0.1
    data_feed = 'qmt'
    strategy_name = 'daily_v1'
    engine = V2DynamicPriceEngine(host=host, port=port, spread_tolerance=spread_tolerance, data_feed=data_feed,
                                  strategy_name=strategy_name)
    res = engine.check_current_position()
    print(res)
