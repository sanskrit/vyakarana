# -*- coding: utf-8 -*-
"""
    vyakarana.reranking
    ~~~~~~~~~~~~~~~~~~~

    Defines various **rankers**, each of which can be used as a key
    function while sorting a list of rules. Something is a ranker if
    and only if it has these three properties:

    1. It is a callable.
    2. It returns a value that can be compared.
    3. It returns a higher value for rules that should have a higher
       rank.

    Rules are sorted with `reverse=True`, so higher values appear
    earlier in the list.

    :license: MIT and BSD
"""

import filters as F
from rules import Rule

#: Artificially boosted rules.
BOOST = ['6.1.45', '6.1.64', '6.1.65']


class NameRanker(object):

    """Ranker for specific rule names."""

    def __init__(self, *args):
        self.names = args

    def __call__(self, rule):
        if rule.name in self.names:
            return 1
        return 0


class FilterRanker(object):

    """Ranker for a specific filter type.

    If the filter domain is small, the score is large.
    """

    def __init__(self, superclass):
        self.superclass = superclass

    def __call__(self, rule):
        score = 0
        for filt in rule.filters:
            for s in filt.supersets:
                if s.domain and isinstance(s, self.superclass):
                    # Smaller domain -> higher score.
                    score += 1.0 / len(s.domain)
        return score


class CompositeRanker(object):

    """Combines multiple rankers."""

    def __init__(self, rankers=None):
        self.rankers = rankers
        if rankers is None:
            self.rankers = [
                # Artificially boosted rules
                NameRanker(*BOOST),
                by_category,
                by_locus,
                FilterRanker(F.UpadeshaFilter),
                FilterRanker(F.SamjnaFilter),
                FilterRanker(F.AlFilter),
            ]

    def __call__(self, rule):
        return tuple(r(rule) for r in self.rankers)


def by_category(rule):
    """Ranker for a rule's category.

    :param rule: the rule to score
    """
    if rule.category in (Rule.SAMJNA, Rule.ATIDESHA, Rule.PARIBHASHA):
        return 1
    return 0


def by_locus(rule):
    """Ranker for a rule's locus.

    :param rule: the rule to score
    """
    if rule.locus == Rule.SIDDHA:
        return 1
    return 0
