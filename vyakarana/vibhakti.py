# -*- coding: utf-8 -*-
"""
    vyakarana.vibhakti
    ~~~~~~~~~~~~~~~~~~

    Rules that apply specifically to a vibhakti.

    :license: MIT and BSD
"""

import itertools

import dhatu as D
import util
from classes import Vibhakti as V


PADA = ['parasmaipada', 'atmanepada']
PURUSHA = ['prathama', 'madhyama', 'uttama']
VACANA = ['ekavacana', 'dvivacana', 'bahuvacana']
VIBHAKTI = ['prathama', 'dvitiya', 'trtiya', 'caturthi', 'pancami', 'sasthi',
            'saptami']


def label_triplets(terms, labels):
    """
    Apply a single label to each triplet of terms.

    :param terms: a list of Terms
    :param labels: a list of strings
    """
    for i, chunk in enumerate(util.iter_group(terms, 3)):
        for v in chunk:
            v.samjna.add(labels[i % len(labels)])


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
    for v in terms:
        v.samjna.add(next(labels))


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
    length = len(terms)
    num_labels = len(labels)
    for i, g in enumerate(util.iter_group(terms, length / num_labels)):
        for v in g:
            v.samjna.add(labels[i])


def la_to_sup(state):
    """

    :param state:
    """

    # Basic endings
    # 4.1.2 svaujasamauTchaSTAbhyAMbhisGebhyAmbhyas-
    #       GasibhyAMbhyasGasosAmGyossup
    sup_list = """su~   O    jas
                  am    Ow   Sas
                  wA    ByAm Bis
                  Ne    ByAm Byas
                  Nasi~ ByAm Byas
                  Nas   os   Am
                  Ni    os   sup""".split()

    base_sup = [V(x) for x in sup_list]

    # Case
    label_triplets(base_sup, VIBHAKTI)

    # Number
    # 1.4.103 supaH (1.4.102 tAnyekavacananadvivacanabahuvacanAnyekazaH)
    label_by_item(base_sup, VACANA)

    endings = sup_list

    for e in endings:
        yield state.swap(-1, e)


def la_to_tin(state):
    """Apply 3.4.77 - 3.4.117 to convert `la` to `tiN`.

    3.4.109 - 3.4.112 are considered in `tin_adesha`.

    :param state:
    """
    # 'la' is always at the end of the word
    _, dhatu = state.find('dhatu')
    la = state[-1]
    if 'tin' in la.samjna:
        return

    # Basic endings
    # 3.4.78 tiptasjhisipthasthamipvasmastAtAmjhathAsAthAMdhvamiDvahimahiG
    base_tin = [V(x) for x in """
                              tip tas  Ji
                              sip Tas  Ta
                              mip vas  mas
                              ta  AtAm Ja
                              TAs ATAm Dvam
                              iw  vahi mahiG
                               """.split()]

    # Pada
    # 1.4.99 laH parasmaipadam
    # 1.4.100 taGAnAv Atmanepadam
    label_by_group(base_tin, PADA)

    # Person
    # 1.4.101 tiGas trINi trINi prathamamadhyamottamAH
    label_triplets(base_tin, PURUSHA)

    # Number
    # 1.4.102 tAnyekavacananadvivacanabahuvacanAnyekazaH
    label_by_item(base_tin, VACANA)

    # Sarvadhatuka / Ardhadhatuka
    # 3.4.113 tiGzit sArvadhAtukam
    # 3.4.114 ArdhadhAtukaM zeSaH
    # 3.4.115 liT ca
    for v in base_tin:
        v.lakshana.add(la.raw)
        v.samjna.add('tin')
        if la.raw == 'li~w':
            v.samjna.add('ardhadhatuka')
        else:
            v.samjna.add('sarvadhatuka')

    # Split in parasmaipada and atmanepada, use as appropriate
    p_base, a_base = list(util.iter_group(base_tin, 9))

    has_para, has_atma = D.pada_options(state)
    p_endings = p_base if has_para else []
    a_endings = a_base if has_atma else []

    # Transformations (3.4)
    # ---------------------
    if has_atma:
        # 3.4.78 Tita AtmanepadAnAM Ter e
        if 'w' in la.it:
            endings = [x.ti('e') for x in a_endings]

            for i, x in enumerate(a_base):
                # 3.4.79 thAsas se
                if x.raw == 'TAs':
                    endings[i] = endings[i].update('se')

                # 3.4.80 liTas tajhayor ezirec
                if la.raw == 'li~w':
                    if x.raw == 'ta':
                        endings[i] = endings[i].update('eS')
                    elif x.raw == 'Ja':
                        endings[i] = endings[i].update('irec')

            a_endings = endings

    if has_para:
        # 3.4.81 parasmaipadAnAM NalatususthalathusaNalvamAH
        if la.raw == 'li~w':
            new = 'Ral atus us Tal aTus a Ral va ma'.split()
            old_new = zip(p_endings, new)
            p_endings = [o.update(n) for (o, n) in old_new]

    endings = p_endings + a_endings

    # Analogous extension
    # -------------------
    # This adds 'it' letters to endings that don't have them by default.
    if la.raw == 'li~w':
        # 1.2.5 asaMyogAl liT kit
        if not dhatu.samyoga:
            for i, e in enumerate(endings):
                if 'p' not in e.it:
                    endings[i] = e.add_it('k')

        # 1.2.6 indhibhavatibhyAM ca
        if dhatu.value in ('BU', 'inD'):
            for i, e in enumerate(endings):
                endings[i] = e.add_it('k')

    # 7.1.91 Nal uttamo vA
    for e in endings:
        yield state.swap(-1, e)
        if la.raw == 'li~w' and 'uttama' in e.samjna and 'R' in e.it:
            e2 = e.remove_it('R')
            yield state.swap(-1, e2)


def tin_adesha(state):
    """
    Apply tin substitutions that depend on the dhatu.

    These rules are separated from `la_to_tin` so that other
    substitutions have time to occur, such as gai -> gA.

    :param state:
    """
    i, dhatu = state.find('dhatu')
    tin = state[-1]

    if 'tin' not in tin.samjna:
        return

    # Root-dependent changes
    # 7.1.34 Ata au NalaH
    if dhatu.antya().value == 'A' and tin.raw == 'Ral' and tin.value != 'O':
        tin = tin.update('O')
        yield state.swap(-1, tin)
