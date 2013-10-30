# -*- coding: utf-8 -*-
"""
    vyakarana.atidesha
    ~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

import filters as F
from templates import *


@atidesha(None, F.lakshana('li~w') & ~F.samyoga & ~F.samjna('pit'))
def asamyogat_lit_kit():
    return [
        ('1.2.4',
            None, None, None,
            'kit')
    ]
