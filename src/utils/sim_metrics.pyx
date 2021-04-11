# distutils: language = c++
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

"""
@Author: tushushu
@Date: 2019-07-03 14:35:36
"""

from typing import List, Tuple
from libc.math cimport sqrt
from cython.operator cimport dereference as deref, preincrement as inc
from .typedefs cimport BINVEC, CONVEC, IFPAIR
 

cdef float jaccard_sim(BINVEC& v1, BINVEC& v2) except +:
    """计算集合A与B的Jaccard相似度，Similarity = A ∩ B / A ∪ B。"""
    cdef:
        int numerator = 0
        int denominator = 0
        int m = v1.size()
        int n = v2.size()
        int i = 0
        int j = 0
    if m == 0 or n == 0:
        return 0.0
    if v1[m - 1] < v2[0]:
        return 0.0
    if v2[n - 1] < v1[0]:
        return 0.0
    while i < m and j < n:
        if v1[i] == v2[j]:
            numerator += 1
            i += 1
            j += 1
        elif v1[i] > v2[j]:
            j += 1
        else:
            i += 1
    if numerator == 0:
        return 0.0
    denominator = m + n - numerator
    return numerator * 1.0 / denominator


def jaccard_sim_py(l1: List[int], l2: List[int])->float:
    """包装jaccard_sim函数给Python程序调用。"""
    return jaccard_sim(l1, l2)


cdef float vector_dot(CONVEC& v1, CONVEC& v2) except +:
    """计算向量A与B的点积。"""
    cdef:
        float ret = 0.0
        int m = v1.size()
        int n = v2.size()
        int i = 0
        int j = 0
        IFPAIR p1
        IFPAIR p2
    if m == 0 or n == 0:
        return 0.0
    if v1[m - 1].first < v2[0].first:
        return 0.0
    if v2[n - 1].first < v1[0].first:
        return 0.0
    while i < m and j < n:
        p1 = v1[i]
        p2 = v2[j]
        if p1.first == p2.first:
            # TODO 如何避免数字溢出, float的范围为-2^128 ~ +2^128
            ret += p1.second * p2.second 
            i += 1
            j += 1
        elif p1.first > p2.first:
            j += 1
        else:
            i += 1
    return ret


cdef float vector_module(CONVEC& v) except +:
    """计算向量的模长。"""
    cdef:
        int i = 0
        int n = v.size()
        float ret = 0.0
    while i < n:
        ret += pow2(v[i].second)
        i += 1
    return sqrt(ret)


cdef float cosine_sim(CONVEC& v1, CONVEC& v2) except +:
    """计算向量A与向量B的余弦相似度，Similarity = A dot B / A x B。"""
    if v1.size() == 0 or v2.size() == 0:
        return 0.0
    cdef:
        float dot_product = vector_dot(v1, v2)
        float module1 = vector_module(v1)
        float module2 = vector_module(v2)
    return fast_cosine_sim(dot_product, module1, module2)


cdef inline float fast_cosine_sim(float dot_product, float module1, float module2) except +:
    """内联函数，除零检查，计算向量A与向量B的余弦相似度，Similarity = A dot B / A x B。"""
    if dot_product == 0.0 or module1 == 0.0 or module2 == 0.0:
        return 0.0
    return dot_product / module1 / module2


cdef inline float pow2(float x) except +:
    """内联函数，计算x的平方。"""
    return x * x


def cosine_sim_py(l1: List[Tuple[int, float]], l2: List[Tuple[int, float]])->float:
    """包装consine_sim函数给Python程序调用。"""
    return cosine_sim(l1, l2)
