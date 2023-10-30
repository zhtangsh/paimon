class QmtPriceType:
    """
    报价类型
    """
    # 最新价
    LATEST_PRICE = 5

    # 指定价/限价
    FIX_PRICE = 11

    # 最优五档即时成交剩余撤销[上交所][股票]
    MARKET_SH_CONVERT_5_CANCEL = 42

    # 最优五档即时成交剩转限价[上交所][股票]
    MARKET_SH_CONVERT_5_LIMIT = 43

    # 对手方最优价格委托[上交所[股票]][深交所[股票][期权]]
    MARKET_PEER_PRICE_FIRST = 44

    # 本方最优价格委托[上交所[股票]][深交所[股票][期权]]
    MARKET_MINE_PRICE_FIRST = 45

    # 即时成交剩余撤销委托[深交所][股票][期权]
    MARKET_SZ_INSTBUSI_RESTCANCEL = 46
    # 最优五档即时成交剩余撤销[深交所][股票][期权]
    MARKET_SZ_CONVERT_5_CANCEL = 47

    # 全额成交或撤销委托[深交所][股票][期权]
    MARKET_SZ_FULL_OR_CANCEL = 48


class QmtOrderType:
    """
    委托类型
    """
    # 买入
    STOCK_BUY = 23
    # 卖出
    STOCK_SELL = 24
