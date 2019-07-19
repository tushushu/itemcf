"""
@Author: tushushu
@Date: 2019-06-13 11:13:03
"""

from typing import Dict, List
from pyspark.sql import DataFrame
from pyspark.sql.functions import collect_set, col, countDistinct  # pylint: disable=no-name-in-module


def get_item_vectors(data: DataFrame, user_col: str, item_col: str) -> Dict[int, List[int]]:
    """获取物品及评分过该物品的用户。

    Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。

    Returns:
        Dict[int, List[int]] -- key: 物品id, value: 评分过该物品的用户id，按升序排列。
    """
    ret = data.groupby(col(item_col))\
        .agg(collect_set(col(user_col)))\
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
    ret = data.groupby(col(user_col))\
        .agg(collect_set(col(item_col)).alias("item_ids"))
    return ret


def get_popular_items(data: DataFrame, user_col: str, item_col: str, n_items: int,
                      show_coverage=False) -> List[int]:
    """取出最热门的物品id，注意n_items不可以过大，因为结果会加载到Master节点的内存中。

    Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。
        n_items {int} -- 物品的数量。

    Keyword Arguments:
        show_coverage {bool} -- 是否打印热门物品的覆盖度。(default: {False})

    Returns:
        List[Row] -- [("物品id", "物品出现次数")]
    """
    ret = data.groupby(col(item_col))\
        .agg(countDistinct(col(user_col)).alias("cnt"))\
        .rdd\
        .top(n_items, lambda x: x[1])
    if show_coverage:
        numerator = sum(x[1] for x in ret)
        denominator = data.select(user_col).distinct().count()
        coverage = numerator / denominator * 100
        print("热门物品的评分次数占总评分次数的%.1f%%！" % coverage)
    return [x[0] for x in ret]
