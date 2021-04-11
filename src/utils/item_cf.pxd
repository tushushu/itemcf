"""
@Author: tushushu
@Date: 2019-07-16 15:36:43
"""
from libcpp cimport bool
from .typedefs cimport IFMAP, CONVEC, ISET, CONVEC_IT, IFPAIR


# 将top_k中element添加到score_map中，如果elment已存在则累加其分数。
cdef void agg_score(IFMAP& score_map, CONVEC& top_k, ISET& exclude_elements) except *
# 根据map的value取出最大的top k pair，并按照value的降序排列。
cdef CONVEC top_k_map(IFMAP& score_map, unsigned int k) except +


# Will got a complie error if directly import libcpp.algorithm.sort_heap and use generic type.
cdef extern from "<algorithm>" namespace "std":
    void sort_heap(CONVEC_IT first, CONVEC_IT last, bool (const IFPAIR &, const IFPAIR &))