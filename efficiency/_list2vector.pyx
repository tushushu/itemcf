# distutils: language = c++
"""
@Author: tushushu
@Date: 2019-06-20 10:32:04
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))

from func_timer import func_timer
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.vector cimport vector
from cpython cimport array

@func_timer(10000, False)
def list2vector_1(list arr):
    cdef vector[int] my_vector
    my_vector = arr

@func_timer(10000, False)
def list2vector_2(array.array arr):
    cdef vector[int] my_vector
    my_vector = arr

