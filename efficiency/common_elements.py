"""
@Author: tushushu
@Date: 2019-06-20 15:04:51
"""

"""
结论：函数count_common_elements_3更快。
***************************************************************************
对比count_common_elements_1函数、count_common_elements_2函数、
count_common_elements_3函数、count_common_elements_4函数的性能...

---------------------------------------------------------------------------
长度为1000的两个集合!

函数count_common_elements_1运行--1000次!
累计运行时间为--0.028 s!

函数count_common_elements_2运行--1000次!
累计运行时间为--0.009 s!

函数count_common_elements_3运行--1000次!
累计运行时间为--0.004 s!

函数count_common_elements_4运行--1000次!
累计运行时间为--0.005 s!

---------------------------------------------------------------------------
---------------------------------------------------------------------------
长度为10000的两个集合!

函数count_common_elements_1运行--1000次!
累计运行时间为--0.347 s!

函数count_common_elements_2运行--1000次!
累计运行时间为--0.076 s!

函数count_common_elements_3运行--1000次!
累计运行时间为--0.026 s!

函数count_common_elements_4运行--1000次!
累计运行时间为--0.030 s!

---------------------------------------------------------------------------
---------------------------------------------------------------------------
长度为100000的两个集合!

函数count_common_elements_1运行--1000次!
累计运行时间为--2.980 s!

函数count_common_elements_2运行--1000次!
累计运行时间为--0.710 s!

函数count_common_elements_3运行--1000次!
累计运行时间为--0.265 s!

函数count_common_elements_4运行--1000次!
累计运行时间为--0.293 s!

---------------------------------------------------------------------------
***************************************************************************
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))

import array
from func_timer import func_timer
from _common_elements import count_common_elements_2
from _common_elements_cpp import CommonElements1, CommonElements2

@func_timer(1000, False)
def count_common_elements_1(set1: set, set2: set)->int:
    """计算两个集合的共同元素数量。

    Arguments:
        set1 {set}
        set2 {set}

    Returns:
        int
    """

    return len(set1 & set2)

def test(n_elements):
    print("---------------------------------------------------------------------------")
    print("长度为%d的两个集合!\n" % n_elements)
    list1 = list(range(n_elements))
    mid = n_elements // 2
    list2 = list(range(mid, n_elements + mid))
    set1 = set(list1)
    set2 = set(list2)
    arr1 = array.array('i', list1)
    arr2 = array.array('i', list2)
    count_common_elements_1(set1, set2)
    count_common_elements_2(arr1, arr2)
    ce1 = CommonElements1(list1, list2)
    ce1.count_common_elements_3()
    ce2 = CommonElements2(list1, list2)
    ce2.count_common_elements_4()
    print("---------------------------------------------------------------------------")

if __name__ == "__main__":
    print("***************************************************************************")
    print("""对比count_common_elements_1函数、count_common_elements_2函数、
    count_common_elements_3函数、count_common_elements_4函数的性能......\n""")
    test(1000)
    test(10000)
    test(100000)
    print("***************************************************************************")
