# distutils: language = c++
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

"""
@Author: tushushu
@Date: 2019-07-03 14:35:36
"""
from libcpp.vector cimport vector
from typing import List


cdef float jaccard_sim(vector[int]& v1, vector[int]& v2) except +:
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
            i += 1
            j += 1
            numerator += 1
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
