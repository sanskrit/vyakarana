# -*- coding: utf-8 -*-
"""
    vyakarana.dhatu
    ~~~~~~~~~~~~~~~

    Rules that apply specifically to a dhātu. Almost all such rules are
    within the domain of 3.1.91:

        3.1.91 dhātoḥ

    which holds until the end of 3.4.

    :license: MIT and BSD
"""

import filters as F
from templates import *
from upadesha import Dhatu, Krt

f = F.auto


@inherit(None, F.raw('Sap'), None)
def sap_lopa():
    return [
        ('2.4.71', F.gana('a\da~'), None, None, 'lu~k'),
        ('2.4.74', F.gana('hu\\'), None, None, 'Slu~')
    ]


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
