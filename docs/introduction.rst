Introduction
============

This system has two goals:

1. To generate the entire set of forms allowed by the Ashtadhyayi without over-
   or under-generating.
2. To do so while staying true to the spirit of the Ashtadhyayi.

Goal 1 is straightforward, but the "under-generating" is subtle. For some
inputs, the Ashtadhyayi can yield multiple results; ideally, we should be able
to generate all of them.

Goal 2 is more vague. I want to create a system that derives words using the
same mechanisms as the Ashtadhyayi, including those used to define rules and
those used to select them.

With these mechanisms in hand, we can define the system's rules in conformance
with the Ashtadhyayi and produce Sanskrit words according to its principles.
In other words, we can create a full simulation of the Ashtadhyayi.


The Ashtadhyayi
---------------

The Ashtadhyayi (*Aṣṭādhyāyi*) is a list of about 4000 rules. There are
ordinary rules, which take some input and yield some output(s), and metarules,
which describe how to interpret the ordinary rules we come across. If Sanskrit
grammar is a factory, then its ordinary rules are the machines inside and its
metarules are the workers who run them.

Given some input, the Ashtadhyayi applies a rule that changes the input in
some way. The output of the rule is then sent to another rule, and so on,
until there's no way to change the result any further. When this occurs, the
process is complete. The result is a correct Sanskrit expression.

The Dhatupatha
--------------

If the Ashtadhyayi is the stuff inside the factory, then the Dhatupatha
(*Dhātupāṭha*) is the raw material that enters the factory. It is a list of
about 2000 verb roots, each annotated in various ways. For example, the root
*kṛ* ("do") has an annotation that tells the system that both *parasmaipada*
endings and *ātmanepada* endings are allowed when making verbs. Thus the
system can produce both *karoti* and *kurute*.

There is no single version of the Dhātupāṭha. I used a version I found on
`Sanskrit Documents`_ (specifically, `this file`_) and made some small
corrections. So far, it's been totally competent for the task.

.. _Sanskrit Documents: http://sanskritdocuments.org
.. _this file: http://sanskritdocuments.org/doc_z_misc_major_works/dhatupatha_svara.itx
