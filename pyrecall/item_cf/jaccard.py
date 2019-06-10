# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from collections import defaultdict
from itertools import product
from typing import List, Any, Dict, Set, DefaultDict
from pandas import DataFrame
from ..utils.load_data import SparseMap
from ..utils.max_heap import MaxHeap
from ..utils.similarity import Similarity


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        mat -- Item相似度矩阵。
    """

    def __init__(self):
        self.mat = defaultdict()

    @staticmethod
    def cal_similarity(vector_1: Set[int], vector_2: Set[int]) -> float:
        """计算Jaccard相似度公式。
        Similarity = (A ∩ B) / (A ∪ B)

        Arguments:
            vector_1 {Set[int]} -- 浏览过该item 1的uid。
            vector_2 {Set[int]} -- 浏览过该item 2的uid。

        Returns:
            float -- 相似度。
        """

        numerator = len(vector_1 & vector_2)
        denominator = len(vector_1 | vector_2)
        return numerator / denominator

    @staticmethod
    def process_data(user_items: SparseMap) -> SparseMap:
        """将用户→物品的sparse map转为物品→用户的sparse map。

        Arguments:
            user_items {SparseMap} -- key: uid, value: 该uid浏览过的item_id。

        Returns:
            SparseMap -- key: item_id, value: 浏览过该item_id的uid。
        """

        item_users = defaultdict(set)  # type: SparseMap
        for uid, item_ids in user_items.items():
            for item_id in item_ids:
                item_users[item_id].add(uid)

        return item_users

    def fit(self, data: DataFrame, max_items=10, scaled=False):
        """训练Jaccard ItemCF模型。

        Arguments:
            data {DataFrame} -- 列名称[uid(int), item_id(int)]

        Keyword Arguments:
            max_items {int} -- 为每个Item最多计算多少个相似的Item。 (default: {10})
            scaled {bool} -- 归一化物品评分 (default: {False})
        """

        sim_mat = defaultdict(lambda: MaxHeap(max_items))  # type: DefaultDict[int, MaxHeap]
        item_users = self.process_data(data)
        _item_pairs = product(item_users, item_users)
        item_pairs = filter(lambda x: x[0] < x[1], _item_pairs)
        for item_1, item_2 in item_pairs:
            vector_1 = item_users[item_1]
            vecotr_2 = item_users[item_2]

            sim = self.cal_similarity(vector_1, vecotr_2)

            similarity_1 = Similarity(item_2, sim)
            similarity_2 = Similarity(item_1, sim)

            sim_mat[item_1].heappush(similarity_1)
            sim_mat[item_2].heappush(similarity_2)

    def predict_one(self, items: Set[int], max_items: int) -> List[Any]:
        """[summary]

        Arguments:
            items {Set[int]} -- [description]
            max_items {int} -- [description]

        Returns:
            List[Any] -- [description]
        """

        raise NotImplementedError

    def predict(self, data: SparseMap, max_items=10) -> Dict[int, List[Any]]:
        """[summary]

        Arguments:
            data {SparseMap} -- [description]

        Keyword Arguments:
            max_items {int} -- [description] (default: {10})

        Returns:
            Dict[int, List[Any]] -- [description]
        """

        return {uid: self.predict_one(items, max_items)
                for uid, items in data.items()}
