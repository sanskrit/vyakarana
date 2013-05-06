# -*- coding: utf-8 -*-
"""
    vyakarana.classes
    ~~~~~~~~~~~~~~~~~

    Classes for working with various sounds and terms.

    :license: MIT and BSD
"""

import re

from sanskrit import sounds


class Sound(object):

    """A Sanskrit sound.

    These sounds can be transformed in ways defined by the grammar."""

    #: This organizes sounds by their point of articulation.
    ASYA = [
        # kaṇṭha
        set('aAkKgGNh'),
        # tālu
        set('iIcCjJYy'),
        # mūrdhan
        set('fFwWqQRr'),
        # danta
        set('xXtTdDnl'),
        # oṣṭha
        set('uUpPbBmv'),
        # kaṇṭha-tālu
        set('eE'),
        # kaṇṭha-oṣṭha
        set('oO'),
        # pure nasal
        set('M')
    ]

    #: This organizes sounds by their articulatory effort.
    PRAYATNA = [
        # spṛṣṭa
        set('kKgGNcCjJYwWqQRtTdDnpPbBmh'),
        # īṣatspṛṣṭa
        set('yrlv'),
        # śar
        set('Szs'),
        # vowels
        set('aAiIuUfFxeEoO'),
    ]

    #: This organizes sounds by their nasality.
    NASIKA = [
        # nasal
        set('NYRnmM'),
        # non-nasal
        set('aAiIuUfFxeEoOkKgGcCjJwWQQtTdDpPbByrlvSzsh'),
    ]

    #: This organizes sounds by their "voice."
    GHOSA = [
        # ghoṣavat (voiced)
        set('aAiIuUfFxXeEoOgGNjJYqQRdDnbBmyrlvh'),
        # aghoṣa (unvoiced)
        set('kKcCwWtTpPSzs'),
    ]

    #: This organizes sounds by their aspiration.
    PRANA = [
        # mahāprāṇa (aspirated)
        set('KGCJWQTDPBh'),
        # alpaprāṇa (unaspirated)
        set('aAiIuUfFxXeEoOkgNcjYwqRtdnpbmyrlvSzs'),
    ]

    def __init__(self, value):
        self.value = value

    def closest(self, items):
        best = self.value
        best_score = 0

        self_names = self.names()
        for x in items:
            score = len(Sound(x).names().intersection(self_names))
            if score > best_score:
                best, best_score = x, score
        return best

    def names(self):
        """Get the various designations that apply to this sound. This
        is used to determine how similar two sounds are to each other.
        """
        items = set()

        categories = [self.ASYA, self.PRAYATNA, self.NASIKA, self.GHOSA,
                      self.PRANA]
        for i, category in enumerate(categories):
            for j, group in enumerate(category):
                if self.value in group:
                    items.add('%s_%s' % (i, j))
        return items

    def savarna_set(self):
        """Return the sounds that are savarna to this one.

        1.1.19 tulyAsyaprayatnaM savarNam
        1.1.20 najjhalau
        """
        s = self.value
        a = p = None
        for a in self.ASYA:
            if s in a:
                break
        for p in self.PRAYATNA:
            if s in p:
                break
        if a is None:
            a = p
        elif p is None:
            p = a

        results = a.intersection(p)
        is_ac = s in Pratyahara('ac')

        # 1.1.10 na ac-halau
        return set([x for x in results if (x in Pratyahara('ac')) == is_ac])

    def asavarna(self, other):
        """

        :param other:
        """
        ac = Pratyahara('ac')
        same_ac = self.value in ac and other in ac
        return same_ac and other not in self.savarna_set()

    def parasavarna(self, other):
        """

        :param other:
        """
        return self.closest(Sound(other).savarna_set())

    def savarna(self, other):
        """

        :param other:
        """
        return other in self.savarna_set()


class Group(object):
    def __init__(self, phrase):
        v = self.values = set()
        for item in phrase.split():

            first, last = (item[0], item[-1])
            simple_vowel = len(item) == 1 and item in Pratyahara('aR')

            # 1.1.69 aNudit savarNasya cApratyayaH
            if last == 'u' or simple_vowel:
                v.update(Sound(first).savarna_set())
            # 1.1.70 taparas tatkAlasya
            elif last == 't':
                v.update([first])
            elif len(item) == 1:
                v.update(item)
            else:
                v.update(Pratyahara(item).letters)

    def __contains__(self, item):
        return item in self.values

    def __iter__(self):
        return iter(self.values)


class Pratyahara(object):

    """A shorthand for grouping Sanskrit sounds.

    The various pratyaharas are defined in the Shiva Sutras, which
    precede the Ashtadhyayi proper.

    :param value: the pratyahara itself, e.g. 'hal', 'ak', 'Jal'
    :param second_R: ``True`` iff we should use the second 'R' as our
                     boundary. Since pratyaharas formed with this letter
                     are usually ambiguous, we have to be explicit here.
    """

    rules = [
        ('aAiIuU', 'R'),
        ('fFxX', 'k'),
        ('eo', 'N'),
        ('EO', 'c'),
        ('hyvr', 'w'),
        ('l', 'R'),
        ('YmGRn', 'm'),
        ('JB', 'Y'),
        ('GQD', 'z'),
        ('jbgqd', 'S'),
        ('KPCWTcwt', 'v'),
        ('kp', 'y'),
        ('Szs', 'r'),
        ('h', 'l'),
    ]

    def __init__(self, value, second_R=False):
        first = value[0]
        limit = value[-1]
        found_first = False

        self.letters = set([first])

        for items, it in self.rules:
            if found_first:
                self.letters.update(items)
            elif first in items:
                self.letters.update(items.partition(first)[-1])
                found_first = True
            if limit == it:
                if second_R:
                    second_R = False
                else:
                    break

    def __contains__(self, key):
        return key in self.letters


class Term(object):

    def __init__(self, value):
        #: the human-readable (no anubandhas) version of this term
        self.value = value

        #: the technical designations that apply to this term
        self.samjna = set()

        #: the names that refer to this term. For example an operation
        #: conditioned by "lit" is also condition by "Nal", since "Nal"
        #: comes frot "lit".
        #:
        #: This term comes from 1.1.62:
        #:
        #:     1.1.62 pratyayalope pratyayalakSaNam
        #:
        #: Technically, it applies only to a pratyaya. But it's been
        #: useful in other contexts so far.
        self.lakshana = set()

        #: The components that constitute this term. For example, the
        #: Term 'BUv' might have two parts: the root 'BU' and the
        #: augment 'v' (from 'vu~k').
        self.parts = [self]

    def __eq__(self, other):
        raise NotImplementedError

    def __nonzero__(self):
        return bool(self.value)

    def __getitem__(self, i):
        return Term(self.value[i])

    def __getslice__(self, i, j):
        return Term(self.value[i:j])

    def __repr__(self):
        return "<{0}('{1}')>".format(self.__class__.__name__, self.value)

    def copy(self):
        cls = self.__class__
        c = cls(self.value)
        c.samjna = self.samjna.copy()
        c.lakshana = self.lakshana.copy()
        c.parts = self.parts[:]
        return c

    @property
    def ac(self):
        """True iff the term ends in a vowel.

        """
        return self[-1].value in Pratyahara('ac')

    @property
    def dirgha(self):
        """True iff the term ends in a long vowel.

        """
        return self[-1].value in sounds.LONG_VOWELS

    @property
    def ec(self):
        """True iff the term ends in an 'ec' vowel.

        """
        return self[-1].value in Pratyahara('ec')

    @property
    def hal(self):
        """True iff the term ends in a consonant.

        """
        return self[-1].value in Pratyahara('hal')

    @property
    def ik(self):
        """True iff the term ends in an 'ik' vowel.

        """
        return self[-1].value in Pratyahara('ik')

    @property
    def guru(self):
        """True iff the end of the term is called 'guru'.

        1.4.11 saMyoge guru
        1.4.12 dIrghaM ca
        """
        return self.samyoga or self.dirgha

    @property
    def hrasva(self):
        """True iff the term ends in a short vowel.

        """
        return self[-1].value in sounds.SHORT_VOWELS

    @property
    def laghu(self):
        """True iff the end of the term is called 'laghu'.

        1.4.10 hrasvaM laghu
        """
        return self.hrasva

    @property
    def num_syllables(self):
        return sounds.num_syllables(self.value)

    @property
    def one_syllable(self):
        """True iff the term has exactly one syllable."""
        return self.num_syllables == 1

    @property
    def samyoga(self):
        """True iff the end of the term is called 'samyoga'.

        1.1.7 halo 'nantarAH saMyogaH
        """
        try:
            cons = sounds.CONSONANTS
            return self.value[-1] in cons and self.value[-2] in cons
        except IndexError:
            return False

    @property
    def samyogadi(self):
        """True iff the end of the term is called 'samyoga'.

        1.1.7 halo 'nantarAH saMyogaH
        """
        try:
            cons = sounds.CONSONANTS
            return self.value[0] in cons and self.value[1] in cons
        except IndexError:
            return False

    def adi(self, replacement=None):
        if replacement is not None:
            c = self.copy()
            c.value = replacement + c.value[1:]
            c.parts = [c]
            return c
        else:
            return Term(self.value[0])

    def add_samjna(self, *names):
        """

        :param name:
        """
        c = self.copy()
        for name in names:
            c.samjna.add(name)
        return c

    def add_lakshana(self, term):
        c = self.copy()
        c.lakshana.add(term)
        return c

    def antya(self, replacement=None):
        if replacement is not None:
            c = self.copy()
            c.value = c.value[:-1] + replacement
            c.parts = [c]
            return c
        else:
            return Term(self.value[-1])

    def deaspirate(self):
        c = self.copy()
        c.value = sounds.deaspirate(c.value[0]) + c.value[1:]
        return c

    def guna(self):
        """Apply guna. But if the term ends in a conjunct consonant,
        do nothing.

        1.1.2 adeG guNaH
        """
        letters = list(self.value[::-1])
        for i, L in enumerate(letters):
            if i > 1:
                break
            if i == 1 and L in sounds.LONG_VOWELS:
                break
            if L in sounds.VOWELS:
                letters[i] = sounds.guna(letters[i])
                break
        value = ''.join(reversed(letters))
        return self.set_value(value)

    def lopa(self):
        """
        Apply 'lopa' to this term.

        1.1.60 adarzanaM lopaH
        1.1.62 pratyayalope pratyayalakSaNa
        """
        return self.set_value('')

    def replace(self, x, y):
        """Replace all instances of `x` with `y`.

        :param x: the string to replace
        :param y: the string replacement
        """
        c = self.copy()
        c.value = c.value.replace(x, y)
        return c

    def reverse(self):
        c = self.copy()
        c.value = c.value[::-1]
        return c

    def samprasarana(self):
        value = self.value
        letters = list(value)

        for i, L in enumerate(letters):
            if L in Pratyahara('ac'):
                samp = sounds.samprasarana(letters[i-1])
                value = value[:i-1] + samp + value[i+1:]
                return self.set_value(value)

        return self

    def savarna(self, other):
        first = self[-1].value
        second = other[0].value
        ak = Pratyahara('ak')
        if first in ak and second in ak and first.lower() == second.lower():
            return True
        else:
            return False

    def set(self, i, value):
        """Replace the letter at index `i` with `value`."""
        c = self.copy()
        letters = list(c.value)
        letters[i] = value
        c.value = ''.join(letters)
        c.parts = [c]
        return c

    def set_value(self, value):
        c = self.copy()
        c.value = value
        c.parts = [c]
        return c

    def tasmat(self, other):
        """

            1.1.67 tasmAd ityuttarasya

        :param other:
        """
        c = self.copy()
        c.value = c.value + other.value
        c.parts = c.parts + other.parts
        return c

    def tasmin(self, other):
        """

            1.1.67 tasminniti nirdiSTe pUrvasya

        :param other:
        """
        c = self.copy()
        c.value = other.value + c.value
        c.parts = other.parts + c.parts
        return c

    def tasya(self, other):
        """

        :param other:
        """
        c = self.copy()
        if 'k' in other.it:
            c.value += other.value
            c.parts.append(other)
        elif 'w' in other.it:
            c.value = other.value + c.value
            c.parts.insert(0, other)
        elif 'N' in other.it:
            c.value = self.value[:-1] + other.value
            c.parts.append(other)
        elif 'm' in other.it:
            raise NotImplementedError
        else:
            raise NotImplementedError
        return c

    def ti(self, replacement=None):
        """The portion starting with the last vowel.

        1.1.64 aco 'ntyAdi ti
        """
        splits = re.split('([%s])' % ''.join(sounds.VOWELS), self.value)
        c = self.copy()

        if replacement is None:
            c.value = ''.join(splits[-2:])
        else:
            c.value = ''.join(splits[:-2]) + replacement
        return c

    def to_hrasva(self):
        return self.antya(sounds.shorten(self.value[-1]))

    def to_dirgha(self):
        return self.antya(sounds.lengthen(self.value[-1]))

    def to_yan(self):
        return self.antya(sounds.semivowel(self.value[-1]))

    def upadha(self, replacement=None):
        """The penult."""
        length = len(self.value)
        if length > 1:
            if replacement is not None:
                c = self.copy()
                letters = list(c.value)
                letters[-2] = replacement
                c.value = ''.join(letters)
                c.parts = [c]
                return c
            else:
                return Term(self.value[-2])
        else:
            return Term('')

    def vrddhi(self):
        """Apply vrddhi."""
        c = self.copy()
        letters = list(self.value[::-1])
        for i, L in enumerate(letters):
            if L in sounds.VOWELS:
                letters[i] = sounds.vrddhi(letters[i])
                break
        return c.set_value(''.join(reversed(letters)))


class Upadesha(Term):

    """A Term with indicatory letters."""

    nasal_re = re.compile('([aAiIuUfFxeEoO]~)')

    def __init__(self, raw=None, **kw):
        Term.__init__(self, raw or '')
        self.raw = None
        self.value = None
        self.it = set()
        if raw:
            self._update(raw, **kw)

    def copy(self):
        c = self.__class__(raw=None)
        c.raw = self.raw
        c.value = self.value
        c.samjna = self.samjna.copy()
        c.lakshana = self.lakshana.copy()
        c.parts = self.parts[:]
        c.it = self.it.copy()
        return c

    def add_it(self, letters):
        c = self.copy()
        c.it.update(letters)
        return c

    def remove_it(self, letters):
        c = self.copy()
        c.it.difference_update(letters)
        return c

    def _update(self, raw, **kw):

        if '^' in raw:
            self.it.add('udatta')
            raw = raw.replace('^', '')
        if '\\' in raw:
            self.it.add('anudatta')
            raw = raw.replace('\\', '')

        self.raw = raw
        core = raw

        vibhakti = kw.pop('vibhakti', False)
        pratyaya = kw.pop('pratyaya', False)
        taddhita = kw.pop('taddhita', False)

        # "ir" is not listed as an 'it' but is treated as one, e.g.
        # 'irito vā'
        irit = False
        if raw.endswith('i~r'):
            core = core[:-3]
            self.it.add('ir')
            irit = True

        # 1.3.2 "upadeśe 'janunāsika iṭ"
        results = self.nasal_re.split(core)
        core = ''.join(results[::2])
        self.it = self.it.union(results[1::2])

        # 1.3.3 "hal antyam"
        if raw[-1] in sounds.CONSONANTS and not vibhakti and not irit:
            self.it.add(raw[-1])
            core = core[:-1]

        # 1.3.4 "na vibhaktau tusmāḥ"
        elif vibhakti:
            L = raw[-1]
            if L in sounds.CONSONANTS and L not in 'tTdDnsm':
                self.it.add(L)
                core = core[:-1]

        # 1.3.5 "ādir ñituḍavaḥ"
        if any(raw.startswith(x) for x in ('Yi', 'wu', 'qu')):
            self.it.add(raw[:2])
            core = core[2:]

        # 1.3.6 "ṣaḥ pratyayasya"
        # 1.3.7 "cuṭū"
        if pratyaya:
            if raw[0] in 'zcCjJYwWqQR':
                self.it.add(raw[0])
                core = core[1:]

            # 1.3.8 "laśakv ataddhite"
            if not taddhita:
                if raw[0] in 'lSkKgGN':
                    self.it.add(raw[0])
                    core = core[1:]

        # 1.3.9 "tasya lopaḥ"
        self.value = core
        self.lakshana.add(raw)
        self.parts = [self]

    def update(self, raw, **kw):
        c = self.copy()
        c._update(raw, **kw)
        return c


# Bases
# -----

class Anga(Upadesha):
    def _update(self, value, **kw):
        Upadesha._update(self, value, **kw)
        self.samjna.add('anga')


class Dhatu(Anga):
    """
    An Upadesha that describes a verb root
    """
    def __init__(self, *a, **kw):
        Upadesha.__init__(self, *a, **kw)
        value = self.value
        if not value:
            return

        # 6.1.64 dhAtvAdeH SaH saH
        if value.startswith('z'):
            value = 's' + value[1:]
            # paribhasha: nimittApAye naimittikasya api apAyaH
            converter = {'w': 't', 'W': 'T'}
            v = value[1]
            value = value[0] + converter.get(v, v) + value[2:]

        # 6.1.65 No naH
        elif value.startswith('R'):
            value = 'n' + value[1:]

        if value != self.value:
            self.value = value

        self.clean = value

    def copy(self):
        c = super(Anga, self).copy()
        c.clean = self.clean
        return c

    def _update(self, value, **kw):
        Anga._update(self, value, **kw)
        self.samjna.add('dhatu')


# Suffixes
# --------

class Pratyaya(Upadesha):
    def _update(self, value, **kw):
        Upadesha._update(self, value, pratyaya=True, **kw)
        self.samjna.add('pratyaya')


class Krt(Pratyaya):
    def _update(self, value, **kw):
        Pratyaya._update(self, value, pratyaya=True, **kw)
        self.samjna.add('krt')


class Vibhakti(Pratyaya):
    def _update(self, raw, **kw):
        value = raw.replace('J', 'ant')
        Pratyaya._update(self, value, vibhakti=True, **kw)
        self.samjna.add('vibhakti')
        self.raw = raw
