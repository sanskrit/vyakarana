from vyakarana.templates import *


def test_init():
    t = RuleTuple('name', 'L', 'C', 'R', 'op')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'
    assert t.base_args is None
    assert t.base_kw is None


def test_init_with_base():
    t = RuleTuple('name', 'L', 'C', 'R', 'op', base_args='args', base_kw='kw')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'
    assert t.base_args == 'args'
    assert t.base_kw == 'kw'


def test_inherit():
    @inherit('a1', 'a2', kw1='kw1', kw2='kw2')
    def rule_fn():
        return [
            ('name1', 'L', 'C', 'R', 'op1'),
            Va('name2', 'L', 'C', 'R', 'op2'),
        ]

    r1, r2 = rule_fn()
    base_args = ('a1', 'a2')
    base_kw = dict(kw1='kw1', kw2='kw2')

    # Non-wrapped
    assert r1.name == 'name1'
    assert r1.window == ['L', 'C', 'R']
    assert r1.operator == 'op1'
    assert r1.base_args == base_args
    assert r1.base_kw == base_kw
    assert isinstance(r1, RuleTuple)

    # Wrapped
    assert r2.name == 'name2'
    assert r2.window == ['L', 'C', 'R']
    assert r2.operator == 'op2'
    assert r2.base_args == base_args
    assert r2.base_kw == base_kw
    assert isinstance(r2, Option)

    assert hasattr(rule_fn, 'rule_generator')
