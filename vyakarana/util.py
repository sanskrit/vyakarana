# -*- coding: utf-8 -*-
"""
    vyakarana.util
    ~~~~~~~~~~~~~~

    Utility functions.

    :license: MIT and BSD
"""

import itertools


def iter_group(items, n):
    """Iterate over `items` by taking `n` items at a time."""
    for i in range(0, len(items), n):
        yield items[i:i+n]


def iter_pairwise(items):
    x, y = itertools.tee(items)
    next(y, None)
    return itertools.izip(x, y)


class Rank(object):

    """
    Among the conflict-solving mechanisms in the Ashtadhyayi is the
    notion of utsarga-apavāda. The idea is that when two rules have
    space to apply, the more general rule (utsarga) is dominated by
    the specific rule (apavāda).

    The "specificity" of a rule can be determined by the conditions
    that allow the rule to act -- for example, some rules apply only
    to certain roots, which makes them very specific -- but to do this
    automatically requires a level of code introspection that would
    greatly complicate the model.

    For that reason, this class provides a simple way to regulate
    utsarga-apavāda relationships in the Ashtadhyayi.

    :param value: an integer value corresponding to the current rank.
                  Higher values dominate lower ones.
    """

    #: Rank of a general rule
    UTSARGA = 1
    #: Rank of a specific rule, as counter to an utsarga
    APAVADA = 2
    #: Rank of a rule that acts on a specific upadesha
    UPADESHA = 4
    #: Rank of a rule that acts on a specific form
    NIPATANA = 5

    def __init__(self, value=0):
        self.value = value

    def __int__(self):
        return self.value

    def __cmp__(self, other):
        """
        :param other: a `Rank` or `int`
        """
        return int(self) - int(other)

    def __repr__(self):
        return '<Rank(%s)>' % self.value

    def allows(self, other):
        """
        Return whether an operation of rank `other` is allowed.

        Rules of lower rank cannot override rules of higher rank.

        :param other: a `Rank` or `int`
        """
        return self.value <= int(other)

    def set(self, other):
        """
        Set the value of the current rank.

        :param other: a `Rank` or `int`
        """
        self.value = int(other)
