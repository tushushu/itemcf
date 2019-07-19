"""
@Author: tushushu
@Date: 2019-07-17 10:55:24
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from collections import defaultdict
from time import time
from typing import Dict, List
from random import randint, sample
from utils.sparse_matrix import SparseMatrixBinary
from tests.test_knn_search import get_test_cases


MAT = {
    0: [1, 2, 3],
    1: [1, 2, 5],
    2: [3, 4, 5],
    3: [2, 4, 5],
}

RECOMMENDATION = {
    0: [5, 4],
    1: [3, 4],
    2: [2, 1],
    3: [3, 1],
}

def transpose(matrix: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """对稀疏矩阵进行转置。

    Arguments:
        matrix {Dict[int, List[int]]} -- 稀疏矩阵。

    Returns:
        DefaultDict[int, List[int]] -- 转置矩阵。
    """
    ret = defaultdict(list)
    for key, val in matrix.items():
        for element in val:
            ret[element].append(key)
    return {key: val for key, val in ret.items()}


def test_recommend(n_rows: int):
    """测试SparseMatrixBinary类的recommend方法是否正确。
    """
    print("测试SparseMatrixBinary类的recommend方法是否正确...")
    print("测试推荐的内容是否准确...")
    k = 2
    print("原矩阵为:\n", MAT, "\n")
    mat_t = transpose(MAT)
    print("转置后的矩阵为:\n", mat_t, "\n")
    sparse_mat = SparseMatrixBinary(mat_t, [2, 5], k)
    for key, val in MAT.items():
        actual = sparse_mat.recommend_py(val, k)
        expected = RECOMMENDATION[key]
        print("key:", key, "val:", val)
        print("expected", expected)
        print("actual", actual)
        print()
        cond1 = len(actual) == len(expected)
        cond2 = set(x[0] for x in actual) == set(expected)
        assert cond1 and cond2, "测试不通过!\n"
    print("测试通过!\n")
    print("测试推荐的内容是否被用户评分过...")
    n_cols = n_rows * 10
    k = int(n_cols ** 0.5)
    test_cases = get_test_cases(n_rows, n_cols)
    mat = SparseMatrixBinary(test_cases, [], 0)
    mat_trans = transpose(test_cases)
    for i, key in enumerate(mat_trans):
        print("第%d次测试！" % (i + 1))
        rated = mat_trans[key]
        recommendation = mat.recommend_py(rated, k)
        print("rated", rated)
        print("recommendation", recommendation)
        print()
        assert all(x[0] not in set(rated) for x in recommendation), "测试不通过!\n"
    print("共计测试%d次, " % n_cols, "测试通过!\n")
