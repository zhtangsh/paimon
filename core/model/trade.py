from dataclasses import dataclass


@dataclass
class Position:
    stock_code: str
    volume: int

    def __init__(self, stock_code, volume):
        self.stock_code = stock_code
        self.volume = int(volume)


@dataclass
class Order:
    stock_code: str
    order_book_id: str
    volume: int
    order_type: int
    price: float
    order_create_ts: int
    qmt_order_id: int
    traded_volume: int

    def __init__(self, stock_code, volume, order_type, order_book_id):
        self.stock_code = stock_code
        self.volume = volume
        self.order_type = order_type
        self.order_book_id = order_book_id
        self.traded_volume = 0
        self.order_create_ts = -1
        self.price = -1
        self.qmt_order_id = -1

    def qmt_submitted(self):
        return self.qmt_order_id != -1

    def volume_to_trade(self):
        return self.volume - self.traded_volume
