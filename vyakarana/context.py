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
        if term is None:
            return False
        if antya:
            return term.antya().value in sounds
        else:
            return term.adi in sounds
    return func


def it(*names):
    def func(term, **kw):
        return term is not None and any(n in term.it for n in names)
    return func


def lakshana(*names):
    def func(term, **kw):
        return term is not None and any(n in term.lakshana for n in names)
    return func


def raw(*names):
    names = frozenset(names)
    def func(term, **kw):
        return term is not None and term.raw in names
    return func


def samjna(*names):
    def func(term, **kw):
        return term is not None and any(n in term.samjna for n in names)
    return func


def upadha(*names):
    sounds = Sounds(*names)
    def func(term, **kw):
        return term is not None and term.upadha().value in sounds
    return func


def value(*names):
    names = frozenset(names)
    def func(term, **kw):
        return term is not None and term.value in names
    return func


def and_(*functions):
    def func(term, **kw):
        return all(f(term, **kw) for f in functions)
    return func


def or_(*functions):
    def func(term, **kw):
        return any(f(term, **kw) for f in functions)
    return func


def Sit_adi(term):
    return term is not None and term.raw and term.raw[0] == 'S'
