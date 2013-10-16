# -*- coding: utf-8 -*-
"""
    vyakarana.vibhakti
    ~~~~~~~~~~~~~~~~~~

    Rules that apply specifically to a vibhakti.

    :license: MIT and BSD
"""

import itertools

import context as c
import dhatu as D
import util
from classes import Vibhakti as V
from decorators import *


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


def c_lakara(p):
    return p is not None and 'vibhakti' in p.samjna and p.raw[0] == 'l'


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


@replace(c.samjna('dhatu'), c_lakara, None)
def lasya(dhatu, la, _):
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

    la_type = la.raw
    has_para, has_atma = D.pada_options(dhatu)
    indices = []
    if has_para:
        indices.append(key2index[tin_key(la.samjna, pada='parasmaipada')])
    if has_atma:
        indices.append(key2index[tin_key(la.samjna, pada='atmanepada')])

    for i in indices:
        base = base_tin[i]
        samjna = base_samjna[i]

        # 3.4.77 lasya
        # 3.4.78 tiptasjhisipthasthamipvasmastAtAmjhathAsAthAMdhvamiDvahimahiG
        la = la.set_raw(base)

        if has_atma:
            # 3.4.79 Tita AtmanepadAnAM Ter e
            if 'w' in la.it:
                la = la.ti('e')

                # 3.4.80 thAsaH se
                if la.raw == 'TAs':
                    la = la.set_raw('se')

                # 3.4.80 liTas tajhayor ezirec
                if la_type == 'li~w':
                    if la.raw == 'ta':
                        la = la.set_raw('eS')
                    elif la.raw == 'Ja':
                        la = la.set_raw('irec')

        if has_para:
            # 3.4.81 parasmaipadAnAM NalatususthalathusaNalvamAH
            if la_type == 'li~w':
                lit_tin = 'Ral atus us Tal aTus a Ral va ma'.split()
                tin_pairs = zip(base_tin[:9], lit_tin)
                for base_ending, lit_ending in tin_pairs:
                    if la.raw == base_ending:
                        la = la.set_raw(lit_ending)

        break

    return la.add_samjna('tin')
