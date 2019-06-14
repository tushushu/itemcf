"""
@Author: tushushu
@Date: 2019-06-14 15:14:55
"""
from typing import Set


def jaccard_sim(vector_1: Set[int], vector_2: Set[int]) -> float:
    """计算Jaccard相似度公式。
    Similarity = (A ∩ B) / (A ∪ B)

    Arguments:
        vector_1 {Set[int]} -- 评分过该物品1的用户id。
        vector_2 {Set[int]} -- 评分过该物品2的用户id。

    Returns:
        float -- 相似度。
    """

    numerator = len(vector_1 & vector_2)
    if numerator == 0:
        return 0.0
    denominator = len(vector_1 | vector_2)
    return numerator / denominator
