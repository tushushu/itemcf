"""
@Author: tushushu
@Date: 2019-06-17 16:53:07
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath("."))


from pyspark.sql import DataFrame, SparkSession
from func_timer import func_timer
from gen_data import gen_data


@func_timer(100)
def collect_dict_1(data: DataFrame) -> dict:
    """将包含两列的DataFrame转为字典，其中第一列作为Key，第二列作为Value。

    Arguments:
        data {DataFrame}

    Returns:
        dict
    """
    return dict(data.collect())


@func_timer(100)
def collect_dict_2(data: DataFrame) -> dict:
    """将包含两列的DataFrame转为字典，其中第一列作为Key，第二列作为Value。

    Arguments:
        data {DataFrame}

    Returns:
        dict
    """
    return data.rdd.collectAsMap()


def test(n_rows: int, n_partitions: int):
    """对比collect_dict_1函数和collect_dict_2函数的性能。
    collect_dict_1使用DataFrame的collect方法再转为Dict，
    collect_dict_2使用Rdd的collect方法再转为Dict，
    结论：两者差异不明显
    ***************************************************************************
    运行时间
    ---------------------------------------------------------------------------
    100,000条数据，10个分区
    函数collect_dict_1运行--100次!
    平均值为--0.006 s!
    中位数为--0.006 s!
    最小值为--0.005 s!
    最大值为--0.010 s!

    函数collect_dict_2运行--100次!
    平均值为--0.007 s!
    中位数为--0.007 s!
    最小值为--0.006 s!
    最大值为--0.010 s!
    ---------------------------------------------------------------------------
    1,000,000条数据， 100个分区
    函数collect_dict_1运行--100次!
    平均值为--0.053 s!
    中位数为--0.052 s!
    最小值为--0.047 s!
    最大值为--0.139 s!

    函数collect_dict_2运行--100次!
    平均值为--0.056 s!
    中位数为--0.056 s!
    最小值为--0.051 s!
    最大值为--0.062 s!
    ---------------------------------------------------------------------------
    ***************************************************************************

    ***************************************************************************
    占用内存
    ---------------------------------------------------------------------------
    函数collect_dict_1把DataFrame全部加载到内存中再转换为Dict，
    最大内存消耗 = DataFrame + Dict + 容器引用的对象

    函数collect_dict_2把Rdd reduce为Dict，
    最大内存消耗 = Dict + 容器引用的对象
    ---------------------------------------------------------------------------
    ***************************************************************************

    Arguments:
        n_rows {int} -- 随机生成的数据行数。
        n_partitions {int} -- 随机生成的数据分区数。
    """
    print("对比collect_dict_1函数和collect_dict_2函数的性能...")
    print("共%d条数据，%d个分区!" % (n_rows, n_partitions))
    spark = SparkSession.builder.appName("gen_data_test").getOrCreate()
    data = gen_data(spark, n_rows=n_rows).repartition(n_partitions).cache()
    data.show()
    collect_dict_1(data)
    collect_dict_2(data)


if __name__ == "__main__":
    test(100000, 10)
    test(1000000, 100)
