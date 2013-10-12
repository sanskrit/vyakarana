# -*- coding: utf-8 -*-
"""
    test.util
    ~~~~~~~~~

    Tests for the utility functions.

    :license: MIT and BSD
"""

from vyakarana.util import *


def test_iter_group():
    items = range(18)
    groups = [range(6), range(6, 12), range(12, 18)]
    assert list(iter_group(items, 6)) == groups


def test_iter_pairwise():
    items = 'abcdefg'

    actual_list = list(iter_pairwise(items))
    expected_list = [tuple(x) for x in 'ab bc cd de ef fg'.split()]
    assert actual_list == expected_list


def test_rank():
    r1 = Rank.UNKNOWN
    r2 = Rank.UTSARGA
    r3 = Rank.APAVADA
    r4 = Rank.UPADESHA
    r5 = Rank.NIPATANA

    assert r1 < r2 < r3 < r4 < r5
