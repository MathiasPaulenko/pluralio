"""Esperanto pluralization and singularization rules.

This module defines the complete set of Esperanto pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``eo`` language in the global registry.

Esperanto has the simplest pluralization system of any language:
every noun takes ``-j`` to form the plural, and the accusative
case adds ``-n`` after the plural marker. There are no irregulars,
no gender, and no exceptions.

Rules:
    - ``libro``   → ``libroj``   (singular → plural, add ``j``)
    - ``libroj``  → ``libro``    (plural → singular, remove ``j``)
    - ``libron``  → ``librojn``  (accusative singular → accusative plural)
    - ``librojn`` → ``libron``   (accusative plural → accusative singular)

Uncountable words: pronouns and correlatives that do not take
plural (``mi``, ``vi``, ``li``, ``ŝi``, ``ĝi``, ``ni``, ``ili``,
``oni``, ``si``).
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_PLURAL_RULES: list[tuple[str, str]] = [
    # Accusative singular: -n → -jn (e.g. libron → librojn)
    (r"n$", "jn"),
    # Default: append -j (e.g. libro → libroj)
    (r"$", "j"),
]

_SINGULAR_RULES: list[tuple[str, str]] = [
    # Accusative plural: -jn → -n (e.g. librojn → libron)
    (r"jn$", "n"),
    # Nominative plural: -j → "" (e.g. libroj → libro)
    (r"j$", ""),
]

_UNCOUNTABLE: set[str] = {
    # Pronouns
    "mi", "vi", "li", "ŝi", "ĝi", "ni", "ili", "oni", "si",
    # Correlatives that don't take plural
    "kio", "tio", "ĉio", "nenio", "iom",
    # Conjunctions, prepositions, particles
    "kaj", "aŭ", "sed", "ĉar", "se", "ke",
    "en", "sur", "sub", "apud", "inter", "post",
    "kun", "sen", "per", "por", "pro", "de", "da",
    "al", "el", "ĝis", "tra", "kontraŭ",
    # Articles
    "la",
}

_RULES = LanguageRules(
    code="eo",
    plural_rules=[(re.compile(p), r) for p, r in _PLURAL_RULES],
    singular_rules=[(re.compile(p), r) for p, r in _SINGULAR_RULES],
    uncountable=_UNCOUNTABLE,
)

register(_RULES)
