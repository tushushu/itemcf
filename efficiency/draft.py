"""
@Author: tushushu
@Date: 2019-06-20 14:30:30
"""

def list_intersection_1(list arr1, list arr2):
    cdef cpp_set[int] my_set1 = arr1
    cdef cpp_set[int] my_set2 = arr2
    cdef cpp_set[int].iterator it
    cdef int ret = 0
    if my_set1.size() < my_set2.size():
        it = my_set1.begin()
        end = my_set1.end()
        while it != end:
            inc(it)