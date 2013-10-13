# -*- coding: utf-8 -*-
"""
    vyakarana.decorators
    ~~~~~~~~~~~~~~~~~~~~

    Various decocators.

    :license: MIT and BSD
"""

from functools import wraps
from classes import *


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


def make_rule_decorator(module_name):
    """Create a special decorator for marking functions as rules.

    :param module_name: the name associated with the calling module.
    """

    rule_list = []
    def rule_decorator(fn):
        rule_list.append(fn)
        return fn

    return rule_decorator, rule_list


def always_true(*a, **kw):
    return True


def tasya(left_ctx, cur_ctx, right_ctx):
    """Decorator for rules that perform substitution ('tasya').

    :param left_ctx: a context function that matches what comes before
                     the sthAna. If ``None``, accept all contexts.
    :param cur_ctx: a context function that matches the sthAna.
                    If ``None``, accept all contexts.
    :param right_ctx: a context function that matches what comes after
                     the sthAna. If ``None``, accept all contexts.
    """
    # If ctx is ``None`` or undefined, it's trivially true.
    left_ctx = left_ctx or always_true
    cur_ctx = cur_ctx or always_true
    right_ctx = right_ctx or always_true

    def matches(left, cur, right):
        return left_ctx(left) and cur_ctx(cur) and right_ctx(right)

    def decorator(fn):
        @wraps(fn)
        def wrapped(left, cur, right):
            result = fn(left, cur, right)

            if isinstance(result, basestring):
                # 1.1.52 alo 'ntyasya
                # 1.1.53 Gic ca (TODO)
                if len(result) == 1:
                    cur = cur.antya(result)
                # 1.1.55 anekAlSit sarvasya
                else:
                    cur = cur.set_value(result)
            else:
                # 1.1.50 sthAne 'ntaratamaH
                last = Sound(cur.antya().value).closest(result)
                cur = cur.antya(last)

            return (left, cur, right)

        wrapped.matches = matches
        return wrapped
    return decorator
