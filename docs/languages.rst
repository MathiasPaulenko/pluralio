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
     - 352 + 81
     - 92
     - Complete
   * - Portuguese
     - ``pt``
     - 8 + 13
     - 388 + 88
     - 88
     - Complete
   * - French
     - ``fr``
     - 6 + 4
     - 104 + 27
     - 81
     - Complete
   * - Italian
     - ``it``
     - 19 + 12
     - 239
     - 144
     - Complete
   * - Esperanto
     - ``eo``
     - 4 + 2
     - 0
     - 33
     - Complete

Language-specific notes
-----------------------

English (``en``)
~~~~~~~~~~~~~~~~

- 684 irregulars covering Latin/Greek plurals, compound words, and
  special cases.
- Regex rules handle ``-s``, ``-es``, ``-ies``, ``-ves``, ``-oes``,
  ``-oes``, and classical plurals (``-i``, ``-a``, ``-ae``, ``-ina``).
- 219 uncountables including mass nouns, non-noun words, and
  invariable terms.

Spanish (``es``)
~~~~~~~~~~~~~~~~

- Accent restoration: singulars that lose an accent in the plural are
  handled via irregular mappings (e.g. ``joven`` → ``jóvenes``).
- 81 extra singular-only entries for accent restoration that cannot
  be derived from regex rules.
- 92 uncountables.

Portuguese (``pt``)
~~~~~~~~~~~~~~~~~~~

- 88 extra singular-only entries for accent restoration.
- Hyphenated compound handling for verb+noun constructions
  (``quebra-mar`` → ``quebra-mares``).

French (``fr``)
~~~~~~~~~~~~~~~

- Both segments of hyphenated compounds are pluralized, skipping
  function words (articles, prepositions).
- ``-al`` → ``-aux``, ``-ail`` → ``-aux``, ``-euil`` → ``-euils``.

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
- 33 uncountables: pronouns, correlatives, and particles.

Roadmap
-------

.. list-table::
   :header-rows: 1

   * - Version
     - Goal
     - Status
   * - ``2.2.0``
     - Catalan (``ca``)
     - Planned
   * - ``2.3.0``
     - Dutch (``nl``)
     - Planned
   * - ``3.0.0``
     - German (``de``)
     - Planned
