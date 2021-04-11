"""
@Author: tushushu
@Date: 2019-07-10 11:19:38
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))


from math import isclose
from collections import Counter
from itertools import chain, repeat
from heapq import nlargest
from time import time
from typing import Dict, List, Set
from random import randint, sample
from src.utils.sparse_matrix_bin import SparseMatrixBinary


def jaccard_sim(set1: Set[int], set2: Set[int]) -> float:
    """计算Jaccard相似度函数。

    Arguments:
        set1 {Set[int]} -- 稀疏向量1。
        set2 {Set[int]} -- 稀疏向量2。

    Returns:
        float -- Jaccard相似度。
    """
    denominator = len(set1 | set2)
    if denominator == 0:
        return 0.0
    numerator = len(set1 & set2)
    return numerator / denominator


def _knn_search(key: int, mat: Dict[int, Set[int]]):
    set1 = mat[key]
    for key2, set2 in mat.items():
        if key2 == key:
            continue
        sim = jaccard_sim(set1, set2)
        if isclose(sim, 0.0, abs_tol=1e-8):
            continue
        yield (key2, sim)


def knn_search(key: int, k: int, mat: Dict[int, Set[int]]) -> list:
    """TOP K相似度最大的向量查找， 用于测试SparseMatrixBinary类的knn_search方法。

    Arguments:
        key {int} -- 向量名称。
        k {int} -- 返回结果的数量。
        mat {Dict[int, Set[int]]} -- 稀疏矩阵。

    Returns:
        list -- TOP K相似度最大的向量。
    """
    return nlargest(k, _knn_search(key, mat), key=lambda x: x[1])


def get_test_cases(n_rows: int, n_cols: int) -> Dict[int, List[int]]:
    """生成n_rows * n_cols的稀疏矩阵，满足矩阵中的每个稀疏向量元素随机。

    Arguments:
        n_rows {int} -- 稀疏矩阵的行数。
        n_cols {int} -- 稀疏矩阵的列数。

    Returns:
        Dict[int, List[int]] -- 稀疏矩阵。
    """
    ret = dict()
    items = list(range(n_cols))
    for i in range(n_rows):
        ret[i] = sorted(sample(items, randint(1, n_cols)))
    return ret


def get_top_popular_element(k: int, mat: Dict[int, Set[int]]) -> List[int]:
    """取出最热门的物品。

    Arguments:
        k {int} -- 取出热门物品的个数。
        mat {Dict[int, Set[int]]} -- 稀疏矩阵。

    Returns:
        List[int]
    """
    return nlargest(k, mat, key=lambda x: len(mat[x]))


def test_knn_search(n_rows: int, tolerance=0.0001):
    """测试SparseMatrixBinary类的knn_search方法是否正确。
    """
    print("测试SparseMatrixBinary类的knn_search方法是否正确...")
    n_cols = int(n_rows ** 0.5)
    k_max = int(n_cols ** 0.5)
    test_cases = get_test_cases(n_rows, n_cols)
    mat_py = {k: set(v) for k, v in test_cases.items()}
    mat_cpp = SparseMatrixBinary(test_cases)
    runtime_expected = runtime_actual = 0.0
    for i, key in enumerate(test_cases):
        print("第%d次测试！" % (i + 1))
        k = randint(1, k_max)
        start = time()
        expected = knn_search(key, k, mat_py)
        end = time()
        runtime_expected += end - start
        start = time()
        actual = mat_cpp.knn_search(key, k)
        end = time()
        # actual是top k，但不保证顺序，需要排序再与expected进行比较
        actual.sort(key=lambda x: x[1], reverse=True)
        runtime_actual += end - start
        print("expected", expected)
        print("actual", actual)
        print()
        diff = all((a[1] - b[1]) < tolerance for a, b in zip(expected, actual))
        assert diff, "测试不通过!\n"
    print("共计测试%d次, " % n_rows, "测试通过!\n")
    print("未优化版本的运行时间为%.3f秒!" % runtime_expected)
    print("优化版本的运行时间为%.3f秒!" % runtime_actual)
    print("性能提升了%.1f倍!" % (runtime_expected / runtime_actual))


def test_knn_search_cache(n_rows: int, tolerance=0.0001):
    """test_knn_search函数的基础上加入缓存，且增加高频物品的测试次数。
    """
    print("test_knn_search函数的基础上加入缓存，且增加高频物品的测试次数...")
    n_cols = int(n_rows ** 0.5)
    test_cases = get_test_cases(n_rows, n_cols)
    mat_py = {k: set(v) for k, v in test_cases.items()}
    # 固定k值
    k = int(n_cols ** 0.5)
    mat_cpp = SparseMatrixBinary(test_cases)
    runtime_expected = runtime_actual = 0.0
    # 缓存10%的高频物品
    n_pop = int(0.1 * n_rows)
    popular_element = get_top_popular_element(n_pop, mat_py)
    cache = {x: mat_cpp.knn_search(x, k) for x in popular_element}
    mat_cpp.cache = cache
    # 增加高频物品的测试次数
    ite = chain(*(list(repeat(k, len(v))) for k, v in mat_py.items()))
    for i, key in enumerate(ite):
        print("第%d次测试！" % (i + 1))
        start = time()
        expected = knn_search(key, k, mat_py)
        end = time()
        runtime_expected += end - start
        start = time()
        actual = mat_cpp.knn_search(key, k)
        end = time()
        # actual是top k，但不保证顺序，需要排序再与expected进行比较
        actual.sort(key=lambda x: x[1], reverse=True)
        runtime_actual += end - start
        print("expected", expected)
        print("actual", actual)
        print()
        diff = all((a[1] - b[1]) < tolerance for a, b in zip(expected, actual))
        assert diff, "测试不通过!\n"
    print("共计测试%d次, " % i, "测试通过!\n")
    print("未优化版本的运行时间为%.3f秒!" % runtime_expected)
    print("优化版本的运行时间为%.3f秒!" % runtime_actual)
    print("性能提升了%.1f倍!" % (runtime_expected / runtime_actual))


if __name__ == "__main__":
    # 测试SparseMatrixBinary类的knn_search方法是否正确。
    test_knn_search(3000)
    # test_knn_search函数的基础上加入缓存，且增加高频物品的测试次数。
    test_knn_search_cache(1000)
