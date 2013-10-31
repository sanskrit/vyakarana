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
from templates import tasya, state, Va, Vibhasha, Anyatarasyam


# asiddhavat (6.4.22 - 6.4.175)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The effects of an asiddhavat rule are hidden from all other asiddhavat
# rules. Asiddhavat rules are identified with the `locus` argument. By
# convention, functions that define asiddhavat rules start with
# `asiddhavat`.

@tasya(None, 'anga', None, locus='asiddhavat')
def asiddhavat_angasya_nalopa():
    return [
        # ('6.4.23',
        #     None, 'Snam', None,
        #     shnam_na_lopa),
        ('6.4.24',
            None, ~F.samjna('idit') & F.al('hal') & F.upadha('Yam'), ('kit', 'Nit'),
            O.upadha(''))
    ]


@tasya(None, 'anga', 'ardhadhatuka', locus='asiddhavat')
def asiddhavat_angasya_ardhadhatuke():
    return []
    return [
        # TODO: anyatarasyam
        ('6.4.47',
            None, 'Bra\sja~^', None,
            _47),
        ('6.4.48',
            None, 'a', None,
            F.lopa),
        ('6.4.49',
            'hal', F.antya('ya'), None,
            None),
        # TODO: vibhasha
        ('6.4.50',
            True, F.antya('kya'), None,
            None),
    ]


# @tasya(None, 'anga', F.adi('ac'), locus='asiddhavat')
def asiddhavat_angasya_aci():
    return [
        ('6.4.77',
            None, ('Snu', 'dhatu', 'BrU'), None,
            'y'),
            # TODO
            #O.replace(Sounds('i u'), ('iyaN', 'uvaN'))),
        ('6.4.78',
            None, 'abhyasa', F.asavarna,
            True),
        ('6.4.79',
            None, 'strI', None,
            True),
        # TODO: va
        ('6.4.80',
            None, True, ('am', 'Sas'),
            True),
        # TODO: nitya
        ('6.4.81',
            None, 'i\R', None,
            Sounds('yaR')),
        ('6.4.82',
            None, F.al('i') & ~F.ekac & ~F.samyogapurva, None,
            True),
        ('6.4.83',
            None, F.al('u') & ~F.ekac & ~F.samyogapurva, 'sup',
            True),
        ('6.4.87',
            None, 'hu\\', 'sarvadhatuka',
            True),
        ('6.4.88',
            None, 'BU', ('luN', 'liw'),
            'vuk'),
        ('6.4.89',
            None, 'goh', None,
            O.upadha('Ut')),
    ]


@state('abhyasa', 'anga', ('li~w', 'kit'))
def asiddhavat_angasya_abhyasa_lopa_liti():
    def _120(state, i):
        abhyasa = state[i]
        anga = state[i + 1]

    def et_abhyasa_lopa(state, i):
        pass

    return [
        # ('6.4.120',
        #     None, _120, None
        #     et_abhyasa_lopa),
        # ('6.4.121',
        #     ),
        # ('6.4.122',
        #     ),
        # ('6.4.123',
        #     ),
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

    # liti = 'li~w' in p.lakshana
    # # e.g. 'pac', 'man', 'ram', but not 'syand', 'grah'
    # at_ekahal_madhya = (anga.upadha().value == 'a' and len(anga.value) == 3)
    # # e.g. 'pac' (pa-pac), 'ram' (ra-ram), but not 'gam' (ja-gam)
    # anadesha_adi = (abhyasa.value[0] == anga.value[0])

    # if liti:
    #     # 'kGiti' is inherited from 6.4.98.
    #     kniti = 'kit' in p.it or 'Nit' in p.it

    #     # 6.4.121 thali ca seTi
    #     thali_seti = p.value == 'iTa'

    #     # This substitution is valid only in these two conditions.
    #     if not (kniti or thali_seti):
    #         return

    #     # 6.4.120 ata ekahalmadhye 'nAdezAder liTi
    #     if at_ekahal_madhya and anadesha_adi:
    #         status = True

    #     # 6.4.126 na zasadadavAdiguNAnAm
    #     vadi = anga.adi == 'v'
    #     if anga.raw in ('Sasu~', 'dada~\\') or vadi or 'guna' in anga.samjna:
    #         status = False

    #     # 6.4.122 tRRphalabhajatrapaz ca
    #     if anga.raw in ('tF', 'YiPalA~', 'Ba\ja~\\', 'trapU~\z'):
    #         status = True

    #     # 6.4.123 rAdho hiMsAyAm
    #     elif anga.value == 'rAD':
    #         status = 'optional'

    #     # 6.4.124 vA jRRbhramutrasAm
    #     elif anga.raw in ('jF', 'Bramu~', 'trasI~'):
    #         status = 'optional'

    #     # 6.4.125 phaNAM ca saptAnAm
    #     elif anga.raw in DP.dhatu_set('PaRa~', 'svana~'):
    #         status = 'optional'

    # if status in (True, 'optional'):
    #     yield state.swap(i, abhyasa.lopa()).swap(j, anga.al_tasya('a', 'et'))

    # if status in (False, 'optional'):
    #     yield state


@tasya('anga', None, None)
def angasya_pratyaya_adesha():
    return [
        ('7.1.4',
            None, None, None,
            O.replace('J', 'ant')),
        ('7.1.5',
            'abhyasta', None, None,
            O.replace('J', 'at')),
        ('7.1.5',
            ~F.al('at'), 'atmanepada', None,
            True)
    ]


@tasya('At', F.samjna('anga') & F.lakshana('Ral'))
def ata_au_nalah():
    return [
        ('7.1.34',
            None, None, None,
            'O')
    ]


@tasya('anga', 'sarvadhatuka')
def angasya_sarvadhatuke_at():
    return [
        ('7.2.81',
            'at', F.adi('At') & F.samjna('Nit'),
            O.adi('iy')
            )
    ]


@tasya(None, 'anga', None)
def angasya_vrddhi():
    return [
        ('7.2.114',
            None, 'mfjU~', None,
            O.vrddhi),
        ('7.2.115',
            None, 'ac', ('Yit', 'Rit'),
            True),
        ('7.2.116',
            None, F.upadha('at'), True,
            True),
    ]


@tasya(None, 'anga', None)
def angasya_ku():
    return [
        ('7.3.52',
            None, F.al('c j'), ('Git', 'Ryat'),
            Sounds('ku')),
        ('7.3.54',
            None, 'ha\\na~', ('Yit', 'Rit', F.adi('n')),
            O.al_tasya('h', 'ku')),
        ('7.3.55',
            'abhyasa', True, None,
            True),
        ('7.3.56',
            True, 'hi\\', ~F.samjna('caN'),
            True),
        ('7.3.57',
            True, 'ji\\', ('san', 'li~w'),
            O.al_tasya('j', 'ku')),
        # TODO: vibhasha
        ('7.3.58',
            True, 'ci\\Y', True,
            O.al_tasya('c', 'ku')),
    ]


@tasya(None, 'anga', 'Syan')
def angasya_shyani():
    return [
        ('7.3.74',
            None, F.gana('Samu~', 'madI~'), None,
            O.dirgha)
    ]


@tasya(None, 'anga', F.Sit_adi)
def angasya_shiti():
    _78_roots = ['pA\\', 'GrA\\', 'DmA\\', 'zWA\\', 'mnA\\', 'dA\R',
                 'df\Si~r', 'f\\', 'sf\\', 'Sa\dx~', 'za\dx~']
    _78_stems = ['piba', 'jiGra', 'Dama', 'tizWa', 'mana', 'yacCa', 'paSya',
                 'fcCa', 'DO', 'SIya', 'sIda']

    return [
        ('7.3.75',
            None, ('zWivu~', 'klamu~'), None,
            O.dirgha),
        ('7.3.76',
            None, F.raw('kramu~') & F.samjna('parasmaipada'), None,
            True),
        ('7.3.77',
            None, ('izu~', 'ga\mx~', 'ya\ma~'), None,
            'C'),
        ('7.3.78',
            None, set(_78_roots), None,
            O.yathasamkhya(_78_roots, _78_stems)),
        ('7.3.79',
            None, ('jYA\\', 'janI~\\'), None,
            'jA'),
        ('7.3.80',
            None, F.gana('pUY', 'plI\\'), None,
            O.hrasva),
        ('7.3.82',
            None, 'YimidA~', None,
            O.force_guna),
    ]


@tasya(None, 'anga', None)
def angasya_guna():

    @F.unparameterized
    def puganta_laghupadha(term, *args):
        # TODO: puganta
        return term and term.upadha in Sounds('at it ut ft xt')

    sarva_ardha = ('sarvadhatuka', 'ardhadhatuka')

    return [
        ('7.3.83',
            None, None, 'jus',
            O.guna),
        ('7.3.84',
            None, F.al('ik'), sarva_ardha,
            True),
        ('7.3.85',
            None, 'jAgf', ~F.samjna('vi', 'ciR', 'Ral', 'Nit'),
            True),
        ('7.3.86',
            None, puganta_laghupadha & F.upadha('ik'), sarva_ardha,
            True),
    ]


@tasya(None, 'anga', 'sarvadhatuka')
def angasya_sarvadhatuke():
    return [
        ('7.3.101',
            None, 'at', F.adi('yaY'),
            O.dirgha)
    ]


@tasya(None, 'anga', 'li~w')
def angasya_liti():
    return [
        ('7.4.10',
            None, F.samyogadi & F.adi('ft'), None,
            O.force_guna),
        ('7.4.11',
            None, F.raw('f\\') | F.al('Ft'), None,
            True),
        # TODO: va,
        ('7.4.12',
            None, ('SF', 'dF', 'pF'), None,
            Va(O.hrasva))
    ]


@tasya(None, 'abhyasa', None)
def angasya_abhyasasya():
    ac = Sounds('ac')
    shar = Sounds('Sar')
    khay = Sounds('Kay')

    def _60_61(state, index):
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

        return state.swap(index, cur.set_value(first_hal + first_ac))

    return [
        ('7.4.59',
            None, None, None,
            O.hrasva),
        ('7.4.60',
            None, None, None,
            _60_61),
        ('7.4.61',
            None, None, None,
            True),
        ('7.4.62',
            None, None, None,
            O.al_tasya('ku h', 'cu')),
        ('7.4.66',
            None, None, None,
            O.al_tasya('f', 'at')),
        ('7.4.69',
            None, 'i\\R', 'kit',
            O.dirgha),
        ('7.4.70',
            None, F.adi('at'), None,
            True),
        ('7.4.73',
            None, 'BU', None,
            'a'),
    ]
