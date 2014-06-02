# -*- coding: utf-8 -*-
"""
    vyakarana.sounds
    ~~~~~~~~~~~~~~~~

    Classes for working with various sounds.

    :license: MIT and BSD
"""


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
        if isinstance(phrase, basestring):
            items = phrase.split()
        else:
            items = phrase

        v = self.values = set()
        for item in items:

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
