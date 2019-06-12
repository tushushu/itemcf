# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from collections import defaultdict
from itertools import product
from typing import List, Any, Dict, Set, DefaultDict, Tuple
from pandas import DataFrame
from ..utils.load_data import SparseMap
from ..utils.max_heap import MaxHeap
from ..utils.element import Element


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        sim_mat -- 物品相似度矩阵。
    """

    def __init__(self):
        self.sim_mat = defaultdict()
        self.max_items = 0

    @staticmethod
    def _cal_similarity(vector_1: Set[int], vector_2: Set[int]) -> float:
        """计算Jaccard相似度公式。
        Similarity = (A ∩ B) / (A ∪ B)

        Arguments:
            vector_1 {Set[int]} -- 浏览过该物品1的用户id。
            vector_2 {Set[int]} -- 浏览过该物品2的用户id。

        Returns:
            float -- 相似度。
        """

        numerator = len(vector_1 & vector_2)
        denominator = len(vector_1 | vector_2)
        return numerator / denominator

    def cal_similarity(self, item_users: SparseMap, element_1: Element, element_2: Element):
        """计算物品间的相似度，并将相似度更新到Element类的属性。

        Arguments:
            user_items {SparseMap} -- key: 用户id, value: 该用户浏览过的物品id。
            element_1 {Element} -- 物品1
            element_2 {Element} -- 物品2
        """

        vector_1 = item_users[element_1.name]
        vector_2 = item_users[element_2.name]
        sim = self._cal_similarity(vector_1, vector_2)

        element_1.sim = sim
        element_2.sim = sim

    @staticmethod
    def process_data(user_items: SparseMap) -> SparseMap:
        """将用户→物品的稀疏矩阵转为物品→用户的稀疏矩阵。

        Arguments:
            user_items {SparseMap} -- key: 用户id, value: 该用户浏览过的物品id。

        Returns:
            SparseMap -- key: 物品id, value: 浏览过该物品的用户id。
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
            max_items {int} -- 为每个物品最多计算多少个相似的物品。 (default: {10})
            scaled {bool} -- 归一化物品评分(default: {False})
        """

        item_users = self.process_data(data)
        _item_pairs = product(item_users, item_users)
        item_pairs = filter(lambda x: x[0] < x[1], _item_pairs)
        element_pairs = map(lambda x: (Element(x[0]), Element(x[1])), item_pairs)
        sim_mat = defaultdict(lambda: MaxHeap(max_items))  # type: DefaultDict[int, MaxHeap]

        for element_1, element_2 in element_pairs:
            self.cal_similarity(item_users, element_1, element_2)
            sim_mat[element_1.name].heappush(element_2)
            sim_mat[element_2.name].heappush(element_1)

        # TODO 归一化相似度
        if scaled:
            pass

        self.sim_mat = sim_mat
        self.max_items = max_items

    def predict_one(self, items: Set[int]) -> List[Tuple[int, float]]:
        """预测一个用户感兴趣的物品。

        Arguments:
            items {Set[int]} -- 用户曾经评分过的物品。

        Returns:
            List[Tuple[int, float]] -- [(物品id, 相似度)...]
        """

        item_sims = defaultdict(float)  # type: DefaultDict[int, float]
        for item in items:
            elements = self.sim_mat[item].elements
            for element in elements:
                if element.name not in items:
                    item_sims[element.name] += element.sim

        return sorted(item_sims.items(), key=lambda x: x[0], reverse=True)[: self.max_items]

    def predict(self, data: SparseMap) -> Dict[int, List[Any]]:
        """预测多个用户感兴趣的物品。

        Arguments:
            data {SparseMap} -- key: uid, value: 该uid浏览过的item_id。

        Returns:
            Dict[int, List[Any]] -- {物品id: [(物品id, 相似度)...]...}
        """

        return {uid: self.predict_one(items) for uid, items in data.items()}
