Design Overview
===============

Philosophy
----------

As much as possible, the program follows the principles of the Ashtadhyayi. It
makes use of almost all of its technical devices, and many of its methods and
classes have 1:1 correspondence to particular concepts from the grammatical
tradition. This is the case for a few reasons:

- We can model a system that's well-known and (fairly) easy to understand.
- We can take advantage of the tradition's prior work.
- We can make it easier to prove certain properties of the system.

The program's performance is currently just OK, but only a few parts of it use
any kind of optimization. With more aggressive caching it can probably run
respectably, but if it stays bad (and if those problems are due to language
features), I will probably port it to Scala or some other statically-typed
functional language.

How the program works
---------------------

We pass a single input to :meth:`ashtadhyayi.Ashtadhyayi.derive`, the most
interesting method in the :class:`Ashtadhyayi` class. This input is stored on
an internal stack. As long as the stack is non-empty, we:

1. Pop an input off of the stack.

2. Find all rules such that that:

   - the rule has space to apply to the input
   - if applied, the rule would yield at least one new result.

   Instead of applying these rules simultaneously, we apply just one then
   repeat the loop.

3. Pick the rule from (2) with highest rank. If no rules were found in (2),
   send the input to the :mod:`asiddha` module and yield the results.

   .. note::
       The :mod:`asiddha` module is basically legacy code. Currently it's
       too complicated to model easily, but in the future it will be modeled
       like the rest of the system.

4. Apply the rule and push the results back onto the stack.

In other words, the main function of interest is a generator that loops over
a stack and yields finished sequences.

The following pages explore elements of this process in detail. In particular:

- what inputs and outputs look like (:doc:`inputs_and_outputs`)
- determining whether a rule has "space to apply" (:doc:`modeling_rules`)
- ranking rules (:doc:`selecting_rules`)
- defining rules tersely (:doc:`defining_rules`)
