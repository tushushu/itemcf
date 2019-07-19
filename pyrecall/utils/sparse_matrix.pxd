"""
@Author: tushushu
@Date: 2019-07-03 15:02:25
"""

from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.unordered_set cimport unordered_set as cpp_set
from libcpp.vector cimport vector
from libcpp.utility cimport pair


cdef class SparseMatrixBinary:
    # 以C++对象存储的稀疏矩阵。
    cdef cpp_map[int, vector[int]] data
    # 热门Key的KNN查找结果。
    cdef cpp_map[int, vector[pair[int, float]]] cache
    # 访问稀疏矩阵中的稀疏向量。
    cdef vector[int] get(self, int key)
    # 线性查找与key对应的向量相似度最大的k个向量，且这些向量的key不能与被查找的key相同。
    cdef vector[pair[int, float]] knn_search(self, int key, unsigned int k) except +
    # 根据用户的评分过的物品列表推荐物品，不推荐用户已经评分过的物品。
    cdef vector[pair[int, float]] recommend(self, cpp_set[int]& items, unsigned int k) except +
