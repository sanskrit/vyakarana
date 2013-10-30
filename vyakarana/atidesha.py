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
        ('1.2.3',
            None, None,
            'Nit')
    ]


@atidesha(None, F.lakshana('li~w') & ~F.samyoga & ~F.samjna('pit'))
def kit_atidesha():
    return [
        ('1.2.4',
            None, None,
            'kit')
    ]
