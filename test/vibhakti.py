# -*- coding: utf-8 -*-
"""
    test.vibhakti
    ~~~~~~~~~~~~~

    Tests for vibhakti.py

    :license: MIT and BSD
"""

from vyakarana import vibhakti
from vyakarana.upadesha import *


a_labels = 'a1'.split()
b_labels = 'b1 b2'.split()
c_labels = 'c1 c2 c3'.split()
d_labels = 'd1 d2 d3 d4 d5 d6'.split()


def make_terms(n):
    """Generate a list of `n` terms."""
    return [Term('a' + str(i)) for i in range(n)]


def verify(terms, all_exp):
    for term, exp in zip(terms, all_exp):
        for e in exp:
            assert e in term.samjna


def test_label_by_triplet():
    terms = make_terms(6)
    for labels in [a_labels, b_labels, c_labels, d_labels]:
        vibhakti.label_by_triplet(terms, labels)

    a_exp = 'a1 a1 a1 a1 a1 a1'.split()
    b_exp = 'b1 b1 b1 b2 b2 b2'.split()
    c_exp = 'c1 c1 c1 c2 c2 c2'.split()
    d_exp = 'd1 d1 d1 d2 d2 d2'.split()
    verify(terms, zip(a_exp, b_exp, c_exp, d_exp))


def test_label_by_item():
    terms = make_terms(6)
    for labels in [a_labels, b_labels, c_labels, d_labels]:
        vibhakti.label_by_item(terms, labels)

    a_exp = 'a1 a1 a1 a1 a1 a1'.split()
    b_exp = 'b1 b2 b1 b2 b1 b2'.split()
    c_exp = 'c1 c2 c3 c1 c2 c3'.split()
    d_exp = 'd1 d2 d3 d4 d5 d6'.split()
    verify(terms, zip(a_exp, b_exp, c_exp, d_exp))


def test_label_by_group():
    terms = make_terms(6)
    for labels in [a_labels, b_labels, c_labels, d_labels]:
        vibhakti.label_by_group(terms, labels)

    a_exp = 'a1 a1 a1 a1 a1 a1'.split()
    b_exp = 'b1 b1 b1 b2 b2 b2'.split()
    c_exp = 'c1 c1 c2 c2 c3 c3'.split()
    d_exp = 'd1 d2 d3 d4 d5 d6'.split()
    verify(terms, zip(a_exp, b_exp, c_exp, d_exp))


def test_la_to_tin():
    pass