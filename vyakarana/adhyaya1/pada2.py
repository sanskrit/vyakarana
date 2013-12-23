# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya1.pada2
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


RULES = [
    Anuvrtti(None, None, None),
    ('1.2.4', None, f('sarvadhatuka') & ~f('pit'), None, 'Nit'),
    ('1.2.5', ~F.samyoga, ~f('pit') & f('li~w'), None, 'kit'),
    Ca('1.2.6', f('YiinDI~\\', 'BU'), f('li~w'), None, True),
]
