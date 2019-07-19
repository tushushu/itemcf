"""
@Author: tushushu
@Date: 2019-07-10 14:18:41
"""

from libcpp cimport bool
from libcpp.utility cimport pair
from libcpp.vector cimport vector


# 比较小顶堆两个元素的大小，其中.first为元素的名称，.second为元素的值。
cdef bool cmp(const pair[int, float]& element1, const pair[int, float]& element2) except +
# 比较大顶堆两个元素的大小，其中.first为元素的名称，.second为元素的值。
cdef bool _cmp(const pair[int, float]& element1, const pair[int, float]& element2) except +
# 将元素Push到一个小顶堆中，保持堆的特性，且元素个数不超过max_size。
cdef void heappush(vector[pair[int, float]]& heap, unsigned int max_size, const pair[int, float]& element) except *
# 将元素Push到一个大顶堆中，保持堆的特性，且元素个数不超过max_size。
cdef void _heappush(vector[pair[int, float]]& heap, unsigned int max_size, const pair[int, float]& element) except *