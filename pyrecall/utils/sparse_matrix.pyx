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
from .heap cimport heappush
from .sim_metrics cimport jaccard_sim
from .item_cf cimport agg_score, top_k_map


cdef class SparseMatrixBinary:
    """稀疏矩阵的C++实现(离散值)。
    如长度为5的稠密向量[0, 1, 0, 0, 1]，其稀疏向量表示为[1, 4]。

    Arguments:
        data {Dict[int, List[int]]} -- 以Python对象存储的稀疏矩阵。
        popular_keys {List[int]} -- 把热门Key对应的KNN查找结果缓存起来提升性能。
        k {unsigned int} -- 热门Key的KNN查找结果返回的元素数量。

    Attributes:
        data {cpp_map[int, vector[int]]} -- 以C++对象存储的稀疏矩阵。
        cache {cpp_map[int, vector[pair[int, float]]]} -- 热门Key的KNN查找结果。
    """

    def __init__(self, dict data, list popular_keys, unsigned int k):
        self.data = data
        for key in popular_keys:
            self.cache[key] = self.knn_search(key, k)

    def __len__(self):
        return self.data.size()

    def __getitem__(self, int key):
        return self.get(key)

    def __setitem__(self, int key, vector[int] value):
        self.data[key] = value

    def __iter__(self):
        cdef:
            cpp_map[int, vector[int]].iterator it = self.data.begin()
            cpp_map[int, vector[int]].iterator end = self.data.end()
        while it != end:
            yield deref(it).first, deref(it).second
            inc(it)

    cdef vector[int] get(self, int key):
        """访问稀疏矩阵中的稀疏向量。"""
        cdef cpp_map[int, vector[int]].iterator it = self.data.find(key)
        if it == self.data.end():
            raise KeyError('%i' % key)
        return deref(it).second

    cdef vector[pair[int, float]] knn_search(self, int key, unsigned int k) except +:
        """线性查找与key对应的向量相似度最大的k个向量，且这些向量的key不能与被查找的key相同。"""
        cdef:
            vector[pair[int, float]] heap
            pair[int, float] element
            cpp_map[int, vector[int]].iterator it1 = self.data.find(key)
            cpp_map[int, vector[int]].iterator it2 = self.data.begin()
            cpp_map[int, vector[int]].iterator end = self.data.end()
        if it1 == end:
            return heap
        while it2 != end:
            element.second = jaccard_sim(deref(it1).second, deref(it2).second)
            if element.second == 0.0 or it2 == it1:
                inc(it2)
                continue
            element.first = deref(it2).first
            heappush(heap, k, element)
            inc(it2)
        return heap

    def knn_search_py(self, key: int, k: int) -> list:
        """包装knn_search方法给Python程序调用。"""
        cdef:
            cpp_map[int, vector[pair[int, float]]].iterator it
            cpp_map[int, vector[pair[int, float]]].iterator end = self.cache.end()
        it = self.cache.find(key)
        if it != end:
            return deref(it).second
        return self.knn_search(key, k)

    cdef vector[pair[int, float]] recommend(self, cpp_set[int]& items, unsigned int k) except +:
        """根据用户的评分过的物品列表推荐物品，不推荐用户已经评分过的物品。"""
        cdef:
            cpp_set[int].iterator it = items.begin()
            cpp_set[int].iterator end = items.end()
            cpp_map[int, float] score_map
            cpp_map[int, vector[pair[int, float]]].iterator it_cache
            cpp_map[int, vector[pair[int, float]]].iterator end_cache = self.cache.end()
        while it != end:
            it_cache = self.cache.find(deref(it))
            if it_cache != end_cache:
                top_k = deref(it_cache).second
            else:
                top_k = self.knn_search(deref(it), k)
            agg_score(score_map, top_k, items)
            inc(it)
        return top_k_map(score_map, k)

    def recommend_py(self, items: list, k: int):
        """包装recommend方法给Python程序调用。"""
        return self.recommend(items, k)
