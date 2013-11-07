# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya7.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *

f = F.auto


@inherit('anga', 'pratyaya', None)
def angasya_pratyaya_adesha():
    return [
        ('7.1.3', None, None, None, O.replace('J', 'ant')),
        ('7.1.4', 'abhyasta', None, None, O.replace('J', 'at')),
        ('7.1.5', ~F.al('at'), 'atmanepada', None, True)
    ]


@inherit(f('At') & F.samjna('anga'), F.raw('Ral'), None)
def ata_au_nalah():
    return [
        ('7.1.34', None, None, None, 'O')
    ]


@inherit(None, None, None)
def nal_uttamo_va():
    return [
        Va('7.1.91', None, f('Ral') & f('uttama'), None, 'Rit')
    ]
