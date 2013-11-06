# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada3
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..sounds import Sounds
from ..templates import *

f = F.auto


@inherit(None, 'anga', None)
def angasya_ku():
    return [
        ('7.3.52', None, F.al('c j'), f('Git', 'Ryat'), Sounds('ku')),
        ('7.3.54', None, 'ha\\na~', f('Yit', 'Rit', F.adi('n')), O.al_tasya('h', 'ku')),
        ('7.3.55', 'abhyasa', True, None, True),
        ('7.3.56', True, 'hi\\', ~F.samjna('caN'), True),
        ('7.3.57', True, 'ji\\', f('san', 'li~w'), O.al_tasya('j', 'ku')),
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
        ('7.3.75', None, f('zWivu~', 'klamu~'), None, O.dirgha),
        ('7.3.76', None, F.raw('kramu~') & F.samjna('parasmaipada'), None, True),
        ('7.3.77', None, f('izu~', 'ga\mx~', 'ya\ma~'), None, 'C'),
        ('7.3.78', None, f(*_78_roots), None, O.yathasamkhya(_78_roots, _78_stems)),
        ('7.3.79', None, f('jYA\\', 'janI~\\'), None, 'jA'),
        ('7.3.80', None, F.gana('pUY', 'plI\\'), None, O.hrasva),
        ('7.3.82', None, 'YimidA~', None, O.force_guna),
    ]


@inherit(None, 'anga', None)
def angasya_guna():

    @F.TermFilter.unparameterized
    def puganta_laghupadha(term):
        # TODO: puganta
        return term.upadha in Sounds('at it ut ft xt')

    sarva_ardha = f('sarvadhatuka', 'ardhadhatuka')

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
