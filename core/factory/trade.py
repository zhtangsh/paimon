from trade.qmt.model import QmtPosition
from core.model import Position
from typing import List
from utils import rq_utils

"""
888880.SH 国债逆回购，为标准债，过滤
"""
special_code_ref = {'888880.SH'}


def from_qmt_position(qmt_position: QmtPosition) -> Position:
    stock_code = qmt_position.stock_code
    volume = qmt_position.volume
    return Position(stock_code, volume)


def from_qmt_position_list(qmt_position_list: List[QmtPosition]) -> List[Position]:
    return [from_qmt_position(qmt_position) for qmt_position in qmt_position_list if
            qmt_position.stock_code not in special_code_ref]


def from_csv_position(obj) -> Position:
    stock_code = rq_utils.reverse_id_convert(obj['order_book_id'])
    volume = obj['order_int'] * 10
    return Position(stock_code, volume)
