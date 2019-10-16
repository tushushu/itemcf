"""
@Author: tushushu
@Date: 2019-07-03 15:27:19
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from utils.sim_metrics import jaccard_sim_py
from random import sample, randint
from typing import List


def jaccard_sim(list1: List[int], list2: List[int]) -> float:
    """计算Jaccard相似度函数，用于校验jaccard_sim_py函数。

    Arguments:
        list1 {List[int]} -- 稀疏向量1。
        list2 {List[int]} -- 稀疏向量2。

    Returns:
        float -- Jaccard距离。
    """
    set1 = set(list1)
    set2 = set(list2)
    denominator = len(set1 | set2)
    if denominator == 0:
        return 0.0
    numerator = len(set1 & set2)
    return numerator / denominator


def gen_test_cases(n_cases: int, low: int, high: int) -> List[List[List[int]]]:
    """随机生成n_cases个List作为测试用例，满足如下条件：
    1. 元素大小介于low和high之间；
    2. 元素个数不超过high-low；
    3. List是升序的。

    Arguments:
        n_cases {int} -- 测试用例的数量。
        low {int} -- 测试用例中元素大小、个数的下界。
        high {int} -- 测试用例中元素大小、个数的上界。

    Returns:
        List[List[List[int]]] -- 测试用例。
    """
    test_cases = []
    for _ in range(n_cases):
        test_case = []
        for _ in range(2):
            rand_list = sample(range(low, high), randint(0, high - low))
            rand_list.sort()
            test_case.append(rand_list)
        test_cases.append(test_case)
    return test_cases


def test_sim_metrics(n_test: int):
    """测试Jaccard相似度计算函数是否正确。

    Arguments:
        n_test {int} -- 测试次数。
    """
    print("测试Jaccard相似度计算函数是否正确...")
    low = 0
    high = 10
    tolerance = 0.001
    test_cases = gen_test_cases(n_test, low, high)
    for test_case in test_cases:
        list1, list2 = test_case
        sim1 = jaccard_sim_py(list1, list2)
        sim2 = jaccard_sim(list1, list2)
        print("预期结果: %.3f" % sim2, "实际结果: %.3f" % sim1)
        assert abs(sim1 - sim2) < tolerance, "测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")


if __name__ == "__main__":
    test_sim_metrics(10000)
