import uuid
import requests
from .model import *
from typing import List


class QmtGrpcClient:

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
        r = requests.post(self._url, data=payload)
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
        r = requests.post(self._url, data=payload)
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
        r = requests.post(self._url, data=payload)
        r_json = r.json()
        res = []
        for obj in r_json['result']:
            res.append(QmtOrder(obj))
        return res
