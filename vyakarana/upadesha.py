# -*- coding: utf-8 -*-
"""
    vyakarana.upadesha
    ~~~~~~~~~~~~~~~~~~

    Classes for working with an upadeśa.

    :license: MIT and BSD
"""

import re
from collections import namedtuple

from sounds import Sounds


_DataSpace = namedtuple('_DataSpace',
                        ['raw', 'clean', 'value', 'asiddhavat', 'asiddha'])

class DataSpace(_DataSpace):

    def replace(self, **kw):
        prev = None
        new = dict()
        for field in self._fields:
            if field in kw:
                new[field] = prev = kw[field]
            elif prev is not None:
                new[field] = prev
        return self._replace(**new)


class Upadesha(object):

    """A Term with indicatory letters."""

    __slots__ = ['data', 'samjna', 'lakshana', 'ops', 'parts', '_filter_cache']
    nasal_re = re.compile('([aAiIuUfFxeEoO])~')

    def __init__(self, raw=None, data=None, samjna=None, lakshana=None, ops=None, parts=None, **kw):
        if raw is not None:
            clean, it_samjna = self._parse_it(raw, **kw)
            data = DataSpace(raw, clean, clean, clean, clean)
            samjna = samjna | it_samjna if samjna else it_samjna

        #: The term`s data space. A given term is represented in a
        #: variety of ways, depending on the circumstance. For example,
        #: a rule might match based on a specific upadeśa (including
        #: 'it' letters) in one context and might match on a term's
        #: final sound (excluding 'it' letters) in another.
        self.data = data

        #: The set of markers that apply to this term. Although the
        #: Ashtadhyayi distinguishes between samjna and 'it' letters,
        #: this simulation merges them together. Thus ``self.samjna``
        #: might contain both ``kit`` and ``pratyaya``.
        self.samjna = samjna

        #: The set of values that this term used to have. Technically,
        #: only pratyaya have access to this information.
        self.lakshana = lakshana or frozenset()

        #: The set of operations that have been applied to this term.
        self.ops = ops or frozenset()

        #: The various augments that have been applied to this term.
        self.parts = parts or frozenset()

        #:
        self._filter_cache = {}

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        return (self.__class__ == other.__class__ and
                self.data == other.data and
                self.samjna == other.samjna and
                self.lakshana == other.lakshana and
                self.ops == other.ops and
                self.parts == other.parts)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s('%s')>" % (self.__class__.__name__, self.value)

    def copy(self, data=None, samjna=None, lakshana=None, ops=None, parts=None):
        return self.__class__(
            data=data or self.data,
            samjna=samjna or self.samjna,
            lakshana=lakshana or self.lakshana,
            ops=ops or self.ops,
            parts=parts or self.parts
            )

    @property
    def adi(self, locus='value'):
        """Return the first sound, or ``None`` if there isn't one."""
        try:
            return getattr(self.data, locus)[0]
        except IndexError:
            return None

    @property
    def antya(self, locus='value'):
        """Return the last sound, or ``None`` if there isn't one."""
        try:
            return getattr(self.data, locus)[-1]
        except IndexError:
            return None

    @property
    def asiddha(self):
        """Return the value stored in the asiddha space."""
        return self.data.asiddha

    @property
    def asiddhavat(self):
        """Return the value stored in the asiddhavat space."""
        return self.data.asiddhavat

    @property
    def clean(self):
        """Return the raw value without svaras and anubandhas."""
        return self.data.clean

    @property
    def raw(self):
        """Return the raw value."""
        return self.data.raw

    @property
    def upadha(self, locus='value'):
        """Return the penultimate sound, or ``None`` if there isn't one."""
        try:
            return getattr(self.data, locus)[-2]
        except IndexError:
            return None

    @property
    def value(self):
        """Return the value created by siddha rules."""
        return self.data.value

    def _parse_it(self, raw, **kw):
        pratyaya = kw.pop('pratyaya', False)
        vibhakti = kw.pop('vibhakti', False)
        taddhita = kw.pop('taddhita', False)

        it = set()
        samjna = set()

        # svara
        for i, L in enumerate(raw):
            if L in ('\\', '^'):
                # anudattet and svaritet
                if raw[i - 1] == '~':
                    if L == '\\':
                        samjna.add('anudattet')
                    else:
                        samjna.add('svaritet')
                # anudatta and svarita
                else:
                    if L == '\\':
                        samjna.add('anudatta')
                    else:
                        samjna.add('svarita')

        clean = re.sub('[\\\\^]', '', raw)
        keep = [True] * len(clean)

        # ir
        if clean.endswith('i~r'):
            it.add('ir')
            keep[-3:] = [True, True, True]

        # 1.3.2 "upadeśe 'janunāsika iṭ"
        for i, L in enumerate(clean):
            if L == '~':
                it.add(clean[i - 1] + 'd')
                keep[i - 1] = False
                keep[i] = False

        # 1.3.3. hal antyam
        antya = clean[-1]
        if antya in Sounds('hal'):
            # 1.3.4 "na vibhaktau tusmāḥ"
            if vibhakti and antya in Sounds('tu s m'):
                pass
            else:
                it.add(antya)
                keep[-1] = False

        # 1.3.5 ādir ñituḍavaḥ
        try:
            two_letter = clean[:2]
            if two_letter in ('Yi', 'wu', 'qu'):
                keep[0] = keep[1] = False
                if two_letter.endswith('u'):
                    samjna.add(clean[0] + 'vit')
                else:
                    samjna.add(clean[0] + 'It')
        except IndexError:
            pass

        # 1.3.6 "ṣaḥ pratyayasya"
        # 1.3.7 "cuṭū"
        #
        #     It is interesting to note that no examples involving the
        #     initial ch, jh, Th, and Dh of an affix were provided. This
        #     omission is significant since affix initials ch, jh, Th,
        #     and Dh always are replaced by Iy (7.1.2 AyaneyI...) ant
        #     (7.1.3 jho 'ntaH), ik (7.3.50 ThasyekaH), and ey (7.1.2)
        #     respectively. Thus the question of treating each of these
        #     as an it does not arise.
        #
        #                         Rama Nath Sharma
        #                         The Ashtadhyayi of Panini Vol. II
        #                         Notes on 1.3.7 (p. 145)
        adi = clean[0]
        if pratyaya:
            # no C, J, W, Q by note above.
            if raw[0] in 'zcjYwqR':
                it.add(adi)
                keep[0] = False

            # 1.3.8 "laśakv ataddhite"
            if not taddhita:
                if adi in Sounds('l S ku'):
                    it.add(adi)
                    keep[0] = False


        # 1.3.9 tasya lopaḥ
        clean = ''.join(L for i, L in enumerate(clean) if keep[i])
        samjna = samjna.union([x + 'it' for x in it])
        return clean, samjna

    def add_lakshana(self, *names):
        return self.copy(
            lakshana=self.lakshana.union(names)
        )

    def add_op(self, *names):
        return self.copy(
            ops=self.ops.union(names)
        )

    def add_part(self, *names):
        return self.copy(
            parts=self.parts.union(names)
        )

    def add_samjna(self, *names):
        return self.copy(
            samjna=self.samjna.union(names)
        )

    def any_samjna(self, *args):
        return any(a in self.samjna for a in args)

    def get_at(self, locus):
        return getattr(self.data, locus)

    def remove_samjna(self, *names):
        return self.copy(
            samjna=self.samjna.difference(names)
        )

    def set_at(self, locus, value):
        if locus == 'raw':
            return self.set_raw(value)
        elif locus == 'value':
            return self.set_value(value)
        elif locus == 'asiddhavat':
            return self.set_asiddhavat(value)
        elif locus == 'asiddha':
            return self.set_asiddha(value)
        else:
            raise NotImplementedError

    def set_raw(self, raw):
        clean, it_samjna = self._parse_it(raw)
        samjna = self.samjna | it_samjna
        return self.copy(
            data=self.data.replace(raw=raw, clean=clean),
            samjna=samjna,
            lakshana=self.lakshana | set([self.raw])
        )

    def set_value(self, value):
        return self.copy(data=self.data.replace(value=value))

    def set_asiddhavat(self, asiddhavat):
        return self.copy(data=self.data.replace(asiddhavat=asiddhavat))

    def set_asiddha(self, asiddha):
        return self.copy(data=self.data.replace(asiddha=asiddha))


class Anga(Upadesha):

    __slots__ = ()

    def __init__(self, *a, **kw):
        Upadesha.__init__(self, *a, **kw)
        self.samjna |= set(['anga'])


class Dhatu(Anga):

    __slots__ = ()

    def __init__(self, *a, **kw):
        Upadesha.__init__(self, *a, **kw)
        self.samjna |= set(['anga', 'dhatu'])


class Pratyaya(Upadesha):

    __slots__ = ()

    def __init__(self, *a, **kw):
        Upadesha.__init__(self, *a, **kw)
        self.samjna |= set(['pratyaya'])

        # 1.1.__ pratyayasya lukzlulupaH
        if self.value in ('lu~k', 'Slu~', 'lu~p'):
            self.data = self.data.replace(raw=self.value, clean='')

    def _parse_it(self, value):
        return Upadesha._parse_it(self, value, pratyaya=True)


class Krt(Pratyaya):

    __slots__ = ()

    def __init__(self, *a, **kw):
        Pratyaya.__init__(self, *a, **kw)
        self.samjna |= set(['krt'])

        # 3.4.113 tiGzit sArvadhAtukam
        # 3.4.115 liT ca (ArdhadhAtukam)
        if 'Sit' in self.samjna and self.raw != 'li~w':
            self.samjna |= set(['sarvadhatuka'])
        else:
            self.samjna |= set(['ardhadhatuka'])

        # 1.2.4 sArvadhAtukam apit
        if 'sarvadhatuka' in self.samjna and 'pit' not in self.samjna:
            self.samjna |= set(['Nit'])


class Vibhakti(Pratyaya):

    __slots__ = ()

    def __init__(self, *a, **kw):
        Pratyaya.__init__(self, *a, **kw)
        self.samjna |= set(['vibhakti'])

    def _parse_it(self, value):
        return Upadesha._parse_it(self, value, pratyaya=True, vibhakti=True)
