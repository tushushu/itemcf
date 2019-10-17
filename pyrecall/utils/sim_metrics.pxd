"""
@Author: tushushu
@Date: 2019-07-03 14:35:36
"""

from libcpp.vector cimport vector
from .typedefs cimport BINVEC, CONVEC


# 计算集合A与B的Jaccard相似度，Similarity = A ∩ B / A ∪ B。
cdef float jaccard_sim(BINVEC& v1, BINVEC& v2) except +
# 计算向量A与B的点积。
cdef float vector_dot(CONVEC& v1, CONVEC& v2) except +
# 计算向量的模长。
cdef float vector_module(CONVEC& v) except +
# 计算向量A与向量B的余弦相似度，Similarity = A dot B / A x B。
cdef float cosine_sim(CONVEC& v1, CONVEC& v2) except +
# 内联函数，除零检查，计算向量A与向量B的余弦相似度，Similarity = A dot B / A x B。
cdef float fast_cosine_sim(float dot_product, float module1, float module2) except +
# 内联函数，计算x的平方。
cdef float pow2(float x) except +
