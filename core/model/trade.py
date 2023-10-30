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
    volume: int
    order_type: int

    def __init__(self, stock_code, volume, order_type):
        self.stock_code = stock_code
        self.volume = volume
        self.order_type = order_type
