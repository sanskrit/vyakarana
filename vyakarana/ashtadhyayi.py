# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the other parts of the grammar.

    :license: MIT and BSD
"""

import itertools
import logging
import os

import abhyasa
import anga
import dhatu
import dhatupatha
import sandhi
import siddha
import vibhakti

from templates import ALL_RULES
from util import State

log = logging.getLogger(__name__)


class Ashtadhyayi(object):

    """The Ashtadhyayi."""

    def __init__(self):
        dirname = os.path.dirname(os.path.dirname(__file__))
        dhatu_file = os.path.join(dirname, 'data', 'dhatupatha.csv')
        dhatupatha.DHATUPATHA.init(dhatu_file)

        self.sorted_rules = sorted(ALL_RULES, key = lambda x: -x.rank)
        self.rule_map = {x.name: x for x in ALL_RULES}


    def apply_next_rule(self, state):
        """Apply one rule and return a list of new states.

        This function applies conflict resolution to a list of candidate
        rules until one rule remains.

        :param state: the current :class:`State`
        """
        for ra, ia in itertools.product(ALL_RULES, range(len(state))):
            ra_states = None

            # List of valid states that could be produced from `ra`
            if ra.matches(state, ia):
                ra_states = list(ra.apply(state, ia))
            if not ra_states:
                continue

            # Marks whether a rule has been overruled
            overruled = False

            for rb, sa in itertools.product(ALL_RULES, ra_states):
                ra_rb_states = []
                for ib in range(len(sa)):
                    if rb.matches(sa, ib):
                        ra_rb_states.extend(rb.apply(sa, ib))

                # `rb` can't apply anywhere.
                if not ra_rb_states:
                    continue

                # cyclical rules
                if state in ra_rb_states:
                    # The stronger rule dominates and should be favored.
                    if ra.rank > rb.rank:
                        log.debug('  %s' % ra.name)
                        return ra_states
                    # The weaker rule should be totally ignored.
                    else:
                        overruled = True
                        break

                else:
                    log.debug('  %s' % ra.name)
                    return ra_states

            if not overruled:
                log.debug('  %s' % ra.name)
                return ra_states

        return None

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
                for s in new_states:
                    log.debug('    %s --> %s' % (state, s))
                stack.extend(new_states)

            # No applicable rules; state is in its final form.
            else:
                log.debug('yield: %s' % state)
                yield ''.join(x.asiddha for x in state)


class NewAshtadhyayi(Ashtadhyayi):

    def apply_next_rule(self, state):
        sorted_rules = self.sorted_rules
        for a, ra in enumerate(sorted_rules):
            for ia in range(len(state)):

                # Ignore redundant applications
                ra_key = state.make_rule_key(ra, ia)
                if ra_key in state.history:
                    continue

                # Only worthwhile rules
                ra_states = None
                if ra.matches(state, ia):
                    ra_states = list(ra.apply(state, ia))
                if not ra_states:
                    # if ra_states is None:
                    #     log.debug('  SKIP %s (no match)' % ra)
                    #     if ra.name == '7.3.86' and ia == 1:
                    #         print ra.filters
                    #         print ra.filters[0](state[0], state, 0)
                    #         print ra.filters[1](state[1], state, 1)
                    #         print ra.filters[2](state[2], state, 2)
                    #         print [x.data for x in state]
                    #         print [x.samjna for x in state]
                    #         print [x.lakshana for x in state]
                    # else:
                    #     log.debug('  SKIP %s (no states)' % ra)
                    continue

                # Verify this doesn't undo a prior rule.
                nullifies_old = False
                for rb_key in state.history:
                    rb = self.rule_map[rb_key[0]]
                    ib = rb_key[1]
                    if any(rb.yields(s, ib) for s in ra_states):
                        nullifies_old = True
                if nullifies_old:
                    continue

                # Verify this isn't dominated by any other rules
                # TODO

                log.debug('  %s' % ra.name)
                return ra_states
