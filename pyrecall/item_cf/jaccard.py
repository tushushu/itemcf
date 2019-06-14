# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from collections import defaultdict
from itertools import product, chain
from typing import List, Any, Dict, Set, DefaultDict, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf
from ..utils.load_data import SparseMap
from ..utils.process_data import get_item_vectors, get_user_vectors
from ..utils.distance import jaccard_sim
from ..utils.element import Element
from ..utils.max_heap import MaxHeap


class JaccardItemCF:
    """JaccardItemCF类。

    Attributes:
        sim_mat -- 物品相似度矩阵。
    """

    def __init__(self):
        self.sim_mat = defaultdict()
        self.max_items = 0

    def fit(self, data: DataFrame, max_items=10, scaled=False):
        """训练Jaccard ItemCF模型。

        Arguments:
            data {DataFrame} -- 需剔除重复数据，列名称[uid(int), item_ids(int)]

        Keyword Arguments:
            max_items {int} -- 最多为每个物品最多计算多少个相似的物品。 (default: {10})
            scaled {bool} -- 是否归一化物品相似度(default: {False})
        """

        # 获取物品及评分过该物品的用户
        item_vectors = get_item_vectors(data)
        # 获取所有的物品
        items = data.select("item_id").distinct()
        def get_sim_mat(items):
            sim_mat = defaultdict(lambda: MaxHeap(max_items))  # type: DefaultDict[int, MaxHeap]
            for item_1 in items:
                vec_1 = item_vectors.get(item_1, set())
                iterator = (x for x in item_vectors if x > item_1)
                for item_2 in iterator:
                    vec_2 = item_vectors.get(item_2, set())
                    sim = jaccard_sim(vec_1, vec_2)
                    if sim == 0:
                        continue
                    ele_1 = Element(item_1, sim)
                    ele_2 = Element(item_2, sim)
                    sim_mat[item_1].heappush(ele_2)
                    sim_mat[item_2].heappush(ele_1)
            return sim_mat


        def sim_mat_iterator(iterator):
            yield get_sim_mat(iterator)

        def merge(sim_mat_1, sim_mat_2):
            for item_2, heap_2 in sim_mat_2:
                if item_2 in sim_mat_1:
                    heap_1 = sim_mat_1[item_2]
                    for ele in heap_2.element:
                        heap_1.heappush(ele)
            return sim_mat_1

        # 计算物品相似度
        sim_mat = items.rdd.mapPartitions(sim_mat_iterator).reduce(merge)

        # TODO 归一化物品相似度
        if scaled:
            pass

        self.sim_mat = sim_mat
        self.max_items = max_items

    def predict_one(self, items: List[int]) -> List[Tuple[int, float]]:
        """预测一个用户感兴趣的物品。

        Arguments:
            items {List[int]} -- 用户曾经评分过的物品。

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

    def predict(self, data: DataFrame) -> DataFrame:
        """预测多个用户感兴趣的物品。

        Arguments:
            data {DataFrame} -- 需剔除重复数据，列名称[uid(int), item_ids(int)]

        Returns:
            DataFrame
        """

        user_vectors = get_user_vectors(data)
        # TODO udf的return类型待修正
        _predict = udf(self.predict_one)
        ret = user_vectors.select("uid", _predict("item_ids").alias("recs"))

        return ret

