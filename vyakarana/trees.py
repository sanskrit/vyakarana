# -*- coding: utf-8 -*-
"""
    vyakarana.trees
    ~~~~~~~~~~~~~~~

    Functions for reading and interpreting the rules of the Ashtadhayayi.

    :license: MIT and BSD
"""

import itertools
from collections import defaultdict

from templates import *


def find_apavada_rules(rules):
    """Find all utsarga-apavāda relationships in the given rules.

    :param rules: a list of rules
    :returns: a `dict` that maps a rule to its apavāda rules.
    """
    apavadas = defaultdict(set)
    for i, rule in enumerate(rules):
        # 'na' negates an operator, so we can just match on operators.
        if rule.modifier == Na:
            for other in rules:
                if (rule.operator == other.operator and rule != other):
                    apavadas[other].add(rule)
        else:
            # For a śeṣa rule, an apavāda comes before the rule:
            if rule.modifier == Shesha:
                rule_slice = itertools.islice(rules, 0, i)
            # But generally, an apavāda comes after the rule:
            else:
                rule_slice = itertools.islice(rules, i, None)

            new_apavadas = (r for r in rule_slice if rule.has_apavada(r))
            apavadas[rule].update(new_apavadas)

    return apavadas


class RuleTree(object):

    """A hierarchical arrangment of rules.

    There are roughly 4000 rules in the Ashtadhyayi, almost all of which
    define operations on some input sequence. Since any of these rules
    could apply at any given moment, we must check all R rules against
    each state. And since a rule could apply to any of the T terms within
    a state, we must check against all terms as well. This leaves us with
    RT candidates for each state.

    By arranging rules hierarchically, we greatly reduce the number of
    comparisons we have to make. Rule selection becomes roughly log(RT).
    """

    def __init__(self, rules, ranker=None, used_features=None):
        # HACK
        if ranker is not None:
            self.ranked_rules = sorted(rules, key=ranker, reverse=True)
            apavadas = find_apavada_rules(rules)
            for rule, values in apavadas.iteritems():
                rule.apavada = values
                for a in values:
                    a.utsarga.append(rule)

        #: A list of rules that could not be subdivided any further.
        #: This is usually because the rule is unspecified in some way.
        self.rules = []
        #: Maps from features to :class:`RuleTree` subtrees.
        self.features = {}
        used_features = used_features or frozenset()

        # Maps a feature tuple to a list of rules
        feature_map = defaultdict(list)
        for rule in rules:
            appended = False
            for feat in rule.features():
                if feat not in used_features:
                    feature_map[feat].append(rule)
                    appended = True

            # No special features: just append to our rule list.
            if not appended:
                self.rules.append(rule)

        # Sort from most general to most specific.
        buckets = sorted(feature_map.iteritems(), key=lambda p: -len(p[1]))

        seen = set()
        for feat, rule_list in buckets:
            unseen = [r for r in rule_list if r not in seen]
            if not unseen:
                continue
            subtree = RuleTree(rules=unseen,
                               used_features=used_features | set([feat]))
            self.features[feat] = subtree
            seen.update(rule_list)

    def __len__(self):
        """The number of rules in the tree."""
        self_len = len(self.rules)
        return self_len + sum(len(v) for k, v in self.features.iteritems())

    def candidates(self, state):
        """Generate all rule-index pairs that could apply to the state.

        :param state: the current state
        """
        state_indices = range(len(state))
        candidates = [self.select(state, i) for i in state_indices]

        for i, ra in enumerate(self.ranked_rules):
            for ia in state_indices:
                if ra in candidates[ia]:
                    yield ra, ia

    def pprint(self, depth=0):
        """Pretty-print the tree."""
        if self.rules:
            rule_token = [x.name for x in self.rules]
            print '    ' * depth, '[%s] %s' % (len(self.rules), rule_token)
        for feature, tree in self.features.iteritems():
            print '    ' * depth, '[%s]' % len(tree), feature
            tree.pprint(depth + 1)

    def select(self, state, index):
        """Return a set of rules that might be applicable.

        :param state: the current :class:`State`
        :param index: the current index
        """
        selection = set(self.rules)

        for feature, tree in self.features.iteritems():
            filt, i = feature
            j = index + i
            if j >= 0 and filt.allows(state, j):
                selection.update(tree.select(state, index))

        return selection
