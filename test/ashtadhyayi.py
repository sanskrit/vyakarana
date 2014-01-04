from vyakarana.ashtadhyayi import Ashtadhyayi


def test_init():
    a = Ashtadhyayi()
    assert a.rules
    assert a.ranked_rules
    assert a.rule_tree
