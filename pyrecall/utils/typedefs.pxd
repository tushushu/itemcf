"""
@Author: tushushu
@Date: 2019-07-29 11:54:53
"""
from libcpp.unordered_map cimport unordered_map as cpp_map
from libcpp.unordered_set cimport unordered_set as cpp_set
from libcpp.utility cimport pair
from libcpp.vector cimport vector


# Element及评分。
ctypedef pair[int, float] IFPAIR
# 稀疏向量，用户对物品的评分为离散值。
ctypedef vector[int] BINVEC
ctypedef vector[int].iterator BINVEC_IT
# 稀疏向量，用户对物品的评分连续值。
ctypedef vector[IFPAIR] CONVEC
ctypedef vector[IFPAIR].iterator CONVEC_IT
# 稀疏向量，泛型。
ctypedef fused VEC:
    BINVEC
    CONVEC
# 稀疏矩阵，用户对物品的评分为离散值。
ctypedef cpp_map[int, BINVEC] BINMAT
ctypedef cpp_map[int, BINVEC].iterator BINMAT_IT
# 稀疏矩阵，用户对物品的评分连续值。
ctypedef cpp_map[int, CONVEC] CONMAT
ctypedef cpp_map[int, CONVEC].iterator CONMAT_IT
# 稀疏矩阵，泛型。
ctypedef fused MAT:
    BINMAT
    CONMAT
# 元素为整数的Set，存储Element
ctypedef cpp_set[int] ISET
ctypedef cpp_set[int].iterator ISET_IT
# Key为整数，Value为浮点数的Map，存储Element及对应的评分
ctypedef cpp_map[int, float] IFMAP
ctypedef cpp_map[int, float].iterator IFMAP_IT
