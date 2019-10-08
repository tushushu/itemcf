## PyRecall
PyRecall 0.1基于PySpark开发的推荐系统召回算法库，使用Cython编写核心计算模块，注册为Spark UDF供Pyspark调用，比Python UDF快14~18倍。  
系统: Linux-64
兼容: Python 3.6  
依赖: PySpark 2.0及以上   

## 算法
已完成
Item CF -- Jaccard  

未来填坑
Item CF -- Cosine, Item2Vector
User CF -- Jaccard, Cosine
Model CF -- ALS


## 参考文献
《推荐系统实践》
