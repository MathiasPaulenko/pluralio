Supported Languages
===================

Built-in languages
------------------

Each language has its own rules module in ``pluralio/rules/`` and is
registered automatically when you ``import pluralio``.

.. list-table::
   :header-rows: 1
   :widths: 15 10 20 20 15 20

   * - Language
     - Code
     - Regex rules (P+S)
     - Irregulars
     - Uncountables
     - Status
   * - English
     - ``en``
     - 7 + 22
     - 684
     - 219
     - Complete
   * - Spanish
     - ``es``
     - 9 + 8
     - 354
     - 92
     - Complete
   * - Portuguese
     - ``pt``
     - 9 + 13
     - 393
     - 88
     - Complete
   * - French
     - ``fr``
     - 6 + 4
     - 100
     - 92
     - Complete
   * - Italian
     - ``it``
     - 19 + 12
     - 249
     - 126
     - Complete
   * - Esperanto
     - ``eo``
     - 4 + 2
     - 0
     - 39
     - Complete

Language-specific notes
-----------------------

English (``en``)
~~~~~~~~~~~~~~~~

- 684 irregulars covering Latin/Greek plurals (``-i``, ``-a``,
  ``-ae``, ``-ina``), compound words, and special cases.
- Regex rules handle ``-s``, ``-es``, ``-ies``, ``-ves``, and
  ``-oes`` endings.
- 219 uncountables including mass nouns, non-noun words, and
  invariable terms.

Spanish (``es``)
~~~~~~~~~~~~~~~~

- Accent restoration: singulars that lose an accent in the plural are
  handled via irregular mappings (e.g. ``joven`` → ``jóvenes``).
- 92 uncountables.

Portuguese (``pt``)
~~~~~~~~~~~~~~~~~~~

- Hyphenated compound handling for verb+noun constructions
  (``quebra-mar`` → ``quebra-mares``).

French (``fr``)
~~~~~~~~~~~~~~~

- Both segments of hyphenated compounds are pluralized, skipping
  function words (articles, prepositions) and invariable compounds
  (``porte-monnaie``).
- ``-al`` → ``-aux``, ``-au``/``-eau`` → ``-aux``/``-eaux``,
  ``-eu`` → ``-eux``; the ``-als``/``-ails``/``-eus``/``-ous``
  exceptions live in the irregular tables.

Italian (``it``)
~~~~~~~~~~~~~~~~

- Gender-aware pluralization: ``-o`` → ``-i``, ``-a`` → ``-e``,
  ``-e`` → ``-i``, ``-ca`` → ``-che``, ``-ga`` → ``-ghe``.
- Hyphenated compounds pluralize all noun segments.

Esperanto (``eo``)
~~~~~~~~~~~~~~~~~~

- Simplest pluralization system: ``-j`` suffix for nominative plural,
  ``-jn`` for accusative plural.
- Zero irregulars — the language is perfectly regular by design.
- 39 uncountables: pronouns, correlatives, and particles.

Roadmap
-------

.. list-table::
   :header-rows: 1

   * - Version
     - Goal
     - Status
   * - ``2.3.0``
     - Catalan (``ca``)
     - Planned
   * - ``3.0.0``
     - German (``de``)
     - Planned
