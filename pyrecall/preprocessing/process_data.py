"""
@Author: tushushu
@Date: 2019-06-13 11:13:03
"""

from typing import Dict, List, Optional, Callable, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import collect_set, col, countDistinct, sum as _sum  # pylint: disable=no-name-in-module


def get_item_vectors(data: DataFrame, user_col: str, item_col: str) -> Dict[int, List[int]]:
    """获取物品及评分过该物品的用户。

    Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。

    Returns:
        Dict[int, List[int]] -- key: 物品id, value: 评分过该物品的用户id，按升序排列。
    """
    ret = data.groupby(item_col)\
        .agg(collect_set(user_col))\
        .rdd\
        .map(lambda x: (x[0], sorted(x[1])))\
        .collectAsMap()
    return ret


def get_user_vectors(data: DataFrame, user_col: str, item_col: str) -> DataFrame:
    """获取用户及用户曾经评分过的物品。

    Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。

    Returns:
        DataFrame -- 列名称[user_col(IntegerType), item_ids(ArrayType[IntegerType])]
    """
    ret = data.groupby(user_col)\
        .agg(collect_set(item_col).alias(item_col))
    return ret


def get_popular_items(data: DataFrame, user_col: str, item_col: str,
                      threshold: Optional[int], show_coverage: bool) -> DataFrame:
    """取出最热门的物品id，注意n_items不可以过大，因为结果会加载到Master节点的内存中。

    Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。
        threshold {Optional[int]} -- 物品最低出现的频次。
        show_coverage {bool} -- 是否打印热门物品的覆盖度。

    Returns:
        DataFrame -- [("物品id")]
    """
    if threshold is None:
        ret = data.select(item_col).distinct()
        if show_coverage:
            print("热门物品的评分次数占总评分次数的100%！")
    else:
        ret = data.groupby(item_col)\
            .agg(countDistinct(user_col).alias("cnt"))\
            .filter(col("cnt") >= threshold)
        if show_coverage:
            numerator = ret.select(_sum("cnt")).collect()[0][0]
            denominator = data.distinct().count()
            coverage = numerator / denominator * 100
            print("热门物品的评分次数占总评分次数的%.1f%%！" % coverage)
        ret = ret.select(item_col)
    return ret

def get_similar_elements(elements: DataFrame, func: Callable, *args)->Dict[int, Any]:
    """计算与用户或物品相似的用户或物品。

    Arguments:
        elements {DataFrame} -- 用户或物品ID。
        func {Callable} -- 计算函数。

    Returns:
        Dict[int, Any] -- key: 用户或物品ID, value: 相似的用户或物品。
    """
    return elements.rdd.map(lambda x: (x[0], func(x[0], *args))).collectAsMap()
