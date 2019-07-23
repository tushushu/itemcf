# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from typing import List, Tuple, Optional
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col  # pylint: disable=no-name-in-module
from pyspark.sql.types import StructField, StructType, LongType, FloatType, ArrayType
from ..utils.sparse_matrix import SparseMatrixBinary  # pylint: disable=no-name-in-module
from ..preprocessing.process_data import get_item_vectors, get_user_vectors, get_popular_items,\
    get_similar_elements


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        mat {SparseMatrixBinary} -- 物品矩阵。
        mat_size {int} -- 物品矩阵每一行的元素个数。
    """

    def __init__(self):
        self.mat = None
        self.mat_size = None
        self.return_type = None

    def fit(self, data: DataFrame, user_col: str, item_col: str, mat_size: int,
            threshold: Optional[int] = None, show_coverage: bool = False):
        """训练Jaccard Item CF模型。

        Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。
        mat_size {int} -- 物品矩阵每一行的元素个数。

        Keyword Arguments:
            threshold {Optional[int]} -- 物品最低出现的频次。(default: {None})
            show_coverage {bool} -- 是否打印热门物品的覆盖度。(default: {False})
        """
        # 模型推荐物品的数量。
        self.mat_size = mat_size
        # 模型的推荐返回格式。
        self.return_type = ArrayType(
            StructType([
                StructField(item_col, LongType()),
                StructField("score", FloatType())
            ])
        )
        # 获取物品及评分过该物品的用户。
        item_vectors = get_item_vectors(data, user_col, item_col)
        # 初始化物品矩阵。
        self.mat = SparseMatrixBinary(item_vectors)
        # 计算最热门物品的相似物品，并缓存到mat中。
        popular_items = get_popular_items(data, user_col, item_col, threshold, show_coverage)
        self.mat.cache = get_similar_elements(popular_items, self.mat.knn_search, mat_size)

    def predict_one(self, items: List[int], n_recommend: int) -> List[Tuple[int, float]]:
        """预测一个用户感兴趣的物品。

        Arguments:
            items {List[int]} -- 用户曾经评分过的物品。
            n_recommend {int} -- 给用户推荐物品的数量。

        Returns:
            List[Tuple[int, float]] -- [(物品id, 相似度)...]
        """

        return self.mat.recommend(items, n_recommend)

    def predict(self, data: DataFrame, user_col: str, item_col: str, n_recommend: int) -> DataFrame:
        """预测多个用户感兴趣的物品。

        Arguments:
            data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
            n_recommend {int} -- 给用户推荐物品的数量。

        Returns:
            DataFrame
        """
        user_vectors = get_user_vectors(data, user_col, item_col)
        _predict = udf(lambda x: self.predict_one(x, n_recommend), self.return_type)
        ret = user_vectors.select(col(user_col), _predict(
            item_col).alias("recommendation"))
        return ret
