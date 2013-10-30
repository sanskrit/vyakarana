import vyakarana.filters as F
from vyakarana.upadesha import *


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
    return filt(term, None, None)


def pratyaya_tester(filt, data):
    return filt(Pratyaya(data), None, None)


def dhatu_tester(filt, data):
    return filt(Dhatu(data), None, None)



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



def test_it_samjna():
    cases = [
        (['kit', 'Nit'],
            'kta ktvA iyaN uvaN kvasu~',
            'GaY ap yat anIyar',
        )
    ]
    verify(cases, F.samjna, pratyaya_tester)


def test_lakshana():
    cases = [
        (['la~w', 'li~w'],
            'la~w li~w',
            'lu~w lo~w',
        )
    ]
    verify(cases, F.lakshana, pratyaya_tester)


def test_raw():
    cases = [
        (['jYA\\', 'janI~\\'],
            'jYA\\ janI~\\',
            'gamx~ SF dF pF',
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
            assert f(Anga(y), None, None)
        for n in no.split():
            assert not f(Pratyaya(n), None, None)


def test_upadha():
    cases = [
        (['Yam'],
            'banD granT stamB pAna',
            'granTa nara nayati',
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