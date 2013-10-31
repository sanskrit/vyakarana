# -*- coding: utf-8 -*-
"""
    vyakarana.operators
    ~~~~~~~~~~~~~~~~~~~

    Excluding paribhāṣā, all rules in the Ashtadhyayi describe a context
    then specify an operation to apply based on that context. Within
    this simulator, operations are defined using *operators*, which
    take some (state, index) and return a new :class:`State`.

    This module defines a variety of parameterized and unparameterized
    operators.

    :license: MIT and BSD
"""

from sounds import Sound, Sounds


# TODO: rewrite operators to more closely model the Ashtadhyayi.


def parameterized(fn):
    def wrapped(*args):
        result = fn(*args)
        result.__name__ = '%s(%s)' % (fn.__name__, repr(args))
        return result
    return wrapped


# Parameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a valid operator.

@parameterized
def adi(result):
    def func(state, index):
        cur = state[index]
        cur = cur.tasya(result, adi=True)
        return state.swap(index, cur)
    return func


@parameterized
def al_tasya(target, result):
    target = Sounds(target)
    result = Sounds(result)
    def func(state, index):
        cur = state[index]
        letters = list(cur.value)
        for i, L in enumerate(letters):
            if L in target:
                letters[i] = Sound(L).closest(result)
                if L in 'fF' and letters[i] in Sounds('aR'):
                    letters[i] += 'r'
                break
        cur = cur.set_value(''.join(letters))
        return state.swap(index, cur)
    return func


@parameterized
def replace(target, result):
    def func(state, index):
        cur = state[index]
        cur = cur.set_value(cur.value.replace(target, result))
        return state.swap(index, cur)
    return func


@parameterized
def ti(result):
    ac = Sounds('ac')
    def func(state, index):
        cur = state[index]
        for i, L in enumerate(reversed(cur.value)):
            if L in ac:
                break

        value = cur.value[:-(i+1)] + result
        cur = cur.set_value(value)
        return state.swap(index, cur)

    return func


@parameterized
def upadha(L):
    def func(state, index):
        cur = state[index]
        try:
            value = cur.value[:-2] + L + cur.value[-1]
            cur = cur.set_value(value)
            return state.swap(index, cur)
        except IndexError:
            return state

    return func


@parameterized
def yathasamkhya(targets, results):
    print 'yathasamkha'
    converter = dict(zip(targets, results))
    def func(state, index):
        cur = state[index]
        cur = cur.set_raw(converter[cur.raw])
        return state.swap(index, cur)
    return func


# Unparameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Each function defines an operator.

def dirgha(state, index):
    cur = state[index]
    converter = dict(zip('aiufx', 'AIUFX'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    cur = cur.set_value(''.join(letters))
    return state.swap(index, cur)


def guna(state, index, force=False):
    cur = state[index]
    try:
        right = state[index + 1]
    except (IndexError, TypeError):
        right = None

    # 1.1.5 kGiti ca (na)
    if not force and right is not None and right.any_samjna('kit', 'Nit'):
        cur = cur
        return state.swap(index, cur)

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

    cur = cur.set_value(''.join(letters)).add_samjna('guna')
    return state.swap(index, cur)


def hrasva(state, index):
    cur = state[index]
    converter = dict(zip('AIUFXeEoO', 'aiufxiiuu'))
    letters = list(cur.value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    cur = cur.set_value(''.join(letters))
    return state.swap(index, cur)


def samprasarana(state, index):
    cur = state[index]
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

    cur = cur.set_value(''.join(reversed(rev_letters)))
    return state.swap(index, cur)


def vrddhi(state, index):
    cur = state[index]
    try:
        right = state[index + 1]
    except (IndexError, TypeError):
        right = None

    # 1.1.5 kGiti ca (na)
    if right and right.any_samjna('kit', 'Nit'):
        cur = cur
        return state.swap(index, cur)

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

    cur = cur.set_value(''.join(letters))
    return state.swap(index, cur)


def force_guna(state, index):
    return guna(state, index, force=True)
