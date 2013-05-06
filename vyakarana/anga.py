# -*- coding: utf-8 -*-
"""
    vyakarana.anga
    ~~~~~~~~~~~~~~

    Rules that apply specifically to an aṅga. Almost all such rules are
    within the domain of 6.4.1:

        6.4.1 aṅgasya

    which holds from the beginning of 6.4 to the end of 7.4. Of these
    rules, however, the ones from 7.4.58 onward apply specifically to
    the abhyāsa of some aṅga, as opposed to the aṅga itself.

    Some of the rules contained in this section apply in contexts where
    only a dhātu would make sense. But since a dhātu is a type of aṅga,
    there's no harm in matching on an aṅga generally.

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


@once('anga_aci')
def aci(state):
    """
    Apply rules conditioned by a following vowel.

    This rule must not apply to terms that haven't gone through the
    vowel strengthening rules. Otherwise, we could get results like:

        tu + stu + a -> tu + stuv + a -> tuzwova

    when what we desire is:

        tu + stu + a -> tu + stO + a -> tuzwAva

    :param state:
    """
    i, anga = state.find('anga')
    p = state[i+1]

    if not anga.value:
        return

    f = anga.value[-1]
    s = p.adi()

    if f in Group('i u') and s.ac:

        # 6.4.77 aci znudhAtubhruvAM yvor iyaGuvaGau
        # TODO: other categories
        _77 = 'dhatu' in anga.samjna

        # 6.4.78 abhyAsasyAsavarNe
        _78 = 'abhyasa' in anga.samjna and Sound(f).asavarna(s.value)
        if _77 or _78:
            if f in Group('i'):
                anga = anga.tasya(U('iya~N'))
            else:
                anga = anga.tasya(U('uva~N'))

            yield state.swap(i, anga)


@once('ac_adesha')
def ac_adesha(state):
    """
    Perform substitutions on the anga. These substitutions can occur
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

    i, anga = state.find('anga')
    tin = state[-1]

    # 6.4.64 Ato lopa iTi ca
    if anga.antya().value == 'A':
        if 'iw' in tin.parts[0].lakshana or 'k' in tin.it:
            anga = anga.antya('')
            yield state.swap(i, anga)
            return

    # 6.4.98 gamahanajanakhanaghasAM lopaH kGityanaGi
    # TODO: aG
    gam_adi = set('gam han jan Kan Gas'.split())
    if anga.value in gam_adi and ('k' in tin.it or 'N' in tin.it):
        anga = anga.upadha('')
        yield state.swap(i, anga)

    else:
        for s in lit_a_to_e(state):
            yield s


def lit_a_to_e(state):
    """Applies rules that cause ed-ādeśa and abhyāsa-lopa.

    Specifically, these rules are 6.4.120 - 6.4.126.

    :param state: some State
    """
    i, abhyasa = state.find('abhyasa')
    j, anga = state.find('anga')
    # The right context of `anga`. This is usually a pratyaya.
    p = state[j+1]
    # True, False, or 'optional'. Crude, but it works.
    status = False

    liti = 'li~w' in p.lakshana
    # e.g. 'pac', 'man', 'ram', but not 'syand', 'grah'
    at_ekahal_madhya = (anga.upadha().value == 'a' and len(anga.value) == 3)
    # e.g. 'pac' (pa-pac), 'ram' (ra-ram), but not 'gam' (ja-gam)
    anadesha_adi = (abhyasa.value[0] == anga.value[0])

    if liti:
        # 6.4.120 ata ekahalmadhye 'nAdezAder liTi
        if at_ekahal_madhya and anadesha_adi:
            # 'kGiti' is inherited from 6.4.119.
            if 'k' in p.it:
                status = True

            # 6.4.121 thali ca seTi
            elif p.value == 'iTa':
                status = True

        # 6.4.122 tRRphalabhajatrapaz ca
        if anga.clean in ('tF', 'Pal', 'Baj', 'trap'):
            status = True

        # 6.4.123 rAdho hiMsAyAm
        elif anga.clean == 'rAD':
            status = 'optional'

        # 6.4.124 vA jRRbhramutrasAm
        elif anga.clean in ('jF', 'Bram', 'tras'):
            status = 'optional'

        # 6.4.125 phaNAM ca saptAnAm
        elif anga.clean in gana.PHAN:
            status = 'optional'

        # 6.4.126 na zasadadavAdiguNAnAm
        # TODO: guna
        vadi = anga.adi().value == 'v'
        if anga.clean in ('Sas', 'dad') or vadi:
            status = False

    if status in (True, 'optional'):
        yield state.swap(i, abhyasa.lopa()).swap(j, anga.upadha('e'))

    if status in (False, 'optional'):
        yield state
