# -*- coding: utf-8 -*-
"""
    vyakarana.dhatu
    ~~~~~~~~~~~~~~~

    Rules that apply specifically to a dhatu.

    :license: MIT and BSD
"""

from classes import Dhatu
from decorators import *


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
