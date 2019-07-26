# distutils: language = c++
#cython: boundscheck=False
#cython: wraparound=False

"""
@Author: tushushu
@Date: 2019-07-16 15:36:10
"""
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.unordered_set cimport unordered_set as cpp_set
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.algorithm cimport sort_heap
from .heap cimport min_heappush, min_cmp


cdef void agg_score(cpp_map[int, float]& score_map, vector[pair[int, float]]& top_k, cpp_set[int]& exclude_elements) except *:
    """将top_k中element添加到score_map中，如果elment已存在则累加其分数。"""
    cdef:
        vector[pair[int, float]].iterator it = top_k.begin()
        vector[pair[int, float]].iterator end = top_k.end()
    while it != end:
        if exclude_elements.count(deref(it).first):
            inc(it)
            continue
        if score_map.count(deref(it).first):
            score_map[deref(it).first] += deref(it).second
        else:
            score_map.insert(deref(it))
        inc(it)


cdef vector[pair[int, float]] top_k_map(cpp_map[int, float]& score_map, unsigned int k) except +:
    """根据map的value取出最大的top k pair，并按照value的降序排列。"""
    cdef:
        vector[pair[int, float]] heap
        cpp_map[int, float].iterator it = score_map.begin()
        cpp_map[int, float].iterator end = score_map.end()
    while it != end:
        min_heappush(heap, k, deref(it))
        inc(it)
    sort_heap(heap.begin(), heap.end(), min_cmp)
    return heap


def agg_score_py(score_map: dict, top_k: list, exclude_elements: list) -> dict:
    """包装agg_score函数给Python程序调用。"""
    cdef cpp_map[int, float] _score_map = score_map
    agg_score(_score_map, top_k, exclude_elements)
    return _score_map


def top_k_map_py(score_map: dict, k: int) -> list:
    """包装top_k_map函数给Python程序调用。"""
    return top_k_map(score_map, k)
