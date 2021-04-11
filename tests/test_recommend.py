"""
@Author: tushushu
@Date: 2019-07-17 10:55:24
"""
import os
from random import sample, randint

os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from collections import defaultdict
from typing import Dict, List
from src.utils.sparse_matrix_bin import SparseMatrixBinary
from tests.test_knn_search import get_test_cases

# 用户的user * item矩阵
MAT = {
    0: [1, 2, 3],
    1: [1, 2, 5],
    2: [3, 4, 5],
    3: [2, 4, 5],
}

# 手动计算的推荐结果 user * item
RECOMMENDATION = {
    0: [5, 4],
    1: [3, 4],
    2: [2, 1],
    3: [3, 1]
}


def transpose(matrix: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """对稀疏矩阵进行转置。

    Arguments:
        matrix {Dict[int, List[int]]} -- 稀疏矩阵。

    Returns:
        DefaultDict[int, List[int]] -- 转置矩阵。
    """
    ret = defaultdict(list)  # type: Dict[int, List[int]]
    for key, val in matrix.items():
        for element in val:
            ret[element].append(key)
    return {key: val for key, val in ret.items()}


def test_recommend_accuracy(n_rows: int):
    """测试SparseMatrixBinary类的recommend方法推出内容是否与手动计算结果一致。
    """
    print("测试SparseMatrixBinary类的recommend方法推出内容是否与手动计算结果一致...")
    k = 2
    print("原矩阵为:\n", MAT, "\n")
    mat_t = transpose(MAT)
    print("转置后的矩阵为:\n", mat_t, "\n")
    sparse_mat = SparseMatrixBinary(mat_t)
    cache = {x: sparse_mat.knn_search(x, k) for x in [2, 5]}
    sparse_mat.cache = cache
    print("sparse_mat.cache", sparse_mat.cache)
    for key, val in MAT.items():
        print("key:", key, "val:", val)
        expected = RECOMMENDATION[key]
        print("expected", expected)
        actual = sparse_mat.recommend(val, k)
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
    mat = SparseMatrixBinary(test_cases)
    mat_trans = transpose(test_cases)
    for i, key in enumerate(mat_trans):
        print("第%d次测试！" % (i + 1))
        rated = mat_trans[key]
        recommendation = mat.recommend(rated, k)
        print("rated", rated)
        print("recommendation", recommendation)
        print()
        assert all(x[0] not in set(rated) for x in recommendation), "测试不通过!\n"
    print("共计测试%d次, " % n_cols, "测试通过!\n")


def _test_recommend_checklist_logic(validlist: set, blacklist: set,
                                    mat: dict, mat_t: dict,
                                    k: int):
    print(f"validlist={validlist}, blacklist={blacklist}")
    sparse_mat = SparseMatrixBinary(mat_t, validlist, blacklist)
    for key, val in mat.items():
        # print("key:", key, "val:", val)
        actual = sparse_mat.recommend(val, k)
        if validlist:
            # print("check recommend in validlist")
            for rec in actual:
                assert rec[0] in validlist, '测试不通过!\n'
        if blacklist:
            # print("check recommend in blacklist")
            for rec in actual:
                assert rec[0] not in blacklist, '测试不通过!\n'


def _test_recommend_checklist_bound(validlist: set, blacklist: set, mat_t: dict):
    print(f"validlist={validlist}, blacklist={blacklist}")
    try:
        SparseMatrixBinary(mat_t, validlist, blacklist)
        raise Exception('测试不通过!\n')
    except AssertionError:
        pass


def test_recommend_checklist(n_rows: int):
    """测试SparseMatrixBinary类的recommend方法中合法非法清单是否生效。
    """
    print("测试SparseMatrixBinary类的recommend方法中合法非法清单是否生效...")
    n_cols = n_rows * 10
    k = int(n_cols ** 0.5)
    mat = get_test_cases(n_rows, n_cols)
    mat_t = transpose(mat)

    print("转置后的矩阵大小为:\n", len(mat_t.keys()), "\n")

    test_cases = get_test_cases_logic(mat_t)
    i = 1
    for valid_list, blacklist in test_cases:
        print(f"\n第{i}次测试！")
        _test_recommend_checklist_logic(valid_list, blacklist, mat, mat_t, k)
        i += 1
    print("测试通过!\n")

    print("合法非法清单边界测试...")
    print("原矩阵为:\n", MAT, "\n")
    mat_t = transpose(MAT)
    print("转置后的矩阵为:\n", mat_t, "\n")
    test_cases = get_test_cases_bound()
    for valid_list, blacklist in test_cases:
        _test_recommend_checklist_bound(valid_list, blacklist, mat_t)
    print("测试通过!\n")


def get_test_cases_logic(mat_t: dict, n_test: int = 1000):
    ret = list()
    valid_list = set()
    blacklist = set()
    for i in range(n_test):
        max_i = max(1, len(mat_t.keys()) // 10)
        valid_list = set(sample(mat_t.keys(), randint(1, max_i)))
        blacklist = set(sample(mat_t.keys(), randint(1, max_i)))

        if valid_list.issubset(blacklist):
            continue
        ret.append([valid_list, blacklist])

    ret.append([None, None])
    ret.append([valid_list, None])
    ret.append([None, blacklist])

    return ret


def get_test_cases_bound():
    # 1两个都在,24仅在合法清单,3仅在非法清单,5两个都不在
    valid_list = {1, 2, 4}
    blacklist = {1, 3}
    # validlist是blacklist的子集
    valid_list2 = {1}

    ret = list()
    ret.append([set(), None])
    ret.append([set(), blacklist])
    ret.append([None, set()])
    ret.append([valid_list, set()])
    ret.append([valid_list2, blacklist])
    return ret


if __name__ == "__main__":
    test_recommend_accuracy(100)
    test_recommend_checklist(50)
