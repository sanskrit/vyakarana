# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the rules of the Sūtrapāṭha.

    :license: MIT and BSD
"""

import expand
import reranking
import sandhi
import siddha
import trees

from . import logger
from derivations import State
from templates import Anuvrtti


class Ashtadhyayi(object):

    """The Ashtadhyayi.

    This class models the most abstract parts of the system, namely:

    - defining rules
    - applying the next appropriate rule to some state
    - deriving results from some initial state

    Most of the interesting stuff is abstracted away into other modules.
    """

    def __init__(self, rules=None):
        ranker = reranking.CompositeRanker()

        #: A list of rules sorted from first (1.1.1) to last (8.4.68).
        self.rules = expand.build_from_stubs(rules)

        trees.do_utsarga_apavada(self.rules) # HACK

        #: A list of rules sorted from highest priority to lowest.
        self.ranked_rules = sorted(self.rules, key=ranker, reverse=True)

        #: Indexed arrangement of rules
        self.rule_tree = trees.RuleTree(self.rules)

    @classmethod
    def with_rules_in(cls, start_name, end_name, **kw):
        """Constructor using only a subset of the Ashtadhyayi's rules.

        This is provided to make it easier to test certain rule groups.

        :param start_name: name of the first rule to use, e.g. "1.1.1"
        :param end_name: name of the last rule to use, e.g. "1.1.73"
        """
        selection = []
        active = False
        for stub in expand.fetch_all_stubs():
            if isinstance(stub, Anuvrtti):
                selection.append(stub)
                continue

            if stub.name == start_name:
                active = True

            if active:
                selection.append(stub)

            if stub.name == end_name:
                active = False

        return cls(rules=selection, **kw)

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
                logger.debug('  %s : %s --> %s' % (ra.name, state, s))
            return ra_states

    def derive(self, sequence):
        """Yield all possible results.

        :param sequence: a starting sequence
        """
        start = State(sequence)
        stack = [start]

        logger.debug('---')
        logger.debug('start: %s' % start)
        while stack:
            state = stack.pop()
            new_states = self.apply_next_rule(state)
            if new_states:
                stack.extend(new_states)

            # No applicable rules; state is in its final form.
            else:
                logger.debug('yield: %s' % state)
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
