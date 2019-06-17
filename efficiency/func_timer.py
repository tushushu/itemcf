"""
@Author: tushushu
@Date: 2019-06-17 17:12:46
"""

from typing import Callable
from time import time


def func_timer(func: Callable, *args) -> Callable:
    """一个打印函数运行时间的装饰器。

    Arguments:
        func {Callable} -- 被装饰的函数。

    Returns:
        Callable
    """
    def wrapper():
        start = time()
        ret = func(*args)
        end = time()
        run_time = end - start
        print("函数%s运行时间%.3f s!" % (func.__name__, run_time))
        return ret

    return wrapper
