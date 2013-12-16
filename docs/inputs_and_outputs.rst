Inputs and Outputs
==================

With rare exception, all data handled by the system is processed functionally.
That is, every operation applied to an input must create a new input, without
exception. The program follows this principle for two reasons:

- branching. Since one input can produce multiple outputs, it's easier to just
  create new outputs and ensure that no implicit information can be propagated.
- basic sanity. This makes the system easier to model mentally.


Terms
-----
A rule accepts a list of **terms** as input and returns the same as output.
A term is an arbitrary piece of sound and usually represents a morphere, but
that's not always the case.

In the Ashtadhyayi, these terms are usually called :term`upadeśa`, since
the grammar is taught (*upadiśyate*) by means of these terms, And in the
program, these terms are usually represented by instances of the
:class:`~vyakarana.upadesha.Upadesha` class. These classes provide some nice
methods for accessing and modifying various parts of the term. For details,
see the documentation on the :class:`~vyakarana.upadesha.Upadesha` class.


.. _data-spaces:

Data spaces
^^^^^^^^^^^

:doc:`As mentioned earlier <asiddha>`, terms in the Ashtadhyayi often contain
multiple values at once. Within the program, these are modeled by **data
spaces**, which make it easier to access and manipulate these values. These
data spaces are basically just tuples; instead of containing a single data
value, each term contains a variety of values that are valid simultaneously.

TODO

States
------

A :class:`~vyakarana.util.State` is a list of terms. Like the other inputs
used by the grammar, states are modified functionally. For details, see the
documentation on the :class:`~vyakarana.util.State` class.
