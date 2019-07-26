"""
@Author: tushushu
@Date: 2019-07-03 15:38:16
"""

from test_sorted_set import test_sorted_set
from test_sim_metrics import test_sim_metrics
from test_sparse_matrix_binary import test_sparse_matrix_binary
from test_min_heap import test_min_heap
from test_knn_search import test_knn_search, test_knn_search_cache
from test_item_cf import test_agg_score, test_top_k_map
from test_recommend import test_recommend_accuracy, test_recommend_checklist


if __name__ == "__main__":
    # 测试C++的set是否会把元素按照升序排列。
    test_sorted_set(1000)
    # 测试Jaccard相似度计算函数是否正确。
    test_sim_metrics(10000)
    # 测试SparseMetrixBinary类的方法是否正确。
    test_sparse_matrix_binary(100)
    # 测试小顶堆的heappush函数是否正确。
    test_min_heap(100)
    # 测试agg_score函数是否正确。
    test_agg_score(1000)
    # 测试top_k_map函数是否正确。
    test_top_k_map(1000)
    # 测试SparseMatrixBinary类的knn_search方法是否正确。
    test_knn_search(3000)
    # test_knn_search函数的基础上加入缓存，且增加高频物品的测试次数。
    test_knn_search_cache(1000)
    # 测试SparseMatrixBinary类的recommend方法推出内容是否与手动计算结果一致。
    test_recommend_accuracy(100)
    # 测试SparseMatrixBinary类的recommend方法中合法非法清单是否生效。
    test_recommend_checklist()
