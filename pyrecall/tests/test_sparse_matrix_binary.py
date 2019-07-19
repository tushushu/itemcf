"""
@Author: tushushu
@Date: 2019-07-03 15:27:19
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from typing import Dict, List
from random import randint, sample
from utils.sparse_matrix import SparseMatrixBinary


def gen_rand_dict(low: int, high: int)->Dict[int, List[int]]:
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
        # 随机抽样几个key作为cache
        popular_keys = sample(rand_dict.keys(), randint(0, len(rand_dict)))
        # 随机设定top k
        k = randint(0, len(popular_keys))
        mat = SparseMatrixBinary(rand_dict, popular_keys, k)
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
        assert len(list(iter(mat))) == len(list(set(map(str, mat)))), "__iter__方法测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")
