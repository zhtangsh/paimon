def reverse_id_convert(x):
    """
    # 重写rq的id_convert函数（原函数报错）
    :param x:
    :return:
    """
    if x.endswith("XSHE"):
        return x[:-4] + "SZ"
    elif x.endswith("XSHG"):
        return x[:-4] + "SH"


def id_convert(x):
    """
    # 重写rq的id_convert函数（原函数报错）
    :param x:
    :return:
    """
    if x.endswith("SZ"):
        return x[:-2] + "XSHE"
    elif x.endswith("SH"):
        return x[:-2] + "XSHG"
