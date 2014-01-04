# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya6.pada1
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Ashtadhyayi 6.1.

    :license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..dhatupatha import DHATUPATHA as DP
from ..sounds import Sounds
from ..templates import *
from ..terms import Upadesha

f = F.auto

#: 6.1.15
VACI_SVAPI = f(*['va\ca~', 'Yizva\pa~'] + DP.dhatu_list('ya\\ja~^'))

#: 6.1.16
GRAHI_JYA = f(*['graha~^', 'jyA\\', 'vaya~\\', 'vya\Da~', 'vaSa~',
             'vyaca~', 'o~vraScU~', 'pra\cCa~', 'Bra\sja~^'])


@O.Operator.no_params
def do_dvirvacana(state, i, locus=None):
    # 6.1.1 ekAco dve prathamasya
    # 6.1.2 ajAder dvitIyasya
    # 6.1.3 na ndrAH saMyogAdayaH
    # 6.1.4 pUrvo 'bhyAsaH
    # 6.1.5 ubhe abhyastam
    cur = state[i]
    abhyasa = Upadesha(data=cur.data, samjna=frozenset(['abhyasa']))
    abhyasta = cur.add_samjna('abhyasta')
    return state.swap(i, abhyasta).insert(i, abhyasa)


@O.DataOperator.no_params
def sa_adesha(value):
    if value.startswith('z'):
        converter = {'w': 't', 'W': 'T', 'R': 'n'}
        v = value[1]
        value = 's' + converter.get(v, v) + value[2:]
    return value

@O.DataOperator.no_params
def na_adesha(value):
    if value.startswith('R'):
        value = 'n' + value[1:]
    return value


@F.TermFilter.no_params
def ec_upadesha(term):
    clean = term.clean
    return clean and clean[-1] in Sounds('ec')


RULES = [
    Anuvrtti(None, 'dhatu', None),
    # TODO: why stated as abhyasa?
    ('6.1.8', None, ~f('abhyasta'), 'li~w', do_dvirvacana),
    ('6.1.9', None, True, f('san', 'yaN'), True),
    ('6.1.10', None, True, F.lakshana('Slu~'), True),
    ('6.1.11', None, True, 'caN', True),

    Anuvrtti(None, None, None),
    ('6.1.15', None, VACI_SVAPI, 'kit', O.samprasarana),
    Ca('6.1.16', None, GRAHI_JYA, F.knit, True),
    ('6.1.17', None, 'abhyasa', VACI_SVAPI | GRAHI_JYA, True),

    Anuvrtti(None, None, None),
    ('6.1.45', None, f('dhatu') & ec_upadesha, f('tin') & ~F.Sit_adi, O.tasya('A')),
    ('6.1.64', None, f('dhatu') & F.adi('z'), None, sa_adesha),
    ('6.1.65', None, f('dhatu') & F.adi('R'), None, na_adesha),
]
