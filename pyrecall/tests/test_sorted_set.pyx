# distutils: language = c++
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

"""
@Author: tushushu
@Date: 2019-06-18 21:07:41
"""
from libcpp.set cimport set as cpp_set
from cython.operator cimport dereference as deref, preincrement as inc
from random import shuffle


def test_sorted_set(n_elements: int):
    """测试C++的set是否会把元素按照升序排列。
    
    Arguments:
        n_elements {int} -- set中元素的数量。
    """
    print("测试C++的set是否会把元素按照升序排列...")
    my_list = list(range(n_elements))
    shuffle(my_list)
    cdef cpp_set[int] my_set = my_list
    my_list.sort()
    cdef cpp_set[int].iterator it = my_set.begin()
    cdef int b

    for i in range(n_elements):
        a = my_list[i]
        b = deref(it)
        inc(it)
        assert a == b, "测试不通过!\n"
    print("测试通过!\n")
