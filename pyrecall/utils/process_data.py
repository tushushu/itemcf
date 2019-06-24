"""
@Author: tushushu
@Date: 2019-06-13 11:13:03
"""

from typing import Dict, Set

from pyspark.sql import DataFrame
from pyspark.sql.functions import collect_set  # pylint: disable=no-name-in-module

SparseVec = Dict[int, Set[int]]

def get_item_vectors(data: DataFrame) -> SparseVec:
    """获取物品及评分过该物品的用户。

    Arguments:
        data {DataFrame} -- 列名称[uid(int), item_id(int)]

    Returns:
        SparseMap -- key: 物品id, value: 评分过该物品的用户id。
    """

    ret = data.groupby(data.item_id)\
        .agg(collect_set(data.uid))\
        .rdd\
        .map(lambda x: (x[0], set(x[1])))\
        .collectAsMap()

    return ret


def get_user_vectors(data: DataFrame) -> DataFrame:
    """获取用户及用户曾经评分过的物品。

    Arguments:
        data {DataFrame} -- 列名称[uid(int), item_id(int)]

    Returns:
        DataFrame -- 列名称[uid(int), item_ids(list)]
    """

    ret = data.groupby(data.uid)\
        .agg(collect_set(data.item_id)\
        .alias("item_ids"))

    return ret
