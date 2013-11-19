Terms and Data
==============

The rules of the Ashtadhyayi accept a list of **terms** as input and produce
a new list of terms as output. Let's start by discussing what terms are and
what information they contain.

Throughout this section, our working example will be *ca + kṛ + a*, a sequence
of three terms. Depending on the data attached to these terms, this sequence
can yield a variety of outputs:

- *cakāra* ("he/I did", perfect tense)
- *cakara* ("I did", perfect tense)
- *cakra* ("he did", perfect tense)


Sounds
------

Our example has three terms, each of which represents a piece of sound.
These "pieces of sound" usually represent morphemes, but that's not always
the case.

We'll have more to say about these sounds later, but for now they're
pretty straightforward.


*Saṃjñā*
--------

Each term has a variety of designations (**saṃjñā**) associated with it.
These *saṃjñā*, which are assigned by the Ashtadhyayi itself, enable
some rules and block others. By assigning names to different terms and
changing which rules can be used, the system can guide the original
input toward the desired output.

Our example uses the following *saṃjñā*:

===============  =============  ====================
ca               kṛ             a
===============  =============  ====================
:term:`abhyāsa`  :term:`dhātu`  :term:`pratyaya`
_                _              :term:`vibhakti`
_                _              :term:`tiṅ`
_                _              :term:`ārdhadhātuka`
===============  =============  ====================

In addition, *ca + kṛ* together are called both :term:`abhyasta` and
:term:`aṅga`.

Some examples of what these *saṃjñā* do:

- *dhātu* allows the rule that creates the *abhyāsa*.
- *abhyāsa* allows a rule that changes *ka* to *ca*.
- *ārdhadhātuka* allows a rule that strengthens the vowel of the term before it.

*it* tags
---------

Terms also use a second set of designations, which we can call **it** tags.
Just a shirt might have a label that tells us how to wash it, a term might
have an *it* that tells us how it behaves in certain contexts.

For example, *kṛ* has two *it* tags. The first is *ḍu*, and it allows *kṛ* to
take a certain suffix. The second is *ñ*, and it allows *kṛ* to use both
:term:`parasmaipada` and :term:`ātmanepada` endings in its verbs. *it* tags
are attached directly to the term of interest, like so:

    *ḍukṛñ*

We can remove *it* tags by applying some metarules. For some term T, the
following are *it* tags:

- nasal vowels (1.3.2)
- at the end of T:

  - consonants (1.3.3)
  - but not {*t, th, d, dh, n, s, m*} when T is a :term:`vibhakti` (1.3.4)

- at the beginning of T:

  - *ñi*, *ṭu*, and *ḍu* (1.3.5)

- at the beginning of T, if T is a :term:`pratyaya`:

  - *ṣ* (1.3.6)
  - *c, ch, j, jh, ñ, ṭ, ṭh, ḍ, ḍh, ṇ* (1.3.7)
  - *l, ś, k, kh, g, gh, ṅ* if not a *taddhita* suffix

*it* tags are not letters in any meaningful sense, and they have no meaning
outside of the metalanguage of the Ashtadhyayi. In other words, all they do
is describe certain properties; they have no deeper linguistic meaning and are
not a fundamental part of Sanskrit. So if you see a term like *ḍukṛñ*, you
should read it as:

    *kṛ* with the *it* tags *ḍu* and *ñ*.

The *it* tags are often stated with the word *it* after them. Thus *ḍvit* and
*ñit*. A term stated with its *it* letters is called the **upadeśa** of the
term. Thus *ḍukṛñ* is the **upadeśa** of the root *kṛ*.

Usage
^^^^^

*it* tags are basically just *saṃjñā* that are expressed more tersely.

To illustrate how alike these two are, let's return to our *ca + kṛ + a*
example. We saw above that this sequence can yield three different results.
But the result depends on the *saṃjñā* and *it* tags applied to the suffix *a*.
As you read on, note how the different *saṃjñā* and *it* tags interact.

- If the *upadeśa* is just *a*, then rule 1.2.5 tags the suffix with *kit*.
  This prevents :term:`guṇa`. After a few more rules, we get *cakra* for our
  result.
- If the *upadeśa* is *ṇal*, the suffix has *ṇit*, which causes :term:`vṛddhi`.
  After a few more rules, we get *cakāra* for our result.
- If the *upadeśa* is *ṇal*, the suffix has *ṇit*. But if the suffix has
  *uttama* as a *saṃjñā* -- that is, if it is in the first person -- then *ṇit*
  is used only optionally. If we reject *ṇit*, then the *ārdhadhātuka-saṃjñā*
  causes :term:`guṇa`. After a few more rules, we get *cakara* for our result.

The :ref:`glossary <it-glossary>` describes the most common *it* tags and some
of the roles they perform. Many *it* tags are overloaded to provide a variety
of different functions.
