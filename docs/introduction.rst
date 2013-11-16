Introduction
============

This program has two goals:

1. To generate the entire set of forms allowed by the Ashtadhyayi without over-
   or under-generating.
2. To do so while staying true to the spirit of the Ashtadhyayi.

Goal 1 is straightforward, but the "under-generating" is subtle. For some
inputs, the Ashtadhyayi can yield multiple results; ideally, we should be able
to generate all of them.

Goal 2 is more vague. I want to create a program that defines and chooses its
rules using the same mechanisms used by the Ashtadhyayi.

In other words, I want to create a full simulation of the Ashtadhyayi.

The Ashtadhyayi
---------------

The Ashtadhyayi (*Aṣṭādhyāyi*) is a list of about 4000 rules. It has **ordinary
rules**, which take some input and yield some output(s), and **metarules**,
which describe how to interpret other rules. If Sanskrit grammar is a factory,
then its ordinary rules are the machines inside and its metarules are the
instructions used to build the machines.

Given some input, the Ashtadhyayi applies a rule that changes the input in
some way. The output of the rule is then sent to another rule, just as items
on the assembly line move from one machine to the other. This continues until
there's no way to change the result any further. When this occurs, the process
is complete. The result is a correct Sanskrit expression.

The Dhatupatha
--------------

If the Ashtadhyayi is the stuff inside the factory, then the Dhatupatha
(*Dhātupāṭha*) is the raw material that enters the factory. It is a list of
about 2000 verb roots, each stated with a basic meaning:

    | 1.1 *bhū sattāyām*
    | *bhū* in the sense of existence (*sattā*)

Modern editions of the Dhatupatha are numbered *x.y*, where *x* is the root's
verb class (**gaṇa**) and *y* is its order within the *gaṇa*. Thus *bhū* is
entry 1 in *gaṇa* 1; it's the first root in the list.

There is no single version of the Dhātupāṭha. I used a version I found on
`Sanskrit Documents`_ (specifically, `this file`_) and made some small
corrections. So far, it's been totally competent for the task.

.. _Sanskrit Documents: http://sanskritdocuments.org
.. _this file: http://sanskritdocuments.org/doc_z_misc_major_works/dhatupatha_svara.itx
