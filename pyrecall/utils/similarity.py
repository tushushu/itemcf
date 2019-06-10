"""
@Author: tushushu
@Date: 2019-06-10 15:50:13
"""


class Similarity:
    """存储一个item的名称以与另外一个item的相似度，维护最相似item的大顶堆时使用。

    Attributes:
        name {str} -- item名称。
        val {float} -- 与另外一个item的相似度。
    """

    def __init__(self, name, sim):
        self.name = name
        self.sim = sim

    def __eq__(self, other):
        return self.sim == other.sim

    def __le__(self, other):
        return self.sim < other.sim

    def __gt__(self, other):
        return self.sim > other.sim

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__, self.name, self.sim)
