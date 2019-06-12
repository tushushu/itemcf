"""
@Author: tushushu
@Date: 2019-06-10 15:50:13
"""


class Element:
    """存储一个element的名称以与另外一个element的相似度，维护最相似element的大顶堆时使用。

    Attributes:
        name {str} -- element名称。
        sim {float} -- 与另外一个element的相似度。
    """

    def __init__(self, name, sim=None):
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
