from vyakarana.dhatupatha import DHATUPATHA as DP


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
    for start, end, expected_len in cases:
        results = DP.dhatu_list(start, end)
        assert len(results) == expected_len
