# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada4
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..sounds import Sounds
from ..templates import *

f = F.auto


@inherit(None, 'anga', F.lakshana('li~w'))
def angasya_liti():
    return [
        ('7.4.10', None, F.samyogadi & F.al('ft'), None, O.force_guna),
        ('7.4.11', None, F.raw('f\\') | F.al('Ft'), None, True),
        Va('7.4.12', None, f('SF', 'dF', 'pF'), None, O.hrasva)
    ]


@inherit(None, 'abhyasa', None)
def angasya_abhyasasya():
    ac = Sounds('ac')
    shar = Sounds('Sar')
    khay = Sounds('Kay')

    @O.Operator.unparameterized
    def _60_61(state, index, locus=None):
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

    return [
        ('7.4.59', None, None, None, O.hrasva),
        ('7.4.60', None, None, None, _60_61),
        ('7.4.61', None, F.adi('Sar'), None, True),
        ('7.4.62', None, None, None, O.al_tasya('ku h', 'cu')),
        ('7.4.66', None, None, None, O.al_tasya('f', 'at')),
        ('7.4.69', None, None, ['i\\R', 'kit'], O.dirgha),
        ('7.4.70', None, F.adi('at'), None, True),
        ('7.4.73', None, None, 'BU', 'a'),
    ]
