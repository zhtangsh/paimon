import logging
from typing import Union, List

import rqdatac

logger = logging.getLogger(__name__)


def get_price(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None,
              adjust_type: str = 'none', frequency: str = '1d'):
    """
    获得可转债行情数据
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param frequency: 数据频度
    :param adjust_type: 是否复权
    """
    logger.info(
        f"get_price:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date},adjust_type={adjust_type},frequency={frequency}")
    return rqdatac.get_price(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        fields=None,
        adjust_type=adjust_type,
        skip_suspended=False,
        market='cn',
        expect_df=True,
        time_slice=None
    )


def all_instruments(date=None):
    """
    获得所有可转债列表
    :param date: 日期
    """
    logger.info(f"all_instruments:date={date}")
    return rqdatac.convertible.all_instruments(date=date)


def instruments(order_book_ids: Union[str, List[str]]):
    """
    获得所有可转债列表
    :param order_book_ids: 可转债ID列表
    """
    logger.info(f"instruments:order_book_ids={order_book_ids}")
    return rqdatac.convertible.instruments(order_book_ids)


def get_indicators(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    获取可转债估值指标数据
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_indicators:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_indicators(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
        fields=None
    )


def get_conversion_price(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    获取可转债转股价格数据
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_conversion_price:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_conversion_price(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
    )


def get_conversion_info(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    获取可转债转股信息数据
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_conversion_info:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_conversion_info(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
    )


def get_call_info(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    可转债强赎信息
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_call_info:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_call_info(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date
    )


def get_put_info(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    可转债回售信息
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_put_info:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_put_info(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date
    )


def get_cash_flow(order_book_ids: Union[str, List[str]], start_date: str = None, end_date: str = None):
    """
    可转债现金流
    :param order_book_ids: 可转债ID列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_cash_flow:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.convertible.get_cash_flow(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
    )


def get_trading_dates(start_date: str, end_date: str):
    """
    获取交易日数据
    :param start_date: 开始日期
    :param end_date: 结束日期
    """
    logger.info(f"get_trading_dates:order_book_ids={order_book_ids},start_date={start_date},end_date={end_date}")
    return rqdatac.get_trading_dates(start_date=start_date, end_date=end_date, market='cn')
