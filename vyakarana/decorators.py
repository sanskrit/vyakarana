# -*- coding: utf-8 -*-
"""
    vyakarana.decorators
    ~~~~~~~~~~~~~~~~~~~~

    Various decocators.

    :license: MIT and BSD
"""

from functools import wraps


def require(name):
    """
    Run `fn` only if the op described by `name` has been attempted. The
    op doesn't have to yield anything or be valid.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapped(state):
            if name not in state.ops:
                return
            for x in fn(state):
                yield x
        return wrapped
    return decorator


def once(name):
    def decorator(fn):
        @wraps(fn)
        def wrapped(state, *a):
            if name in state.ops:
                return
            state = state.add_op(name)
            try:
                for x in fn(state, *a):
                    yield x
            except TypeError:
                for x in fn(state):
                    yield x
        return wrapped
    return decorator
