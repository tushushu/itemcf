"""
@Author: tushushu
@Date: 2019-06-17 16:54:54
"""
from random import randint
from pyspark.sql import DataFrame, SparkSession


def gen_data(spark: SparkSession, n_rows=100000) -> DataFrame:
    """随机生成一个DataFrame，列名称{"_1":int, "_2": int}

    Arguments:
        spark {SparkSession}

    Keyword Arguments:
        n_rows {int} -- 行数 (default: {100000})

    Returns:
        DataFrame
    """

    ite = ((randint(1, n_rows), i) for i in range(n_rows))
    data = spark.createDataFrame(ite)
    return data


def test():
    """测试gen_data函数是否能够正常执行。
    """
    spark = SparkSession.builder.appName("gen_data_test").getOrCreate()
    data = gen_data(spark, n_rows=10)
    data.show()


if __name__ == "__main__":
    test()
