# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-08 09:31:13
"""
import os
from collections import defaultdict
from typing import Set, Tuple, DefaultDict

import pandas as pd
from pandas import DataFrame

os.chdir(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.abspath("..")
PATH = os.path.join(BASE_PATH, "dataset", "movie_ratings.csv")
SparseMap = DefaultDict[int, Set[int]]


def load_movie_ratings()->DataFrame:
    """读取用户对电影评分的数据。
    列名称[uid(int), item_id(int), rating(float), timestamp(float)]

    Returns:
        data {ndarray}
    """

    data = pd.read_csv(PATH)
    data.columns = ["uid", "item_id", "rating", "timestamp"]
    return data


def load_sparse_map()->Tuple[SparseMap, SparseMap]:
    """将用户对电影评分的数据转为sparse map，适用于User CF和Item CF算法。

    Returns:
        SparseMap -- key: uid, value: 该uid浏览过的item_id。
        SparseMap -- key: item_id, value: 浏览过该item_id的uid。
    """

    data = load_movie_ratings().loc[:, ["uid", "item_id"]]
    user_items = defaultdict(set)  # type: SparseMap
    item_users = defaultdict(set)  # type: SparseMap
    for _, uid, item_id in data.itertuples():
        user_items[uid].add(item_id)
        item_users[item_id].add(uid)

    return user_items, item_users
