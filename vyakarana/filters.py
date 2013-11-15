# -*- coding: utf-8 -*-
"""
    vyakarana.filters
    ~~~~~~~~~~~~~~~~~

    Excluding paribhāṣā, all rules in the Ashtadhyayi describe a context
    then specify an operation to apply based on that context. Within
    this simulator, a rule's context is defined using *filters*, which
    return a true or false value for a given index within some state.

    This module defines a variety of parameterized and no_params
    filters, as well as as some basic operators for combining filters.

    :license: MIT and BSD
"""

from collections import defaultdict

import lists
from dhatupatha import DHATUPATHA as DP
from sounds import Sounds
from upadesha import Upadesha as U
from util import Rank


DHATU_SET = set(DP.all_dhatu)


class Filter(object):

    """A callable class that returns true or false.

    The program uses :class:`Filter` objects in order to make use of
    ``&``, ``|``, and ``~``. These operators give us a terse way to
    create more complex conditions, e.g. ``al('hal') & upadha('a')``.
    """

    #: An internal cache to avoid creating redundant filter objects.
    #: When a filter is declared, the constructor creates a `name` for
    #: the filter and checks it against the cache. If `name` is found
    #: in the cache, the cached result is returned instead.
    CACHE = {}

    def __init__(self, *args, **kw):
        #: The filter type. For example, a filter on the first letter
        #: of a term has the category ``adi``.
        self.category = kw.get('category') or self._make_category(*args, **kw)

        #: A unique name for the filter. This is used as a key to the
        #: filter cache.
        self.name = kw.get('name') or self._make_name(*args, **kw)

        #: The function that corresponds to this filter. The input and
        #: output of the function depend on the filter class. For
        #: a general :class:`Filter`, this function accepts a state and
        #: index and returns ``True`` or ``False``.
        self.body = kw.get('body') or self._make_body(*args, **kw)

        #: A collection that somehow characterizes the domain of the
        #: filter. Some examples:
        #: - for an `al` filter, the set of matching letters
        #: - for a `samjna` filter, the set of matching samjna
        #: - for a `raw` filter, the set of matching raw values
        #: - for an and/or/not filter, the original filters
        self.domain = self._make_domain(*args, **kw)

        #: A :class:`Rank` that characterizes the relative power of
        #: this filter. Rules with more powerful filters tend to have
        #: higher priority over rules with less powerful filters.
        self.rank = kw.get('rank') or self._make_rank(self.domain)

    def __call__(self, state, index):
        return self.body(state, index)

    def __and__(self, other):
        """Bitwise "and" (``&``).

        The result is a function that matches the logical "and" of the
        two filters.

        :param other: the other :class:`Filter`.
        """
        return Filter.and_(self, other)

    def __eq__(self, other):
        """Equality operator.

        Two filters are the same if they allow exactly the same set
        of items.

        :param other: the other :class:`Filter`.
        """
        if self is other:
            return True
        if other is None:
            return False
        return self.name == other.name and self.domain == other.domain

    def __hash__(self):
        return hash(self.name)

    def __invert__(self):
        """Bitwise "not" (``~``).

        The result is a function that matches the "not" of the current
        filter.
        """
        return Filter.not_(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __or__(self, other):
        """Bitwise "or" (``|``).

        The result is a function that matches the logical "or" of the
        two filters.

        :param other: the other :class:`Filter`.
        """
        return Filter.or_(self, other)

    def __repr__(self):
        return '<f(%s)>' % self.name

    def _make_category(self, *args, **kw):
        return self.__class__.__name__

    def _make_body(self, *args, **kw):
        return self.body

    def _make_name(self, *args, **kw):
        try:
            return kw['name']
        except KeyError:
            class_name = self.__class__.__name__
            str_args = [str(a) for a in args]
            return '{}({})'.format(class_name, ', '.join(str_args))

    def _make_domain(self, *args, **kw):
        try:
            return kw['domain']
        except KeyError:
            if args:
                return frozenset(args)
            return None

    def _make_rank(self, domain):
        return Rank()

    @staticmethod
    def and_(*filters):
        """Return the logical "AND" over all filters."""
        cls = Filter._select_class(filters)
        name = 'and(%s)' % ', '.join(f.name for f in filters)
        body = cls._make_and_body(filters)
        domain = set(filters)
        rank = Rank.and_(f.rank for f in filters)
        return cls(category='and', name=name, body=body, domain=domain, rank=rank)

    @staticmethod
    def or_(*filters):
        """Return the logical "OR" over all filters."""
        cls = Filter._select_class(filters)
        name = 'or(%s)' % ', '.join(f.name for f in filters)
        body = cls._make_or_body(filters)
        domain = set(filters)
        rank = Rank.or_(f.rank for f in filters)
        return cls(category='or', name=name, body=body, domain=domain, rank=rank)

    @staticmethod
    def not_(filt):
        """Return the logical "NOT" of the filter.

        :param filt: some :class:`Filter`
        """
        cls = Filter._select_class([filt])
        name = 'not(%s)' % filt.name
        body = cls._make_not_body(filt)
        domain = set([filt])
        rank = filt.rank
        return cls(category='not', name=name, body=body, domain=domain, rank=rank)

    @staticmethod
    def _select_class(filters):
        """Return the lowest common ancestor of the given filters.

        :param filters: a list of filters
        """
        if all(isinstance(f, TermFilter) for f in filters):
            return TermFilter
        return Filter

    @classmethod
    def _make_and_body(cls, filters):
        """Make a body function for the "and" filter.

        This routine is in its own method so that other classes can
        override it.

        :param filters:
        """
        def func(state, index):
            return all(f(state, index) for f in filters)
        return func

    @classmethod
    def _make_or_body(cls, filters):
        """Make a body function for the "or" filter.

        This routine is in its own method so that other classes can
        override it.

        :param filters:
        """
        def func(state, index):
            return any(f(state, index) for f in filters)
        return func

    @classmethod
    def _make_not_body(cls, filt):
        """Make a body function for the "not" filter.

        This routine is in its own method so that other classes can
        override it.

        :param filt: a filter
        """
        def func(state, index):
            return not filt.body(state, index)
        return func

    @classmethod
    def no_params(cls, fn):
        """Decorator constructor for unparameterized filters.

        :param fn: some filter function.
        """
        category = name = fn.__name__
        domain = None
        body = fn
        return cls(category=category, name=name, body=body, domain=domain)

    @property
    def feature_sets(self):
        """Return the indivisible filters that compose this one.

        Consider a universal set that contains every possible element.
        A filter defines a subset of the universal set, i.e. the set of
        items for which the filter returns `True`. Thus every filter
        defines a subset. For two filters `f1` and `f2`:
        - `f1 & f2` is like an intersection of two sets
        - `f1 | f2` is like a union of two sets
        - `~f1` is like an "antiset"

        Now consider a filter `f` composed of `n` filters, as in:

            f = f1 & f2 & ... & fn

        This function returns the `n` filters that compose `f`. Each
        `fi` is essentially a superset of `f`.

        "Or" and "not" filters are tough to break up, so they're
        treated as indivisible.
        """
        stack = [self]
        returned = set()
        while stack:
            cur = stack.pop()
            if cur.category == 'and':
                stack.extend(cur.domain)
            else:
                returned.add(cur)
        return returned

    @property
    def supersets(self):
        """Return some interesting supersets of this filter.

        For what a "set" means in the context of a filter, see the
        comments on :meth:`Filter.feature_sets`.
        """
        try:
            return self._supersets
        except AttributeError:
            pass

        returned = set()

        # Break up 'and' filters
        if self.name.startswith('and'):
            for m in self.domain:
                returned |= m.supersets

        # All others are treated as indivisible. Ignore `allow_all`,
        # since it applies for every filter and isn't too interesting.
        else:
            name = self.name
            if name != 'allow_all':
                returned.add(self)

        self._supersets = returned
        return returned

    def domain_subset_of(self, other):
        if self.domain == other.domain:
            return True
        return self.domain.issubset(other.domain)

    def subset_of(self, other):
        """Return whether this filter is a subset of some other filter.

        All members of some subset S are in the parent set O. So if it
        is the case that:

            S applies -> O applies

        then S is a subset of P. For the "set" interpretation of a
        filter, see the comments on :meth:`~Filter.supersets`.

        :param other: a filter
        """
        s_sets = self.supersets
        o_sets = other.supersets

        # If `self` is a subset of `other`, then `self` is *more*
        # specific and has *more* components than `other`. If every
        # component of `other` (or something more specific) is in
        # `self`, then the subset relation holds.
        for o in o_sets:
            # Both filters share the condition.
            if o in s_sets:
                continue

            # `o` is an "or" condition that must be matched by at least
            # one member of `s_sets`
            if o.category == 'or' and any(s in o.domain for s in s_sets):
                continue

            skip = False
            for s in s_sets:
                if s.category == o.category and s.domain_subset_of(o):
                    skip = True
                    break
            if skip:
                continue

            return False
        return True


class TermFilter(Filter):

    """A :class:`Filter` whose body takes an :class:`Upadesha` as input.

    Term filters are used for the following reasons.

    1. Convenience. Most filters apply to just a single term.
    2. Performance. Since we can guarantee that the output of a term
       filter will change only if its term changes, we can cache results
       for an unchanged term and avoid redundant calls.
    """

    def __call__(self, state, index):
        try:
            term = state[index]
            name = self.name
            cache = term._filter_cache
            if name not in cache:
                cache[name] = term and self.body(term)
            return cache[name]
        except IndexError:
            return False

    @classmethod
    def _make_and_body(cls, filters):
        bodies = [f.body for f in filters]
        def func(term):
            return all(b(term) for b in bodies)
        return func

    @classmethod
    def _make_or_body(cls, filters):
        bodies = [f.body for f in filters]
        def func(term):
            return any(b(term) for b in bodies)
        return func

    @classmethod
    def _make_not_body(cls, filt):
        def func(term):
            return not filt.body(term)
        return func


class AlFilter(TermFilter):
    def _make_domain(self, domain_str=None, *args, **kw):
        if domain_str is None:
            return None
        return Sounds(domain_str)

    def _make_rank(self, domain):
        if domain is None:
            return Rank()
        return Rank.with_al(domain)

    def domain_subset_of(self, other):
        if self.domain == other.domain:
            return True
        ov = other.domain.values
        sv = self.domain.values
        return sv.issubset(ov)

    def body(self, term):
        return self.op(term)


class SamjnaFilter(TermFilter):
    def _make_rank(self, domain):
        return Rank.with_samjna(domain)


class UpadeshaFilter(TermFilter):
    def _make_rank(self, domain):
        return Rank.with_upadesha(domain)


class DhatuFilter(UpadeshaFilter):
    @property
    def supersets(self):
        try:
            return self._supersets
        except AttributeError:
            antya = ' '.join(U(x).antya for x in self.domain)
            _al = al(antya)
            _samjna = samjna('dhatu')
            self._supersets = set([self, _samjna, _al])
            return self._supersets


# Parameterized filters
# ~~~~~~~~~~~~~~~~~~~~~
# Each function accepts arbitrary arguments and returns a body and rank.


class adi(AlFilter):

    """Filter on a term's first sound."""

    def body(self, term):
        return term.adi in self.domain


class al(AlFilter):

    """Filter on a term's final sound."""

    def body(self, term):
        return term.antya in self.domain


class contains(AlFilter):

    """Filter on whether a term has a certain sound."""

    def body(self, term):
        return any(s in term.value for s in self.domain)


class dhatu(DhatuFilter):

    """Filter on whether a term represents a particular dhatu."""

    def body(self, term):
        return term.raw in self.domain and 'dhatu' in term.samjna


def gana(start, end=None):
    """Return a filter on whether a term is in a particular dhatu set.

    :param start: the ``raw`` value of the first dhatu in the list
    :param end: the ``raw`` value of the last dhatu in the list. If
                ``None``, use all roots from ``start`` to the end of
                the gana.
    """

    names = DP.dhatu_list(start, end)
    return dhatu(*names)


class lakshana(UpadeshaFilter):

    """Filter on a term's prior values."""

    def body(self, term):
        return any(x in term.lakshana for x in self.domain)


class part(TermFilter):

    """Filter on a term's augments."""

    def body(self, term):
        return any(x in term.parts for x in self.domain)


class raw(UpadeshaFilter):

    """Filter on a term's raw value."""

    def body(self, term):
        return term.raw in self.domain


class samjna(SamjnaFilter):

    """Filter on a term's designations."""

    def body(self, term):
        return any(x in term.samjna for x in self.domain)


class upadha(AlFilter):

    """Filter on a term's penultimate sound."""

    def body(self, term):
        return term.upadha in self.domain


class value(UpadeshaFilter):

    """Filter on a term's current value."""

    def body(self, term):
        return term.value in self.domain



# Unparameterized filters
# ~~~~~~~~~~~~~~~~~~~~~~~
# Each function defines a filter body.

@AlFilter.no_params
def Sit_adi(term):
    """Filter on whether a term starts with ś in upadeśa."""
    return term.raw and term.raw[0] == 'S'


@Filter.no_params
def placeholder(*args):
    """Matches nothing."""
    return False


@Filter.no_params
def allow_all(*args):
    """Matches everything."""
    return True


@AlFilter.no_params
def ekac(term):
    seen = False
    ac = Sounds('ac')
    for L in term.value:
        if L in ac:
            if seen:
                return False
            seen = True
    return True


@AlFilter.no_params
def samyoga(term):
    """Filter on whether a term ends with a conjunct."""
    hal = Sounds('hal')
    return term.antya in hal and term.upadha in hal


@AlFilter.no_params
def samyogadi(term):
    """Filter on whether a term begins with a conjunct."""
    value = term.value
    hal = Sounds('hal')
    try:
        return value[0] in hal and value[1] in hal
    except IndexError:
        return False


@AlFilter.no_params
def samyogapurva(term):
    """Filter on whether a term's final sound follows a conjunct."""
    value = term.value
    hal = Sounds('hal')
    try:
        return value[-3] in hal and value[-2] in hal
    except IndexError:
        return False


@TermFilter.no_params
def term_placeholder(term):
    return False


asavarna = term_placeholder
each = term_placeholder


# Automatic filter
# ~~~~~~~~~~~~~~~~

def auto(*data):
    """Create a filter to match the context specified by `data`.

    :param data: arbitrary data, usually a list of strings
    """

    # Maps a filter type to a list of selectors. This is populated in
    # the loop below.
    parsed = defaultdict(list)

    for datum in data:
        # ``None`` implies no filter -> allow all
        if datum is None:
            return allow_all

        # String selector: value, samjna, or sound
        if isinstance(datum, basestring):
            if datum in lists.SAMJNA or datum in lists.IT:
                key = 'samjna'
            elif datum in lists.SOUNDS:
                key = 'al'
            elif datum in lists.LA:
                key = 'lakshana'
            elif datum in DHATU_SET:
                key = 'dhatu'
            else:
                key = 'raw'
            parsed[key].append(datum)

        # Function
        elif hasattr(datum, '__call__'):
            parsed['functions'].append(datum)

        # Unknown
        else:
            raise NotImplementedError(datum)

    # Create filter
    base_filter = None
    name2creator = {
        'raw': raw,
        'dhatu': dhatu,
        'lakshana': lakshana,
        'samjna': samjna,
        'al': al
    }
    for name in name2creator:
        values = parsed[name]
        if values:
            filt_creator = name2creator[name]
            filt = filt_creator(*values)
            if base_filter is None:
                base_filter = filt
            else:
                base_filter |= filt

    # Combine filter with `functions` filters
    if base_filter:
        if parsed['functions']:
            base_filter = Filter.or_(base_filter, *parsed['functions'])
    else:
        base_filter = parsed['functions'][0]
    return base_filter


# Common filters
# ~~~~~~~~~~~~~~

knit = samjna('kit', 'Nit')
