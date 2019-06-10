"""
@Author: tushushu
@Date: 2019-06-10 15:29:16
"""
from heapq import heappush
from heapq import _heapreplace_max as heapreplace  # type: ignore
from heapq import _heappop_max as heappop  # type: ignore
from typing import List, Any


class MaxHeap:
    """大顶堆。

    Attributes:
        max_size {int} -- 堆的最大元素数量。
        size {int} -- 堆的当前元素数量。
        heap {List[Any]} -- 存储堆的元素。
    """

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.size = 0
        self.heap = []  # type: List[Any]

    def __getitem__(self, i):
        return self.heap[i]

    def __len__(self):
        return len(self.heap)

    @property
    def full(self) -> bool:
        """判断堆是否已经满了。

        Returns:
            bool
        """

        return self.size == self.max_size

    def heappush(self, item: Any):
        """将item加入 heap 中，保持堆的不变性。

        Arguments:
            item {Any} -- 可进行大小比较的对象。
        """

        if self.full:
            heapreplace(self.heap, item)
        else:
            heappush(self.heap, item)
            self.size += 1

    def heappop(self)->Any:
        """弹出并返回heap的最大的元素，保持堆的不变性。

        Returns:
            Any
        """

        assert self.size > 0, "Cannot pop item! The MaxHeap is empty!"
        return heappop(self.heap)
