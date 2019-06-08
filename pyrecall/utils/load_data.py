# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-08 09:31:13
"""
import os
from collections import defaultdict
from typing import Dict, Set, Tuple

import numpy as np
from numpy import ndarray

os.chdir(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.abspath("..")
PATH = os.path.join(BASE_PATH, "dataset", "movie_ratings.csv")


def load_data()->Tuple[ndarray, ndarray]:
    """读取用户对电影评分的数据。

    Returns:
        data {ndarray} -- 用户对哪些电影进行了评分，列名称[uid(int), item_id(int),
                          timestamp(float)]
        label {ndarray} -- 用户对电影的评分，列名称[rating(float)]
    """

    data = np.loadtxt(PATH, delimiter=',')
    data, label = data[:, :-1], data[:, -1]

    return data, label


def load_ucf_data()->Dict[int, Set[int]]:
    """读取用户对电影评分的数据，适用于User CF算法。

    Returns:
        Dict[int, Set[int]] -- uid及其对应的item_id。
    """

    data, _ = load_data()
    ret = defaultdict(set)  # type: defaultdict
    for uid, item_id, _ in data:
        ret[uid].add(item_id)

    return ret


def load_icf_data()->Dict[int, Set[int]]:
    """读取用户对电影评分的数据，适用于Item CF算法。

    Returns:
        Dict[int, Set[int]] -- item_id及其对应的uid。
    """

    data, _ = load_data()
    ret = defaultdict(set)  # type: defaultdict
    for uid, item_id, _ in data:
        ret[item_id].add(uid)

    return ret
