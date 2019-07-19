"""
@Author: tushushu
@Date: 2019-07-03 14:35:36
"""
from libcpp.vector cimport vector


cdef float jaccard_sim(vector[int]& v1, vector[int]& v2) except +
