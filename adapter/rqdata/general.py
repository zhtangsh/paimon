import os
import rqdatac
import pandas as pd
import logging
from typing import Union, List

logger = logging.getLogger(__name__)


def get_live_ticks(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None,
                   fields: List[str] = None, market: str = 'cn'):
    """
    获得可转债实时tick数据
    :param order_book_ids: 可转债ID列表
    :param start_dt: 开始日期
    :param end_dt: 结束日期
    :param fields: 返回字段
    :param market: 市场
    :return:
    """
    logger.debug(
        f"get_live_ticks:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date},market={market}")
    return rqdatac.get_live_ticks(
        order_book_ids=order_book_ids,
        start_dt=start_date,
        end_dt=end_date,
        fields=fields,
        market=market
    )


def get_open_auction_info(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None,
                          fields: List[str] = None, market: str = 'cn'):
    logger.debug(
        f"get_live_ticks:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date},market={market}")
    return rqdatac.get_open_auction_info(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
        fields=fields,
        market=market
    )