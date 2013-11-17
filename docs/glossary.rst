Glossary
========

Sanskrit
--------

Generally, these are used to describe concepts from the grammatical tradition.

.. glossary::
    aṅga
        _

    anubandha
        See :term:`it`.

    abhyāsa
        If a term is doubled, the *abhyāsa* refers to the first of the two.

    abhyasta
        If a term is doubled, the *abhyasta* refers to the two parts together.

    ātmanepada
        The second set of tiṅ suffixes.

    ārdhadhātuka
        Refers to certain kinds of verb suffixes.

    Aṣṭādhyāyī
    Ashtadhyayi
        The set of rules that takes some input and produces one or more valid
        Sanskrit expressions.

    it
        An indicatory letter.

    upadeśa
        A term stated with its indicatory letters (:term:`it`).

    tiṅ
        Refers to one of the 18 basic verb suffixes: 9 in :term:`parasmaipada`
        and 9 in :term:`ātmanepada`.

    dhātu
        A verb root.

    Dhātupāṭha
    Dhatupatha
        A list of verb roots. These roots are used as input to the Ashtadhyayi.

    parasmaipada
        The second set of tiṅ suffixes.

    pratyaya
        A suffix.

    vibhakti
        A triplet of noun/verb endings.

    saṃjñā
        A technical name for a group of terms. For example, *pratyaya* is a
        *saṃjñā* for the set of all suffixes.

    sthānī
        In a substitution, the term where the substitution occurs.


English
-------

Generally, these are used to describe concepts in the program.

.. glossary::

    center context
        The term that undergoes substitution. In a *saṃjñā* rule: the term
        that receives the *saṃjñā*.

    left context
        The term(s) that appear immediately before the center context. If no
        center context is defined: the term(s) after which something is
        inserted.

    metarule
        A rule that defines part of the metalanguage of the Ashtadhyayi. Some
        are explicitly stated, but many are implicit.

    ordinary rule
        A rule that takes some input and produces some output(s). In this
        documentation, such rules are usually just called "rules."

    right context
        The term(s) that appear immediately after the center context. If no
        center context is defined: the term(s) before which something is
        inserted.

.. _it-glossary:

*it* letters
------------

.. glossary::
    kit
        Prevents *guṇa* and *vṛddhi* operations. If a replacement is marked
        with *k*, it's added to the end of the :term:`sthānī`.

    ṅit
        Prevents *guṇa* and *vṛddhi* operations. If a replacement is marked
        with *ṅ*, it replaces the last letter of the *sthānī*.

    ñit
        Causes *vṛddhi*.

    ṇit
        Causes *vṛddhi*.

    pit
        pass

    mit
        If a replacement is marked with *m*, it is inserted after the last
        vowel of the *sthānī*.

    śit
        If a replacement is marked with *ś*, it replaces the entire *sthānī*.