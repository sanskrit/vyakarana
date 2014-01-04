from vyakarana.rules import *


def test_init():
    r = Rule('name', list('filters'), 'operator')
    assert r.name == 'name'
    assert r.filters == list('filters')
    assert r.operator == 'operator'
    assert not r.optional
    assert not r.utsarga


def test_new_paribhasha():
    pass


def test_new_samjna():
    pass


def test_new_tasmat():
    pass


def test_new_tasya():
    pass


