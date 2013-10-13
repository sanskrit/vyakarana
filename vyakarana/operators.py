# -*- coding: utf-8 -*-
"""
    vyakarana.operators
    ~~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

# TODO: rewrite operators to more closely model the Ashtadhyayi.

def guna(cur, right=None):
    converter = dict(zip('iIuUfFxX', 'eeooaaaa'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return cur.set_value(''.join(letters))


def dirgha(cur, right=None):
    converter = dict(zip('aiufx', 'AIUFX'))
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
