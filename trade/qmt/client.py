import json
import uuid
import requests
import logging
from trade.qmt.constant import QmtPriceType

from .model import *
from typing import List, Dict

logger = logging.getLogger(__name__)


class QmtGrpcClient:

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._url = f"http://{host}:{port}/api"

    def build_header(self):
        return {
            'Content-Type': 'application/json'
        }

    def _do_post(self, retry=3, **kwargs):
        while retry > 0:
            try:
                r = requests.post(**kwargs)
                return r
            except Exception as e:
                logger.error("_do_post error", e)
                retry -= 1
                if retry == 0:
                    raise e

    def get_stock_positions(self) -> List[QmtPosition]:
        payload = {
            "jsonrpc": "2.0",
            "params": [],
            "method": "tradeInfo.getStockPositions",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
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
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        res = []
        for obj in r_json['result']:
            res.append(QmtTrade(obj))
        return res

    def get_stock_orders(self, cancelable_only: bool) -> List[QmtOrder]:
        params = {
            "cancelable_only": cancelable_only
        }
        payload = {
            "jsonrpc": "2.0",
            "params": params,
            "method": "tradeInfo.getStockOrders",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
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
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        return r_json['result']

    def cancel_order_stock(self, order_id: int) -> int:
        params = {
            "order_id": order_id
        }
        payload = {
            "jsonrpc": "2.0",
            "params": params,
            "method": "trade.cancel_order_stock",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        return r_json['result']

    def get_stock_asset(self) -> QmtAsset:
        payload = {
            "jsonrpc": "2.0",
            "params": [],
            "method": "accountInfo.getStockAsset",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
        r_json = r.json()
        return QmtAsset(r_json['result'])

    def live_tick_data(self, order_book_id_list) -> List[Dict[str, any]]:
        payload = {
            "jsonrpc": "2.0",
            "params": {'order_id_list': order_book_id_list},
            "method": "data.live_tick_data",
            'id': str(uuid.uuid4()),
        }
        header = self.build_header()
        r = self._do_post(url=self._url, data=json.dumps(payload), headers=header)
        return r.json()['result']
