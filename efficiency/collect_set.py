"""
@Author: tushushu
@Date: 2019-06-18 11:52:24
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))


from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, collect_list, collect_set  # pylint: disable=no-name-in-module
from func_timer import func_timer
from gen_data import gen_data


@func_timer(100)
def collect_set_1(data: DataFrame) -> int:
    """通过Spark自带的collect_set函数实现。

    Arguments:
        data {DataFrame}

    Returns:
        int
    """
    ret = data.groupBy(col("_1"))\
        .agg(collect_set(col("_2")))\
        .count()

    return ret


@func_timer(100)
def collect_set_2(data: DataFrame) -> int:
    """通过Spark自带的distinct方法配合collect_list函数实现。

    Arguments:
        data {DataFrame}

    Returns:
        int
    """
    ret = data.distinct()\
        .groupBy(col("_1"))\
        .agg(collect_list(col("_2")))\
        .count()

    return ret


def test(n_rows: int, n_partitions: int):
    """对比collect_set_1函数和collect_set_2函数的性能。
    结论：函数collect_dict_1更快。
    ***************************************************************************
    运行时间
    ---------------------------------------------------------------------------
    100,000条数据，10个分区
    函数collect_dict_1运行--100次!
    平均值为--0.017 s!
    中位数为--0.016 s!
    最小值为--0.011 s!
    最大值为--0.038 s!

    函数collect_dict_2运行--100次!
    平均值为--0.034 s!
    中位数为--0.032 s!
    最小值为--0.027 s!
    最大值为--0.068 s!
    ---------------------------------------------------------------------------
    1,000,000条数据， 100个分区
    函数collect_dict_1运行--100次!
    平均值为--0.021 s!
    中位数为--0.021 s!
    最小值为--0.018 s!
    最大值为--0.029 s!

    函数collect_dict_2运行--100次!
    平均值为--0.069 s!
    中位数为--0.068 s!
    最小值为--0.062 s!
    最大值为--0.093 s!
    ---------------------------------------------------------------------------
    ***************************************************************************

    Arguments:
        n_rows {int} -- 随机生成的数据行数。
        n_partitions {int} -- 随机生成的数据分区数。
    """
    print("对比collect_dict_1函数和collect_dict_2函数的性能...")
    print("共%d条数据，%d个分区!" % (n_rows, n_partitions))
    spark = SparkSession.builder.appName("gen_data_test").getOrCreate()

    # 产生重复数据
    n_duplicated = 10
    data = gen_data(spark, n_rows // n_duplicated)
    for _ in range(n_duplicated):
        data.union(data)

    data = data.repartition(n_partitions).cache()
    data.show()
    collect_set_1(data)
    collect_set_2(data)


if __name__ == "__main__":
    test(100000, 10)
    test(1000000, 100)
