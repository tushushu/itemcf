# -*- coding: utf-8 -*-
"""
@Author: tushushu
@Date: 2019-06-06 12:21:13
"""
from typing import List, Any, Dict, Set
from ..utils.load_data import SparseMap


class JaccardItemCF:
    """[summary]

    Returns:
        [type] -- [description]
    """

    def __init__(self):
        self.similarity_matrix = dict()

    def fit(self, data: SparseMap, max_items=10, scaled=False):
        """[summary]

        Arguments:
            data {SparseMap} -- [description]

        Keyword Arguments:
            max_items {int} -- [description] (default: {10})
            scaled {bool} -- [description] (default: {False})
        """

        raise NotImplementedError

    def predict_one(self, items: Set[int], max_items: int)->List[Any]:
        """[summary]

        Arguments:
            items {Set[int]} -- [description]
            max_items {int} -- [description]

        Returns:
            List[Any] -- [description]
        """

        raise NotImplementedError

    def predict(self, data: SparseMap, max_items=10)->Dict[int, List[Any]]:
        """[summary]

        Arguments:
            data {SparseMap} -- [description]

        Keyword Arguments:
            max_items {int} -- [description] (default: {10})

        Returns:
            Dict[int, List[Any]] -- [description]
        """

        return {uid: self.predict_one(items, max_items)
                for uid, items in data.items()}
