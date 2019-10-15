"""
@Author: tushushu
@Date: 2019-06-13 11:13:03
"""

from typing import Dict, List, Optional, Callable, Any
from pandas import DataFrame
from numpy import ndarray


def get_item_vectors(data: DataFrame, user_col: str, item_col: str) -> Dict[int, List[int]]:
    """获取物品及评分过该物品的用户，并将用户id按照升序排列。

    Arguments:
        data {DataFrame} -- [user_col(int), item_col(int)...]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。

    Returns:
        Dict[int, List[int]] -- key: 物品id, value: [用户id...]
    """
    ret = data.loc[:, [user_col, item_col]]\
        .groupby(item_col)\
        .aggregate(lambda x: sorted(set(x)))\
        .to_dict()\
        .get(user_col)
    return ret


def get_user_vectors(data: DataFrame, user_col: str, item_col: str) -> DataFrame:
    """获取用户及用户曾经评分过的物品。

    Arguments:
        data {DataFrame} -- [user_col(int), item_col(int)...]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。

    Returns:
        DataFrame -- 列名称[user_col(int), item_ids(List[int])]
    """
    ret = data.loc[:, [user_col, item_col]]\
        .groupby(user_col)\
        .aggregate(lambda x: list(set(x)))\
        .reset_index()
    return ret


def get_popular_items(data: DataFrame, user_col: str, item_col: str,
                      threshold: Optional[int], show_coverage: bool) -> ndarray:
    """取出最热门的物品id。

    Arguments:
        data {DataFrame} -- [user_col(int), item_col(int)...]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。
        threshold {Optional[int]} -- 物品最低出现的频次。
        show_coverage {bool} -- 是否打印热门物品的覆盖度。

    Returns:
        ndarray -- 物品id
    """
    if threshold is None:
        ret = data.loc[:, item_col].unique()
        if show_coverage:
            print("热门物品的评分次数占总评分次数的100%！")
    else:
        ret = data.loc[:, [user_col, item_col]]\
            .groupby(item_col)\
            .aggregate(lambda x: len(x.unique()))\
            .query("{user_col} > {threshold}".format(user_col=user_col, threshold=threshold))
        if show_coverage:
            numerator = ret.loc[:, user_col].sum()
            denominator = len(
                data.loc[:, [user_col, item_col]].drop_duplicates())
            coverage = numerator / denominator * 100
            print("热门物品的评分次数占总评分次数的%.1f%%！" % coverage)
        ret = ret.index.values
    return ret


def get_similar_elements(elements: ndarray, func: Callable, *args) -> Dict[int, Any]:
    """计算与用户或物品相似的用户或物品。

    Arguments:
        elements {ndarray} -- 用户或物品ID。
        func {Callable} -- 计算函数。

    Returns:
        Dict[int, Any] -- key: 用户或物品ID, value: 相似的用户或物品。
    """
    return {x: func(x, *args) for x in elements}
