# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada2
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..upadesha import Upadesha as U, Pratyaya

f = F.auto
it_ashtadhyayi = None
TAS = Pratyaya('tAsi~').add_samjna('ardhadhatuka')


@O.Operator.no_params
def tasvat(state, index, **kw):
    global it_ashtadhyayi
    if it_ashtadhyayi is None:
        from ..ashtadhyayi import Ashtadhyayi
        it_ashtadhyayi = Ashtadhyayi.with_rules_in('7.2.8', '7.2.78')

    print state
    import sys; sys.exit()


titutra = f('ti', 'tu', 'tra', 'ta', 'Ta', 'si', 'su', 'sara', 'ka', 'sa')
kr_sr_bhr = F.value('kf', 'sf', 'Bf', 'vf', 'stu', 'dru', 'sru', 'Sru')
svarati_suti = f('svf', 'zUG', 'zUN', 'DUY', 'Udit')


RULES = [
    Anuvrtti('anga', None, None),
    Na('7.2.8', None, None, f('krt') & F.adi('vaS'), O.tasya(U('iw'))),
    Ca('7.2.9', None, f('krt') & titutra, None, True),
    Na('7.2.13', kr_sr_bhr, f('li~w'), None, True),
    ('7.2.35', None, f('ardhadhatuka') & F.adi('val'), None, True),
    Va('7.2.44', svarati_suti, True, None, True),
    # ('7.2.61', 'ac', True, None, True),

    Anuvrtti('anga', 'sarvadhatuka', None),
    ('7.2.81', 'at', F.adi('At') & F.samjna('Nit'), None, O.adi('iy')),

    Anuvrtti(None, 'anga', None),
    ('7.2.114', None, 'mfjU~', None, O.vrddhi),
    ('7.2.115', None, 'ac', f('Yit', 'Rit'), True),
    # This should really apply `O.vrddhi`, but by 1.1.3 it's tricky.
    # Since this is a one-off, apply a fuction with the same effect:
    ('7.2.116', None, F.upadha('at'), True, O.upadha('A')),
]
