"""
@Author: tushushu
@Date: 2019-06-17 17:12:46
"""

from typing import Callable
from time import time
import numpy as np


def func_timer(n_runs: int, show_details=True) -> Callable:
    """一个打印函数运行时间的装饰器。

    Arguments:
        n_runs {int} -- 函数运行次数。

    Returns:
        Callable
    """
    def _func_timer(func: Callable) -> Callable:
        """func_timer的辅助函数。

        Arguments:
            func {Callable} -- 被装饰的函数。

        Returns:
            Callable
        """
        def wrapper(*args):
            run_times = np.empty(n_runs)
            start_tot = time()
            for i in range(n_runs):
                start = time()
                ret = func(*args)
                end = time()
                run_time = (end - start) / n_runs
                run_times[i] = round(run_time, 3)
            end_tot = time()

            print("函数%s运行--%d次!" % (func.__name__, n_runs))
            if show_details:
                print("运行时间明细为--%s" % run_times)
                print("平均值为--%.3f s!" % (np.mean(run_times)))
                print("中位数为--%.3f s!" % (np.median(run_times)))
                print("最小值为--%.3f s!" % (np.min(run_times)))
                print("最大值为--%.3f s!" % (np.max(run_times)))
            print("累计运行时间为--%.3f s!" % (end_tot - start_tot))
            print()
            return ret
        return wrapper
    return _func_timer
