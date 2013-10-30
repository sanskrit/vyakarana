# -*- coding: utf-8 -*-
"""
    vyakarana.atidesha
    ~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

import filters as F
from templates import *


@atidesha(None, F.samjna('sarvadhatuka') & ~F.samjna('pit'))
def Nit_atidesha():
    return [
        ('1.2.4',
            None, None,
            'Nit')
    ]


@atidesha('dhatu', F.lakshana('li~w'))
def kit_atidesha():
    return [
        ('1.2.5',
            None,  ~F.samyoga & ~F.samjna('pit'),
            'kit'),
        ('1.2.6',
            ('YiinDI~\\', 'BU'), None,
            True)
    ]
