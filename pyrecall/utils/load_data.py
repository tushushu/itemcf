# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-08 09:31:13
"""
import os
from collections import defaultdict
from typing import Set, DefaultDict

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

def load_cf_data() -> SparseMap:
    """读取用户对电影的评分的数据，并转为sparse map，适用于协同过滤算法。

    Arguments:
        data {DataFrame} -- 列名称[uid(int), item_id(int)]

    Returns:
        SparseMap -- key: uid, value: 该uid浏览过的item_id。
    """

    data = load_movie_ratings()
    user_items = defaultdict(set)  # type: SparseMap
    for _, uid, item_id in data.itertuples():
        user_items[uid].add(item_id)

    return user_items
