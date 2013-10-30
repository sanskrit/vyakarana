# -*- coding: utf-8 -*-
"""
    vyakarana.filters
    ~~~~~~~~~~~~~~~~~

    Excluding paribhāṣā, all rules in the Ashtadhyayi describe a context
    then specify an operation to apply based on that context. Within
    this simulator, a rule's context is defined using *filters*, which
    return a true or false value for a given term within some state.

    This module defines a variety of parameterized and unparameterized
    filters, as well as as some basic operators for combining filters.

    :license: MIT and BSD
"""

from dhatupatha import DHATUPATHA as DP
from sounds import Sounds


#: Used to cache parameterized filters
FILTER_CACHE = {}


class FilterType(object):
    UNKNOWN = -1
    AL = 0
    SAMJNA = 1
    LAKSHANA = 2
    VALUE = 5
    UPADESHA = 10


class Filter(object):

    """
    A callable class that returns true or false.

    The program uses :class:`Filter` objects in order to make use of
    ``&``, ``|``, and ``~``. These operators give us a terse way to
    create more complex conditions, e.g. ``al('hal') & upadha('a')``.

    Additionally, using a class
    """

    def __init__(self, name, body, rank):
        #: A unique name for this filter
        self.name = name
        #: The function that corresponds to this filter
        self.body = body
        #: The relative rank of this filter. More specific filters
        #: have higher rank.
        self.rank = rank

    def __call__(self, term, state, index):
        return self.body(term, state, index)

    def __repr__(self):
        return '<f(%s)>' % self.name

    def __and__(self, other):
        """Bitwise "and" (``&``).

        The result is a function that matches the logical "and" of the
        two filters.

        :param other: the other :class:`Filter`.
        """
        return and_(self, other)

    def __invert__(self):
        """Bitwise "not" (``~``).

        The result is a function that matches the "not" of the current
        filter.
        """
        return not_(self)

    def __or__(self, other):
        """Bitwise "or" (``|``).

        The result is a function that matches the logical "or" of the
        two filters.

        :param other: the other :class:`Filter`.
        """
        return or_(self, other)


def parameterized(fn):
    """
    Decorator for parameterized filters. This creates :class:`Filter`
    objects automatically.

    :param fn: the function factory. It accepts parameters and returns
               a parameterized function.
    """
    cache = FILTER_CACHE

    def wrapped(*names):
        # Create ``name``
        try:
            if hasattr(names[0], '__call__'):
                params = ', '.join(f.name for f in names)
                name = "%s(%s)" % (fn.__name__, params)
            else:
                name = "%s(%s)" % (fn.__name__, ', '.join(names))
        except IndexError:
            name = "%s()" % fn.__name__
        name = name.replace('_', '')

        if name not in cache:
            body, rank = fn(*names)
            cache[name] = Filter(name=name, body=body, rank=rank)
        return cache[name]
    return wrapped


def unparameterized(fn):
    """
    Decorator for unparameterized filters. This creates :class:`Filter`
    objects automatically.

    :param fn: some filter function.
    """
    return Filter(name=fn.__name__, body=fn, rank=FilterType.UNKNOWN)


# Parameterized filters
# ~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a body and rank.

@parameterized
def adi(*names):
    """Filter on the sounds at the beginning of the term.

    :param names: a list of sounds
    """
    sounds = Sounds(*names)
    def func(term, state, index):
        return term and term.adi in sounds

    return func, FilterType.AL


@parameterized
def al(*names):
    """Filter on the sounds at the end of the term.

    :param names: a list of sounds
    """
    sounds = Sounds(*names)
    def func(term, state, index):
        return term and term.antya in sounds

    return func, FilterType.AL


@parameterized
def gana(start, end):
    gana_set = DP.dhatu_set(start, end)

    def func(term, state, index):
        print term.raw, start, end, len(gana_set), term.raw in gana_set
        return term.raw in gana_set

    return func, FilterType.UPADESHA


@parameterized
def lakshana(*names):
    """Filter on the ``raw`` property of the term, as well as `lakshana`.

    :param names: a list of raw values
    """
    names = frozenset(names)
    def func(term, state, index):
        if not term:
            return False
        if term.raw in names:
            return True
        try:
            return any(n in term.lakshana for n in names)
        except AttributeError:
            return False

    return func, FilterType.LAKSHANA


@parameterized
def raw(*names):
    """Filter on the ``raw`` property of the term.

    :param names: a list of raw values
    """
    names = frozenset(names)
    def func(term, state, index):
        return term is not None and term.raw in names

    return func, FilterType.UPADESHA


@parameterized
def samjna(*names):
    """Filter on the ``samjna`` property of the term.

    :param names: a list of samjnas
    """
    def func(term, state, index):
        return term is not None and any(n in term.samjna for n in names)

    return func, FilterType.SAMJNA


@parameterized
def upadha(*names):
    """Filter on the penultimate letter of the term.

        1.1.65 alo 'ntyāt pūrva upadhā

    :param names:
    """
    sounds = Sounds(*names)
    def func(term, state, index):
        return term is not None and term.upadha in sounds

    return func, FilterType.AL


@parameterized
def value(*names):
    """Filter on the ``value`` property of the term.

    :param names: a list of values
    """
    names = frozenset(names)
    def func(term, state, index):
        return term is not None and term.value in names

    return func, FilterType.VALUE


@parameterized
def and_(*filters):
    """Creates a filter that returns ``all(f(*args) for f in filters)``

    :param filters: a list of :class:`Filter`s.
    """
    def func(term, state, index):
        return all(f(term, state, index) for f in filters)
    return func, max(x.rank for x in filters)

@parameterized
def or_(*filters):
    """Creates a filter that returns ``any(f(*args) for f in filters)``

    :param filters: a list of :class:`Filter`s.
    """
    def func(term, state, index):
        return any(f(term, state, index) for f in filters)
    return func, min(x.rank for x in filters)


@parameterized
def not_(filt):
    """Creates a filter that returns ``not any(f(*args) for f in filters)``

    :param filt: a :class:`Filter`.
    """
    def func(term, state, index):
        return not filt(term, state, index)

    return func, filt.rank


# Unparameterized filters
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function defines a filter body.

@unparameterized
def Sit_adi(term, *args):
    return term is not None and term.raw and term.raw[0] == 'S'


@unparameterized
def placeholder(*args):
    """Matches nothing."""
    return False


@unparameterized
def allow_all(*args):
    """Matches everything."""
    return True


@unparameterized
def samyoga(term, *args):
    hal = Sounds('hal')
    return term and term.antya in hal and term.upadha in hal

asavarna = placeholder
ekac = placeholder
each = placeholder
samyogadi = placeholder
samyogapurva = placeholder


# Automatic filter
# ~~~~~~~~~~~~~~~~

def auto(data):
    """Creates a filter to match the context specified by `data`.

    :param data:
    """
    hal_it = set([L + 'it' for L in 'kKGNYwqRpmS'])
    ac_it = set([L + 'dit' for L in 'aiufx'])
    samjna_set = set([
        'atmanepada', 'parasmaipada',
        'dhatu', 'anga', 'pada', 'pratyaya',
        'krt', 'taddhita',
        'sarvadhatuka', 'ardhadhatuka',
        'abhyasa', 'abhyasta',
        'tin', 'sup',
    ])
    samjna_set |= (hal_it | ac_it)
    sound_set = set([
        'a', 'at',
        'i', 'it',
        'u', 'ut',
        'f', 'ft',
        'ak', 'ik',
        'ac', 'ec',
        'yaY',
        'JaS', 'jaS',
        'car',
        'hal', 'Jal',
    ])
    pratyaya_set = set([
        'luk', 'Slu', 'lup',
        'la~w', 'li~w', 'lu~w', 'lf~w', 'le~w', 'lo~w',
        'la~N', 'li~N', 'lu~N', 'lf~N',
        'Sap', 'Syan', 'Snu', 'Sa', 'Snam', 'u', 'SnA',
        'Ric',
    ])

    if data is None:
        return allow_all

    # Make `data` iterable
    if isinstance(data, basestring) or hasattr(data, '__call__'):
        data = [data]

    base_filter = None
    for datum in data:
        matcher = None
        # String selector: value, samjna, or sound
        if isinstance(datum, basestring):
            if datum in samjna_set:
                matcher = samjna(datum)
            elif datum in sound_set:
                matcher = al(datum)
            elif datum in pratyaya_set:
                matcher = lakshana(datum)
            else:
                matcher = raw(datum)

        # Function
        else:
            matcher = datum

        if base_filter is None:
            base_filter = matcher
        else:
            base_filter |= matcher

    return base_filter
