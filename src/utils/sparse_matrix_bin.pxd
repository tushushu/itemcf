"""
@Author: tushushu
@Date: 2019-07-03 15:02:25
"""

from libcpp cimport bool
from .typedefs cimport BINMAT, ISET, CONMAT, BINVEC, CONVEC


# 内联函数，判断一个浮点数是否等于0.0。
cdef inline bool iszero(float x)


cdef class SparseMatrixBinary:
    # 以C++对象存储的稀疏矩阵。
    cdef BINMAT _data
    # 以C++对象存储的合法的element清单。
    cdef ISET _valid_list
    # 以C++对象存储的非法的element清单。
    cdef ISET _blacklist
    # 热门Key的KNN查找结果。
    cdef CONMAT _cache
    # 访问稀疏矩阵中的稀疏向量。
    cdef BINVEC _get(self, int key)
    # 线性查找与key对应的向量相似度最大的k个向量，且这些向量的key不能与被查找的key相同。
    cdef CONVEC _knn_search(self, int key, unsigned int k, bool is_sorted=*) except +
    # 根据用户的评分过的物品列表推荐物品，不推荐用户已经评分过的物品。
    cdef CONVEC _recommend(self, ISET& items, unsigned int k) except +
