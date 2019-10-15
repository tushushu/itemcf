提到Item CF(基于物品的协同过滤)相信大家应该都不会觉得陌生(不陌生你点进来干嘛[捂脸])，本文就Item CF的基本原理进行讲解，并分享一下个人实现的高性能、分布式的Item CF轮子。

主要代码代码请参考本人的p...哦不是...github：
[jaccard.py](hhttps://github.com/tushushu/pyrecall/blob/master/pyrecall/item_cf/jaccard.py)
[sparse_matrix.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/sparse_matrix.pyx)
[heap.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/heap.pyx)
[sim_metrics.pyx](https://github.com/tushushu/pyrecall/blob/master/pyrecall/utils/sim_metrics.pyx)


我们讲讲基于物品的协同过滤是怎么一回事。

### 1 温故知新
大顶堆/小顶堆做Top K查找是协同过滤的基础，之前的一篇文章曾经讲过大顶堆的原理和实现。链接如下：
[max_heap.md](https://github.com/tushushu/imylu/blob/master/docs_cn/max_heap.md)

### 2 用户对物品的评分
物化男性

### 3 物品向量
物化男性

### 4 Jaccard相似度
写个公式

### 5 物品相似度矩阵
TOP K查找

### 6 生成推荐

### 7 分布式计算

### 8 性能分析

提到Item CF(基于物品的协同过滤)相信大家应该都不会觉得陌生(不陌生你点进来干嘛[捂脸])，本文就Item CF的基本原理进行讲解，并分享一下个人实现的高性能、分布式的Item CF轮子。

完整代码请参考本人的p...哦不是...github：
[pyrecall](https://github.com/tushushu/pyrecall)

我们讲讲基于物品的协同过滤是怎么一回事。

### 1 温故知新
用大顶堆/小顶堆来执行Top K查找是协同过滤的基础，之前的一篇文章曾经讲过大顶堆的原理和实现。链接如下：
[max_heap.md](https://github.com/tushushu/imylu/blob/master/docs_cn/max_heap.md)

### 2 物品向量
假设豆瓣只有3个用户和5部电影。用户1看过电影A\B，用户2看过电影A\B\E，用户3看过电影C\D\E。电影A被用户1和用户2看过，所以可以用向量[1, 2]来表示。同理，电影E被用户2和用户3看过，可以用向量[2, 3]表示。

### 3 物品相似度
如果想要计算电影之间的相似度，该如何计算呢？最简单的公式就是计算Jaccard相似度。公式如下：  
Similarity = Length(A∩B) / Length(A∪B)  
以电影A[1, 2]和电影E[2, 3]为例，两者的交集是[2]，集合长度为1，并集是[1, 2, 3]，集合长度为3，所以相似度为1/3。  
使用Python实现Jaccard相似度计算代码如下：
```python
def jaccard_sim(set1: Set[int], set2: Set[int]) -> float:
    """计算Jaccard相似度函数。"""
    denominator = len(set1 | set2)
    if denominator == 0:
        return 0.0
    numerator = len(set1 & set2)
    return numerator / denominator
```

使用Cython实现Jaccard相似度计算代码如下，性能大约是Python版本的7~14倍。
```python
cdef float jaccard_sim(vector[int]& v1, vector[int]& v2) except +:
    """计算集合A与B的Jaccard相似度，Similarity = A ∩ B / A ∪ B。"""
    cdef:
        int numerator = 0
        int denominator = 0
        int m = v1.size()
        int n = v2.size()
        int i = 0
        int j = 0
    if m == 0 or n == 0:
        return 0.0
    if v1[m - 1] < v2[0]:
        return 0.0
    if v2[n - 1] < v1[0]:
        return 0.0
    while i < m and j < n:
        if v1[i] == v2[j]:
            i += 1
            j += 1
            numerator += 1
        elif v1[i] > v2[j]:
            j += 1
        else:
            i += 1
    if numerator == 0:
        return 0.0
    denominator = m + n - numerator
    return numerator * 1.0 / denominator
```

### 4 物品相似度矩阵
有了物品向量和物品相似度计算公式之后，我们就可以两两计算物品的相似度，形成物品相似度矩阵。  
物品向量  
A → {1, 2}   
B → {1, 2}   
C → {3}   
D → {3}   
E → {2, 3}   

物品相似度  
A - A → 1.0   
A - B → 1.0   
A - C → 0.0   
A - D → 0.0   
A - E → 0.3   
B - A → 1.0   
B - B → 1.0   
B - C → 0.0   
B - D → 0.0   
B - E → 0.3   
C - A → 0.0   
C - B → 0.0   
C - C → 1.0   
C - D → 1.0   
C - E → 0.5   
D - A → 0.0   
D - B → 0.0   
D - C → 1.0   
D - D → 1.0   
D - E → 0.5   
E - A → 0.3   
E - B → 0.3   
E - C → 0.5   
E - D → 0.5   
E - E → 1.0   


### 5 生成推荐
用户1看过电影A/B，假如我们需要给用户A推荐k个电影(假设k=2)。

### 6 分布式计算

### 7 性能分析
