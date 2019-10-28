"""
@Author: tushushu
@Date: 2019-07-26 17:39:47
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))

from typing import Optional
import pandas as pd
from pyrecall.item_cf.jaccard import JaccardItemCF
from pyrecall.preprocessing.load_data import MovieRatingsData
from pyrecall.utils.utils import run_time


def run(threshold: Optional[int], show_coverage: bool):
    """读取电影评分数据，并推荐用户喜欢的电影。

    Arguments:
        threshold {Optional[int]} -- 物品最低出现的频次。
        show_coverage {bool} -- 是否打印热门物品的覆盖度。
    """
    # 读取数据
    movie_ratings = MovieRatingsData()
    user_col = movie_ratings.user_col
    item_col = movie_ratings.item_col
    data = movie_ratings.data
    # 训练模型
    mat_size = 20  # 用户可自定义该参数
    model = JaccardItemCF()
    model.fit(data, user_col, item_col, mat_size, threshold, show_coverage)
    # 生成推荐
    n_recommend = 20  # 用户可自定义该参数
    recommendation = model.predict(data, user_col, item_col, n_recommend)
    return recommendation


@run_time
def main():
    """展示推荐的性能和结果。"""
    print("开始执行!\n")
    threshold = None
    show_coverage = False
    recommendation = run(threshold, show_coverage)
    print("推荐结果展示(用户id, [(电影id, 推荐分数)]):")
    pd.set_option('display.max_colwidth', 80)
    samples = recommendation.iloc[:3, :].copy()
    samples.recommendations = samples.recommendations\
        .apply(lambda x: [(y[0], round(y[1], 3))for y in x])
    print(samples.head())
    print()

if __name__ == "__main__":
    main()
