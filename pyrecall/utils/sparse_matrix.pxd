"""
@Author: tushushu
@Date: 2019-06-18 20:54:54
"""


from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.vector cimport vector

###############################################################################
# An object to be used in Python

cdef class SparseMatrix:
    cdef cpp_map[int, vector[int]] my_map