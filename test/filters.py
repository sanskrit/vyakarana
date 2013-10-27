from vyakarana.classes import *
from vyakarana.context import *


def verify(cases, context_creator, test):
    """Verify a context function on some input.

    :param cases: a list of 3-tuples containing:
                  - a list of arguments to `context_creator`
                  - a list of positive examples
                  - a list of negative examples
    :param context_creator: a function that takes a list of *args and
                            returns a parameterized context function.
    :param test: a function that takes a parameterized context function
                 and an example and returns a bool.
    """
    for pattern, yes, no in cases:
        context = context_creator(*pattern)
        for y in yes.split():
            assert test(context, y)
        for n in no.split():
            assert not test(context, n)


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
    verify(cases, adi, lambda f, x: f(Term(x)))


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
    verify(cases, al, lambda f, x: f(Term(x)))



def test_it():
    cases = [
        (['k', 'N'],
            'kta ktvA iyaN uvaN kvasu~',
            'GaY ap yat anIyar',
        )
    ]
    verify(cases, it, lambda f, x: f(Pratyaya(x)))


def test_lakshana():
    cases = [
        (['la~w', 'li~w'],
            'la~w li~w',
            'lu~w lo~w',
        )
    ]
    verify(cases, lakshana, lambda f, x: f(Pratyaya(x)))


def test_raw():
    cases = [
        (['jYA\\', 'janI~\\'],
            'jYA\\ janI~\\',
            'gamx~ SF dF pF',
        )
    ]
    verify(cases, raw, lambda f, x: f(Dhatu(x)))


def test_samjna():
    cases = [
        (['anga'],
            'nara grAma vIra',
            'nara grAma vIra',
        )
    ]

    for pattern, yes, no in cases:
        f = samjna(*pattern)
        for y in yes.split():
            assert f(Anga(y))
        for n in no.split():
            assert not f(Pratyaya(n))


def test_upadha():
    cases = [
        (['Yam'],
            'banD granT stamB pAna',
            'granTa nara nayati',
        )
    ]
    verify(cases, upadha, lambda f, x: f(Term(x)))


def test_value():
    cases = [
        (['jYA', 'jan'],
            'jYA\\ janI~\\',
            'gamx~ SF dF pF',
        )
    ]
    verify(cases, value, lambda f, x: f(Dhatu(x)))


def test_and_():
    cases = [
        (['Yam'],
            'banD granT stamB',
            'car pAna granTa nara nayati',
        )
    ]
    verify(cases, lambda names: and_(upadha(names), al('hal')),
           lambda f, x: f(Term(x)))


def test_or_():
    cases = [
        (['Yam'],
            'banD granT stamB pAna car',
            'granTa nara nayati',
        )
    ]
    verify(cases, lambda names: or_(upadha(names), al('hal')),
           lambda f, x: f(Term(x)))