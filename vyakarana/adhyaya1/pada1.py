# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


@inherit(None, 'mit', None, category='paribhasha')
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

    @O.Operator.unparameterized
    def move_mit(state, index, locus=None):
        base = state[index - 1]
        mit = state[index]
        base = base.tasya(mit)
        return state.remove(index).swap(index - 1, base)

    return [
        ('1.1.47', None, None, None, move_mit)
    ]


@inherit(None, ('lu~k', 'Slu~', 'lu~p'), None, category='paribhasha')
def pratyaya_lopa():
    @O.Operator.unparameterized
    def do_lopa(state, index, locus=None):
        lopa = state[index]
        raw = lopa.raw
        pratyaya = state[index + 1].add_lakshana(raw)
        return state.remove(index).swap(index, pratyaya)

    return [
        ('1.1.60 - 1.1.63', None, None, None, do_lopa),
    ]
