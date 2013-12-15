# -*- coding: utf-8 -*-
"""
    vyakarana.templates
    ~~~~~~~~~~~~~~~~~~~

    This module contains classes and functions that let us define
    the Ashtadhyayi's rules as tersely as possible.

    :license: MIT and BSD
"""


class RuleTuple(object):

    """Wrapper for tuple rules.

    The Ashtadhyayi uses a variety of terms to control when and how a
    rule applies. For example, 'anyatarasyām' denotes that a rule
    specifies an optional operation that can be accepted or rejected.

    In this system, these terms are marked by wrapping a rule in this
    class or one of its subclasses.
    """

    def __init__(self, name, left, center, right, op, **kw):
        #: Thte rule name
        self.name = name

        #: The rule context
        self.window = [left, center, right]

        #: The rule operator
        self.operator = op

        #: Inherited args. These define base filters.
        self.base_args = kw.pop('base_args', None)

        #: Inherited kwargs. These control how the rule is interpreted.
        self.base_kw = kw.pop('base_kw', None)

    def __repr__(self):
        cls_name = self.__class__.__name__
        if cls_name == 'RuleTuple':
            cls_name = 'R'
        return '<%s(%s)>' % (cls_name, repr(self.name))


class Boost(RuleTuple):

    """A hack that artificially boosts a rule's priority."""


class Ca(RuleTuple):

    """Wrapper for a rule that contains the word "ca".

    "ca" has a variety of functions, but generally it preserves parts
    of the previous rule in the current rule.
    """


class Na(RuleTuple):

    """Wrapper for a rule that just blocks other rules."""


class Nityam(RuleTuple):

    """Wrapper for a rule that cannot be rejected.

    This is used to cancel earlier conditions.
    """


class Option(RuleTuple):

    """Wrapper for a rule that can be accepted optionally.

    This is a superclass for a variety of optional conditions.
    """


class Anyatarasyam(Option):

    """Wrapper for a rule that is indifferently accepted.

    Modern scholarship rejects the traditional definition of anyatarasyām,
    but this system treats it as just a regular option.
    """


class Va(Option):

    """Wrapper for a rule that is preferably accepted.

    Modern scholarship rejects the traditional definiton of vā, but
    this system treats it as just a regular option.
    """


class Vibhasha(Option):

    """Wrapper for a rule that is preferably not accepted.

    Modern scholarship rejects the traditional definiton of vibhāṣā,
    but this system treats it as just a regular option.
    """


class Artha(Option):

    """Wrapper for a rule that applies only in some semantic condition.

    Since the semantic condition can be declined, this is essentially
    an optional provision.
    """


class Opinion(Option):

    """Wrapper for a rule that is accepted by prior opinion.

    Since the opinion can be declined, this is essentially the same as
    an optional provision.
    """


#: Signals use of the *śeṣa* device, which affects utsarga-apavāda
#: inference.
Shesha = object()


# Rule decorator
# ~~~~~~~~~~~~~~

def inherit(*args, **kw):
    """Decorator for functions that define rule tuples.

    This decorator is used to mark functions that return a list of rule
    tuples. The decorator takes three arguments, each of which is a
    *base filter* that is "and"-ed with the rules contained in the
    function itself. The decorator also accepts various keyword
    arguments, which are attached to the rule tuples and used later on
    when the tuples are expanded into actual rules.
    """

    def decorator(fn):
        def get_processed_rows():
            processed_rows = []
            unprocessed_rows = fn()

            for item in unprocessed_rows:
                if isinstance(item, RuleTuple):
                    row = item
                else:
                    row = RuleTuple(*item)

                # Attach args from 'inherit'
                row.base_args = args
                row.base_kw = kw

                processed_rows.append(row)
            return processed_rows

        get_processed_rows.rule_generator = True
        return get_processed_rows
    return decorator
