# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya3.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..upadesha import Krt

f = F.auto


@inherit('dhatu', None, 'tin')
def sanadyanta_dhatu():

    def k(s):
        return Krt(s).add_samjna('anga')

    gupu_dhupa = ('gupU~', 'DUpa~', 'vicCa~', 'paRa~\\', 'pana~\\')

    return [
        ('3.1.28', gupu_dhupa, None, 'tin', k('Aya')),
        ('3.1.30', 'kamu~\\', None, True, k('RiN')),
    ]


@inherit('dhatu', None, f('tin') & f('sarvadhatuka'))
def vikarana():

    def k(s):
        return Krt(s).add_samjna('anga')

    # 3.1.70 vā bhrāśabhlāśabhramukramuklamutrasitrutilaṣaḥ
    bhrasha_bhlasha = ('wuBrASf~\\', 'wuBlASf~\\', 'Bramu~', 'kramu~',
                     'klamu~', 'trasI~', 'truwa~', 'laza~^')
    # 3.1.82 stambhustumbhuskambhuskumbhuskuñbhyaḥ śnuś ca
    stambhu_stumbhu = ('sta\mBu~', 'stu\mBu~', 'ska\mBu~', 'sku\mBu~',
                       'sku\Y')

    return [
        ('3.1.68', None, None, None, k('Sap')),
        ('3.1.69', F.gana('divu~'), None, None, k('Syan')),
        Va('3.1.70', bhrasha_bhlasha, None, None, True),
        ('3.1.73', F.gana('zu\\Y'), None, None, k('Snu')),
        ('3.1.77', F.gana('tu\da~^'), None, None, k('Sa')),
        ('3.1.78', F.gana('ru\Di~^r'), None, None, k('Snam')),
        ('3.1.79', F.gana('tanu~^'), None, None, k('u')),
        ('3.1.81', F.gana('qukrI\\Y'), None, None, k('SnA')),
        Ca('3.1.82', stambhu_stumbhu, None, None, k('Snu')),
    ]
