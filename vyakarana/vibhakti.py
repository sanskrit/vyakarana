# -*- coding: utf-8 -*-
"""
    vyakarana.vibhakti
    ~~~~~~~~~~~~~~~~~~

    Rules that apply specifically to a vibhakti.

    :license: MIT and BSD
"""

import itertools

import filters as F
import operators as O
import dhatu as D
import util
from upadesha import Vibhakti as V
from templates import state, tasya


PADA = ['parasmaipada', 'atmanepada']
PURUSHA = ['prathama', 'madhyama', 'uttama']
VACANA = ['ekavacana', 'dvivacana', 'bahuvacana']
VIBHAKTI = ['prathama', 'dvitiya', 'trtiya', 'caturthi', 'pancami', 'sasthi',
            'saptami']


def label_by_triplet(terms, labels):
    """
    Apply a single label to each triplet of terms.

    :param terms: a list of Terms
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
        term[0] -> label[1]
        term[1] -> label[0]
        term[1] -> label[1]

    :param terms: a list of Terms
    :param terms: a list of strings
    """
    labels = itertools.cycle(labels)
    for term in terms:
        term.add(next(labels))


def label_by_group(terms, labels):
    """
    Split `terms` into `len(labels)` groups and mark each group accordingly.

    Suppose there are 4 terms and 2 labels. Then::

        term[0] -> label[0]
        term[0] -> label[0]
        term[1] -> label[1]
        term[1] -> label[1]

    :param terms: a list of Terms
    :param terms: a list of strings
    """
    num_groups = len(terms) /  len(labels)
    for i, group in enumerate(util.iter_group(terms, num_groups)):
        for term in group:
            term.add(labels[i])


@F.TermFilter.unparameterized
def f_lakara(term):
    return 'vibhakti' in term.samjna and term.raw[0] == 'l'
f_lakara.rank = F.FilterType.UPADESHA

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


@state('dhatu', f_lakara)
def lasya():
    """3.4.77 lasya"""

    base_tin = """tip tas Ji sip Tas Ta mip vas mas
                  ta AtAm Ja TAs ATAm Dvam iw vahi mahiG""".split()
    base_samjna = [set(['tin']) for s in base_tin]

    # 1.4.99 laH parasmaipadam
    # 1.4.100 taGAnAv Atmanepadam
    label_by_group(base_samjna, PADA)

    # 1.4.101 tiGas trINi trINi prathamamadhyamottamAH
    label_by_triplet(base_samjna, PURUSHA)

    # 1.4.102 tAnyekavacananadvivacanabahuvacanAnyekazaH
    label_by_item(base_samjna, VACANA)

    key2index = {tin_key(x): i for i, x in enumerate(base_samjna)}

    def tin_adesha(state, index, locus=None):
        dhatu = state[index]
        la = state[index + 1]
        la_type = la.raw
        # TODO: remove hacks
        dhatuka = 'ardhadhatuka' if la_type == 'li~w' else 'sarvadhatuka'
        has_para, has_atma = D.pada_options(dhatu)
        indices = []
        if has_para:
            i = key2index[tin_key(la.samjna, pada='parasmaipada')]
            new_raw = base_tin[i]
            tin = la.set_raw(new_raw).add_samjna('tin', 'parasmaipada', dhatuka)
            yield state.swap(index + 1, tin)
        if has_atma:
            i = key2index[tin_key(la.samjna, pada='atmanepada')]
            new_raw = base_tin[i]
            tin = la.set_raw(new_raw).add_samjna('tin', 'atmanepada', dhatuka)
            yield state.swap(index + 1, tin)


    return [
        ('3.4.78',
            None, None,
            tin_adesha),
    ]


@tasya(None, 'tin')
def tin_adesha():
    """3.4.77 lasya"""

    base_p_tin = 'tip tas Ji sip Tas Ta mip vas mas'.split()
    lit_p_tin = 'Ral atus us Tal aTus a Ral va ma'.split()

    return [
        ('3.4.79',
            None, F.samjna('atmanepada') & F.samjna('wit'),
            O.ti('e')),
        ('3.4.80',
            None, F.samjna('atmanepada') & F.samjna('wit') & F.raw('TAs'),
            'se'),
        ('3.4.81',
            None, F.samjna('atmanepada') & F.raw('ta', 'Ja') & F.auto('li~w'),
            O.yathasamkhya(['ta', 'Ja'], ['eS', 'irec'])),
        ('3.4.82',
            None, F.raw(*base_p_tin) & F.auto('parasmaipada') & F.auto('li~w'),
            O.yathasamkhya(base_p_tin, lit_p_tin)),
    ]
