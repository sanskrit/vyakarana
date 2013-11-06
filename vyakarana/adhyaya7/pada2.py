# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada2
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..upadesha import Upadesha as U

f = F.auto

@inherit('anga', None, None)
def it():

    titutra = f('ti', 'tu', 'tra', 'ta', 'Ta', 'si', 'su', 'sara', 'ka', 'sa')
    kr_sr_bhr = f('kf', 'sf', 'Bf', 'vf', 'zwu', 'dru', 'sru', 'Sru')

    return [
        Na('7.2.13', kr_sr_bhr, f('li~w'), None, U('iw')),
        ('7.2.35', None, f('ardhadhatuka') & F.adi('val'), None, U('iw')),
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
        ('7.2.115', None, 'ac', f('Yit', 'Rit'), True),

        # This should really apply `O.vrddhi`, but by 1.1.3 it's tricky.
        # Since this is a one-off, apply a fuction with the same effect:
        ('7.2.116', None, F.upadha('at'), True, O.upadha('A')),
    ]
