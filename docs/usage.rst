=====
Usage
=====

.. _composite-roles:

Composite Roles
===============

Users can create composite roles by adding an item to configuration item
:confval:`comboroles_roles`. For example:

.. code:: python

   comboroles_roles = {
       'strong_literal': ['strong', 'literal'],
   }

=============================== ===========================
``:strong_literal:`bold code``` :strong_literal:`bold code`
=============================== ===========================

The above configuration creates a composite role ``strong_literal``,
and consists of two existing roles :parsed_literal:`strong_` and
:parsed_literal:`literal_`. The `Interpreted Text`_ of ``strong_literal``
(in this case, it is "bold code") will be interpreted first by role ``literal``
and then by ``strong``. In pseudo reStructuredText, it looks like:

.. code:: rst

   :strong:`:literal:`bold code``

That is why we said we implement `nested inline markups`_ in a sense.

.. hint::

   Here are some role names of commonly used markups:

   ======================= ===========================
   Usage                   Role
   ======================= ===========================
   *emphasis*              :parsed_literal:`emphasis_`
   **strong emphasis**     :parsed_literal:`strong_`
   ``inline literals``     :parsed_literal:`literal_`
   :sub:`sub` script       :parsed_literal:`sub_`
   :sup:`super` script     :parsed_literal:`sup_`
   ======================= ===========================

.. _Interpreted Text: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#interpreted-text
.. _nested inline markups: https://docutils.sourceforge.io/FAQ.html#is-nested-inline-markup-possible
.. _emphasis: https://docutils.sourceforge.io/docs/ref/rst/roles.html#emphasis
.. _strong: https://docutils.sourceforge.io/docs/ref/rst/roles.html#strong
.. _literal: https://docutils.sourceforge.io/docs/ref/rst/roles.html#literal
.. _sub: https://docutils.sourceforge.io/docs/ref/rst/roles.html#subscript
.. _sup: https://docutils.sourceforge.io/docs/ref/rst/roles.html#superscript

.. _nested-parse:

Nested Parse
============

Normally, `Interpreted Text`_ will **not be parsed**, but will be passed directly to
the role. Once the ``nested_parse`` flag of :confval:`comboroles_roles` is enabled,
Interpreted Text of composite roles will **be parsed**, and then passed to the
role. For example:

.. code:: python

   comboroles_roles = {
       'parsed_literal': (['literal'], True),
   }

=================================== =============================
````**bold code**````               ``**bold code**``
``:parsed_literal:`**bold code**``` :parsed_literal:`**bold code**`
=================================== =============================

The above configuration creates a composite role `parsed_literal` with
``nested_parse`` enabled, so the text "\*\*bold code\**" can be parsed.

Further, hyperlinks, substitutions, and even roles inside interpreted text can
be parsed too:

========================================== =====================================
``:parsed_literal:`https://example.com```` :parsed_literal:`https://example.com`
``:parsed_literal:`|release|````           :parsed_literal:`|release|`
``:parsed_literal:`RFC: :rfc:\`1459\````   :parsed_literal:`RFC: :rfc:\`1459\``
========================================== =====================================

.. note:: For nested roles, note that the backquote ````` needs to be escaped.

Works with other Extensions
===========================

The extensions can also work with roles provided by the some other extensions
(not all, see :ref:`limitation`).

``sphinx.ext.extlink``
----------------------

:parsed_literal:`sphinx.ext.extlink_` is a Sphinx builtin extension to create
shorten external links.

Assume that we have the following configuration, extlink creates the ``issue`` role,
then comboroles creates a ``literal_issue`` role based on it:

.. code:: python

   extlinks = {
       'issue': ('https://github.com/sphinx-notes/comboroles/issues/%s', '💬%s'),
   }

   comboroles_roles = {
       'literal_issue': ['literal', 'issue'],
   }

========================== ====================
``:issue:`new```           :issue:`new`
``:literal_issue:`new````  :literal_issue:`new`
========================== ====================

.. seealso:: https://github.com/sphinx-doc/sphinx/issues/11745

.. _sphinx.ext.extlinks: https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

.. _limitation:

Limitation
==========

.. warning::

   Due to internal implementation, the extension can only used to composite
   simple roles and may CRASH Sphinx when compositing complex roles.
   DO NOT report to Sphinx first if it crashes, please report to here :issue:`new`
   instead.
