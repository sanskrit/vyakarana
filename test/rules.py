from vyakarana.rules import *


def test_init():
    r = Rule('name', 'filters', 'operator', rank='rank')
    assert r.name == 'name'
    assert r.filters == 'filters'
    assert r.operator == 'operator'
    assert r.rank == 'rank'
    assert not r.option
    assert not r.utsarga


def test_new_paribhasha():
    pass


def test_new_samjna():
    pass


def test_new_tasmat():
    pass


def test_new_tasya():
    pass


