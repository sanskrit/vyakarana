# -*- coding: utf-8 -*-
"""
    vyakarana.anga
    ~~~~~~~~~~~~~~

    Rules that apply specifically to an anga.

    :license: MIT and BSD
"""

import gana
from classes import Group, Sound, Upadesha as U
from decorators import *
from util import iter_pairwise


@require('dvirvacana')
@once('anga_adesha')
def adesha(state):
    i, dhatu = state.find('dhatu')
    value = dhatu.value
    next = state[i+1]

    # 6.1.16 vacisvapiyajAdInAM kiti
    # 6.1.17 grahi... Giti ca
    vac_condition = 'k' in next.it and value in gana.VAC
    grah_condition = value in gana.GRAH and ('k' in next.it or 'N' in next.it)
    if vac_condition or grah_condition:
        dhatu = dhatu.samprasarana()
        yield state.swap(i, dhatu)

    # 7.2.115 aco `Jniti (vrddhi)
    # 7.2.116 ata upadhAyAH
    if 'Y' in next.it or 'R' in next.it:
        if dhatu.ac or dhatu.upadha().value == 'a':
            dhatu = dhatu.vrddhi()
        else:
            dhatu = dhatu.guna()

        yield state.swap(i, dhatu)

    # 7.3.84 sArvadhAtukArdhadhAtukayoH
    elif 'sarvadhatuka' in next.samjna or 'ardhadhatuka' in next.samjna:
        # 1.1.5 kGiti ca
        if 'k' in next.it or 'N' in next.it:
            yield state
        else:
            dhatu = dhatu.guna()
            yield state.swap(i, dhatu)

    else:
        yield state


def rt(state):
    i, dhatu = state.find('dhatu')
    lit = 'li~w' in state[i+1].lakshana
    if dhatu.samyogadi and dhatu.antya().value == 'f':
        yield state.swap(i, dhatu.guna())


@once('anga_iyan_uvan')
def iyan_uvan(state):
    """
    This rule must not apply to terms that haven't gone through the
    vowel strengthening rules. Otherwise, we could get results like:

        tu + stu + a -> tu + stuv + a -> tuzwova

    when what we desire is:

        tu + stu + a -> tu + stO + a -> tuzwAva

    :param state:
    """
    for i, (cur, next) in enumerate(iter_pairwise(state.items)):
        value = cur.value
        if not value:
            continue

        f = value[-1]

        if f in Group('i u') and next.adi().ac:
            s = next.adi().value[0]

            # 6.4.77 aci znudhAtubhruvAM yvor iyaGuvaGau
            # TODO: other categories
            _77 = 'dhatu' in cur.samjna

            # 6.4.78 abhyAsasyAsavarNe
            _78 = 'abhyasa' in cur.samjna and Sound(f).asavarna(s)
            if _77 or _78:
                if f in Group('i'):
                    cur = cur.tasya(U('iya~N'))
                else:
                    cur = cur.tasya(U('uva~N'))

                yield state.swap(i, cur)
