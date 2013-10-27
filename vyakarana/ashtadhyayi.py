# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the other parts of the grammar.

    :license: MIT and BSD
"""

import itertools
import logging

import abhyasa
import anga
import dhatu
import sandhi
import siddha
import vibhakti
from templates import NEW_RULES
from util import State

log = logging.getLogger(__name__)
initialized = False


class History(list):
    def __str__(self):
        lines = ['History:']
        for state in self:
            lines.append('  %s' % repr([x.value for x in state]))
        return '\n'.join(lines)


def apply_next_rule(state):
    """Apply one rule and return a list of new states.

    This function applies conflict resolution to a list of candidate
    rules until one rule remains.

    :param state: the current :class:`State`
    """
    for ra, ia in itertools.product(NEW_RULES, range(len(state))):
        ra_states = None
        if not ra.name.startswith('3'):
            continue

        # List of valid states that could be produced from `ra`
        if ra.matches(state, ia):
            ra_states = list(ra.apply(state, ia))
        if not ra_states:
            continue

        # Marks whether a rule has been overruled
        overruled = False

        for rb, sa in itertools.product(NEW_RULES, ra_states):
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


def derive(sequence):
    """Yield all possible results.

    :param sequence: a starting sequence
    """
    if not initialized:
        init()

    start = State(sequence)
    history = History()
    history.append(start)

    print '---'
    print start
    while history:
        state = history.pop()
        new_states = apply_next_rule(state)
        if new_states:
            for s in new_states:
                log.debug('    %s --> %s' % (state, s))
            history.extend(new_states)

        # No applicable rules; state is in its final form.
        else:
            print state
            yield ''.join(x.asiddha for x in state)


def init():
    global initialized
    import dhatupatha
    import os
    dirname = os.path.dirname(os.path.dirname(__file__))
    dhatu_file = os.path.join(dirname, 'data', 'dhatupatha.csv')
    dhatupatha.DHATUPATHA.init(dhatu_file)
    initialized = True
