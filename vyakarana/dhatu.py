# -*- coding: utf-8 -*-
"""
    vyakarana.dhatu
    ~~~~~~~~~~~~~~~

    Rules that apply specifically to a dhatu.

    :license: MIT and BSD
"""

from classes import Dhatu, Pratyaya
from decorators import *
from dhatupatha import DHATUPATHA as DP


@once('dhatu_adesha')
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
        dhatu = dhatu.antya('A')
        yield state.swap(i, dhatu)


@once('vikarana')
def vikarana(state):
    """Vikarana for classes 1 through 9."""

    i, dhatu = state.find('dhatu')
    gana_set = DP.gana(dhatu)

    def _yield(s):
        p = Pratyaya(s)
        p.samjna.add('anga')
        return state.insert(i+1, p)

    next = state[i+1]
    if 'sarvadhatuka' not in next.samjna:
        return

    # 3.1.68 kartari śap
    if '1' in gana_set or '10' in gana_set:
        yield _yield('Sap')

    # 2.4.75 juhotyādibhyaḥ śluḥ
    # TODO: move to proper section
    if '3' in gana_set:
        yield _yield('Slu~')

    # 3.1.69 divādibhyaḥ śyan
    if '4' in gana_set:
        yield _yield('Syan')

    # 3.1.73 svādibhyaḥ śnuḥ
    if '5' in gana_set:
        yield _yield('Snu')

    # 3.1.77 tudādibhyaḥ śaḥ
    if '6' in gana_set:
        yield _yield('Sa')

    # 3.1.78 rudhādhibhyaḥ śnam
    if '7' in gana_set:
        yield _yield('Snam')

    # 3.1.79 tanādikṛñbhya uḥ
    if '8' in gana_set:
        yield _yield('u')

    # 3.1.81 kryādibhyaḥ śnā
    if '9' in gana_set:
        yield _yield('SnA')

        # 3.1.82 stambhustumbhuskambhuskumbhuskuñbhyaḥ śnuś ca
        if dhatu.raw in ('sta\mBu~', 'stu\mBu~', 'ska\mBu~', 'sku\mBu~', 'sku\Y'):
            yield _yield('Snu')

    # 3.1.25 satyApa...
    # TODO: move to proper section
    if '10' in gana_set:
        yield _yield('Ric')


def pada_options(state):
    """Decide whether a state can use parasmaipada and atmanepada.
    Some states can use both.

    :param state:
    """
    # TODO: accent
    has_para = has_atma = False

    _, dhatu = state.find('dhatu')

    # 1.3.12 anudAttaGita Atmanepadam
    if 'N' in dhatu.it:
        has_para, has_atma = (False, True)

    # 1.3.72 svaritaJitaH kartrabhiprAye kriyAphale
    elif 'Y' in dhatu.it:
        has_para, has_atma = (True, True)

    # 1.3.76 anupasargAj jJaH
    # TODO: no upasarga
    elif dhatu.raw == 'jYA\\':
        has_para, has_atma = (True, True)

    # 1.3.78 zeSAt kartari parasmaipadam
    else:
        has_para, has_atma = (True, False)

    return (has_para, has_atma)
