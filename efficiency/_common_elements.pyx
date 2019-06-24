"""
@Author: tushushu
@Date: 2019-06-20 15:04:01
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))

from func_timer import func_timer
cimport cython
from cpython cimport array
from libc.string cimport memcmp

@func_timer(1000, False)
def count_common_elements_2(array.array arr1, array.array arr2):
    cdef:
        int ret = 0
        int m = len(arr1)
        int n = len(arr2)
        int i = 0
        int j = 0
        int* p = arr1.data.as_ints
        int* q = arr2.data.as_ints
        int int_size = sizeof(int)
    while i < m and j < n:
        if memcmp(p + i, q + j, int_size):
            i += 1
            j += 1
            ret += 1
        elif arr1[i] > arr1[j]:
            j += 1
        else:
            i += 1
    return ret
