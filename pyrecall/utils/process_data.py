"""
@Author: tushushu
@Date: 2019-06-13 11:13:03
"""

from typing import Dict, Set

from pyspark.sql import DataFrame
from pyspark.sql.functions import collect_set  # pylint: disable=no-name-in-module

SparseMap = Dict[int, Set[int]]

def get_item_users(data: DataFrame) -> SparseMap:
    """[summary]

    Arguments:
        data {DataFrame} -- [description]

    Returns:
        SparseMap -- [description]
    """

    ret = data.groupby(data.item_id)\
        .agg(collect_set(data.uid))\
        .rdd\
        .map(lambda x: (x[0], set(x[1])))\
        .collectAsMap()

    return ret


def get_user_items(data: DataFrame) -> SparseMap:
    """[summary]

    Arguments:
        data {DataFrame} -- [description]

    Returns:
        SparseMap -- [description]
    """

    ret = data.groupby(data.uid)\
        .agg(collect_set(data.item_id))

    return ret
