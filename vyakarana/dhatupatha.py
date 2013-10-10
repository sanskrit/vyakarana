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
        self.all_gana = defaultdict(set)

        if filename is not None:
            self.init(filename)

    def init(self, filename):
        """
        :param filename: path to the Dhatupatha file
        """
        with open(filename) as f:
            for line in f:
                gana, number, dhatu = line.strip().split(',')
                self.all_gana[dhatu].add(gana)

    def gana(self, dhatu):
        return self.all_gana[dhatu.raw]


DHATUPATHA = Dhatupatha()
DHATUPATHA.init('data/dhatupatha.csv')
