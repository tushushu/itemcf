"""
@Author: tushushu
@Date: 2019-06-18 21:07:41
"""


cimport cython

# C++
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.utility cimport pair
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.vector cimport vector


cdef class SparseMatrix:

    def __init__(self, iterator):
        for k, v in iterator:
            self.my_map[k] = v


    def __len__(self):
        return self.my_map.size()


    def __getitem__(self, int key):
        cdef cpp_map[int, cpp_set[int]].iterator it = self.my_map.find(key)
        if it == self.my_map.end():
            raise KeyError('%i' % key)
        return deref(it).second


    def __setitem__(self, int key, vector[int] value):
        self.my_map[key] = value


    def __iter__(self):
        cdef cpp_map[int, cpp_set[int]].iterator it = self.my_map.begin()
        cdef cpp_map[int, cpp_set[int]].iterator end = self.my_map.end()
        while it != end:
            yield deref(it).first, deref(it).second
            inc(it)
    
    # 使用cdivision的时候，不做除零检查，也不会把int类型自动转为float类型
    @cython.cdivision(True)
    cdef float _get_jaccard_sim(self, vector[int] vector_1, vector[int] vector_2):
        cdef:
            float ret = 0.0
            int numerator = 0
            int m = vector_1.size()
            int n = vector_2.size()
            int i = 0
            int j = 0
        if m == 0 or n == 0:
            return ret
        if vector_1[m - 1] < vector_2[0]:
            return ret
        if vector_2[n - 1] < vector_1[0]:
            return ret
        while i < m and j < n:
            if vector_1[i] == vector_2[j]:
                i += 1
                j += 1
                numerator += 1
            elif vector_1[i] > vector_2[j]:
                j += 1
            else:
                i += 1
        if numerator == 0:
            return ret
        ret = float(numerator) / (m + n - numerator)
        return ret

    def get_jaccard_sim(self):
        pass
