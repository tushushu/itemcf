# distutils: language = c++
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

"""
@Author: tushushu
@Date: 2019-07-03 14:52:49
"""

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.unordered_set cimport unordered_set as cpp_set
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from .heap cimport min_heappush
from .sim_metrics cimport jaccard_sim
from .item_cf cimport agg_score, top_k_map


cdef class SparseMatrixBinary:
    """稀疏矩阵的C++实现(离散值)。
    如长度为5的稠密向量[0, 1, 0, 0, 1]，其稀疏向量表示为[1, 4]。

    合法清单和非法清单同时存在时，合法清单对非法清单取差集，只保留合法清单。

    Arguments:
        data {Dict[int, List[int]]} -- 以Python对象存储的稀疏矩阵。
        valid_list {Optional[Set[int]]} -- 合法的element清单。(default: {None})
        blacklist {Optional[Set[int]]} -- 非法的element清单。(default: {None})

    Attributes:
        _data {cpp_map[int, vector[int]]} -- 以C++对象存储的稀疏矩阵。
        _valid_list {cpp_set[int]} -- 以C++对象存储的合法的element清单。
        _blacklist {cpp_set[int]} -- 以C++对象存储的非法的element清单。
        _cache {cpp_map[int, vector[pair[int, float]]]} -- 热门Key的KNN查找结果。
    """

    def __init__(self, dict data, valid_list=None, blacklist=None):
        assert valid_list != set(), "valid_list不可以为空！"
        assert blacklist != set(), "blacklist不可以为空！"
        if valid_list is not None:
            if blacklist is not None:
                assert not blacklist.issubset(valid_list), "valid_list不可以是blacklist的子集！"
                self._valid_list = valid_list - blacklist
            else:
                self._valid_list = valid_list
        else:
            if blacklist is not None:
                self._blacklist = blacklist
            else:
                pass
        self._data = data

    def __len__(self):
        return self._data.size()

    def __getitem__(self, int key):
        return self._get(key)

    def __setitem__(self, int key, vector[int] value):
        self._data[key] = value

    def __iter__(self):
        cdef:
            cpp_map[int, vector[int]].iterator it = self._data.begin()
            cpp_map[int, vector[int]].iterator end = self._data.end()
        while it != end:
            yield deref(it).first, deref(it).second
            inc(it)

    @property
    def data(self):
        """访问Cython的_data属性。"""
        return self._data

    @property
    def valid_list(self):
        """访问Cython的_valid_list属性。"""
        return self._valid_list

    @property
    def blacklist(self):
        """访问Cython的_blacklist属性。"""
        return self._blacklist

    @property
    def cache(self):
        """访问Cython的_cache属性。"""
        return self._cache
    
    @cache.setter
    def cache(self, data):
        """修改Cython的_cache属性。"""
        self._cache = data

    cdef vector[int] _get(self, int key):
        """访问稀疏矩阵中的稀疏向量。"""
        cdef cpp_map[int, vector[int]].iterator it = self._data.find(key)
        if it == self._data.end():
            raise KeyError('%i' % key)
        return deref(it).second

    cdef vector[pair[int, float]] _knn_search(self, int key, unsigned int k) except +:
        """线性查找与key对应的向量相似度最大的k个向量，且这些向量的key不能与被查找的key相同。
        合法清单过滤，合法清单存在且元素不在合法清单中，不参与计算；
        非法清单过滤，非法清单存在且元素在非法清单中，不参与计算。
        """
        cdef:
            vector[pair[int, float]] heap
            pair[int, float] element
            cpp_map[int, vector[int]].iterator it1 = self._data.find(key)
            cpp_map[int, vector[int]].iterator it2 = self._data.begin()
            cpp_map[int, vector[int]].iterator end = self._data.end()
        if it1 == end:
            return heap
        while it2 != end:
            if self._valid_list.size() and self._valid_list.count(deref(it2).first) == 0:
                inc(it2)
                continue
            elif self._blacklist.size() and self._blacklist.count(deref(it2).first):
                inc(it2)
                continue
            element.second = jaccard_sim(deref(it1).second, deref(it2).second)
            if (element.second >= -0.000001 and element.second <= 0.000001) or it2 == it1:
                inc(it2)
                continue
            element.first = deref(it2).first
            min_heappush(heap, k, element)
            inc(it2)
        return heap

    def knn_search(self, key: int, k: int) -> list:
        """包装knn_search方法给Python程序调用。"""
        cdef:
            cpp_map[int, vector[pair[int, float]]].iterator it
            cpp_map[int, vector[pair[int, float]]].iterator end = self._cache.end()
        it = self._cache.find(key)
        if it != end:
            return deref(it).second
        return self._knn_search(key, k)

    cdef vector[pair[int, float]] _recommend(self, cpp_set[int]& items, unsigned int k) except +:
        """根据用户的评分过的物品列表推荐物品，不推荐用户已经评分过的物品。"""
        cdef:
            cpp_set[int].iterator it = items.begin()
            cpp_set[int].iterator end = items.end()
            cpp_map[int, float] score_map
            cpp_map[int, vector[pair[int, float]]].iterator it_cache
            cpp_map[int, vector[pair[int, float]]].iterator end_cache = self._cache.end()
        while it != end:
            it_cache = self._cache.find(deref(it))
            if it_cache != end_cache:
                top_k = deref(it_cache).second
            else:
                top_k = self._knn_search(deref(it), k)
            agg_score(score_map, top_k, items)
            inc(it)
        return top_k_map(score_map, k)

    def recommend(self, items: list, k: int):
        """包装recommend方法给Python程序调用。"""
        return self._recommend(items, k)
