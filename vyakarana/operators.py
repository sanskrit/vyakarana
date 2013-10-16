# -*- coding: utf-8 -*-
"""
    vyakarana.operators
    ~~~~~~~~~~~~~~~~~~~

    Various operators. An operator takes an :class:`Upadesha`, applies
    some sort of transformation, and returns a new :class:`Upadesha` for
    its result.

    All converters accept an optional right context `right`.

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
    # 1.1.5 kGiti ca (na)
    if right is not None and right.any_it('k', 'N'):
        return cur

    # 1.1.2 adeG guNaH
    # 1.1.3 iko guNavRddhI
    converter = dict(zip('iIuUfFxX', 'eeooaaaa'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            if L in 'fF':
                letters[i] += 'r'
            break

    return cur.set_value(''.join(letters)).add_samjna('guna')


def hrasva(cur, right=None):
    converter = dict(zip('AIUFXeEoO', 'aiufxiiuu'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return cur.set_value(''.join(letters))


def samprasarana(cur, right=None):
    rev_letters = list(reversed(cur.value))
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


def replace(target, result):
    def func(cur, right=None):
        return cur.set_value(cur.value.replace(target, result))
    return func


def vrddhi(cur, right=None):
    # 1.1.5 kGiti ca (na)
    if right and right.any_it('k', 'N'):
        return cur

    # 1.1.1 vRddhir Adaic
    # 1.1.3 iko guNavRddhI
    converter = dict(zip('iIuUfFxX', 'EEOOAAAA'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            if L in 'fF':
                letters[i] += 'r'
            break

    return cur.set_value(''.join(letters))


def upadha(L):
    def func(cur, right=None):
        return cur.upadha(L)
    return func


def al_tasya(target, result):
    target = Sounds(target)
    result = Sounds(result)
    def func(cur):
        letters = list(cur.value)
        for i, L in enumerate(letters):
            if L in target:
                letters[i] = Sound(L).closest(result)
                if L in 'fF':
                    letters[i] += 'r'
                break
        return cur.set_value(''.join(letters))
    return func
