# -*- coding: utf-8 -*-
"""
    vyakarana.abhyasa
    ~~~~~~~~~~~~~~~~~

    Routines for reduplication.

    :license: MIT and BSD
"""

import gana

from classes import Term, Pratyahara as P, Upadesha as U, Sound, Group
from decorators import *

@once('dvirvacana')
def dvirvacana(state):
    """Apply the operation of 'dvirvacana'.

    This creates the abhyasa and abhyasta.

    :param state:
    """

    i, dhatu = state.find('dhatu')
    p = state[i+1]

    # 6.1.8 liTi dhAtor anabhyAsasya
    if state.find('abhyasa')[1]:
        return
    _8 = 'li~w' in p.lakshana

    # 6.1.9 sanyaGoH
    _9 = 'san' in p.lakshana or 'yaN' in p.lakshana

    # 6.1.10 zlau
    _10 = 'Slu~' in p.lakshana

    # 6.1.11 caGi
    _11 = 'caN' in p.lakshana

    if not (_8 or _9 or _10 or _11):
        return

    # 6.1.1 ekAco dve prathamasya
    abhyasa = Term(dhatu.value)

    # 6.1.2 ajAder dvitIyasya
    if dhatu.adi().ac:
        pass

    # 6.1.3 na ndrAH saMyogAdayaH

    # 6.1.4 pUrvo 'bhyAsaH
    # 6.1.5 ubhe abhyastam
    abhyasa = abhyasa.add_samjna('abhyasa', 'abhyasta')
    dhatu = dhatu.add_samjna('abhyasta')

    if _8:
        # 6.1.17 liTyabhyAsyobhayeSAm
        if dhatu.value in gana.VAC or dhatu.value in gana.GRAH:
            abhyasa = abhyasa.samprasarana()

    new_state = state.swap(i, dhatu).insert(i, abhyasa)

    for x in clean_abhyasa(new_state):
        yield x


def abhyasa_adesha(state):
    i, abhyasa = state.find('abhyasa')
    j, dhatu = state.find('dhatu')

    if not abhyasa:
        return

    # 6.4.78 abhyAsasyAsavarNe
    # TODO

    a = abhyasa.antya()
    d = dhatu.adi()

    if a.value in 'iIuU' and Sound(a.value).asavarna(d.value):
        abhyasa = abhyasa.set_value(abhyasa.value + a.to_yan().value)
        yield state.swap(i, abhyasa)


def clean_abhyasa(state):
    i, abhyasa = state.find('abhyasa')
    j, dhatu = state.find('dhatu')
    tin = state[-1]

    if not abhyasa.value:
        return

    # 7.4.66 ur at
    abhyasa = abhyasa.replace('f', 'ar')
    abhyasa = abhyasa.replace('F', 'ar')

    # 7.4.59 hrasvaH
    abhyasa = abhyasa.to_hrasva()

    # 7.4.60 halAdiH zeSaH
    # 7.4.61 zarpUrvAH khayaH
    try:
        v = abhyasa.value
        if v[0] in P('Sar') and v[1] in P('Kay'):
            abhyasa = abhyasa.set_value(v[1:])
        else:
            temp = []
            first = True
            for x in abhyasa.value:
                if x in P('ac'):
                    temp.append(x)
                    break
                elif x in P('hal') and first:
                    temp.append(x)
                    first = False
            abhyasa = abhyasa.set_value(''.join(temp))
    except IndexError:
        pass

    # 7.4.62 kuhoz cuH
    # 7.4.63 na kavater yaGi
    adi = abhyasa.adi().value
    if adi in Group('ku h'):
        abhyasa = abhyasa.adi(Sound(adi).closest(Group('cu')))

    # Exceptions for lit:
    if 'li~w' in tin.lakshana:
        special_case = True

        # 7.4.69 dIrgha iRaH kiti
        if dhatu.raw == 'iR' and 'k' in tin.it:
            abhyasa = abhyasa.set_value('I')

        elif abhyasa.adi().value == 'a':
            # 7.4.70 ata AdeH
            abhyasa = abhyasa.set_value('A')

            # 7.4.71 tasmAn nuD dvihalaH
            # 'dvihal' is supposedly used to additionally refer to roots
            # like 'fD', which would become saMyogAnta when combined
            # with the abhyasa.
            dvihal = dhatu.samyoga or (dhatu.hal
                                       and dhatu.upadha().value == 'f')

            # 7.4.72 aznotez ca
            # 'aznoti' refers specifically to 'aSU~'.
            ashnoti = (dhatu.raw == 'aSU~')
            if dvihal or ashnoti:
                abhyasa = abhyasa.tasmat(U('nu~w'))

        # 7.4.73 bhavater aH
        elif dhatu.raw == 'BU':
            abhyasa = abhyasa.set_value('ba')
            new_state = state.swap(i, abhyasa)

        # All others are general
        else:
            special_case = False

        if special_case:
            yield state.swap(i, abhyasa)
            return

    # 8.4.54 the consonant becomes deaspirated
    abhyasa = abhyasa.adi(abhyasa.adi().deaspirate().value)

    new_state = state.swap(i, abhyasa)
    yield new_state
