# -*- coding: utf-8 -*-
"""
    vyakarana.abhyasa
    ~~~~~~~~~~~~~~~~~

    Routines for reduplication.

    :license: MIT and BSD
"""

import gana

from classes import Term, Pratyahara as P, Upadesha as U, Sound
from decorators import *


def dvirvacana(state):
    """Apply the operation of 'dvirvacana'.

    This creates the abhyasa and abhyasta.

    :param state:
    """
    i, dhatu = state.find('dhatu')
    tin = state[-1]

    if 'dvirvacana' in state.ops:
        return

    # Imposed order: no abhyasta unless the endings have been created.
    if 'vibhakti' not in tin.samjna:
        return

    state = state.add_op('dvirvacana')

    if 'li~w' in tin.lakshana:
        for x in lit_abhyasta(state):
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

    # General exceptions for lit
    if 'li~w' in tin.lakshana:
        # 6.1.17 liTyabhyAsyobhayeSAm
        if dhatu.value in gana.VAC or dhatu.value in gana.GRAH:
            abhyasa = abhyasa.samprasarana()

    # 7.4.66 ur at
    abhyasa = abhyasa.replace('f', 'ar')

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

    # 7.4.60 halAdiH zeSaH
    # 7.4.61 zarpUrvoH khayaH
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

    # 7.4.59 hrasvaH
    abhyasa = abhyasa.to_hrasva()

    # 7.4.62 kuhoz cuH
    converter = dict(zip('kKgGNh', 'cCjJYj'))
    adi = abhyasa.adi().value
    abhyasa = abhyasa.adi(converter.get(adi, adi))

    # 8.4.54 the consonant becomes deaspirated
    abhyasa = abhyasa.adi(abhyasa.adi().deaspirate().value)

    new_state = state.swap(i, abhyasa)
    yield new_state


def lit_abhyasta(state):
    """

    :param state: some State
    """

    i, dhatu = state.find('dhatu')

    # 6.1.1 ekAco dve prathamasya
    # TODO: other rules
    abhyasa = Term(dhatu.value)

    # 6.1.4 pUrvo 'bhyAsaH
    # 6.1.5 ubhe abhyastam
    abhyasa = abhyasa.add_samjna('abhyasa').add_samjna('abhyasta')
    dhatu = dhatu.add_samjna('abhyasta')

    new_state = state.swap(i, dhatu).insert(i, abhyasa)

    return clean_abhyasa(new_state)
