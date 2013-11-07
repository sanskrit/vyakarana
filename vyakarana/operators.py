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

conflicts = [
    ('dirgha', 'hrasva'),
    ('insert', ),
    ('replace', ),
    ('add_samjna', ),
    ('ti', 'tasya'),
]

class Operator(object):

    """A callable class that returns :class:`State`s."""

    def __init__(self, name, body, category=None, params=None):
        #: A unique name for this operator.
        self.name = name

        #: The function that corresponds to this operator.
        self.body = body

        self.params = params

        #:
        self.category = category or name

    def __call__(self, state, index, locus='value'):
        return self.body(state, index, locus)

    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        else:
            return self.name == other.name and self.params == other.params

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<op(%s)>' % self.name

    @classmethod
    def parameterized(cls, fn):
        """Decorator constructor for parameterized operators.

        :param fn: a function factory. It accepts parameters and returns
                   a parameterized operator function.
        """
        def wrapped(*args, **kw):
            category = fn.__name__
            try:
                name = '%s(%s)' % (category, ', '.join(args))
            except TypeError:
                name = '%s(...)' % category
            body = fn(*args, **kw)
            return cls(name, body, category, params=args)
        return wrapped

    @classmethod
    def unparameterized(cls, fn):
        """Decorator constructor for unparameterized operators.

        :param fn: some operator function
        """
        return cls(fn.__name__, fn)

    def conflicts_with(self, other):
        """
        Return whether this operator conflicts with another.

        Two operators are in conflict if any of the following hold:
        - they each insert something into the state
        - one prevents or nullifies the change caused by the other. By
          "nullify" I mean that the result is as if neither operator
          was applied.

        For example, two 'tasmat' operators are always in conflict. And
        `hrasva` and `dirgha` are in conflict, since `hrasva` undoes
        `dirgha`. But `hrasva` and `guna` are not in conflict, since
        neither blocks or nullifies the other.

        :param other: an operator
        """
        for c in conflicts:
            # print self.category, other.category
            if self.category in c and other.category in c:
                return True
        return False


class DataOperator(Operator):

    """An operator whose `body` modifies a term's data.

    `body` accepts and returns a single string.
    """

    def __call__(self, state, index, locus='value'):
        cur = state[index]
        _input = cur.value
        if not _input:
            return state
        output = self.body(_input)
        if output != _input:
            return state.swap(index, cur.set_at(locus, output))
        else:
            return state


# Parameterized operators
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a valid operator.

@Operator.parameterized
def add_samjna(*names):
    def func(state, index, locus=None):
        cur = state[index]
        return state.swap(index, cur.add_samjna(*names))
    return func

def adi(result):
    return tasya(result, adi=True)


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


@Operator.parameterized
def insert(term):
    def func(state, index, *a):
        return state.insert(index, term)
    return func


@DataOperator.parameterized
def replace(target, result):
    def func(value):
        return value.replace(target, result)
    return func


@Operator.parameterized
def tasya(sthani, adi=False):
    def func(state, index, locus=None):
        cur = state[index]
        return state.swap(index, cur.tasya(sthani, adi=adi, locus=locus))
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


@Operator.unparameterized
def guna(state, index, locus=None):
    cur = state[index]
    try:
        right = state[index + 1]
    except (IndexError, TypeError):
        right = None

    # 1.1.5 kGiti ca (na)
    if right is not None and right.any_samjna('kit', 'Nit'):
        return state

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


@Operator.unparameterized
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


@Operator.unparameterized
def force_guna(state, index, locus=None):
    cur = state[index]
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
