# -*- coding: utf-8 -*-
"""
    vyakarana.templates
    ~~~~~~~~~~~~~~~~~~~

    This module contains classes and functions that let us define
    the Ashtadhyayi's rules as tersely as possible.

    :license: MIT and BSD
"""


class RuleStub(object):

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

    @property
    def center(self):
        return self.window[1]

    def __repr__(self):
        cls_name = self.__class__.__name__
        if cls_name == 'RuleStub':
            cls_name = 'R'
        return '<%s(%s)>' % (cls_name, repr(self.name))


class Adhikara(RuleStub):

    def __init__(self, name, end, on_tuple=None):
        RuleStub.__init__(self, name, None, None, None, None)
        self.end = end
        self.on_tuple = on_tuple

    def transform_tuple(self, rule_tuple):
        if self.on_tuple is None:
            return rule_tuple
        return self.on_tuple(rule_tuple)


class Ca(RuleStub):

    """Wrapper for a rule that contains the word "ca".

    "ca" has a variety of functions, but generally it preserves parts
    of the previous rule in the current rule.
    """


class Na(RuleStub):

    """Wrapper for a rule that just blocks other rules."""


class Nityam(RuleStub):

    """Wrapper for a rule that cannot be rejected.

    This is used to cancel earlier conditions.
    """


class Option(RuleStub):

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


class Anuvrtti(object):
    def __init__(self, left=None, center=None, right=None, **kw):
        self.base_args = [left, center, right]
        self.base_kw = kw


#: Signals use of the *śeṣa* device, which affects utsarga-apavāda
#: inference.
Shesha = object()
