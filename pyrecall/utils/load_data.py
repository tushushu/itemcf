# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-08 09:31:13
"""
import numpy as np
from numpy import ndarray
from collections import defaultdict
from typing import Dict, Set
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.abspath("..")
PATH = os.path.join(BASE_PATH, "dataset", "movie_ratings.csv")


def load_movie_ratings()->ndarray:
    """读取用户对电影评分的数据。"""

    data = np.loadtxt(PATH, delimiter=',')
    data, label = data[:, :-1], data[:, -1]

    return data, label


def f(mapping: defaultdict, key: int, value: int):
    mapping[key].add(value)


def get_user_rating_history():
    pass


def get_item_rated_history():
    pass
