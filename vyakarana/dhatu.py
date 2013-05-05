# -*- coding: utf-8 -*-
"""
    vyakarana.dhatu
    ~~~~~~~~~~~~~~~

    Rules that apply specifically to a dhatu.

    :license: MIT and BSD
"""

import gana
from classes import Dhatu, Upadesha as U
from decorators import *


def augment(state):
    """

    :param state:
    """

    i, dhatu = state.find('dhatu')
    tin = state[i+1]

    # 6.4.88 bhuvo vuk luGliToH
    if dhatu.raw == 'BU':
        if dhatu.parts[-1].raw == 'vu~k':
            return
        elif tin.adi().ac:
            dhatu = dhatu.tasya(U('vu~k'))
            yield state.swap(i, dhatu)


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
    if Dhatu(dhatu.raw).ec and tin.raw[0] != 'S':
        dhatu = dhatu.antya('A')
        yield state.swap(i, dhatu)


@once('ac_adesha')
def ac_adesha(state):
    """
    Perform substitutions on the dhatu. These substitutions can occur
    after dvirvacana has been attempted.

    :param state:
    """

    # 1.1.59 dvirvacane 'ci
    # If dvirvacana has not been attempted, don't make any (root)
    # substitutions. Otherwise, we could get results like:
    #
    #     sTA + iTa -> sT + iTa -> t + sT + iTa -> tsTita
    #     gam + iva -> gm + iva -> j + gm + iva -> jgmiva
    #
    # when what we desire is:
    #
    #     sTA + iTa -> ta + sTA + iTa -> ta + sT + iTa -> tasTita
    #     gam + iva -> ja + gam + iva -> ja + gm + iva -> jagmiva
    if 'dvirvacana' not in state.ops:
        return

    state = state.add_op('ac_adesha')

    i, dhatu = state.find('dhatu')
    tin = state[-1]

    # 6.4.64 Ato lopa iTi ca
    if dhatu.antya().value == 'A':
        if 'iw' in tin.parts[0].lakshana or 'k' in tin.it:
            dhatu = dhatu.antya('')
            yield state.swap(i, dhatu)

    # 6.4.98 gamahanajanakhanaghasAM lopaH kGityanaGi
    # TODO: aG
    gam_adi = set('gam han jan Kan Gas'.split())
    if dhatu.value in gam_adi and ('k' in tin.it or 'N' in tin.it):
        dhatu = dhatu.upadha('')
        yield state.swap(i, dhatu)

    # 6.4.121 - 6.4.122
    elif lit_a_to_e_condition(state):
        j, abhyasa = state.find('abhyasa')
        dhatu = dhatu.upadha('e')
        abhyasa = abhyasa.lopa()
        yield state.swap(i, dhatu).swap(j, abhyasa)


def lit_a_to_e_condition(state):
    """True iff this state qualifies for substition of 'e' and lopa of
    the abhyasa.

        6.4.120 ata ekahalmadhye 'nAdezAder liTi
        6.4.121 thali ca seTi

    :param state: some State
    """
    i, abhyasa = state.find('abhyasa')
    j, dhatu = state.find('dhatu')
    tin = state[-1]

    if 'li~w' not in tin.lakshana:
        return False

    if dhatu.clean in gana.KRADI:
        return False

    # e.g. 'pac', 'man', 'ram', but not 'syand', 'grah'
    at_ekahal_madhya = (dhatu.upadha().value == 'a' and len(dhatu.value) == 3)
    # e.g. 'pac' (pa-pac), 'ram' (ra-ram), but not 'gam' (ja-gam)
    anadesha_adi = (abhyasa.value[0] == dhatu.value[0])

    if at_ekahal_madhya and anadesha_adi:
        if 'k' in tin.it or tin.value == 'iTa':
            return True
    return False


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

    # 1.3.78 zeSAt kartari parasmaipadam
    else:
        has_para, has_atma = (True, False)

    return (has_para, has_atma)
