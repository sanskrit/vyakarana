# -*- coding: utf-8 -*-
"""
    vyakarana.decorators
    ~~~~~~~~~~~~~~~~~~~~

    Various decorators.

    :license: MIT and BSD
"""

from classes import Option
from itertools import chain, islice, izip, repeat

# New-style rules. Temporary.
NEW_RULES = []


def always_true(*a, **kw):
    return True


def padslice(state, i):
    return chain(islice(state, i, None), repeat(None))


class Procedure(object):

    """Represents a group of related rules from the Ashtadhyayi.

    """

    def __init__(self, filters, body):
        #: Unique ID for this function. This is used to mark certain
        #: terms with the operations applied to them. For example, if an
        #: optional rule is rejected, we mark the result to prevent
        #: applying that rule again.
        self._id = len(NEW_RULES)

        #: An array of filters from `vyakarana.contexts`.
        self.filters = [f or always_true for f in filters]

        self.num_filters = len(self.filters)

        #: The function body. The input and output of this function can
        #: take any form.
        self.body = body

        self._name = body.__name__

        NEW_RULES.append(self)

    def __repr__(self):
        cls = self.__class__.__name__
        return '<%s(%s)>' % (cls, self._name)

    def _window(self, state, i):
        if i:
            window = state[i-1:i-1+self.num_filters]
        else:
            window = [None] + state[i:i-1+self.num_filters]

        window = window + [None] * (self.num_filters - len(window))
        return window

    def matches(self, state, i):
        return False

    def apply(self, state, i):
        yield


class StateProcedure(Procedure):

    """Procedure that performs an arbitrary transformation."""

    def matches(self, state, i):
        return all(f(x) for f, x in izip(self.filters, padslice(state, i)))

    def apply(self, state, i):
        result = self.body(state, i)
        if result is None:
            return

        yield result


class TasyaProcedure(Procedure):

    """Procedure that performs substitution on a single term.

        1.1.49 SaSThI sthAneyogA
    """

    def matches(self, state, i):
        window = self._window(state, i)
        return all(f(x) for f, x in izip(self.filters, window))

    def apply(self, state, i):
        fn = self.body
        window = self._window(state, i)
        result = fn(*window)
        if result is None:
            return

        cur = window[1]
        # Optional substitution
        if isinstance(result, Option):
            if fn._id in cur.ops:
                return
            # declined
            yield state.swap(i, cur.add_op(fn._id))
            # accepted
            result = result.data

        # Operator substitution
        if hasattr(result, '__call__'):
            new_cur = result(cur, right=window[2])

        # Other substitution
        else:
            new_cur = cur.tasya(result)

        if new_cur != cur:
            yield state.swap(i, new_cur)



class ReplaceProcedure(TasyaProcedure):

    """Procedure that replaces a single term."""

    def apply(self, state, i):
        fn = self.body
        window = self._window(state, i)
        result = fn(*window)
        if result is None:
            return

        cur = window[1]
        new_cur = result
        if new_cur != cur:
            yield state.swap(i, new_cur)


class TasmatProcedure(Procedure):

    """Procedure that performs insertion after a single term.

        1.1.67 tasmAdityuttarasya
    """

    def matches(self, state, i):
        return all(f(x) for f, x in izip(self.filters, state.window(i)))

    def apply(self, state, i):
        # If previously applied, reject and avoid looping.
        # TODO: find more elegant way to control this
        if self._id in state.ops:
            return

        fn = self.body
        left, right, _ = state.window(i)
        result = fn(left, right)
        if result is None:
            return

        for r in result:
            if r is not None:
                yield state.insert(i, r).add_op(self._id)


def tasmat(*filters):
    """Decorator to create a :class:`TasmatProcedure`"""
    def decorator(body):
        return TasmatProcedure(filters=filters, body=body)
    return decorator


def tasya(*filters):
    """Decorator to create a :class:`TasyaProcedure`"""
    def decorator(body):
        return TasyaProcedure(filters=filters, body=body)
    return decorator

def replace(*filters):
    """Decorator to create a :class:`ReplaceProcedure`"""
    def decorator(body):
        return ReplaceProcedure(filters=filters, body=body)
    return decorator


def state(*filters):
    """Decorator to create a :class:`StateProcedure`"""
    def decorator(body):
        return StateProcedure(filters=filters, body=body)
    return decorator