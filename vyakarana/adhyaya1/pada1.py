# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


@O.Operator.no_params
def _47(state, index, locus=None):
    """Apply 'mit' substitution more generally.

    Rule 1.1.47 of the Ashtadhyayi defines how to substitute a term
    marked with indicatory 'm':

        1.1.47 mid aco 'ntyāt paraḥ

    But if the term is introduced by a "tasmāt" rule instead, then this
    rule has no time to act. This function allows 1.1.47 to act even
    when a 'mit' term is introduced by a "tasmāt" rule.
    """
    mit = state[index]
    op = O.tasya(mit)
    state = op.apply(state, index - 1, locus)
    return state.remove(index)


@O.Operator.no_params
def _60_63(state, index, locus=None):
    """Perform pratyaya-lopa."""
    lopa = state[index]
    raw = lopa.raw
    pratyaya = state[index + 1].add_lakshana(raw)
    return state.remove(index).swap(index, pratyaya)


RULES = [
    Anuvrtti(category='paribhasha'),
    ('1.1.47', None, 'mit', None, _47),
    ('1.1.60', None, f('lu~k', 'Slu~', 'lu~p'), None, _60_63),
]
