# -*- coding: utf-8 -*-
"""
    vyakarana.adhyaya3.pada4
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""

import itertools

from .. import filters as F, operators as O, util
from ..lists import PADA, PURUSHA, VACANA, VIBHAKTI, TIN, LA
from ..sounds import Sounds
from ..templates import *


f = F.auto


def label_by_triplet(terms, labels):
    """
    Apply a single label to each triplet of terms.

    :param terms: a list of sets
    :param labels: a list of strings
    """
    num_labels = len(labels)
    for i, chunk in enumerate(util.iter_group(terms, 3)):
        for term in chunk:
            term.add(labels[i % num_labels])


def label_by_item(terms, labels):
    """
    Label each term with a corresponding label.

    Suppose there are 4 terms and 2 labels. Then::

        term[0] -> label[0]
        term[1] -> label[1]
        term[2] -> label[0]
        term[3] -> label[1]

    :param terms: a list of sets
    :param labels: a list of strings
    """
    labels = itertools.cycle(labels)
    for term in terms:
        term.add(next(labels))


def label_by_group(terms, labels):
    """
    Split `terms` into `len(labels)` groups and mark each group accordingly.

    Suppose there are 4 terms and 2 labels. Then::

        term[0] -> label[0]
        term[1] -> label[0]
        term[2] -> label[1]
        term[3] -> label[1]

    :param terms: a list of sets
    :param labels: a list of strings
    """
    num_groups = len(terms) / len(labels)
    for i, group in enumerate(util.iter_group(terms, num_groups)):
        for term in group:
            term.add(labels[i])


def tin_key(samjna, pada=None):
    if pada:
        x = pada
    else:
        for x in PADA:
            if x in samjna:
                break
    for y in PURUSHA:
        if y in samjna:
            break
    for z in VACANA:
        if z in samjna:
            break

    return x, y, z


base_samjna = [set(['tin']) for s in TIN]

# 1.4.99 laH parasmaipadam
# 1.4.100 taGAnAv Atmanepadam
label_by_group(base_samjna, PADA)

# 1.4.101 tiGas trINi trINi prathamamadhyamottamAH
label_by_triplet(base_samjna, PURUSHA)

# 1.4.102 tAnyekavacananadvivacanabahuvacanAnyekazaH
label_by_item(base_samjna, VACANA)

key2index = {tin_key(x): i for i, x in enumerate(base_samjna)}

BASE_TIN = 'tip tas Ji sip Tas Ta mip vas mas'.split()
LIT_TIN = 'Ral atus us Tal aTus a Ral va ma'.split()


@O.Operator.no_params
def tin_adesha(state, index, locus=None):
    """tiṅ ādeśa"""
    la = state[index]
    la_type = la.raw
    # TODO: remove hacks
    dhatuka = 'ardhadhatuka' if la_type == 'li~w' else 'sarvadhatuka'
    i = key2index[tin_key(la.samjna)]
    new_raw = TIN[i]
    tin = la.set_raw(new_raw).add_samjna('tin', dhatuka)
    return state.swap(index, tin)


RULES = [
    Anuvrtti(None, None, None),
    ('3.4.78', None, F.raw(*LA), None, tin_adesha),
    ('3.4.79', None, f('atmanepada') & f('wit'), None, O.ti('e')),
    ('3.4.80',
        None, f('atmanepada') & f('wit') & F.raw('TAs'), None,
        'se'),
    ('3.4.81',
        None, f('atmanepada') & F.raw('ta', 'Ja') & f('li~w'), None,
        O.yathasamkhya(['ta', 'Ja'], ['eS', 'irec'])),
    ('3.4.82',
        None, F.raw(*BASE_TIN) & f('parasmaipada') & f('li~w'), None,
        O.yathasamkhya(BASE_TIN, LIT_TIN)),
]
