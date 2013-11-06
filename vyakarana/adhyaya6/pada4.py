# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya6.pada4
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Ashtadhyayi 6.4

    The chapter starts with an adhikāra aṅga:

        6.4.1 aṅgasya

    which lasts until the end of 7.4.

    Some of the rules contained in this section apply in filters where
    only a dhātu would make sense. But since a dhātu is a type of aṅga,
    there's no harm in matching on an aṅga generally.

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..sounds import Sounds
from ..upadesha import Upadesha

f = F.auto

# asiddhavat (6.4.22 - 6.4.175)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The effects of an asiddhavat rule are hidden from all other asiddhavat
# rules. Asiddhavat rules are identified with the `locus` argument. By
# convention, functions that define asiddhavat rules start with
# `asiddhavat`.

@inherit(None, 'anga', None, locus='asiddhavat')
def nalopa():
    @O.DataOperator.unparameterized
    def shnam_na_lopa(value):
        ac = Sounds('ac')
        nasal = Sounds('Yam')
        letters = list(reversed(value))
        for i, L in enumerate(letters):
            if L in ac:
                break
            if L in nasal:
                letters[i] = ''
                break
        return ''.join(reversed(letters))

    return [
        ('6.4.23',
            None, F.part('Snam'), None,
            shnam_na_lopa),
        ('6.4.24', None, ~F.samjna('idit') & F.al('hal') & F.upadha('Yam'), ('kit', 'Nit'), O.upadha(''))
    ]


@inherit(None, 'anga', 'ardhadhatuka', locus='asiddhavat')
def ardhadhatuke():
    return []
    return [
        Anyatarasyam('6.4.47', None, 'Bra\sja~^', None, _47),
        ('6.4.48', None, 'a', None, F.lopa),
        ('6.4.49', 'hal', F.antya('ya'), None, None),
        Vibhasha('6.4.50', True, F.antya('kya'), None, None),
    ]


@inherit(None, 'anga', F.adi('ac'), locus='asiddhavat')
def aci():

    @O.Operator.unparameterized
    def _6_4_77(state, index, locus):
        cur = state[index]
        if cur.antya in 'iI':
            return state.swap(index, cur.tasya(Upadesha('iya~N'), locus=locus))
        else:
            return state.swap(index, cur.tasya(Upadesha('uva~N'), locus=locus))

    gama_hana = ('ga\\mx~', 'ha\\na~', 'janI~\\', 'Kanu~^', 'Gasx~')

    snu_dhatu_yvor = f(('Snu', 'dhatu', 'BrU')) & F.al('i u')

    return [
        ('6.4.77', None, snu_dhatu_yvor, None, _6_4_77),
        ('6.4.78', None, 'abhyasa', F.asavarna, True),
        ('6.4.79', None, 'strI', None, True),
        Va('6.4.80', None, True, ('am', 'Sas'), True),
        ('6.4.81', None, 'i\R', None, Sounds('yaR')),
        ('6.4.82', None, F.al('i') & ~F.ekac & ~F.samyogapurva, None, True),
        ('6.4.83', None, F.al('u') & ~F.ekac & ~F.samyogapurva, 'sup', True),
        ('6.4.87', None, 'hu\\', 'sarvadhatuka', True),
        ('6.4.88', None, 'BU', ('luN', 'liw'), 'vuk'),
        ('6.4.89', None, F.value('goh'), None, O.upadha('U')),
        ('6.4.98', None, gama_hana, F.knit & ~F.raw('aN'), O.upadha(''))
    ]


@inherit(None, 'anga', F.knit & f('sarvadhatuka'), locus='asiddhavat')
def kniti_sarvadhatuke():

    @O.DataOperator.unparameterized
    def allopa(value):
        letters = list(reversed(value))
        for i, L in enumerate(letters):
            if L == 'a':
                letters[i] = ''
                break

        return ''.join(reversed(letters))

    return [
        ('6.4.111',
            None, F.part('Snam'), None,
            allopa),
    ]


@inherit('abhyasa', 'anga', 'li~w', locus='asiddhavat')
def abhyasa_lopa_liti():

    @F.Filter.unparameterized
    def at_ekahalmadhya_anadeshadi(state, index):
        abhyasa = state[index - 1]
        anga = state[index]
        try:
            a, b, c = anga.value
            hal = Sounds('hal')
            # Anga has the pattern CVC, where C is a consonant and V
            # is a vowel.
            eka_hal_madhya = a in hal and b == 'a' and c in hal
            # Abhyasa and anga have the same initial letter. I'm not
            # sure how to account for 8.4.54 in the normal way, so as
            # a hack, I check for the consonants that 8.4.54 would
            # modify.
            _8_4_54 = anga.adi not in Sounds('Jaz')
            anadeshadi = abhyasa.adi == anga.adi and _8_4_54

            return eka_hal_madhya and anadeshadi
        except ValueError:
            return False

    @O.Operator.unparameterized
    def et_abhyasa_lopa(state, i, locus):
        abhyasa = state[i - 1].set_asiddhavat('')
        ed_adesha = O.replace('a', 'e')

        abhyasta = state[i]
        abhyasta_value = ed_adesha.body(abhyasta.value)
        abhyasta = abhyasta.set_asiddhavat(abhyasta_value)
        return state.swap(i - 1, abhyasa).swap(i, abhyasta)

    return [
        ('6.4.120', None, at_ekahalmadhya_anadeshadi, 'kit', et_abhyasa_lopa),
        Ca('6.4.121', None, True, F.value('iTa'), True),
        Ca('6.4.122', None, ('tF', 'YiPalA~', 'Ba\ja~^', 'trapU~\z'), F.samjna('kit') | F.value('iTa'), True),
        Artha('6.4.123', None, F.value('rAD'), True, True),
        # # TODO: va
        # ('6.4.124',
        #     ),
        # # TODO: va
        # ('6.4.125',
        #     ),
        # # TODO: na
        # ('6.4.126',
        #     ),
    ]

    #     # 6.4.126 na zasadadavAdiguNAnAm
    #     vadi = anga.adi == 'v'
    #     if anga.raw in ('Sasu~', 'dada~\\') or vadi or 'guna' in anga.samjna:
    #         status = False

    #     # 6.4.123 rAdho hiMsAyAm
    #     elif anga.value == 'rAD':
    #         status = 'optional'

    #     # 6.4.124 vA jRRbhramutrasAm
    #     elif anga.raw in ('jF', 'Bramu~', 'trasI~'):
    #         status = 'optional'

    #     # 6.4.125 phaNAM ca saptAnAm
    #     elif anga.raw in DP.dhatu_set('PaRa~', 'svana~'):
    #         status = 'optional'
