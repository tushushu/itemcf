# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from typing import List, Tuple, Optional, Set
from pandas import DataFrame
from pyrecall.utils.sparse_matrix_bin import SparseMatrixBinary  # pylint: disable=import-error, no-name-in-module
from ..preprocessing.process_data import get_item_vectors, get_user_vectors, get_popular_items,\
    get_similar_elements


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        mat {SparseMatrix} -- 物品矩阵。
        mat_size {int} -- 物品矩阵每一行的元素个数。
    """

    def __init__(self):
        self.mat = None
        self.mat_size = None

    def fit(self, data: DataFrame, user_col: str, item_col: str, mat_size: int,
            threshold: Optional[int] = None, show_coverage: bool = False,
            valid_list: Optional[Set[int]] = None, blacklist: Optional[Set[int]] = None):
        """训练Jaccard Item CF模型。

        Arguments:
        data {DataFrame} -- [user_col(IntegerType), item_col(IntegerType)]
        user_col {str} -- 用户id所在的列名称。
        item_col {str} -- 物品id所在的列名称。
        mat_size {int} -- 物品矩阵每一行的元素个数。

        Keyword Arguments:
            threshold {Optional[int]} -- 物品最低出现的频次。(default: {None})
            show_coverage {bool} -- 是否打印热门物品的覆盖度。(default: {False})
            valid_list {Optional[Set[int]]} -- 合法的element清单。(default: {None})
            blacklist {Optional[Set[int]]} -- 非法的element清单。(default: {None})
        """
        # 模型推荐物品的数量。
        self.mat_size = mat_size
        # 获取物品及评分过该物品的用户。
        item_vectors = get_item_vectors(data, user_col, item_col)
        # 初始化物品矩阵。
        self.mat = SparseMatrixBinary(item_vectors, valid_list, blacklist)
        # 计算最热门物品的相似物品，并缓存到mat中。
        popular_items = get_popular_items(
            data, user_col, item_col, threshold, show_coverage)
        self.mat.cache = get_similar_elements(
            popular_items, self.mat.knn_search, mat_size)

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
        user_vectors.loc[:, "recommendations"] = user_vectors.loc[:, item_col]\
            .apply(lambda x: self.predict_one(x, n_recommend))
        user_vectors.drop(item_col, axis=1, inplace=True)
        return user_vectors
