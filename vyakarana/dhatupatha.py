# -*- coding: utf-8 -*-
"""
    vyakarana.dhatupatha
    ~~~~~~~~~~~~~~~~~~~~

    Coordinates access to the Dhatupatha.

    :license: MIT and BSD
"""

from collections import defaultdict


class Dhatupatha(object):

    def __init__(self, filename=None):
        self.gana_map = defaultdict(set)
        self.all_dhatu = []
        self.index_map = {}


        if filename is not None:
            self.init(filename)

    def init(self, filename):
        """
        :param filename: path to the Dhatupatha file
        """
        with open(filename) as f:
            i = 0
            for line in f:
                gana, number, dhatu = line.strip().split(',')
                self.gana_map[dhatu].add(gana)
                self.all_dhatu.append(dhatu)
                self.index_map[dhatu] = i
                i += 1

    def gana_set(self, dhatu):
        return self.gana_map[dhatu.raw]

    def dhatu_range(self, start, end):
        start_index = self.index_map[start]
        end_index = self.index_map[end]
        return self.all_dhatu[start_index:end_index]

    def dhatu_set(self, start, end):
        return frozenset(self.dhatu_range(start, end))


DHATUPATHA = Dhatupatha()
DHATUPATHA.init('data/dhatupatha.csv')
