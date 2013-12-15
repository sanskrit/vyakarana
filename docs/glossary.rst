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
        If a term is doubled, *abhyāsa* refers to the first part.

    abhyasta
        If a term is doubled, *abhyasta* refers to the two parts together.

    ātmanepada
        The last 9 tiṅ suffixes.

    ārdhadhātuka
        Refers to certain kinds of verb suffixes.

    Aṣṭādhyāyī
    Ashtadhyayi
        A list of rules. It takes some input and produces one or more valid
        Sanskrit expressions.

    it
        An indicatory letter.

    upadeśa
        A term stated with its indicatory letters (:term:`it`).

    guṇa
        An operation that strengthens a vowel to the "medium" level
        (*a, e, o*, but *ṛ* and *ṝ* become *ar*). Also refers to the result
        of this operation.

    vṛddhi
        An operation that strengthens a vowel to the "strong" level
        (*ā, ai, au*, but *ṛ* and *ṝ* become *ār*). Also refers to the result
        of this operation.

    tiṅ
        Refers to one of the 18 basic verb suffixes: 9 in :term:`parasmaipada`
        and 9 in :term:`ātmanepada`.

    dhātu
        A verb root.

    Dhātupāṭha
    Dhatupatha
        A list of verb roots. These roots are used as input to the Ashtadhyayi.

    parasmaipada
        The first 9 tiṅ suffixes.

    pratyaya
        A suffix.

    vibhakti
        A triplet of noun/verb endings. Also, an ending within that triplet.

    saṃjñā
        A technical name that is assigned to a group of terms. For
        example, *pratyaya* is a *saṃjñā* for the set of all suffixes.

    sārvadhātuka
        Refers to certain kinds of verb suffixes. Generally, :term:`tiṅ` and
        :term:`śit` suffixes receive this saṃjñā.

    sthānī
        In a substitution, the term where the substitution occurs.


English
-------

Generally, these are used to describe concepts in the program.

.. glossary::

    base filter
        A filter defined in an :func:`~vyakarana.rules.inherit` decorator.
        It is "and"-ed with all of the rule tuples created by the decorated
        function.

    center context
        The term that undergoes substitution. In a *saṃjñā* rule: the term
        that receives the *saṃjñā*.

    filter
        A callable object that is used to test for a certain context. For
        details, see the :class:`~vyakarana.filters.Filter` class.

    left context
        The term(s) that appear immediately before the center context. If no
        center context is defined: the term(s) after which something is
        inserted.

    metarule
        A rule that defines part of the metalanguage of the Ashtadhyayi. Some
        are explicitly stated, but many are implicit.

    operator
        A callable object that is used to apply an operation to a state. For
        details, see the :class:`~vyakarana.operators.Operator` class.

    ordinary rule
        A rule that takes some input and produces some output(s). In this
        documentation, such rules are usually just called "rules."

    right context
        The term(s) that appear immediately after the center context. If no
        center context is defined: the term(s) before which something is
        inserted.

    rule tuple
        A special shorthand for specifying rules of the Ashtadhyayi. This must
        be expanded into a full :class:`~vyakarana.rules.Rule` definition
        before it can be used.

.. _it-glossary:

*it* tags
---------

.. glossary::
    kit
        Prevents *guṇa* and *vṛddhi*. If a replacement is marked with *k*, it
        is added to the end of the :term:`sthānī`.

    ṅit
        Prevents *guṇa* and *vṛddhi*. If a replacement is marked with *ṅ*, it
        replaces the last letter of the *sthānī*.

    ñit
        Causes *vṛddhi* for certain vowels.

    ṭit
        If a replacement is marked with *ṭ*, it is added to the beginning of
        the *sthānī*. If a *lakāra* is marked with *ṭ*, then it undergoes
        some basic rules, e.g. replacement of *thās* with *se*.

    ṇit
        Causes *vṛddhi* for certain vowels.

    pit
        Causes *anudātta* accent on a :term:`pratyaya`. A :term:`sārvadhātuka`
        suffix not marked by *p* is treated as :term:`ṅit`.

    mit
        If a replacement is marked with *m*, it is inserted after the last
        vowel of the *sthānī*.

    śit
        If a replacement is marked with *ś*, it replaces the entire *sthānī*.
        Generally, a :term:`pratyaya` marked with *ś* can be called
        :term:`sārvadhātuka`.
