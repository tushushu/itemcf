# distutils: language = c++
"""
@Author: tushushu
@Date: 2019-06-20 19:54:32
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))

from func_timer import func_timer
from libcpp.vector cimport vector as vector
cimport cython



cdef class CommonElements1:
    def __init__(self, list arr1, list arr2):
        self.vector_1 = arr1
        self.vector_2 = arr2

    @func_timer(1000, False)
    def count_common_elements_3(self):
        cdef:
            int ret = 0
            vector[int] vector_1 = self.vector_1
            vector[int] vector_2 = self.vector_2
            int m = vector_1.size()
            int n = vector_2.size()
            int i = 0
            int j = 0

        while i < m and j < n:
            if vector_1[i] == vector_2[j]:
                i += 1
                j += 1
                ret += 1
            elif vector_1[i] > vector_2[j]:
                j += 1
            else:
                i += 1
        return ret


cdef class CommonElements2:
    def __init__(self, list arr1, list arr2):
        self.vector_1 = arr1
        self.vector_2 = arr2

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @func_timer(1000, False)
    def count_common_elements_4(self):
        cdef:
            int ret = 0
            vector[int] vector_1 = self.vector_1
            vector[int] vector_2 = self.vector_2
            int m = vector_1.size()
            int n = vector_2.size()
            int i = 0
            int j = 0

        while i < m and j < n:
            if vector_1[i] == vector_2[j]:
                i += 1
                j += 1
                ret += 1
            elif vector_1[i] > vector_2[j]:
                j += 1
            else:
                i += 1
        return ret
