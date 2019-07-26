"""
@Author: tushushu
@Date: 2019-07-03 15:27:19
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from typing import Dict, List, Tuple
from random import randint, sample
from utils.sparse_matrix import SparseMatrixBinary


def gen_rand_dict(low: int, high: int) -> Dict[int, List[int]]:
    """生成随机字典，满足如下条件：
    1. 字典长度介于low和high之间；
    2. Key, Value的大小介于0和n_elements之间。

    Arguments:
        low {int} -- 字典长度的下界。
        high {int} -- 字典长度的上界。

    Returns:
        Dict[int, List[int]] -- 随机字典。
    """
    n_elements = randint(low, high)
    pairs = ((i, [i]) for i in range(n_elements))
    return dict(pairs)


def cmp_dict(dict1: Dict[int, List[int]], dict2: Dict[int, List[int]]) -> bool:
    """比较两个字典是否相同。

    Arguments:
        dict1 {Dict[int, List[int]]}
        dict2 {Dict[int, List[int]]}

    Returns:
        bool
    """
    if len(dict1) != len(dict2):
        return False
    for key1, val1 in dict1.items():
        if key1 not in dict2:
            return False
        val2 = dict2[key1]
        if len(val1) != len(val2) or any(a != b for a, b in zip(val1, val2)):
            return False
    return True

def cmp_cache(dict1: Dict[int, List[Tuple[int, float]]], 
    dict2: Dict[int, List[Tuple[int, float]]]):
    if len(dict1) != len(dict2):
        return False
    for key1, val1 in dict1.items():
        val2 = dict2[key1]
        if len(val1) != len(val2):
            return False
        for a, b in zip(val1, val2):
            if a[0] != b[0] or abs(a[1] - b[1]) > 0.001:
                return False
    return True

def test_sparse_matrix_binary(n_test: int):
    """测试SparseMetrixBinary类的方法是否正确。

    Arguments:
        n_test {int} -- 测试次数。
    """
    print("测试SparseMetrixBinary类的方法是否正确...")
    low = 0
    high = 100
    for i in range(n_test):
        print("第%d次测试！" % (i + 1))
        rand_dict = gen_rand_dict(low, high)
        print("测试用例：", rand_dict)
        print()
        mat = SparseMatrixBinary(rand_dict)
        assert len(mat) == len(rand_dict), "__len__方法测试不通过!\n"
        for key in rand_dict:
            assert rand_dict[key] == mat[key], "__getitem__方法测试不通过!\n"
        mat[high + 1] = [high + 1]
        rand_dict[high + 1] = [high + 1]
        assert mat[high + 1] == [high + 1], "__setitem__方法测试不通过!\n"
        rand_num = randint(0, len(rand_dict))
        mat[rand_num] = [rand_num + 1]
        rand_dict[rand_num] = [rand_num + 1]
        assert mat[rand_num] == [rand_num + 1], "__setitem__方法测试不通过!\n"
        for key, value in mat:
            assert rand_dict[key] == value, "__iter__方法测试不通过!\n"
        assert len(list(iter(mat))) == len(rand_dict), "__iter__方法测试不通过!\n"
        assert len(list(iter(mat))) == len(
            list(set(map(str, mat)))), "__iter__方法测试不通过!\n"
        assert cmp_dict(mat.data, rand_dict), "data属性测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")
    cache = {1: [(2, 0.5), (3, 0.4)], 4: [(5, 0.5), (6, 0.4)]}
    print("cache", cache)
    mat.cache = cache
    assert cmp_cache(mat.cache, cache), "cache属性测试不通过!\n"
    print("cache属性测试通过!\n")


if __name__ == "__main__":
    test_sparse_matrix_binary(100)
