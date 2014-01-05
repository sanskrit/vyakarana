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


class Ashtadhyayi(object):

    """The Ashtadhyayi.

    This class models the most abstract parts of the system, namely:

    - defining rules
    - applying the next appropriate rule to some state
    - deriving results from some initial state

    Most of the interesting stuff is abstracted away into other modules.
    """

    def __init__(self, stubs=None):
        rules = expand.build_from_stubs(stubs)
        ranker = reranking.CompositeRanker()

        #: Indexed arrangement of rules
        self.rule_tree = trees.RuleTree(rules, ranker=ranker)

    @classmethod
    def with_rules_in(cls, start, end, **kw):
        """Constructor using only a subset of the Ashtadhyayi's rules.

        This is provided to make it easier to test certain rule groups.

        :param start: name of the first rule to use, e.g. "1.1.1"
        :param end: name of the last rule to use, e.g. "1.1.73"
        """

        stubs = expand.fetch_stubs_in_range(start, end)
        return cls(stubs=stubs, **kw)

    def apply_next_rule(self, state):
        """Apply one rule and return a list of new states.

        This function applies conflict resolution to a list of candidate
        rules until one rule remains.

        :param state: the current state
        """
        for ra, ia in self.rule_tree.candidates(state):
            # Ignore redundant applications
            if ra in state[ia].ops:
                continue

            # Only worthwhile rules
            ra_states = list(ra.apply(state, ia))
            if not ra_states:
                continue

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
