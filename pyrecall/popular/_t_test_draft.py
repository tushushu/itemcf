"""
@Author: tushushu
@Date: 2019-10-08 17:23:24
"""
from scipy import stats as ss


def hypothesis_test_ratio(numerator: int, denominator: int, alpha=0.01) -> tuple:
    """利用t分布对总体比率做参数估计。

    Arguments:
        numerator {int} -- [description]
        denominator {int} -- [description]

    Keyword Arguments:
        alpha {float} -- [description] (default: {0.01})

    Returns:
        tuple -- [description]
    """

    # 生成待检验的总体比率
    ratio = numerator / denominator
    # 计算总体的标准差，TODO 自由度-1
    std = (ratio * (1 - ratio)) ** 0.5
    delta = float(ss.t.ppf(1 - alpha / 2, df=denominator - 1)) * std / denominator ** 0.5
    return ratio - delta, ratio + delta
