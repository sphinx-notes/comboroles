.. This file is generated from sphinx-notes/cookiecutter.
   You need to consider modifying the TEMPLATE or modifying THIS FILE.

======================
sphinxnotes-comboroles
======================

.. |docs| image:: https://img.shields.io/github/deployments/sphinx-notes/comboroles/github-pages
   :target: https://sphinx.silverrainz.me/comboroles
   :alt: Documentation Status

.. |license| image:: https://img.shields.io/github/license/sphinx-notes/comboroles
   :target: https://github.com/sphinx-notes/comboroles/blob/master/LICENSE
   :alt: Open Source License

.. |pypi| image:: https://img.shields.io/pypi/v/sphinxnotes-comboroles.svg
   :target: https://pypi.python.org/pypi/sphinxnotes-comboroles
   :alt: PyPI Package

.. |download| image:: https://img.shields.io/pypi/dm/sphinxnotes-comboroles
   :target: https://pypi.python.org/pypi/sphinxnotes-comboroles
   :alt: PyPI Package Downloads

|docs| |license| |pypi| |download|

.. _intro:

Introduction
============

.. INTRODUCTION START

The extension allows users to create roles composited by multiple roles.

As we know, reStructuredText does not yet support `nested inline markups`__,
so text like "bold code" or "italic link" doesn't render as expected.
With the extension, we make nested inline markups possible by compositing roles:

========================================== ====================================== ==
````**bold code**````                      ``**bold code**``                      ❌
``:strong_literal:`bold code```            :strong_literal:`bold code`            ✔️
``*https://example.com*``                  *https://example.com*                  ❌
``:parsed_emphasis:`https://example.com``` :parsed_emphasis:`https://example.com` ✔️
========================================== ====================================== ==

__ https://docutils.sourceforge.io/FAQ.html#is-nested-inline-markup-possible

.. INTRODUCTION END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation,
   if not, see `Getting Started with Sphinx`_.

First, downloading extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-comboroles

Then, add the extension name to ``extensions`` configuration item in your
:parsed_literal:`conf.py_`:

.. code-block:: python

   extensions = [
             # …
             'sphinxnotes.comboroles',
             # …
             ]

.. _Getting Started with Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _conf.py: https://www.sphinx-doc.org/en/master/usage/configuration.html

.. ADDITIONAL CONTENT START

To create a "bold code" role that same as described in :ref:`intro`,
Continue to add the following configuration, which tells the extension to
composite roles :parsed_literal:`strong_` (markup: ``**foo**``) and
:parsed_literal:`literal_` (markup: ````foo````) into a new role ``strong_literal``:

.. code:: python

   comboroles_roles = {
       'strong_literal': ['strong', 'literal'],
   }

Then you can use it:

=============================== ===========================
``:strong_literal:`bold code``` :strong_literal:`bold code`
=============================== ===========================

See :doc:`usage` for more details.

.. _strong: https://docutils.sourceforge.io/docs/ref/rst/roles.html#strong
.. _literal: https://docutils.sourceforge.io/docs/ref/rst/roles.html#literal

.. ADDITIONAL CONTENT END

Contents
========

.. toctree::
   :caption: Contents

   usage
   examples
   conf
   changelog

The Sphinx Notes Project
========================

The project is developed by `Shengyu Zhang`__,
as part of **The Sphinx Notes Project**.

.. toctree::
   :caption: The Sphinx Notes Project

   Home <https://sphinx.silverrainz.me/>
   Blog <https://silverrainz.me/blog/category/sphinx.html>
   PyPI <https://pypi.org/search/?q=sphinxnotes>

__ https://github.com/SilverRainZ
