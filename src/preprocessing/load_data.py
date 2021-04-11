"""
@Author: tushushu
@Date: 2019-10-15 15:21:17
"""
import pandas as pd
from pandas import DataFrame

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))




os.chdir(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.abspath("..")


class MovieRatingsData:
    """读取电影评分的数据。

    Attributes:
        user_col {str} -- 用户id对应的列名称。
        item_col {str} -- 物品id对应的列名称。
        rating_col {str} -- 用户对物品的评分对应的列名称。
        file_name {str} -- 数据文件名称。
        data {DataFrame} -- 数据。
    """

    def __init__(self):
        self.user_col = "userId"
        self.item_col = "movieId"
        self.rating_col = "rating"
        self.file_name = "movie_ratings"
        self.data = self.load()

    def __str__(self):
        return self.data.head(3)

    def load(self) -> DataFrame:
        """读取数据。

        Returns:
            DataFrame
        """
        path = os.path.join(BASE_PATH, "dataset", "%s.csv" % self.file_name)
        data = pd.read_csv(path)
        return data
