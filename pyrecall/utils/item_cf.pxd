"""
@Author: tushushu
@Date: 2019-07-16 15:36:43
"""
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.unordered_set cimport unordered_set as cpp_set
from libcpp.vector cimport vector
from libcpp.utility cimport pair


# 将top_k中element添加到score_map中，如果elment已存在则累加其分数。
cdef void agg_score(cpp_map[int, float]& score_map, vector[pair[int, float]]& top_k, cpp_set[int]& exclude_elements) except *
# 根据map的value取出最大的top k pair，并按照value的降序排列。
cdef vector[pair[int, float]] top_k_map(cpp_map[int, float]& score_map, unsigned int k) except +
