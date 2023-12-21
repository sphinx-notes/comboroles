.. This file is generated from sphinx-notes/template.
   You need to consider modifying the TEMPLATE or modifying THIS FILE.

.. include:: ../README.rst

Introduction
============

.. ADDITIONAL CONTENT START

The extension allows users to create roles composited by multiple roles.

As we know, |rst| does not yet support `nested inline markups/roles`__,
so text like ````***bold italic code***```` doesn't render as expected.
With the extension, we can compose roles ``literal`` (code), ``emphasis``
(italic), and ``strong`` (bold) to composite roles ``literal_emphasis_strong``,
to achieve the same effect as nested inline roles:

.. list-table::

   * - ````***bold italic code***````
     - ``***bold italic code***``
     - ❌
   * - ``:literal_emphasis_strong:`bold italic code```
     - :literal_emphasis_strong:`bold italic code`
     - ✔️

.. warning::

   Due to :ref:`internal-impl`, the extension can only composite simple roles
   (such as `docutils' Standard Roles`__),
   and may crash Sphinx when compositing complex roles,
   so DO NOT report to Sphinx first if it crashes, report to here
   :issue:`new` instead.

.. |rst| image:: /_images/rst.png
   :target: https://docutils.sourceforge.io/rst.html
   :alt: reStructuredText
   :height: 1em
   :align: bottom

__ https://docutils.sourceforge.io/FAQ.html#is-nested-inline-markup-possible
__ https://docutils.sourceforge.io/docs/ref/rst/roles.html#standard-roles

.. ADDITIONAL CONTENT END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation,
   if not, see `Getting Started with Sphinx`_.

First, downloading extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-comboroles

Then, add the extension name to ``extensions`` configuration item in your conf.py_:

.. code-block:: python

   extensions = [
             # …
             'sphinxnotes.comboroles',
             # …
             ]

.. _Getting Started with Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _conf.py: https://www.sphinx-doc.org/en/master/usage/configuration.html

.. ADDITIONAL CONTENT START

TODO: cfg

.. list-table::

   * - ``:literal_emphasis_strong:`Sphinx```
     - :literal_emphasis_strong:`Sphinx`
   * - ``:parsed_literal:`https://silverrainz.me```
     - :parsed_literal:`https://silverrainz.me`

See :doc:`usage` for more details.

.. ADDITIONAL CONTENT END

Contents
========

.. toctree::
   :caption: Contents

   usage
   changelog

The Sphinx Notes Project
========================

This project is a developed by `Shengyu Zhang`__,
as part of **The Sphinx Notes Project**.

.. toctree::
   :caption: The Sphinx Notes Project

   Home <https://sphinx.silverrainz.me/>
   Blog <https://silverrainz.me/blog/category/sphinx.html>
   PyPI <https://pypi.org/search/?q=sphinxnotes>

__ https://github.com/SilverRainZ
