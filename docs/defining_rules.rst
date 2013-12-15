Defining Rules
==============

The machinery behind a given rule is often complex and complicated. But by
abstracting away the right things, we can greatly reduce the code required
per rule, often to just **one line** in length.

Rule tuples
-----------

A :term:`rule tuple` is a 5-tuple containing the following elements:

1. the rule name, e.g. ``'6.4.77'``
2. the left context
3. the center context
4. the right context
5. the operator to apply

These tuples contain the essential information needed to create a full rule,
but they are often underspecified in various ways. Some examples:

- A context can take the value ``True``, which means that the rule should use
  the context defined for the previous rule.
- A context can take the value ``None``, which means that it uses the base
  filter (see :ref:`below <inherit>`).
- A context can be an arbitrary string. All contexts are post-processed with
  :func:`~vyakarana.filters.auto`, which converts them into actual
  :class:`~vyakarana.filters.Filter` objects.
- An operator can be an arbitrary object, usually a string. The program
  usually does a good job of transforming these "operator strings" into actual
  :class:`~vyakarana.operators.Operator` objects. For example, if the operator
  is just ``'Nit'``, the program recognizes that this is an *it* and that the
  rule is assigning a *saṃjñā*.

Rule tuples are usually contained in :class:`~vyakarana.templates.RuleTuple`
objects, but most rules are just stated as tuples.

Some example rule tuples, from throughout the program::

    # Analogous extension of ṅit
    ('1.2.4', None, f('sarvadhatuka') & ~f('pit'), None, 'Nit'),

    # Adding vikaraṇa "śap"
    ('3.1.77', F.gana('tu\da~^'), None, None, k('Sa')),

    # Performing dvirvacana
    # do_dvirvacana is an unparameterized operator defined separately.
    ('6.1.8', None, ~f('abhyasta'), 'li~w', do_dvirvacana),

    # Vowel substitution
    # _6_4_77 is an unparameterized operator defined separately.
    ('6.4.77', None, snu_dhatu_yvor, None, _6_4_77),

    # Replacing 'jh' with 'a'
    ('7.1.3', None, None, None, O.replace('J', 'ant')),

Those familiar with these rules will wonder why so much crucial information
is missing (e.g. that the center context in 7.1.3 should be a *pratyaya*).
This information is supplied in a special decorator, which we discuss now.

.. _inherit:

``@inherit``
------------

When an :class:`~vyakarana.ashtadhyayi.Ashtadhyayi` object is created, the
system searches through all modules for functions decorated with the
:func:`~vyakarana.rules.inherit` decorator. These functions create and return
a list of rule tuples. An example::

    @inherit(None, F.raw('Sap'), None)
    def sap_lopa():
        return [
            ('2.4.71', F.gana('a\da~'), None, None, 'lu~k'),
            ('2.4.74', F.gana('hu\\'), None, None, 'Slu~')
        ]

:func:`~vyakarana.rules.inherit` takes at least 3 arguments, which correspond
to the three contexts (left, center, and right). These arguments define
:term:`base filters <base filter>` that are "and"-ed with all of the returned
tuples. If the context in some rule tuple is ``None``, the system uses just
the base filter. That is, the rules above will take the following form::

    ('2.4.71', F.gana('a\da~'), F.raw('Sap'), None, 'lu~k'),
    ('2.4.74', F.gana('hu\\'), F.raw('Sap'), None, 'Slu~')

Rule conditions
---------------

The majority of the Ashtadhyayi's rules consists of some context window and an operator. But many rules are modified by some other term, such as *na* (blocking) or *vibhāṣā* (optionality). These terms are defined as subclasses of :class:`~vyakarana.templates.RuleTuple`::

    # 'iṭ' augment denied
    Na('7.2.8', None, None, f('krt') & F.adi('vaS'), U('iw')),

    #: Denied in another context
    Ca('7.2.9', None, f('krt') & titutra, None, True),

Converting tuples to rules
--------------------------

To interpret a rule tuple, we need:

- the tuple itself
- the previous tuple
- any base filters defined in the :func:`~vyakarana.rules.inherit` function.

These are combined as described above. For details, see
:func:`vyakarana.inference.create_rules`.
