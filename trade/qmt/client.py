import json
import uuid
import requests
from trade.qmt.constant import QmtPriceType

from .model import *
from typing import List


class QmtGrpcClient:

    def build_header(self):
        return {
            'Content-Type': 'application/json'
        }

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._url = f"http://{host}:{port}/api"

    def get_stock_positions(self) -> List[QmtPosition]:
        payload = {
            "jsonrpc": "2.0",
            "params": [],
            "method": "tradeInfo.getStockPositions",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = requests.post(self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        res = []
        for obj in r_json['result']:
            res.append(QmtPosition(obj))
        return res

    def get_stock_trades(self) -> List[QmtTrade]:
        payload = {
            "jsonrpc": "2.0",
            "params": [],
            "method": "tradeInfo.getStockTrades",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = requests.post(self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        res = []
        for obj in r_json['result']:
            res.append(QmtTrade(obj))
        return res

    def get_stock_orders(self) -> List[QmtOrder]:
        payload = {
            "jsonrpc": "2.0",
            "params": [],
            "method": "tradeInfo.getStockOrders",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = requests.post(self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        res = []
        for obj in r_json['result']:
            res.append(QmtOrder(obj))
        return res

    def order_stock(
            self,
            stock_code: str,
            order_type: int,
            order_volume: int,
            price_type: int = QmtPriceType.LATEST_PRICE,
            price: float = 0,
            strategy_name: str = 'default_strategy_name',
            order_remark: str = 'default_order_remark'
    ) -> int:
        params = {
            'stock_code': stock_code,
            'order_type': order_type,
            'order_volume': order_volume,
            'price_type': price_type,
            'price': price,
            'strategy_name': strategy_name,
            'order_remark': order_remark
        }
        payload = {
            "jsonrpc": "2.0",
            "params": params,
            "method": "trade.orderStock",
            'id': str(uuid.uuid4()),
        }

        header = self.build_header()
        r = requests.post(self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        return r_json['result']
