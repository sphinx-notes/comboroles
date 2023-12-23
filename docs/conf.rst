=============
Configuration
=============

.. confval:: comboroles_roles
   :type: dict[str, list[str] | tuple[list[str], bool]]
   :default: {}

   Every item of the confval declares the name of composite role and how they
   are composited.

   The ``str`` key of dict is the name of composite roles.

   The value can be ``list[str]`` with an optional ``bool``.
   The ``list[str]`` is a list of existing role name to be composited,
   see :ref:`composite-roles` for more details.

   The optional ``bool`` is flag of ``nested_parse``, indicates
   whether the :ref:`nested-parse` function is enabled.
   If no optional bool is given, ``nested_parse`` is disabled by default.
