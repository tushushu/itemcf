提到Item CF(基于物品的协同过滤)相信大家应该都不会觉得陌生(不陌生你点进来干嘛[捂脸])，本文就Item CF的基本原理进行讲解，并分享一下个人实现的高性能、分布式的Item CF轮子。

主要代码代码请参考本人的p...哦不是...github：
[jaccard.py](hhttps://github.com/tushushu/pyrecall/blob/master/pyrecall/item_cf/jaccard.py)
[sparse_matrix.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/sparse_matrix.pyx)
[heap.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/heap.pyx)
[sim_metrics.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/sim_metrics.pyx)


我们讲讲基于物品的协同过滤是怎么一回事。

## 1 温故知新
大顶堆/小顶堆做Top K查找是协同过滤的基础，之前的一篇文章曾经讲过大顶堆的原理和实现。链接如下：
[max_heap.md](https://github.com/tushushu/imylu/blob/master/docs_cn/max_heap.md)

## 2 用户对物品的评分
物化男性

## 3 物品向量
物化男性

## 4 Jaccard相似度
写个公式

## 5 物品相似度矩阵
TOP K查找

## 6 生成推荐

## 7 分布式计算

## 8 性能分析

