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
import util
from dhatupatha import DHATUPATHA as DP
from templates import *
from upadesha import Dhatu, Krt


def adesha(state):
    """
    Perform substitutions on the dhatu. These substitutions can occur
    before ___.

    :param state:
    """

    i, dhatu = state.find('dhatu')
    tin = state[-1]

    if 'vibhakti' not in tin.samjna:
        return

    # 6.1.45 Ad eca upadeze 'ziti
    # One would expect that 'azit' means "that which does not have 'z'."
    # But instead we should interpret it as "that which does not start
    # with 'z' in upadesha. This difference allows us to apply the rules
    # when the suffix 'eS' follows. 'eS' has indicatory 'S', so normally
    # the rule would not apply; but with this change in interpretation,
    # the rule can apply.
    _45 = Dhatu(dhatu.raw).ec and tin.raw[0] != 'S'
    if _45:
        dhatu = dhatu.tasya('A')
        yield state.swap(i, dhatu)


@tasmat('dhatu', 'tin')
def sanadyanta_dhatu():

    def k(s):
        return Krt(s).add_samjna('dhatu').add_samjna('anga')

    return [
        ('3.1.28',
            # TODO: vicCi, pani
            ('gupU~', 'DUpa~', 'paRa~\\'), None,
            k('Aya')),
        ('3.1.30',
            'kamu~\\', None,
            k('Rin')),
    ]


@tasmat('dhatu', F.samjna('tin') & F.samjna('sarvadhatuka'))
def vikarana():
    """Vikarana for classes 1 through 10."""

    # 3.1.70 vā bhrāśabhlāśabhramukramuklamutrasitrutilaṣaḥ
    bhrasha_bhlasha = ('wuBrASf~\\', 'wuBlASf~\\', 'Bramu~', 'kramu~',
                     'klamu~', 'trasI~', 'truwa~', 'laza~^')
    # 3.1.82 stambhustumbhuskambhuskumbhuskuñbhyaḥ śnuś ca
    stambhu_stumbhu = ('sta\mBu~', 'stu\mBu~', 'ska\mBu~', 'sku\mBu~',
                       'sku\Y')

    def k(s):
        return Krt(s).add_samjna('anga')

    return [
        ('3.1.68',
            None, None,
            k('Sap')),
        ('3.1.69',
            F.gana('divu~'), None,
            k('Syan')),
        ('3.1.70',
            bhrasha_bhlasha, None,
            True),
        ('3.1.73',
            F.gana('zu\\Y'), None,
            k('Snu')),
        ('3.1.77',
            F.gana('tu\da~^'), None,
            k('Sa')),
        ('3.1.78',
            F.gana('ru\Di~^r'), None,
            k('Snam')),
        ('3.1.79',
            F.gana('tanu~^'), None,
            k('u')),
        ('3.1.81',
            F.gana('qukrI\Y'), None,
            k('SnA')),
        # TODO: ca
        ('3.1.68',
            stambhu_stumbhu, None,
            k('Snu')),
    ]


def pada_options(dhatu):
    """Decide whether a state can use parasmaipada and atmanepada.
    Some states can use both.

    :param state:
    """
    # TODO: accent
    has_para = has_atma = False

    # 1.3.12 anudAttaGita Atmanepadam
    if dhatu.any_samjna('Nit', 'anudattet'):
        has_para, has_atma = (False, True)

    # 1.3.72 svaritaJitaH kartrabhiprAye kriyAphale
    if dhatu.any_samjna('Yit', 'svaritet'):
        has_para, has_atma = (True, True)

    # 1.3.76 anupasargAj jJaH
    # TODO: no upasarga
    elif dhatu.raw == 'jYA\\':
        has_para, has_atma = (True, True)

    # 1.3.78 zeSAt kartari parasmaipadam
    else:
        has_para, has_atma = (True, False)

    return (has_para, has_atma)
