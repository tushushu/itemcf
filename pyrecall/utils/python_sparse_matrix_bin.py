"""
@Author: tushushu
@Date: 2019-10-29 14:23:40
"""
from typing import Dict, List, Set, Tuple, Optional, Union
from heapq import nlargest


def iszero(num: float) -> bool:
    """判断一个浮点数是否等于0.0。"""
    return -0.000001 < num < 0.000001


def jaccard_sim(set1: Set[int], set2: Set[int]) -> float:
    """计算Jaccard相似度函数。

    Arguments:
        set1 {Set[int]} -- 稀疏向量1。
        set2 {Set[int]} -- 稀疏向量2。

    Returns:
        float -- Jaccard相似度。
    """
    denominator = len(set1 | set2)
    if denominator == 0:
        return 0.0
    numerator = len(set1 & set2)
    return numerator / denominator


def agg_score(score_map: Dict[int, float], top_k: List[Tuple[int, float]],
              exclude_elements: Set[int]):
    """将top_k中element添加到score_map中，如果elment已存在则累加其分数。"""
    for key, val in top_k:
        if key in exclude_elements:
            continue
        if key in score_map:
            score_map[key] += val
        else:
            score_map[key] = val


def top_k_map(score_map: Dict[int, float], k: int):
    """根据map的value取出最大的top k pair，并按照value的降序排列。"""
    return nlargest(k, score_map.items(), key=lambda x: x[1])


class PythonSparseMatrixBinary:
    """稀疏矩阵的Python实现(离散值)。如长度为5的稠密向量[0, 1, 0, 0, 1]，其稀疏向量表示为[1, 4]。

    Attributes:
        _data {Dict[int, Set[int]]} -- 以C++对象存储的稀疏矩阵。
        _valid_list {Set[int]} -- 以C++对象存储的合法的element清单。
        _blacklist {Set[int]} -- 以C++对象存储的非法的element清单。
        _cache {Dict[int, List[Tuple[int, float]]]} -- 热门Key的KNN查找结果。
    """

    def __init__(self, data: Dict[int, Union[List[int], Set[int]]],
                 valid_list: Optional[Set[int]] = None, blacklist: Optional[Set[int]] = None):
        """合法清单和非法清单同时存在时，合法清单对非法清单取差集，只保留合法清单。

        Arguments:
            data {Dict[int, Union[List[int], Set[int]]]} -- 以Python对象存储的稀疏矩阵。

        Keyword Arguments:
            valid_list {Optional[Set[int]]} -- 合法的element清单。(default: {None})
            blacklist {Optional[Set[int]]} -- 非法的element清单。(default: {None})
        """
        assert valid_list != set(), "valid_list不可以为空！"
        assert blacklist != set(), "blacklist不可以为空！"
        self._valid_list = set()
        self._blacklist = set()
        if valid_list is not None:
            if blacklist is not None:
                assert not valid_list.issubset(
                    blacklist), "valid_list不可以是blacklist的子集！"
                self._valid_list = valid_list - blacklist
            else:
                self._valid_list = valid_list
        else:
            if blacklist is not None:
                self._blacklist = blacklist
            else:
                pass
        self._data = {k: set(v) for k, v in data.items()}
        self._cache = dict()

    @property
    def cache(self):
        """访问_cache属性。"""
        return self._cache

    @cache.setter
    def cache(self, data):
        """修改_cache属性。"""
        self._cache = data

    def _knn_search(self, key1: int, k: int) -> List[Tuple[int, float]]:
        """线性查找与key对应的向量相似度最大的k个向量，且这些向量的key不能与被查找的key相同。
        合法清单过滤，合法清单存在且元素不在合法清单中，不参与计算；
        非法清单过滤，非法清单存在且元素在非法清单中，不参与计算。
        """
        val1 = self._data.get(key1)
        if val1 is None:
            return []

        def filter_elemnts():
            for key2, val2 in self._data.items():
                if self._valid_list and key2 not in self._valid_list:
                    continue
                elif self._blacklist and key2 in self._blacklist:
                    continue
                sim = jaccard_sim(val1, val2)
                if iszero(sim) or key2 == key1:
                    continue
                key = key2
                yield key, sim
        elements = filter_elemnts()
        return nlargest(k, elements, key=lambda x: x[1])

    def knn_search(self, key: int, k: int) -> List[Tuple[int, float]]:
        """包装knn_search方法给Python程序调用。"""
        if key in self._cache:
            return self._cache[key]
        return self._knn_search(key, k)

    def _recommend(self, items: Set[int], k: int):
        """根据用户的评分过的物品列表推荐物品，不推荐用户已经评分过的物品。"""
        score_map = dict()  # type: Dict[int, float]
        for item in items:
            if item in self._cache:
                top_k = self._cache[item]
            else:
                top_k = self._knn_search(item, k)
            agg_score(score_map, top_k, items)
        return top_k_map(score_map, k)

    def recommend(self, items: Set[int], k: int):
        """包装recommend方法给Python程序调用。"""
        return self._recommend(items, k)
