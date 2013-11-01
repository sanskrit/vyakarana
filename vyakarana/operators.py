# -*- coding: utf-8 -*-
"""
    vyakarana.operators
    ~~~~~~~~~~~~~~~~~~~

    Excluding paribhāṣā, all rules in the Ashtadhyayi describe a context
    then specify an operation to apply based on that context. Within
    this simulator, operations are defined using *operators*, which
    take some (state, index) pair and return a new :class:`State`.

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
        return self.body(state, index, locus)

    def __repr__(self):
        return '<op(%s)>' % self.name

    @classmethod
    def parameterized(cls, fn):
        """Decorator constructor for parameterized operators.

        :param fn: a function factory. It accepts parameters and returns
                   a parameterized operator function.
        """
        def wrapped(*args):
            try:
                name = '%s(%s)' % (fn.__name__, ', '.join(args))
            except TypeError:
                name = '%s(...)' % fn.__name__
            body = fn(*args)
            return cls(name, body)
        return wrapped

    @classmethod
    def unparameterized(cls, fn):
        """Decorator constructor for unparameterized operators.

        :param fn: some operator function
        """
        return cls(fn.__name__, fn)


class DataOperator(Operator):

    """An operator whose `body` modifies a term's data.

    `body` accepts a single string and returns a single string.
    """

    def __call__(self, state, index, locus='value'):
        cur = state[index]
        _input = cur.value
        output = self.body(_input)
        if output != _input:
            return state.swap(index, cur.set_at(locus, output))
        else:
            return state


# Parameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a valid operator.

@Operator.parameterized
def adi(result):
    def func(state, index, locus):
        cur = state[index]
        cur = cur.tasya(result, adi=True)
        return state.swap(index, cur)
    return func


@DataOperator.parameterized
def al_tasya(target, result):
    target = Sounds(target)
    result = Sounds(result)
    def func(value):
        letters = list(value)
        for i, L in enumerate(letters):
            if L in target:
                letters[i] = Sound(L).closest(result)
                # 1.1.51 ur aṇ raparaḥ
                if L in 'fF' and letters[i] in Sounds('aR'):
                    letters[i] += 'r'
                break
        return ''.join(letters)
    return func


@DataOperator.parameterized
def replace(target, result):
    def func(value):
        return value.replace(target, result)
    return func


@DataOperator.parameterized
def ti(result):
    """Create an operator that replaces the *ṭi* of some value.

        1.1.64 aco 'ntyādi ṭi
        The portion starting with the last vowel is called *ṭi*.

    :param result: the replacement
    """
    ac = Sounds('ac')
    def func(value):
        for i, L in enumerate(reversed(value)):
            if L in ac:
                break
        return value[:-(i+1)] + result

    return func


@DataOperator.parameterized
def upadha(result):
    """Create an operator that replaces the *upadhā* of some value.

        1.1.65 alo 'ntyāt pūrva upadhā
        The letter before the last is called *upadhā*.

    :param result: the replacement
    """
    def func(value):
        try:
            return value[:-2] + result + value[-1]
        except IndexError:
            return value

    return func


@Operator.parameterized
def yathasamkhya(targets, results):
    converter = dict(zip(targets, results))
    def func(state, index, locus):
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


def guna(state, index, locus=None, force=False):
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
    found = False
    for i, L in enumerate(rev_letters):
        # 1.1.45 ig yaNaH saMprasAraNAm
        # TODO: enforce short vowels automatically
        if L in Sounds('yaR'):
            rev_letters[i] = Sound(L).closest('ifxu')
            found = True
            break

    if not found:
        return value

    # 6.4.108 saMprasAraNAc ca
    try:
        L = rev_letters[i - 1]
        if L in Sounds('ac'):
            rev_letters[i - 1] = ''
    except IndexError:
        pass

    return ''.join(reversed(rev_letters))


def vrddhi(state, index, locus=None):
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


def force_guna(state, index, locus=None):
    return guna(state, index, force=True)
