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


def do_utsarga_apavada(rules):
    """Annotate rules with their utsargas and apavādas.

    :param rules: a list of rules
    """
    # Rules are sorted from earliest appearance to latest.
    rules = sorted(rules, key=lambda rule: rule.name)
    utsargas = defaultdict(list)
    apavadas = defaultdict(list)

    for i, rule in enumerate(rules):

        # 'na' negates an operator, so we can just match on operators.
        if rule.modifier == Na:
            for other in rules:
                if (rule.operator == other.operator
                    and rule != other):
                    utsargas[rule].append(other)
                    apavadas[other].append(rule)

        else:
            # śeṣa covers all of the contexts not already mentioned.
            # That is, a śeṣa rule is an utsarga to all conflicting
            # rules that come before it.
            if rule.modifier == Shesha:
                rule_slice = itertools.islice(rules, 0, i)

            # Generally, an apavāda follows an utsarga.
            else:
                rule_slice = itertools.islice(rules, i, None)

            for other in rule_slice:
                if rule.has_apavada(other):
                    apavadas[rule].append(other)
                    utsargas[other].append(rule)

    for rule in rules:
        rule.utsarga = utsargas[rule]
        rule.apavada = apavadas[rule]


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

    def __init__(self, rules, used_features=None):
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
            self.features[feat] = RuleTree(unseen, used_features | set([feat]))
            seen.update(rule_list)

    def __len__(self):
        """The number of rules in the tree."""
        self_len = len(self.rules)
        return self_len + sum(len(v) for k, v in self.features.iteritems())

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
