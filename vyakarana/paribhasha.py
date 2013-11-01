# -*- coding: utf-8 -*-
"""
    vyakarana.paribhasha
    ~~~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

import filters as F
from templates import *


@paribhasha(('lu~k', 'Slu~', 'lu~p'), None)
def pratyaya_lopa():
    def do_lopa(state, index, locus=None):
        lopa = state[index]
        raw = lopa.raw
        pratyaya = state[index + 1].add_lakshana(raw)
        yield state.remove(index).swap(index, pratyaya)

    return [
        ('1.1.60 - 1.1.63',
            None,  None,
            do_lopa),
    ]


@paribhasha(None, 'mit')
def mit_aco_ntyat_parah():
    """
    Apply 'mit' substitution more generally.

    Rule 1.1.47 of the Ashtadhyayi defines how to substitute a term
    marked with indicatory 'm':

        1.1.47 mid aco 'ntyāt paraḥ

    But if the term is introduced by a "tasmāt" rule instead, then this
    rule has no time to act. This function allows 1.1.47 to act even
    when a 'mit' term is introduced by a "tasmāt" rule.
    """
    def move_mit(state, index, locus=None):
        base = state[index]
        mit = state[index + 1]
        yield state.remove(index + 1).swap(index, base.tasya(mit))

    return [
        ('1.1.47',
            None, None,
            move_mit)
    ]