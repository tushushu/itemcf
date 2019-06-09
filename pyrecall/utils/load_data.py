# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-08 09:31:13
"""
import os
from collections import defaultdict
from typing import Dict, Set

import pandas as pd
from pandas import DataFrame

os.chdir(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.abspath("..")
PATH = os.path.join(BASE_PATH, "dataset", "movie_ratings.csv")


def load_movie_ratings()->DataFrame:
    """读取用户对电影评分的数据。
    列名称[uid(int), item_id(int), rating(float), timestamp(float)]

    Returns:
        data {ndarray}
    """

    data = pd.read_csv(PATH)
    data.columns = ["uid", "item_id", "rating", "timestamp"]
    return data


def load_ucf_data()->Dict[int, Set[int]]:
    """读取用户对电影评分的数据，适用于User CF算法。

    Returns:
        Dict[int, Set[int]] -- uid及其对应的item_id。
    """

    data = load_movie_ratings().loc[:, ["uid", "item_id"]]
    ret = defaultdict(set)  # type: defaultdict
    for _, uid, item_id in data.itertuples():
        ret[uid].add(item_id)

    return ret


def load_icf_data()->Dict[int, Set[int]]:
    """读取用户对电影评分的数据，适用于Item CF算法。

    Returns:
        Dict[int, Set[int]] -- item_id及其对应的uid。
    """

    data = load_movie_ratings().loc[:, ["uid", "item_id"]]
    ret = defaultdict(set)  # type: defaultdict
    for _, uid, item_id in data.itertuples():
        ret[item_id].add(uid)

    return ret
