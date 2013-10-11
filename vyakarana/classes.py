# -*- coding: utf-8 -*-
"""
    vyakarana.classes
    ~~~~~~~~~~~~~~~~~

    Classes for working with various sounds and terms.

    :license: MIT and BSD
"""

import re

from sanskrit import sounds


def memoize(c):
    cache = {}
    get_key = lambda a, kw: tuple(a) + (frozenset(kw.items()),)
    def memoized(*a, **kw):
        key = get_key(a, kw)
        if key not in cache:
            cache[key] = c(*a, **kw)
        return cache[key]
    return memoized


@memoize
class Sound(object):

    """A Sanskrit sound.

    These sounds can be transformed in ways defined by the grammar.

    :param value: the Sound's value
    """

    #: This organizes sounds by their point of articulation.
    ASYA = [
        # kaṇṭha
        set('aAkKgGNh'),
        # tālu
        set('iIcCjJYyS'),
        # mūrdhan
        set('fFwWqQRrz'),
        # danta
        set('xXtTdDnls'),
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

    def asavarna(self, other):
        """Returns the sounds that are not savarna to this one.

        One subtle point here is that the 'savarna' and 'asavarna' are
        both undefined between consonants and vowels.

        :param other:
        """
        ac = Pratyahara('ac')
        same_ac = self.value in ac and other in ac
        return same_ac and other not in self.savarna_set

    def closest(self, items):
        """Return the phonetically closest value. If no close value
        exists, return `self.value`.

        :param items: a list of letters
        """
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
        try:
            return self._names
        except AttributeError:
            pass

        self._names = set()
        categories = [self.ASYA, self.PRAYATNA, self.NASIKA, self.GHOSA,
                      self.PRANA]
        for i, category in enumerate(categories):
            for j, group in enumerate(category):
                if self.value in group:
                    self._names.add('%s_%s' % (i, j))

        return self._names

    def savarna(self, other):
        """

        :param other: some sound
        """
        return other in self.savarna_set

    @property
    def savarna_set(self):
        """Return the sounds that are savarna to this one. The 'savarna'
        relation is defined by the following rules:

            1.1.9  tulyAsyaprayatnaM savarNam
            1.1.10 nAjjhalau
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


class SoundCollection(object):

    def __init__(self, *a, **kw):
        raise NotImplementedError

    def __contains__(self, item):
        """
        :param item: some sound
        """
        return item in self.values

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "<%s('%s')>" % (self.__class__.__name__, self.name)


@memoize
class Sounds(SoundCollection):

    """A shorthand for grouping Sanskrit sounds.

    :param phrase: a group of designations
    """

    def __init__(self, phrase):
        self.name = phrase

        v = self.values = set()
        for item in phrase.split():

            first, last = (item[0], item[-1])
            simple_vowel = len(item) == 1 and item in Pratyahara('ak')

            # 1.1.69 aNudit savarNasya cApratyayaH
            if last == 'u' or simple_vowel:
                v.update(Sound(first).savarna_set)
            # 1.1.70 taparas tatkAlasya
            elif last == 't':
                v.update([first])
            # Generic letter
            elif len(item) == 1:
                v.update(item)
            # Pratyahara
            else:
                v.update(Pratyahara(item).values)


@memoize
class Pratyahara(SoundCollection):

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
        ('YmNRn', 'm'),
        ('JB', 'Y'),
        ('GQD', 'z'),
        ('jbgqd', 'S'),
        ('KPCWTcwt', 'v'),
        ('kp', 'y'),
        ('Szs', 'r'),
        ('h', 'l'),
    ]

    def __init__(self, name, second_R=False):
        first = name[0]
        limit = name[-1]
        found_first = False

        self.name = name
        self.values = set([first])

        for items, it in self.rules:
            if found_first:
                self.values.update(items)
            elif first in items:
                self.values.update(items.partition(first)[-1])
                found_first = True
            if found_first and it == limit:
                if second_R:
                    second_R = False
                else:
                    break


class Term(object):

    """
    A :class:`Term` models the strings used in the grammar and provides
    an easy interface for applying the various rules of the grammar. In
    addition, it contains the various designations that apply to some
    value.

    Terms are used in a functional way; modifying a term creates a new
    copy. This approach is used to keep the derivations sane.

    :param value: the human-readable version of this term
    :param samjna: the technical designations that apply to this term

    :param lakshana: the names that refer to this term. For example, an
                     operation conditioned by "lit" is also condition by
                     "Nal", since "Nal" comes from "lit". This term
                     comes from 1.1.62:

                         1.1.62 pratyayalope pratyayalakSaNam

                     Technically, it applies only to a pratyaya. But
                     it's been useful in other contexts so far.

    :param parts: The components that constitute this term. For example,
                  the Term 'BUv' might have two parts: the root 'BU' and
                  the augment 'v' (from 'vu~k').
    """

    def __init__(self, value):
        # The raw string, including 'it' letters and accent marks
        self.raw = value
        # The raw string with 'it' letters and accent marks removed.
        self.value = value
        #
        self.samjna = set()
        #
        self.lakshana = set()
        self.parts = [self]

    def __eq__(self, other):
        raise NotImplementedError

    def __nonzero__(self):
        return bool(self.value)

    def __getitem__(self, i):
        try:
            return Term(self.value[i])
        except IndexError:
            return Term('')

    def __getslice__(self, i, j):
        return Term(self.value[i:j])

    def __repr__(self):
        return "<{0}('{1}')>".format(self.__class__.__name__, self.value)

    def copy(self):
        """Create a full copy of the :class:`Term`."""
        cls = self.__class__
        c = cls(self.value)
        c.samjna = self.samjna.copy()
        c.lakshana = self.lakshana.copy()
        c.parts = self.parts[:]
        return c

    def _ends_in(selection):
        group = Sounds(selection)

        def fn(self):
            return self[-1].value in group
        return fn

    ac = property(_ends_in('ac'))
    dirgha = property(_ends_in('At It Ut Ft'))
    hrasva = property(_ends_in('at it ut ft xt'))
    ec = property(_ends_in('ec'))
    hal = property(_ends_in('hal'))
    ik = property(_ends_in('ik'))
    del _ends_in

    @property
    def guru(self):
        """True iff the end of the term is called 'guru'.

        1.4.11 saMyoge guru
        1.4.12 dIrghaM ca
        """
        return self.samyoga or self.dirgha

    @property
    def laghu(self):
        """True iff the end of the term is called 'laghu'.

        1.4.10 hrasvaM laghu
        """
        return self.hrasva

    @property
    def num_syllables(self):
        return sum(1 for L in self.value if L in Sounds('ac'))

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
            hal = Sounds('hal')
            return self.value[-1] in hal and self.value[-2] in hal
        except IndexError:
            return False

    @property
    def samyogadi(self):
        """True iff the end of the term is called 'samyoga'.

        1.1.7 halo 'nantarAH saMyogaH
        """
        try:
            hal = Sounds('hal')
            return self.value[0] in hal and self.value[1] in hal
        except IndexError:
            return False

    def adi(self, replacement=None):
        if replacement is not None:
            c = self.copy()
            c.value = replacement + c.value[1:]
            c.parts = [c]
            return c
        else:
            if self.value:
                return Term(self.value[0])
            else:
                return Term('')

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

    def al_tasya(self, src, dest):
        src, dest = Sounds(src), Sounds(dest)

        c = self.copy()
        letters = list(self.value)
        for i, L in enumerate(letters):
            x = L
            if L in src:
                x = Sound(L).closest(dest)
                # 1.1.51 ur aN raparaH
                if L in Sounds('f') and x in Sounds('aR'):
                    x += 'r'

            letters[i] = x

        c.value = ''.join(letters)
        return c

    def antya(self, replacement=None):
        if replacement is not None:
            c = self.copy()
            c.value = c.value[:-1] + replacement
            c.parts = [c]
            return c
        else:
            return Term(self.value[-1])

    def any_it(self, *args):
        return any(a in self.it for a in args)

    def any_lakshana(self, *args):
        return any(a in self.lakshana for a in args)

    def any_samjna(self, *args):
        return any(a in self.samjna for a in args)

    def deaspirate(self):
        c = self.copy()
        c.value = sounds.deaspirate(c.value[0]) + c.value[1:]
        return c

    def ends_in(self, selection):
        group = Sounds(selection)
        return self[-1].value in group

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
            if L in Sounds('ac'):
                letters[i] = sounds.guna(letters[i])
                break
        value = ''.join(reversed(letters))
        return self.set_value(value)

    def lopa(self):
        """
        Apply 'lopa' to this term.

        1.1.60 adarzanaM lopaH
        1.1.62 pratyayalope pratyayalakSaNam
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
        Insert a term before this one:

            1.1.67 tasmAd ityuttarasya

        :param other: the term to insert
        """
        c = self.copy()
        c.value = c.value + other.value
        c.parts = c.parts + other.parts
        return c

    def tasmin(self, other):
        """
        Insert a term after this one:

            1.1.67 tasminniti nirdiSTe pUrvasya

        :param other: the term to insert
        """
        c = self.copy()
        c.value = other.value + c.value
        c.parts = other.parts + c.parts
        return c

    def tasya(self, other, adi=False):
        """
        Perform a substitution according to the normal rules.

        :param other: the term to insert
        """
        c = self.copy()

        # 1.1.54 AdeH parasya
        if adi:
            c.value = other.value + self.value[1:]
            return c

        # 1.1.46 Adyantau Takitau
        if 'k' in other.it:
            c.value += other.value
            c.parts.append(other)

        # 1.1.46 Adyantau Takitau
        elif 'w' in other.it:
            c.value = other.value + self.value
            c.parts.insert(0, other)

        # 1.1.47 mid aco 'ntyAt paraH
        elif 'm' in other.it:
            raise NotImplementedError

        # 1.1.52 alo 'ntyasya
        # 1.1.53 Gic ca
        elif len(other.value) == 1 or 'N' in other.it:
            c.value = self.value[:-1] + other.value
            c.parts.append(other)

        # 1.1.55 anekAlSit sarvasya
        elif 'S' in other.it or len(other.value) > 1:
            c.value = other.value
            c.parts = [other]

        else:
            raise NotImplementedError

        return c

    def ti(self, replacement=None):
        """The portion starting with the last vowel.

        1.1.64 aco 'ntyAdi ti
        """
        splits = re.split('([%s])' % ''.join(Sounds('ac')), self.value)
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

    nasal_re = re.compile('([aAiIuUfFxXeEoO]~)')

    def __init__(self, raw=None, **kw):
        Term.__init__(self, raw or '')
        self.svara = raw
        self.raw = None
        self.value = None
        self.it = set()
        if raw:
            self.set_raw(raw, **kw)

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

    def set_raw(self, raw, **kw):
        self.raw = raw

        if '^' in raw:
            self.it.add('udatta')
            raw = raw.replace('^', '')
        if '\\' in raw:
            self.it.add('anudatta')
            raw = raw.replace('\\', '')

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
        c.set_raw(raw, **kw)
        return c


# Bases
# -----

class Anga(Upadesha):
    def set_raw(self, value, **kw):
        Upadesha.set_raw(self, value, **kw)
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

    def set_raw(self, value, **kw):
        Anga.set_raw(self, value, **kw)
        self.samjna.add('dhatu')


# Suffixes
# --------

class Pratyaya(Upadesha):
    def set_raw(self, value, **kw):
        Upadesha.set_raw(self, value, pratyaya=True, **kw)
        self.samjna.add('pratyaya')

        # 1.1.__ pratyayasya lukzlulupaH
        if value in ('lu~k', 'Slu~', 'lu~p'):
            self.value = ''

        # 3.4.113 tiGzit sArvadhAtukam
        if 'S' in self.it:
            self.samjna.add('sarvadhatuka')

        # 1.2.4 sArvadhAtukam apit
        if 'sarvadhatuka' in self.samjna and 'p' not in self.it:
            self.it.add('k')


class Krt(Pratyaya):
    def set_raw(self, value, **kw):
        Pratyaya.set_raw(self, value, pratyaya=True, **kw)
        self.samjna.add('krt')


class Vibhakti(Pratyaya):
    def set_raw(self, raw, **kw):
        value = raw.replace('J', 'ant')
        Pratyaya.set_raw(self, value, vibhakti=True, **kw)
        self.samjna.add('vibhakti')
        self.raw = raw
