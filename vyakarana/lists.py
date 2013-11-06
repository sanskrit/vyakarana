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
    'ak', 'ik',
    'ac', 'ec',
    'yaY',
    'JaS', 'jaS',
    'car',
    'hal', 'Jal',
])
