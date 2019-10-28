"""
@Author: tushushu
@Date: 2019-10-28 17:01:55
"""
from time import time
from typing import Callable


def run_time(func: Callable) -> Callable:
    """计算并打印函数的运行时间，并根据数字的大小选择恰当的时间单位。

    Arguments:
        func {Callable}

    Returns:
        Callable
    """

    def inner():
        start = time()
        func()
        ret = time() - start
        if ret < 1e-6:
            unit = "ns"
            ret *= 1e9
        elif ret < 1e-3:
            unit = "us"
            ret *= 1e6
        elif ret < 1:
            unit = "ms"
            ret *= 1e3
        else:
            unit = "s"
        print("运行时间为 %.1f %s\n" % (ret, unit))
    return inner
