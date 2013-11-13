# -*- coding: utf-8 -*-
"""
    vyakarana.lists
    ~~~~~~~~~~~~~~~

    Lists of terms, designations, and sounds.

    :license: MIT and BSD
"""

#: Defined in rule 3.4.78. These 18 affixes are used to form verbs.
#: The first 9 are called "parasmaipada" (1.4.99), and the last 9 are
#: called "ātmanepada" (1.4.100).
TIN = ['tip', 'tas', 'Ji', 'sip', 'Tas', 'Ta', 'mip', 'vas', 'mas',
       'ta', 'AtAm', 'Ja', 'TAs', 'ATAm', 'Dvam', 'iw', 'vahi', 'mahiN']


#: Abstract suffixes that are replaced with items from `TIN`.
#: Collectively, they are called the "lakāra" or just "la".
LA = set([
    'la~w', 'li~w', 'lu~w', 'lf~w', 'le~w', 'lo~w',
    'la~N', 'li~N', 'lu~N', 'lf~N'
])


#: Various pratyaya
PRATYAYA = set([
    'luk', 'Slu', 'lup',
    'Sap', 'Syan', 'Snu', 'Sa', 'Snam', 'u', 'SnA',
    'Ric', 'Rin'
]) | LA


#: Technical designations (1.3.2 - 1.3.9)
IT = (set([L + 'it' for L in 'kKGNcYwqRpmS'])
      | set([L + 'dit' for L in 'aiuUfxo'])
      | set(['qvit', 'wvit'])
      | set(['svaritet', 'anudattet', 'svarita', 'anudatta']))


#: saṃjñā for verb 'pada'
PADA = ['parasmaipada', 'atmanepada']


#: saṃjñā for various persons
PURUSHA = ['prathama', 'madhyama', 'uttama']


#: saṃjñā for various numbers
VACANA = ['ekavacana', 'dvivacana', 'bahuvacana']


#: saṃjñā for case triplets
VIBHAKTI = ['prathama', 'dvitiya', 'trtiya', 'caturthi',
            'pancami', 'sasthi', 'saptami']


#: saṃjñā for verb suffixes
DHATUKA = ['sarvadhatuka', 'ardhadhatuka']


#: saṃjñā for kāraka relations (currently unused)
KARAKA = ['karta', 'karma', 'karana', 'adhikarana', 'sampradana', 'apadana']


#: All saṃjñā
SAMJNA = set([
    'guna', 'vrddhi',
    'dhatu', 'anga', 'pada', 'pratyaya',
    'krt', 'taddhita',
    'abhyasa', 'abhyasta',
    'tin', 'sup',
]) | set(PADA + PURUSHA + VACANA + VIBHAKTI + DHATUKA + KARAKA)


#: A collection of various sounds, including:
#: - savarṇa sets (1.1.69)
#: - single-item sets (1.1.70)
#: - pratyāhāra (1.1.71)
SOUNDS = set([
    # 1.1.69 aṇudit savarṇasya cāpratyayaḥ
    'a', 'i', 'u', 'f', 'x',
    'ku~', 'cu~', 'wu~', 'tu~', 'pu~',

    # 1.1.70 taparas tatkālasya
    'at', 'At', 'it', 'It', 'ut', 'Ut', 'ft', 'Ft', 'et', 'Et', 'ot', 'Ot',

    # 1.1.71 ādir antyena sahetā
    # Although the Shiva Sutras allow a large number of pratyāhāras,
    # only the following are used in the Ashtadhyayi.
    # (Sharma Volume I, p. 33)
    'eN', 'yaY', 'aR', 'Cav', 'aw',
    'Jaz', 'Baz',
    'ak', 'ik', 'uk', 'yaR', 'iR', 'Nam', 'am', 'yam',
    'ac', 'ec', 'Ec', 'ic', 'may', 'Jay', 'Kay', 'yay',
    'Sar', 'yar', 'Jar', 'Kar', 'car',
    'JaS', 'jaS', 'baS', 'S', 'haS', 'vaS',
    'al', 'hal', 'sal', 'val', 'ral', 'Jal'
])
