# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the rules of the Sūtrapāṭha.

    :license: MIT and BSD
"""

import itertools
import logging
import os
from collections import OrderedDict, defaultdict

import adhyaya1.pada1
import adhyaya1.pada2
import adhyaya1.pada3
import adhyaya2.pada4
import adhyaya3.pada1
import adhyaya3.pada4
import adhyaya6.pada1
import adhyaya6.pada4
import adhyaya7.pada1
import adhyaya7.pada2
import adhyaya7.pada3
import adhyaya7.pada4
import dhatupatha
import sandhi
import siddha
import vibhakti
import filters as F
import templates as T

from templates import ALL_RULES
from util import State

log = logging.getLogger(__name__)


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
        depth = len(used_features)
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
            if j >= 0 and filt(state, j):
                selection.update(tree.select(state, index))

        return selection


class Ashtadhyayi(object):

    """The Ashtadhyayi."""

    def __init__(self):
        dirname = os.path.dirname(os.path.dirname(__file__))
        dhatu_file = os.path.join(dirname, 'data', 'dhatupatha.csv')
        dhatupatha.DHATUPATHA.init(dhatu_file)

        #: The rules of the grammar, from highest priority to lowest.
        self.sorted_rules = sorted(ALL_RULES, cmp = lambda x, y: cmp(y.rank, x.rank))
        #: Maps a rule's name to a :class:`Rule` instance.
        self.rule_map = {x.name: x for x in ALL_RULES}

        self.rule_tree = RuleTree(self.sorted_rules)

        self.utsarga = {}
        for rule in ALL_RULES:
            self.utsarga[rule] = []
            for other in ALL_RULES:
                if rule.has_utsarga(other):
                    self.utsarga[rule].append(other)

        for rule in ALL_RULES:
            rule.utsarga = self.utsarga[rule]

    def matching_rules(self, state):
        state_indices = range(len(state))
        candidates = [self.rule_tree.select(state, i) for i in state_indices]

        for i, ra in enumerate(self.sorted_rules):
            for ia in state_indices:
                if ra in candidates[ia]:
                    yield ra, ia

    def apply_next_rule(self, state):
        """Apply one rule and return a list of new states.

        This function applies conflict resolution to a list of candidate
        rules until one rule remains.

        :param state: the current :class:`State`
        """

        sorted_rules = self.sorted_rules
        for ra, ia in self.matching_rules(state):
            # Ignore redundant applications
            if ra in state[ia].ops:
                continue

            # Only worthwhile rules
            ra_states = list(ra.apply(state, ia))
            if not ra_states:
                continue

            # Verify this isn't dominated by any other rules
            # TODO

            for s in ra_states:
                log.debug('  %s : %s --> %s' % (ra.name, state, s))
            return ra_states

    def derive(self, sequence):
        """Yield all possible results.

        :param sequence: a starting sequence
        """
        start = State(sequence)
        stack = [start]

        log.debug('---')
        log.debug('start: %s' % start)
        while stack:
            state = stack.pop()
            new_states = self.apply_next_rule(state)
            if new_states:
                stack.extend(new_states)

            # No applicable rules; state is in its final form.
            else:
                log.debug('yield: %s' % state)
                for x in self.sandhi_asiddha(state):
                    yield x

    def sandhi_asiddha(self, state):
        for s in sandhi.apply(state):
            for t in siddha.asiddha(s):
                yield ''.join(x.asiddha for x in t)
