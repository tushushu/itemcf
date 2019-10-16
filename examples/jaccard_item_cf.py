"""
@Author: tushushu
@Date: 2019-07-26 17:39:47
vi /usr/lib/anaconda3/lib/python3.6/site-packages/sitecustomize.py 
import site
site.addsitedir("pyrecall文件夹的上级目录")
"""
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

import sys
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))
print(os.path.abspath("../.."))

from typing import Optional
from pyrecall.item_cf.jaccard import JaccardItemCF
from pyrecall.preprocessing.load_data import MovieRatingsData


def main(threshold: Optional[int], show_coverage: bool):
    """[summary]

    Arguments:
        threshold {Optional[int]} -- [description]
        show_coverage {bool} -- [description]
    """
    print("开始执行!")
    # 读取数据
    movie_ratings = MovieRatingsData()
    user_col = movie_ratings.user_col
    item_col = movie_ratings.item_col
    data = movie_ratings.data

    # 训练模型
    mat_size = 100  # 用户可自定义该参数
    model = JaccardItemCF()
    model.fit(data, user_col, item_col, mat_size, threshold, show_coverage)
    # 生成推荐
    n_recommend = 200  # 用户可自定义该参数
    recommendation = model.predict(data, user_col, item_col, n_recommend)
    recommendation.show()

if __name__ == "__main__":
    main(None, False)
