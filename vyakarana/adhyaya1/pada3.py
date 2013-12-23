# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1.pada3
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..dhatupatha import DHATUPATHA as DP

f = F.auto


RULES = [
    Anuvrtti(None, None, None),
    ('1.3.1', None, F.raw(*DP.all_dhatu), None, 'dhatu'),

    # Strictly speaking, the rules below are distortions of the actual
    # rules in the Ashtadhyayi. The terms "parasamipada" and "atmanepada"
    # refer to the *replacements* of the "la" affixes, not to the "la"
    # affixes themselves.
    Anuvrtti('dhatu', None, None),
    ('1.3.12', f('anudattet', 'Nit'), None, None, 'atmanepada'),
    Artha('1.3.72', f('svaritet', 'Yit'), None, None, True),
    # TODO: infer by anuvrtti
    Artha('1.3.76', 'jYA\\', None, None, True),
    ('1.3.78', Shesha, None, None, 'parasmaipada'),
]
