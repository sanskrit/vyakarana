# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya2.pada4
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


RULES = [
    Anuvrtti(None, F.raw('Sap'), None),
    ('2.4.71', F.gana('a\da~'), None, None, 'lu~k'),
    ('2.4.74', F.gana('hu\\'), None, None, 'Slu~'),
]
