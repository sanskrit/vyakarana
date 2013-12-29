# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada4
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..sounds import Sounds
from ..templates import *
from ..upadesha import Upadesha as U

f = F.auto

ac = Sounds('ac')
shar = Sounds('Sar')
khay = Sounds('Kay')


@O.Operator.no_params
def hal_shesha(state, index, locus=None):
    cur = state[index]
    first_hal = first_ac = ''
    for i, L in enumerate(cur.value):
        if i == 1 and cur.value[0] in shar and L in khay:
            first_hal = L
        if L in ac:
            first_ac = L
            break
        elif not first_hal:
            first_hal = L

    new_value = first_hal + first_ac
    if new_value != cur.value:
        return state.swap(index, cur.set_value(new_value))
    else:
        return state


@F.AlFilter.no_params
def dvihal(term):
    hal = Sounds('hal')
    hal_r = Sounds('hal f')
    return term.upadha in hal_r and term.antya in hal


RULES = [
    Anuvrtti(None, 'anga', F.lakshana('li~w')),
    ('7.4.10', None, F.samyogadi & F.al('ft'), None, O.force_guna),
    ('7.4.11', None, F.raw('f\\') | F.al('Ft'), None, True),
    Va('7.4.12', None, f('SF', 'dF', 'pF'), None, O.hrasva),

    Anuvrtti(None, 'abhyasa', None),
    ('7.4.59', None, None, None, O.hrasva),
    ('7.4.60', None, None, None, hal_shesha),
    ('7.4.61', None, F.adi('Sar'), None, True),
    ('7.4.62', None, None, None, O.al_tasya('ku h', 'cu')),
    ('7.4.66', None, F.contains('f'), None, O.al_tasya('f', 'at')),
    ('7.4.69', None, None, ['i\\R', 'kit'], O.dirgha),
    ('7.4.70', None, F.adi('at'), None, True),

    Anuvrtti('abhyasa', 'anga', None),
    ('7.4.71', F.value('A'), dvihal, None, U('nu~w')),
    Ca('7.4.72', True, 'aSU~\\', None, True),

    Anuvrtti(None, 'abhyasa', None),
    ('7.4.73', None, None, 'BU', 'a'),
]
