"""
@Author: tushushu
@Date: 2019-07-10 11:19:38
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from typing import List, Tuple
from random import shuffle
from pyrecall.utils.heap import min_heappush_py


def test_min_heap(n_test: int):
    """测试小顶堆的heappush函数是否正确。

    Arguments:
        n_test {int} -- 测试次数。
    """
    print("测试小顶堆的heappush函数是否正确...")
    for i in range(n_test):
        n_elements = i
        arr = list(enumerate(map(float, range(n_elements))))
        shuffle(arr)
        print("测试数组为", arr)
        for j in range(n_elements):
            max_size = j + 1
            print("寻找top %d个元素" % max_size)
            heap = []  # type: List[Tuple[int, float]]
            for element in arr:
                heap = min_heappush_py(heap, max_size, element)
            expected = sorted(arr, reverse=True)[:max_size]
            actual = sorted(heap, reverse=True)
            print("expected", expected)
            print("actual", actual)
            print()
            assert str(expected) == str(actual), "测试不通过!\n"
            heap = []
    print("共计测试%d次, " % n_test, "测试通过!\n")


if __name__ == "__main__":
    test_min_heap(100)
