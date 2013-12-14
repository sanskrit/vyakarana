Modeling Rules
==============

As a reminder, this is how :ref:`ordinary rules <ordinary-rules>` are usually
structured:

- C is replaced by X (when L comes before C) (when C comes before R).
- C is called X (when L comes before C) (when C comes before R).
- X is inserted after L (when L comes before R).
- C does not accept rule Y (when L comes before C) (when C comes before X).

We can rewrite these templates into a more general form:

    When we see some context window W, perform some operation O.

where *W* is an arbitrary set of contexts and *O* is an abstraction for some
arbitrary change, such as:

- replacing C with X
- calling C by the name of X
- inserting X after L
- blocking rule Y on C

With this general form in mind, we can decompose a rule model into two parts:

- matching a context. To do so, we use :term:`filters <filter>`.
- applying an operation. To do so, we use :term:`operators <operator>`.

Filters
-------

A :class:`~vyakarana.filters.Filter` is a callable object that accepts a state
and index, performs some test on ``state[index]``, and returns ``True`` or
``False`` as appropriate. For example, the :class:`~vyakarana.filters.samjna`
filter returns whether or not ``state[index]`` has some particular samjna.

If all of a rule's filters return ``True``, then the rule has scope to apply.

In older version of the code base, filters were functions that accepted an
:class:`~vyakarana.upadesha.Upadesha` and returned ``True`` or ``False``. This
approach changed for two reasons:

- A few filters require global access to the state. If they accept just a
  single `term`, there`s no way to get information on the rest of the state.
  So filters were changed to accept state-index pairs.
- Usually, a rule`s filter is a combination of two other filters. One nice
  way to do this is to use Python's unary operators (e.g. ``&``, ``|``). But
  custom operators are supported only for class instances. So filters were
  changed to class instances.

Parameterized filters
^^^^^^^^^^^^^^^^^^^^^

*Parameterized filters* group filters into families and make it easier to
create a lot of related filters. Specifically, they are classes that can be
instantiated (parameterized) by passing arguments.

For example, the :class:`~vyakarana.filters.al` class tests whether a term
has a particular final letter::

    ac = al('ac')
    ak = al('ak')
    hal = al('hal')

.. note::
    Parameterized filters have lowercase names for historical reasons. Also,
    they better match the names for unparameterized filters, e.g.
    ``al('i') & ~samyogapurva``.

Combining filters
^^^^^^^^^^^^^^^^^

We can create new filters by using Python's unary operators.

We can invert a filter ("not")::

    # ekac: having one vowel
    anekac = ~ekac

take the intersection of two filters ("and")::

    # samyoga: ending in a conjunct consonant
    # samjna('dhatu'): having 'dhatu' samjna
    samyoga_dhatu = samyoga & samjna('dhatu')

and take the union of two filters ("or")::

    # raw('Snu'): raw value is the 'nu' of e.g. 'sunute', 'Apnuvanti'
    # samjna('dhatu'): having 'dhatu' samjna
    # raw('BrU'): raw value is 'BrU'
    snu_dhatu_bhru = raw('Snu') | samjna('dhatu') | raw('BrU')

Operators
---------

An :class:`~vyakarana.operators.Operator` is a callable object that accepts a
state and index, performs some operation, and returns the result. For example,
the :class:`~vyakarana.operators.guna` operator applies guna to
``state[index]`` and returns a new state.
