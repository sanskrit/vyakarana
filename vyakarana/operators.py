# -*- coding: utf-8 -*-
"""
    vyakarana.operators
    ~~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

from classes import Sound, Sounds


# TODO: rewrite operators to more closely model the Ashtadhyayi.


def dirgha(cur, right=None):
    converter = dict(zip('aiufx', 'AIUFX'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return cur.set_value(''.join(letters))


def guna(cur, right=None):
    converter = dict(zip('iIuUfFxX', 'eeooaaaa'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return cur.set_value(''.join(letters))


def hrasva(cur, right=None):
    converter = dict(zip('AIUFXeEoO', 'aiufxiiuu'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return cur.set_value(''.join(letters))


def samprasarana(cur):
    rev_letters = list(reversed(cur.value))
    found = False
    for i, L in enumerate(rev_letters):
        # 1.1.45 ig yaNaH saMprasAraNAm
        # TODO: enforce short vowels automatically
        if L in Sounds('yaR'):
            rev_letters[i] = Sound(L).closest('ifxu')
            break

    # 6.4.108 saMprasAraNAc ca
    try:
        L = rev_letters[i - 1]
        if L in Sounds('ac'):
            rev_letters[i - 1] = ''
    except IndexError:
        pass

    return cur.set_value(''.join(reversed(rev_letters)))
