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

import abhyasa
import anga
import atidesha
import dhatu
import dhatupatha
import pratyaya
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

        #: The rules of the grammar, from highest priority to lowest.
        self.sorted_rules = sorted(ALL_RULES, cmp = lambda x, y: cmp(y.rank, x.rank))
        #: Maps a rule's name to a :class:`Rule` instance.
        self.rule_map = {x.name: x for x in ALL_RULES}

    def apply_next_rule(self, state):
        """Apply one rule and return a list of new states.

        This function applies conflict resolution to a list of candidate
        rules until one rule remains.

        :param state: the current :class:`State`
        """
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
                for x in self.sandhi_asiddha(state):
                    yield x

    def sandhi_asiddha(self, state):
        for s in sandhi.apply(state):
            yield ''.join(x.asiddha for x in s)


class NewAshtadhyayi(Ashtadhyayi):

    pass