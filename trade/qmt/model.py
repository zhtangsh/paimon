from dataclasses import dataclass


@dataclass
class QmtPosition:
    account_id: str
    account_type: int
    can_use_volume: float
    frozen_volume: float
    market_value: float
    on_road_volume: float
    open_price: float
    stock_code: str
    volume: float
    yesterday_volume: float

    def __init__(self, o):
        self.account_id = o.get('account_id')
        self.account_type = o.get('account_type')
        self.can_use_volume = o.get('can_use_volume')
        self.frozen_volume = o.get('frozen_volume')
        self.market_value = o.get('market_value')
        self.on_road_volume = o.get('on_road_volume')
        self.open_price = o.get('open_price')
        self.stock_code = o.get('stock_code')
        self.volume = o.get('volume')
        self.yesterday_volume = o.get('yesterday_volume')


@dataclass
class QmtTrade:
    account_id: str
    account_type: int
    order_remark: str
    order_sysid: str
    order_type: int
    stock_code: str
    strategy_name: str
    traded_amount: float
    traded_id: str
    traded_price: float
    traded_time: str
    traded_volume: float

    def __init__(self, o):
        self.account_id = o.get('account_id')
        self.account_type = o.get('account_type')
        self.order_id = o.get('order_id')
        self.order_remark = o.get('order_remark')
        self.order_sysid = o.get('order_sysid')
        self.order_type = o.get('order_type')
        self.stock_code = o.get('stock_code')
        self.strategy_name = o.get('strategy_name')
        self.traded_amount = o.get('traded_amount')
        self.traded_id = o.get('traded_id')
        self.traded_price = o.get('traded_price')
        self.traded_time = o.get('traded_time')
        self.traded_volume = o.get('traded_volume')


@dataclass
class QmtOrder:
    account_id: str
    account_type: int
    order_id: int
    order_remark: str
    order_status: int
    order_sysid: str
    order_status: str
    order_time: str
    order_type: int
    order_volume: float
    price: float
    price_type: str
    stock_code: str
    status_msg: str
    strategy_name: str
    traded_price: float
    traded_volume: float

    def __init__(self, o):
        self.account_id = o.get('account_id')
        self.account_type = o.get('account_type')
        self.order_id = o.get('order_id')
        self.order_remark = o.get('order_remark')
        self.order_status = o.get('order_status')
        self.order_sysid = o.get('order_sysid')
        self.order_status = o.get('order_status')
        self.order_time = o.get('order_time')
        self.order_type = o.get('order_type')
        self.order_volume = o.get('order_volume')
        self.price = o.get('price')
        self.price_type = o.get('price_type')
        self.status_msg = o.get('status_msg')
        self.stock_code = o.get('stock_code')
        self.strategy_name = o.get('strategy_name')
        self.traded_price = o.get('traded_price')
        self.traded_volume = o.get('traded_volume')


@dataclass
class QmtAsset:
    account_id: str
    account_type: str
    cash: float
    frozen_cash: float
    market_value: float
    total_asset: float

    def __init__(self, o):
        self.account_id = o.get('account_id')
        self.account_type = o.get('account_type')
        self.cash = o.get('cash')
        self.frozen_cash = o.get('frozen_cash')
        self.market_value = o.get('market_value')
        self.total_asset = o.get('total_asset')
