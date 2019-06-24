"""
@Author: tushushu
@Date: 2019-06-20 19:54:30
"""

from libcpp.vector cimport vector as vector

###############################################################################
# An object to be used in Python

cdef class CommonElements1:
    cdef vector[int] vector_1
    cdef vector[int] vector_2


cdef class CommonElements2:
    cdef vector[int] vector_1
    cdef vector[int] vector_2