# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from typing import List, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col  # pylint: disable=no-name-in-module
from pyspark.sql.types import StructField, StructType, LongType, FloatType, ArrayType
from ..utils.sparse_matrix import SparseMatrixBinary  # pylint: disable=no-name-in-module
from ..preprocessing.process_data import get_item_vectors, get_user_vectors, get_popular_items


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        mat {SparseMatrixBinary} -- 物品矩阵。
        n_recommend {int} -- 模型推荐物品的数量。
    """

    def __init__(self):
        self.mat = None
        self.n_recommend = None
        self.return_type = None

    def fit(self, data: DataFrame, user_col: str, item_col: str, n_recommend: int, n_cache: int):
        """训练Jaccard Item CF模型。

        Arguments:
            data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
            user_col {str} -- 用户id所在的列名称。
            item_col {str} -- 物品id所在的列名称。
            n_recommend {int} -- 模型推荐物品的数量。
            n_cache {int} -- 模型缓存n_cache个物品对应的n_recommend个相似物品。
        """
        # 模型推荐物品的数量。
        self.n_recommend = n_recommend
        # 模型的推荐返回格式。
        self.return_type = ArrayType(
            StructType([
                StructField(item_col, LongType()),
                StructField("score", FloatType())
            ])
        )
        # 获取物品及评分过该物品的用户。
        item_vectors = get_item_vectors(data, user_col, item_col)
        # 取出最热门的物品id。
        popular_items = get_popular_items(data, user_col, item_col, n_cache)
        # 计算物品矩阵。
        self.mat = SparseMatrixBinary(item_vectors, popular_items, n_recommend)

    def predict_one(self, items: List[int]) -> List[Tuple[int, float]]:
        """预测一个用户感兴趣的物品。

        Arguments:
            items {List[int]} -- 用户曾经评分过的物品。

        Returns:
            List[Tuple[int, float]] -- [(物品id, 相似度)...]
        """

        return self.mat.recommend_py(items, self.n_recommend)

    def predict(self, data: DataFrame, user_col: str, item_col: str) -> DataFrame:
        """预测多个用户感兴趣的物品。

        Arguments:
            data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]

        Returns:
            DataFrame
        """
        user_vectors = get_user_vectors(data, user_col, item_col)
        _predict = udf(self.predict_one, self.return_type)
        ret = user_vectors.select(col(user_col), _predict(
            item_col).alias("recommendation"))
        return ret
