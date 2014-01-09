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

    """Given some input terms, yields a list of Sanskrit words.

    This is the most abstract part of the system and doesn't expect any
    internal knowledge about how the system works. This is almost always
    the only class that client libraries should use.

    The heart of the class is :meth:`derive`, which accepts a list of
    terms and yields :class:`~vyakarana.derivations.State` objects that
    represent finished words.
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

    def _apply_next_rule(self, state):
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

    def _sandhi_asiddha(self, state):
        """Apply rules from the 'sandhi' and 'asiddha' sections.

        TODO: rewrite the rules in the sandhi and asiddha sections until
        this function is no longer needed.

        :param state: the current state
        """
        for s in sandhi.apply(state):
            for t in siddha.asiddha(s):
                yield ''.join(x.asiddha for x in t)

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
            new_states = self._apply_next_rule(state)
            if new_states:
                stack.extend(new_states)

            # No applicable rules; state is in its final form.
            else:
                for result in self._sandhi_asiddha(state):
                    logger.debug('yield: %s' % result)
                    yield result
