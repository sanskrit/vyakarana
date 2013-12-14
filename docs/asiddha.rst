*asiddha* and *asiddhavat*
==========================

When a rule applies to some input to yield some output, the input is discarded
and all future applications act on the output. But sometimes the original input
preserves some information that we want to keep.

*asiddha*
---------

TODO


*asiddhavat*
------------

Consider the following input:

    *śās + hi*

By 6.4.35, *śās* becomes *śā* when followed by *hi*. By 6.4.101, *hi* becomes
*dhi* when preceded by a consonant. If one applies, the other is blocked. But
to get the correct form *śādhi*, we have to apply both rules together.

The Ashtadhyayi solves this problem by placing both rules in a section called
**asiddhavat**. For any two rules A and B within this section, the results of
A are invisible to B (or "as if not completed", i.e. *a-siddha-vat*). This
allows each rule to act without being blocked by the other.

In practical terms, this means that each term has at least two values
simultaneously: one accessible only to the non-*asiddhavat* world (e.g. *śā*)
and one accessible only to the *asiddhavat* world (*śās*).

To see how the program handles these problems, see the :ref:`data spaces
<data-spaces>` stuff in :doc:`inputs_and_outputs`.

.. note::
    Issues of *asiddha* and *asiddhavat* are subtle and outside the scope of
    this documentation. Those interested might see `rule 6.4.22`_ of the
    Ashtadhyayi or section 3.5 of `Goyal et al.`_

.. _rule 6.4.22: http://avg-sanskrit.org/avgupload/dokuwiki/doku.php?id=sutras:6-4-22
.. _Goyal et al.: http://sanskrit1.ccv.brown.edu/Sanskrit/Symposium/Papers/AmbaSimulation.pdf
