"""
@Author: tushushu
@Date: 2019-07-26 17:39:47
"""

from typing import Optional
from pyspark.sql import DataFrame
from pyrecall.item_cf.jaccard import JaccardItemCF  # 需要将pyrecall文件夹拷贝到Python三方库的路径下。


def load_data() -> DataFrame:
    """用户需要自定义一个读取数据的函数，得到一个Spark DataFrame。

    Returns:
        DataFrame -- ["uid", "item_id"]
    """
    pass

def main(threshold: Optional[int], show_coverage: bool):
    print("开始执行!")
    # 读取数据
    user_col = "uid"  # 用户可自定义该参数
    item_col = "item_id"  # 用户可自定义该参数
    data = load_data()
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
