# -*- coding: utf-8 -*-
"""
    vyakarana.decorators
    ~~~~~~~~~~~~~~~~~~~~

    Various decocators.

    :license: MIT and BSD
"""

from functools import wraps
from classes import Option

# New-style rules. Temporary.
NEW_RULES = []

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


def new_window(left_ctx, cur_ctx, right_ctx):
    # If ctx is ``None`` or undefined, it's trivially true.
    left_ctx = left_ctx or always_true
    cur_ctx = cur_ctx or always_true
    right_ctx = right_ctx or always_true

    def matches(state, i):
        left, cur, right = state.window(i)
        return left_ctx(left) and cur_ctx(cur) and right_ctx(right)

    def decorator(fn):
        @wraps(fn)
        def wrapped(state, i):
            left, cur, right = state.window(i)
            result = fn(left, cur, right)
            if result is not None:
                yield state.swap_window(i, result)

        wrapped.matches = matches
        NEW_RULES.append(wrapped)
        return wrapped
    return decorator


def tasmat(left_ctx, right_ctx):
    """Decorator for rules that perform insertion after a single term.

    :param left_ctx: a context function that matches what comes before
                     the insertion. If ``None``, accept all contexts.
    :param right_ctx: a context function that matches what comes after
                     the insertion. If ``None``, accept all contexts.
    """
    left_ctx = left_ctx or always_true
    right_ctx = right_ctx or always_true

    def matches(state, i):
        left, right, _ = state.window(i)
        return left_ctx(left) and right_ctx(right)

    function_id = len(NEW_RULES)

    def decorator(fn):
        @wraps(fn)
        def wrapped(state, i):
            # If previously applied, reject and avoid looping.
            # TODO: find more elegant way to control this
            if function_id in state.ops:
                return

            left, right, _ = state.window(i)
            result = fn(left, right)
            if result is None:
                return

            for r in result:
                if r is not None:
                    yield state.insert(i, r).add_op(function_id)


        wrapped.matches = matches
        NEW_RULES.append(wrapped)
        return wrapped
    return decorator


def tasya(left_ctx, cur_ctx, right_ctx):
    """Decorator for rules that perform substitution on a single term.

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

    def matches(state, i):
        left, cur, right = state.window(i)
        return left_ctx(left) and cur_ctx(cur) and right_ctx(right)

    # Unique ID for this function, since functions are added sequentially
    # to a single shared list. This is used to mark certain terms with
    # the operations applied to them. For example, if an optional rule
    # is rejected, we mark the result to prevent applying that rule
    # again.
    function_id = len(NEW_RULES)

    def decorator(fn):
        @wraps(fn)
        def wrapped(state, i):
            left, cur, right = state.window(i)
            result = fn(left, cur, right)
            if result is None:
                return

            # Optional substitution
            if isinstance(result, Option):
                if function_id in cur.ops:
                    return
                # declined
                yield state.swap_window(i, (left, cur.add_op(function_id), right))
                # accepted
                result = result.data

            # Operator substitution
            if hasattr(result, '__call__'):
                new_cur = result(cur, right=right)

            # Other substitution
            else:
                new_cur = cur.tasya(result)

            if (left, new_cur, right) != (left, cur, right):
                yield state.swap_window(i, (left, new_cur, right))

        wrapped.matches = matches
        NEW_RULES.append(wrapped)
        return wrapped
    return decorator
