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


class Operator(object):

    """A callable class that returns :class:`State`s."""

    def __init__(self, name, body):
        #: A unique name for this operator.
        self.name = name
        #: The function that corresponds to this operator.
        self.body = body

    def __call__(self, state, index, locus='value'):
        return self.body(state, index)

    def __repr__(self):
        return '<op(%s)>' % self.name

    @classmethod
    def parameterized(cls, fn):
        def wrapped(*args):
            print args
            try:
                name = '%s(%s)' % (fn.__name__, ', '.join(args))
            except TypeError:
                name = '%s(...)' % fn.__name__
            body = fn(*args)
            return cls(name, body)
        return wrapped

    @classmethod
    def unparameterized(cls, fn):
        return cls(fn.__name__, fn)


class DataOperator(Operator):

    """An operator whose `body` modifies a term's data.

    `body` accept a single string and returns a single string.
    """

    def __call__(self, state, index, locus='value'):
        cur = state[index]
        output = self.body(cur.value)
        return state.swap(index, cur.set_value(output))


# Parameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a valid operator.

@Operator.parameterized
def adi(result):
    def func(state, index):
        cur = state[index]
        cur = cur.tasya(result, adi=True)
        return state.swap(index, cur)
    return func


@Operator.parameterized
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


@Operator.parameterized
def replace(target, result):
    def func(state, index):
        cur = state[index]
        cur = cur.set_value(cur.value.replace(target, result))
        return state.swap(index, cur)
    return func


@Operator.parameterized
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


@Operator.parameterized
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


@Operator.parameterized
def yathasamkhya(targets, results):
    converter = dict(zip(targets, results))
    def func(state, index):
        cur = state[index]
        cur = cur.set_raw(converter[cur.raw])
        return state.swap(index, cur)
    return func


# Unparameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Each function defines an operator.

@DataOperator.unparameterized
def dirgha(value):
    converter = dict(zip('aiufx', 'AIUFX'))
    letters = list(value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return ''.join(letters)


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


@DataOperator.unparameterized
def hrasva(value):
    converter = dict(zip('AIUFXeEoO', 'aiufxiiuu'))
    letters = list(value)
    for i, L in enumerate(letters):
        if L in converter:
            letters[i] = converter[L]
            break

    return ''.join(letters)


@DataOperator.unparameterized
def samprasarana(value):
    rev_letters = list(reversed(value))
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

    return ''.join(reversed(rev_letters))


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
