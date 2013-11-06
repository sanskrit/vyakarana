# -*- coding: utf-8 -*-
"""
    vyakarana.anga
    ~~~~~~~~~~~~~~

    Rules that apply specifically to an aṅga. Almost all such rules are
    within the domain of 6.4.1:

        6.4.1 aṅgasya

    which holds from the beginning of 6.4 to the end of 7.4.

    Some of the rules contained in this section apply in filters where
    only a dhātu would make sense. But since a dhātu is a type of aṅga,
    there's no harm in matching on an aṅga generally.

    :license: MIT and BSD
"""

import filters as F
import operators as O
from sounds import Sounds
from upadesha import Upadesha
from templates import *

f = F.auto

# asiddhavat (6.4.22 - 6.4.175)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The effects of an asiddhavat rule are hidden from all other asiddhavat
# rules. Asiddhavat rules are identified with the `locus` argument. By
# convention, functions that define asiddhavat rules start with
# `asiddhavat`.

@inherit(None, 'anga', None, locus='asiddhavat')
def asiddhavat_angasya_nalopa():
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
def asiddhavat_angasya_ardhadhatuke():
    return []
    return [
        Anyatarasyam('6.4.47', None, 'Bra\sja~^', None, _47),
        ('6.4.48', None, 'a', None, F.lopa),
        ('6.4.49', 'hal', F.antya('ya'), None, None),
        Vibhasha('6.4.50', True, F.antya('kya'), None, None),
    ]


@inherit(None, 'anga', F.adi('ac'), locus='asiddhavat')
def asiddhavat_angasya_aci():

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
def asiddhavat_angasya_kniti_sarvadhatuke():

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
def asiddhavat_angasya_abhyasa_lopa_liti():

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


@inherit('anga', 'pratyaya', None)
def angasya_pratyaya_adesha():
    return [
        ('7.1.3', None, None, None, O.replace('J', 'ant')),
        ('7.1.4', 'abhyasta', None, None, O.replace('J', 'at')),
        ('7.1.5', ~F.al('at'), 'atmanepada', None, True)
    ]


@inherit(f('At') & F.samjna('anga'), F.raw('Ral'), None)
def ata_au_nalah():
    return [
        ('7.1.34', None, None, None, 'O')
    ]


@inherit('anga', 'sarvadhatuka', None)
def angasya_sarvadhatuke_at():
    return [
        ('7.2.81', 'at', F.adi('At') & F.samjna('Nit'), None, O.adi('iy'))
    ]


@inherit(None, 'anga', None)
def angasya_vrddhi():
    return [
        ('7.2.114', None, 'mfjU~', None, O.vrddhi),
        ('7.2.115', None, 'ac', ('Yit', 'Rit'), True),

        # This should really apply `O.vrddhi`, but by 1.1.3 it's tricky.
        # Since this is a one-off, apply a fuction with the same effect:
        ('7.2.116', None, F.upadha('at'), True, O.upadha('A')),
    ]


@inherit(None, 'anga', None)
def angasya_ku():
    return [
        ('7.3.52', None, F.al('c j'), ('Git', 'Ryat'), Sounds('ku')),
        ('7.3.54', None, 'ha\\na~', ('Yit', 'Rit', F.adi('n')), O.al_tasya('h', 'ku')),
        ('7.3.55', 'abhyasa', True, None, True),
        ('7.3.56', True, 'hi\\', ~F.samjna('caN'), True),
        ('7.3.57', True, 'ji\\', ('san', 'li~w'), O.al_tasya('j', 'ku')),
        # TODO: vibhasha
        ('7.3.58', True, 'ci\\Y', True, O.al_tasya('c', 'ku')),
    ]


@inherit(None, 'anga', F.raw('Syan'))
def angasya_shyani():
    return [
        ('7.3.74', None, F.gana('Samu~', 'madI~'), None, O.dirgha)
    ]


@inherit(None, 'anga', F.Sit_adi)
def angasya_shiti():
    _78_roots = ['pA\\', 'GrA\\', 'DmA\\', 'zWA\\', 'mnA\\', 'dA\R',
                 'df\Si~r', 'f\\', 'sf\\', 'Sa\dx~', 'za\dx~']
    _78_stems = ['piba', 'jiGra', 'Dama', 'tizWa', 'mana', 'yacCa', 'paSya',
                 'fcCa', 'DO', 'SIya', 'sIda']

    return [
        ('7.3.75', None, ('zWivu~', 'klamu~'), None, O.dirgha),
        ('7.3.76', None, F.raw('kramu~') & F.samjna('parasmaipada'), None, True),
        ('7.3.77', None, ('izu~', 'ga\mx~', 'ya\ma~'), None, 'C'),
        ('7.3.78', None, set(_78_roots), None, O.yathasamkhya(_78_roots, _78_stems)),
        ('7.3.79', None, ('jYA\\', 'janI~\\'), None, 'jA'),
        ('7.3.80', None, F.gana('pUY', 'plI\\'), None, O.hrasva),
        ('7.3.82', None, 'YimidA~', None, O.force_guna),
    ]


@inherit(None, 'anga', None)
def angasya_guna():

    @F.TermFilter.unparameterized
    def puganta_laghupadha(term):
        # TODO: puganta
        return term.upadha in Sounds('at it ut ft xt')

    sarva_ardha = ('sarvadhatuka', 'ardhadhatuka')

    return [
        ('7.3.83', None, None, 'jus', O.guna),
        ('7.3.84', None, F.al('ik'), sarva_ardha, True),
        ('7.3.85', None, 'jAgf', ~F.samjna('vi', 'ciR', 'Ral', 'Nit'), True),
        ('7.3.86', None, puganta_laghupadha & F.upadha('ik'), sarva_ardha, True),
    ]


@inherit(None, 'anga', 'sarvadhatuka')
def angasya_sarvadhatuke():
    return [
        ('7.3.101', None, 'at', F.adi('yaY'), O.dirgha)
    ]


@inherit(None, 'anga', 'li~w')
def angasya_liti():
    return [
        ('7.4.10', None, F.samyogadi & F.adi('ft'), None, O.force_guna),
        ('7.4.11', None, F.raw('f\\') | F.al('Ft'), None, True),
        Va('7.4.12', None, ('SF', 'dF', 'pF'), None, O.hrasva)
    ]


@inherit(None, 'abhyasa', None)
def angasya_abhyasasya():
    ac = Sounds('ac')
    shar = Sounds('Sar')
    khay = Sounds('Kay')

    @O.Operator.unparameterized
    def _60_61(state, index, locus=None):
        cur = state[index]
        first_hal = first_ac = ''
        for i, L in enumerate(cur.value):
            if i == 1 and cur.value[0] in shar and L in khay:
                first_hal = L
            if L in ac:
                first_ac = L
                break
            elif not first_hal:
                first_hal = L

        new_value = first_hal + first_ac
        if new_value != cur.value:
            return state.swap(index, cur.set_value(new_value))
        else:
            return state

    return [
        ('7.4.59', None, None, None, O.hrasva),
        ('7.4.60', None, None, None, _60_61),
        ('7.4.61', None, F.adi('Sar'), None, True),
        ('7.4.62', None, None, None, O.al_tasya('ku h', 'cu')),
        ('7.4.66', None, None, None, O.al_tasya('f', 'at')),
        ('7.4.69', None, 'i\\R', 'kit', O.dirgha),
        ('7.4.70', None, F.adi('at'), None, True),
        ('7.4.73', None, None, 'BU', 'a'),
    ]
