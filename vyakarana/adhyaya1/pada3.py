# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1.pada3
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


@inherit('dhatu', None, None)
def pada3():
    """Apply the rules that select atmanepada and parasmaipada.

    Strictly speaking, the rules below are distortions of the actual
    rules in the Ashtadhyayi. The terms "parasamipada" and "atmanepada"
    refer to the *replacements* of the "la" affixes, not to the "la"
    affixes themselves.
    """

    return [
        ('1.3.12', f('anudattet', 'Nit'), None, None, 'atmanepada'),
        Artha('1.3.72', f('svaritet', 'Yit'), None, None, True),
        ('1.3.76', 'jYA\\', None, None, True),
        ('1.3.78', Shesha, None, None, 'parasmaipada'),
    ]
