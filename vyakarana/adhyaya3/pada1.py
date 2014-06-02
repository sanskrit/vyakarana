# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya3.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..terms import Krt

f = F.auto


def k_dhatu(s):
    return Krt(s).add_samjna('dhatu', 'anga')


def k_anga(s):
    return Krt(s).add_samjna('anga')


GUPU_DHU = f('gupU~', 'DUpa~', 'vicCa~', 'paRa~\\', 'pana~\\')


BHRASHA_BHLASHA = f('wuBrASf~\\', 'wuBlASf~\\', 'Bramu~', 'kramu~',
                    'klamu~', 'trasI~', 'truwa~', 'laza~^')


STAMBHU_STUMBHU = f('sta\mBu~', 'stu\mBu~', 'ska\mBu~', 'sku\mBu~',
                    'sku\Y')


RULES = [
    Anuvrtti('dhatu', None, 'tin'),
    ('3.1.25', F.gana('cura~'), None, 'tin', k_dhatu('Ric')),
    ('3.1.28', GUPU_DHU, None, 'tin', k_dhatu('Aya')),
    ('3.1.29', 'fti~\\', None, True, k_dhatu('IyaN')),
    ('3.1.30', 'kamu~\\', None, True, k_dhatu('RiN')),

    Anuvrtti('dhatu', None, f('tin') & f('sarvadhatuka')),
    ('3.1.33', None, None, 'lf~w', k_anga('sya')),
    ('3.1.68', None, None, None, k_anga('Sap')),
    ('3.1.69', F.gana('divu~'), None, None, k_anga('Syan')),
    Va('3.1.70', BHRASHA_BHLASHA, None, None, True),
    ('3.1.73', F.gana('zu\\Y'), None, None, k_anga('Snu')),
    ('3.1.77', F.gana('tu\da~^'), None, None, k_anga('Sa')),
    ('3.1.78', F.gana('ru\Di~^r'), None, None, k_anga('Snam')),
    ('3.1.79', F.gana('tanu~^'), None, None, k_anga('u')),
    ('3.1.81', F.gana('qukrI\\Y'), None, None, k_anga('SnA')),
    Ca('3.1.82', STAMBHU_STUMBHU, None, None, k_anga('Snu')),
]
