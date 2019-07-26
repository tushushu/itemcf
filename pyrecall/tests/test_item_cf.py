"""
@Author: tushushu
@Date: 2019-07-16 19:39:46
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict
from random import randint, random, sample
from utils.item_cf import agg_score_py, top_k_map_py


def gen_random_list(n_elements: int) -> List[Tuple[int, float]]:
    """随机生成列表，满足列表的元素值随机，且有可能存在元素的第一个值相同的元素。

    Arguments:
        n_elements {int} -- 元素数量。

    Returns:
        List[Tuple[int, float]]
    """
    return [(randint(1, n_elements), random()) for _ in range(n_elements)]


def gen_random_dict(n_elements: int) -> Dict[int, float]:
    """随机生成字典，满足字典的元素值随机。

    Arguments:
        n_elements {int} -- 元素数量。

    Returns:
        Dict[int, float]
    """
    return {key: random() for key in range(n_elements)}


def agg_score(random_list: List[Tuple[int, float]], exclude_elements: List[int]) -> DefaultDict[int, float]:
    """对相同的Item的Score进行求和，用于校验agg_score_py的函数。

    Arguments:
        random_list {List[Tuple[int, float]]} -- 将Item, Score成对存储的列表。
        exclude_elements {List[int]} -- 需要剔除的元素列表。

    Returns:
        DefaultDict[int, float]
    """
    ret = defaultdict(float)  # type: DefaultDict[int, float]
    for key, val in random_list:
        if key not in exclude_elements:
            ret[key] += val
    return ret


def cmp_dict(dict1: DefaultDict[int, float], dict2: Dict[int, float]) -> bool:
    """比较两个字典是否相同。

    Arguments:
        dict1 {DefaultDict[int, float]}
        dict2 {Dict[int, float]}

    Returns:
        bool
    """
    tolerance = 0.001
    if len(dict1) != len(dict2):
        return False
    for key1, val1 in dict1.items():
        if key1 not in dict2:
            return False
        val2 = dict2[key1]
        if abs(val1 - val2) > tolerance:
            return False
    return True


def cmp_list(list1: List[Tuple[int, float]], list2: List[Tuple[int, float]]) -> bool:
    """比较两个列表是否相同。
    """
    if len(list1) != len(list2):
        return False
    for element1, element2 in zip(list1, list2):
        if element1[0] != element2[0]:
            return False
    return True


def print_dict(name: str, my_dict: Dict[int, float]):
    """打印字典，value保留三位小数。
    """
    print(name, [(k, round(v, 3)) for k, v in my_dict.items()])


def print_list(name: str, my_list: List[Tuple[int, float]]):
    """打印列表，value保留三位小数。
    """
    print(name, [(k, round(v, 3)) for k, v in my_list])


def test_agg_score(n_test: int):
    """测试agg_score函数是否正确。
    """
    print("测试agg_score函数是否正确...")
    for i in range(n_test):
        print("第%d次测试！" % (i + 1))
        n_elements = randint(0, 20)
        random_list = gen_random_list(n_elements)
        keys = set(x[0] for x in random_list)
        exclude_elements = sample(keys, randint(0, len(keys)))
        expected = agg_score(random_list, exclude_elements)
        actual = agg_score_py(dict(), random_list, exclude_elements)
        print_dict("expected", expected)
        print_dict("actual", actual)
        print()
        assert cmp_dict(expected, actual), "测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")


def test_top_k_map(n_test: int):
    """测试top_k_map函数是否正确。
    """
    print("测试top_k_map函数是否正确...")
    for i in range(n_test):
        print("第%d次测试！" % (i + 1))
        n_elements = randint(0, 20)
        k = 1 if n_elements <= 1 else randint(1, n_elements)
        random_dict = gen_random_dict(n_elements)
        expected = sorted(random_dict.items(), reverse=True, key=lambda x: x[1])[:k]
        actual = top_k_map_py(random_dict, k)
        print_list("expected", expected)
        print_list("actual", actual)
        print()
        assert cmp_list(expected, actual), "测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")


if __name__ == "__main__":
    # 测试agg_score函数是否正确。
    test_agg_score(1000)
    # 测试top_k_map函数是否正确。
    test_top_k_map(1000)
