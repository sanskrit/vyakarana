import vyakarana.dhatupatha as D


def test_init():
    d = D.Dhatupatha()
    assert not d.gana_map
    assert not d.all_dhatu
    assert not d.index_map


def test_init_with_filename():
    d = D.Dhatupatha(D.DHATUPATHA_CSV)
    assert d.gana_map
    assert d.all_dhatu
    assert d.index_map


def test_dhatu_list():
    cases = [
        # 6.1.15
        ('ya\\ja~^', None, 9),
        # 6.4.125
        ('PaRa~', 'svana~', 7),
        # 7.3.74
        ('Samu~', 'madI~', 8),
        # 7.3.80
        ('pUY', 'plI\\', 25),
    ]
    d = D.Dhatupatha(D.DHATUPATHA_CSV)
    for start, end, expected_len in cases:
        results = d.dhatu_list(start, end)
        assert len(results) == expected_len
