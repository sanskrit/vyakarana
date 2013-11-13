import vyakarana.filters as F
import vyakarana.lists as L
from vyakarana.upadesha import *
from vyakarana.dhatupatha import DHATUPATHA as DP


def verify(cases, filter_creator, tester):
    """Verify a filter function on some input.

    :param cases: a list of 3-tuples containing:
                  - a list of arguments to `filter_creator`
                  - a list of positive examples
                  - a list of negative examples
    :param filter_creator: a function that takes a list of *args and
                            returns a parameterized filter function.
    :param test: a function that takes a parameterized filter function
                 and an example and returns a bool.
    """
    for pattern, yes, no in cases:
        filt = filter_creator(*pattern)
        for y in yes.split():
            assert tester(filt, y)
        for n in no.split():
            assert not tester(filt, n)


def term_tester(filt, data):
    term =  Upadesha('a~').set_value(data)
    return filt([term], 0)


def pratyaya_tester(filt, data):
    return filt([Pratyaya(data)], 0)


def dhatu_tester(filt, data):
    return filt([Dhatu(data)], 0)


# Ordinary filters
# ~~~~~~~~~~~~~~~~

def test_adi():
    cases = [
        (['al'],
            'indra agni vAyu jAne agnO Bagavat Atman lih dfS',
            '',
        ),
        (['ac'],
            'indra agni agnO Atman',
            'vAyu jAne Bagavat lih dfS',
        ),
        (['hal'],
            'vAyu jAne Bagavat lih dfS',
            'indra agni agnO Atman',
        ),
        (['ec'],
            'eDa ozaDi EkzvAka Oqulomi',
            'indra agni vAyu jAne agnO Bagavat Atman lih dfS',
        ),
        (['Sar'],
            'SItala za sarpa',
            'indra agni vAyu jAne agnO Bagavat Atman lih dfS',
        ),
    ]
    verify(cases, F.adi, term_tester)


def test_al():
    cases = [
        (['al'],
            'indra agni vAyu jAne agnO Bagavat Atman lih dfS',
            '',
        ),
        (['ac'],
            'indra agni vAyu jAne agnO',
            'Bagavat Atman lih dfS',
        ),
        (['hal'],
            'Bagavat Atman lih dfS',
            'indra agni vAyu jAne agnO',
        ),
        (['ec'],
            'jAne agnO',
            'indra agni vAyu Bagavat Atman lih dfS',
        ),
        (['Sar'],
            'dfS',
            'indra agni vAyu jAne agnO Bagavat Atman lih',
        ),
    ]
    verify(cases, F.al, term_tester)


def test_gana():
    pairs = [
        ('BU', 'wvo~Svi'),
        ('a\\da~', 'hnu\N'),
        ('hu\\', 'gA\\'),
        ('divu~', 'gfDu~'),
        ('zu\Y', 'kzI'),
        ('tu\da~^', 'piSa~'),
        ('ru\Di~^r', 'pfcI~'),
        ('tanu~^', 'qukf\Y'),
        ('qukrI\Y', 'graha~^'),
        ('cura~', 'tutTa~'),
    ]
    cases = []
    for i, pair in enumerate(pairs):
         first, last = pair
         yes = ' '.join(pair)
         no = ' '.join(' '.join(p) for j, p in enumerate(pairs) if i != j)
         cases.append(([first], yes, no))

    verify(cases, F.gana, dhatu_tester)


def test_it_samjna():
    cases = [
        (['kit', 'Nit'],
            'kta ktvA iyaN uvaN kvasu~',
            'GaY ap yat anIyar',
        ),
        (['Rit'],
            'Ral Rvul',
            'tip lyuw',
        ),
    ]
    verify(cases, F.samjna, pratyaya_tester)


def test_raw():
    cases = [
        (['jYA\\', 'janI~\\'],
            'jYA\\ janI~\\',
            'gamx~ SF dF pF jYA janI janI~',
        )
    ]
    verify(cases, F.raw, dhatu_tester)


def test_samjna():
    cases = [
        (['anga'],
            'nara grAma vIra',
            'nara grAma vIra',
        )
    ]

    for pattern, yes, no in cases:
        f = F.samjna(*pattern)
        for y in yes.split():
            assert f([Anga(y)], 0)
        for n in no.split():
            assert not f([Pratyaya(n)], 0)


def test_upadha():
    cases = [
        (['Yam'],
            'banD granT stamB pAna',
            'granTa nara narAn',
        ),
        (['at'],
            'vac svap yaj',
            'granT nI paca',
        )
    ]
    verify(cases, F.upadha, term_tester)


def test_value():
    cases = [
        (['jYA', 'jan'],
            'jYA\\ janI~\\',
            'gamx~ SF dF pF',
        )
    ]
    verify(cases, F.value, dhatu_tester)


# Filter combination
# ~~~~~~~~~~~~~~~~~~

def test_and_():
    cases = [
        (['Yam'],
            'banD granT stamB',
            'car pAna granTa nara nayati',
        )
    ]
    verify(cases, lambda names: F.upadha(names) & F.al('hal'),
           term_tester)


def test_or_():
    cases = [
        (['Yam'],
            'banD granT stamB pAna car',
            'granTa nara nayati',
        )
    ]
    verify(cases, lambda names: F.upadha(names) | F.al('hal'),
           term_tester)


def test_not_():
    cases = [
        (['al'],
            '',
            'indra agni vAyu jAne agnO Bagavat Atman lih dfS',
        ),
        (['ac'],
            'Bagavat Atman lih dfS',
            'indra agni vAyu jAne agnO',
        ),
        (['hal'],
            'indra agni vAyu jAne agnO',
            'Bagavat Atman lih dfS',
        ),
        (['ec'],
            'indra agni vAyu Bagavat Atman lih dfS',
            'jAne agnO',
        ),
        (['Sar'],
            'indra agni vAyu jAne agnO Bagavat Atman lih',
            'dfS',
        ),
    ]
    verify(cases, lambda x: ~F.al(x), term_tester)


# 'auto' filter
# ~~~~~~~~~~~~~

def test_auto_on_lists():
    pairs = [
        (L.IT, F.samjna),
        (L.LA, F.lakshana),
        (L.SAMJNA, F.samjna),
        (L.SOUNDS, F.al),
        (L.TIN, F.raw),
    ]

    for items, function in pairs:
        for item in items:
            assert F.auto(item) == function(item)


def test_auto_on_dhatu():
    for item in DP.all_dhatu:
        # Ambiguity with F.al('f')
        if item == 'f':
            continue
        assert F.auto(item) == F.dhatu(item)


# Filter relationships
# ~~~~~~~~~~~~~~~~~~~~

def test_subset_of_and_or():
    """Ordinary subset ("and", "or")"""
    cases = [
        [F.al('ac'), F.samjna('dhatu'), F.upadha('Yam')]
    ]
    for filters in cases:
        intersection = F.Filter.and_(*filters)
        for f in filters:
            assert intersection.subset_of(f)

        union = F.Filter.or_(*filters)
        for f in filters:
            assert f.subset_of(union)


def test_subset_of_inference():
    """Inferential subset"""
    bhu = F.dhatu('BU')
    dhatu = F.samjna('dhatu')
    assert bhu.subset_of(dhatu)


def test_subset_of_domain():
    """Subset with different domains."""
    ak = F.auto('ak')
    ac = F.auto('ac')
    assert ak.subset_of(ac)
    assert not ac.subset_of(ak)

    dhatu = F.auto('dhatu')
    anga = F.auto('dhatu', 'anga')
    assert dhatu.subset_of(anga)
    assert not anga.subset_of(dhatu)


def test_subset_of_combined():
    """Combined subset (ordinary, inferential, domain)"""
    f = F.auto

    # Examples from 6.4.77 and 6.4.88
    snu_dhatu_bhru = f('Snu', 'dhatu', 'BrU')
    bhu = f('BU')
    assert bhu.subset_of(snu_dhatu_bhru)
    assert not snu_dhatu_bhru.subset_of(bhu)

    snu_dhatu_bhru_yv = snu_dhatu_bhru & F.al('i u')
    assert bhu.subset_of(snu_dhatu_bhru_yv)
    assert not snu_dhatu_bhru_yv.subset_of(bhu)
