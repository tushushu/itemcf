"""
@Author: tushushu
@Date: 2019-06-17 16:53:07
"""
from pyspark.sql import DataFrame, SparkSession
from .func_timer import func_timer
from .gen_data import gen_data


@func_timer
def collect_dict_1(data: DataFrame) -> dict:
    """将包含两列的DataFrame转为字典，其中第一列作为Key，第二列作为Value。

    Arguments:
        data {DataFrame}

    Returns:
        dict
    """
    return dict(data.collect())


@func_timer
def collect_dict_2(data: DataFrame) -> dict:
    """将包含两列的DataFrame转为字典，其中第一列作为Key，第二列作为Value。

    Arguments:
        data {DataFrame}

    Returns:
        dict
    """
    return data.rdd.collectAsMap()


def test():
    """对比collect_dict_1函数和collect_dict_2函数的性能。
    """
    spark = SparkSession.builder.appName("gen_data_test").getOrCreate()
    data = gen_data(spark, n_row=1000000).repartition(100).cache()
    print("共%d条数据，%d个分区!")
    data.show()
    collect_dict_1(data)
    collect_dict_2(data)
