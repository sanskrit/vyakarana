# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the rules of the Sūtrapāṭha.

    :license: MIT and BSD
"""

import importlib
import logging
import os
from collections import defaultdict

import inference
import sandhi
import siddha

from templates import Anuvrtti, RuleTuple
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

    """The Ashtadhyayi.

    This class models the most abstract parts of the system, namely:

    - defining rules
    - applying the next appropriate rule to some state
    - deriving results from some initial state

    Most of the interesting stuff is abstracted away into other modules.
    """

    def __init__(self, rules=None):
        #: A list of rules sorted from first (1.1.1) to last (8.4.68).
        self.rules = inference.create_rules(rules or self.fetch_all_rules())

        #: A list of rules sorted from highest priority to lowest.
        self.ranked_rules = sorted(self.rules,
                                   cmp = lambda x, y: cmp(y.rank, x.rank))

        #: Indexed arrangement of rules
        self.rule_tree = RuleTree(self.rules)

    @staticmethod
    def fetch_all_rules():
        """Create a list of all rule tuples defined in the system.

        We find rule tuples by programmatically importing every pada in
        the Ashtadhyayi. Undefined padas are skipped.
        """

        # All padas follow this naming convention.
        mod_string = 'vyakarana.adhyaya{0}.pada{1}'
        combos = [(a, p) for a in '12345678' for p in '1234']
        rule_tuples = []

        for adhyaya, pada in combos:
            try:
                mod_name = mod_string.format(adhyaya, pada)
                mod = importlib.import_module(mod_name)
                rule_tuples.extend(mod.RULES)
            except ImportError as e:
                print e
                pass

        # Convert tuples to RuleTuples
        for i, r in enumerate(rule_tuples):
            if isinstance(r, tuple):
                rule_tuples[i] = RuleTuple(*r)

        return rule_tuples

    @classmethod
    def with_rules_in(cls, start_name, end_name):
        """Constructor using only a subset of the Ashtadhyayi's rules.

        This is provided to make it easier to test certain rule groups.

        :param start_name: name of the first rule to use, e.g. "1.1.1"
        :param end_name: name of the last rule to use, e.g. "1.1.73"
        """
        selection = []
        active = False
        for r in cls.fetch_all_rules():
            if isinstance(r, Anuvrtti):
                selection.append(r)
                continue

            if r.name == start_name:
                active = True

            if active:
                selection.append(r)

            if r.name == end_name:
                active = False

        return cls(selection)

    def matching_rules(self, state):
        """Generate all rules that could apply to the state.

        :param state: the current state
        """
        state_indices = range(len(state))
        candidates = [self.rule_tree.select(state, i) for i in state_indices]

        for i, ra in enumerate(self.ranked_rules):
            for ia in state_indices:
                if ra in candidates[ia]:
                    yield ra, ia

    def apply_next_rule(self, state):
        """Apply one rule and return a list of new states.

        This function applies conflict resolution to a list of candidate
        rules until one rule remains.

        :param state: the current state
        """
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
        """Apply rules from the 'sandhi' and 'asiddha' sections.

        TODO: rewrite the rules in the sandhi and asiddha sections until
        this function is no longer needed.

        :param state: the current state
        """
        for s in sandhi.apply(state):
            for t in siddha.asiddha(s):
                yield ''.join(x.asiddha for x in t)
