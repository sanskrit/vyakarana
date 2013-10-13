# -*- coding: utf-8 -*-
"""
    vyakarana.context
    ~~~~~~~~~~~~~~~~~



    :license: MIT and BSD
"""

from classes import Sounds


def al(*names):
    sounds = Sounds(*names)
    def func(term, antya=True):
        if antya:
            return term.antya().value in sounds
        else:
            return term.adi().value in sounds
    return func


def it(*names):
    def func(term, **kw):
        return any(n in term.it for n in names)
    return func


def lakshana(*names):
    def func(term, **kw):
        return any(n in term.lakshana for n in names)
    return func


def raw(*names):
    names = frozenset(names)
    def func(term, **kw):
        return term.raw in names
    return func


def samjna(*names):
    def func(term, **kw):
        return any(n in term.samjna for n in names)
    return func


def upadha(*names):
    sounds = Sounds(*names)
    def func(term, **kw):
        return term.upadha().value in sounds
    return func


def value(*names):
    names = frozenset(names)
    def func(term, **kw):
        return term.value in names
    return func


def and_(*functions):
    def func(term, **kw):
        return all(f(term, **kw) for f in functions)
    return func


def or_(*functions):
    def func(term, **kw):
        return any(f(term, **kw) for f in functions)
    return func
