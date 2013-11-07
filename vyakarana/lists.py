IT = (set([L + 'it' for L in 'kKGNYwqRpmS'])
      | set([L + 'dit' for L in 'aiuUfx'])
      | set(['svaritet', 'anudattet', 'svarita', 'anudatta']))

LA = set([
    'la~w', 'li~w', 'lu~w', 'lf~w', 'le~w', 'lo~w',
    'la~N', 'li~N', 'lu~N', 'lf~N'
])

PRATYAYA = set([
    'luk', 'Slu', 'lup',
    'Sap', 'Syan', 'Snu', 'Sa', 'Snam', 'u', 'SnA',
    'Ric',
]) | LA

SAMJNA = set([
    'guna', 'vrddhi',
    'atmanepada', 'parasmaipada',
    'dhatu', 'anga', 'pada', 'pratyaya',
    'krt', 'taddhita',
    'sarvadhatuka', 'ardhadhatuka',
    'abhyasa', 'abhyasta',
    'tin', 'sup',
])

SOUNDS = set([
    'a', 'at', 'At',
    'i', 'it', 'It',
    'u', 'ut', 'Ut',
    'f', 'ft', 'Ft',

    # Sharma Volume I, p. 33
    'eN', 'yaY', 'aR', 'Cav', 'aw',
    'Jaz', 'Baz',
    'ak', 'ik', 'uk', 'yaR', 'iR', 'Nam', 'am', 'yam',
    'ac', 'ec', 'Ec', 'ic', 'may', 'Jay', 'Kay', 'yay',
    'Sar', 'yar', 'Jar', 'Kar', 'car',
    'JaS', 'jaS', 'baS', 'S', 'haS', 'vaS',
    'al', 'hal', 'sal', 'val', 'ral', 'Jal'
])
