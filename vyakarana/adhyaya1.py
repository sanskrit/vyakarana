# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1
    ~~~~~~~~~~~~~~~~~~

    Rules from the first book of the Ashtadhyayi.

    :license: MIT and BSD
"""

import filters as F
from templates import *

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


@inherit(None, None, None)
def pada2():
    return [
        ('1.2.4', None, f('sarvadhatuka') & ~f('pit'), None, 'Nit'),
        ('1.2.5', ~F.samyoga, ~f('pit') & f('li~w'), None, 'kit'),
        Ca('1.2.6', ('YiinDI~\\', 'BU'), f('li~w'), None, True),
    ]


@inherit('dhatu', None, None)
def pada3():
    """Apply the rules that select atmanepada and parasmaipada.

    Strictly speaking, the rules below are distortions of the actual
    rules in the Ashtadhyayi. The terms "parasamipada" and "atmanepada"
    refer to the *replacements* of the "la" affixes, not to the "la"
    affixes themselves.
    """

    return [
        ('1.3.12', ('anudattet', 'Nit'), None, None, 'atmanepada'),
        Artha('1.3.72', ('svaritet', 'Yit'), None, None, True),
        ('1.3.76', 'jYA\\', None, None, True),
        ('1.3.78', None, None, None, 'parasmaipada'),
    ]
