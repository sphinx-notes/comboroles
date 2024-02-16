========
Examples
========

Due to :ref:`limitation`, the extension can not work with all roles, so we list
all use cases we have tested.

.. _example-nested-parse:

Nested Parse
============

.. seealso:: :ref:`nested-parse`.

========================================== =====================================
``:parsed_literal:`https://example.com```` :parsed_literal:`https://example.com`
``:parsed_literal:`|release|````           :parsed_literal:`|release|`
``:parsed_literal:`RFC: :rfc:\`1459\````   :parsed_literal:`RFC: :rfc:\`1459\``
========================================== =====================================

.. note:: For nested roles, note that the backquote ````` needs to be escaped by ``\\``.

Cross references: ``:ref:``, ``:doc:`` and more…
=================================================

.. code:: python

   comboroles_roles = {
       'literal_ref': ['literal', 'ref'],
       'literal_doc': ['literal', 'doc'],
   }

================================== ==============================
``:ref:`composite-roles```         :ref:`composite-roles`
``:literal_ref:`composite-roles``` :literal_ref:`composite-roles`
``:doc:`changelog```               :doc:`changelog`
``:literal_doc:`changelog```       :literal_doc:`changelog`
================================== ==============================

Works with other Extensions
===========================

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
``:literal_issue:`new```   :literal_issue:`new`
========================== ====================

.. seealso:: https://github.com/sphinx-doc/sphinx/issues/11745

.. _sphinx.ext.extlinks: https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

``sphinxnotes.strike``
----------------------

:parsed_literal:`sphinxnotes.strike_` is an extension that adds
:del:`strikethrough text` support to Sphinx.

.. code:: python

   comboroles_roles = {
      'literal_strike': ['literal', 'strike'],
   }

=========================== ======================
``:strike:`text```          :strike:`text`
``:literal_strike:`text```  :literal_strike:`text`
=========================== ======================

.. _sphinxnotes-strike: https://sphinx.silverrainz.me/strike/

