"""
@Author: tushushu
@Date: 2019-07-24 18:09:07
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from random import randint
from tests.dymanic_method import Cal


def test_dymanic_method(n_test: int):
    """测试动态方法，根据类的初始化参数绑定对应的函数指针。
    """
    my_sum = Cal("my_sum")
    my_mul = Cal("my_mul")
    for _ in range(n_test):
        num1 = randint(1, 100)
        num2 = randint(1, 100)
        assert my_sum(num1, num2) == num1 + num2, "测试不通过!\n"
        assert my_mul(num1, num2) == num1 * num2, "测试不通过!\n"
    print("共计测试%d次, " % n_test, "测试通过!\n")


if __name__ == "__main__":
    test_dymanic_method(100)
