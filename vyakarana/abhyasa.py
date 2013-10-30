# -*- coding: utf-8 -*-
"""
    vyakarana.abhyasa
    ~~~~~~~~~~~~~~~~~

    Rules that apply specifically to an abhyāsa. These rules fall into
    two groups. The first is at the beginning of 6.1:

        6.1.1 ekAco dve prathamasya

    The second is from 7.4.58 to the end of book 7:

        7.4.58 atra lopo 'bhyAsasya

    :license: MIT and BSD
"""


import filters as F
import operators as O
from sounds import Sounds
from templates import state
from upadesha import Upadesha


@state('dhatu', None)
def dvirvacana():
    def do_dvirvacana(state, i):
        # 6.1.1 ekAco dve prathamasya
        # 6.1.2 ajAder dvitIyasya
        # 6.1.3 na ndrAH saMyogAdayaH
        # 6.1.4 pUrvo 'bhyAsaH
        # 6.1.5 ubhe abhyastam
        cur = state[i]
        abhyasa = Upadesha(data=cur.data, samjna=frozenset(['abhyasa']))
        abhyasta = cur.add_samjna('abhyasta')
        yield state.swap(i, abhyasta).insert(i, abhyasa)

    return [
        # TODO: why stated as abhyasa?
        ('6.1.8',
            ~F.samjna('abhyasta'), 'li~w',
        do_dvirvacana),
        ('6.1.9',
            True, ('san', 'yaN'),
        True),
        ('6.1.10',
            True, 'Slu~',
        True),
        ('6.1.11',
            True, 'caN',
        True),
    ]
