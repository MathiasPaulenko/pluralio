"""Language registry for pluralio.

This module provides the central registry that maps language codes
to their corresponding :class:`LanguageRules` instances. Each language
module in :mod:`pluralio.rules` (e.g. ``rules.en``, ``rules.es``) builds
a ``LanguageRules`` dataclass and calls :func:`register` at import time.

The registry is a plain dictionary, so custom languages can be added
at runtime via :func:`register` or :func:`pluralio.register_language`.

Example:
    >>> from pluralio.registry import supported_languages
    >>> supported_languages()
    ['en', 'es', 'fr', 'it', 'pt']
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field

__all__ = ["LanguageRules", "register", "get_rules", "supported_languages", "snapshot", "restore"]


@dataclass(frozen=True)
class LanguageRules:
    """Container for all pluralization/singularization rules of a language.

    Attributes:
        code: ISO 639-1 language code (e.g. ``"en"``, ``"es"``, ``"fr"``).
        irregular_plurals: Mapping of singular → plural for words that
            do not follow regex rules. Keys and values are lowercase.
            Checked **before** regex rules during pluralization.
        irregular_singles: Mapping of plural → singular for words that
            do not follow regex rules. Keys and values are lowercase.
            Checked **before** regex rules during singularization.
            Typically the inverse of ``irregular_plurals``, but may
            include extra entries (e.g. Spanish accent restoration).
        plural_rules: Ordered list of ``(compiled_regex, replacement)``
            tuples applied during pluralization. First match wins.
        singular_rules: Ordered list of ``(compiled_regex, replacement)``
            tuples applied during singularization. First match wins.
        uncountable: Set of lowercase words that are invariable — both
            ``pluralize`` and ``singularize`` return them unchanged.
            Checked **first**, before irregulars and regex.

    .. warning::
        ``frozen=True`` prevents reassigning attributes
        (``rules.code = "fr"`` raises ``FrozenInstanceError``),
        but the mutable containers (``dict``, ``list``, ``set``) can
        still be modified in place. This is **by design** — the
        extensibility API (:func:`pluralio.add_irregular`,
        :func:`pluralio.add_plural`, etc.) mutates the contents of
        already-registered instances. Always use those functions
        instead of mutating containers directly.
    """

    code: str
    irregular_plurals: dict[str, str] = field(default_factory=dict)
    irregular_singles: dict[str, str] = field(default_factory=dict)
    plural_rules: list[tuple[re.Pattern[str], str]] = field(default_factory=list)
    singular_rules: list[tuple[re.Pattern[str], str]] = field(default_factory=list)
    uncountable: set[str] = field(default_factory=set)


_REGISTRY: dict[str, LanguageRules] = {}
"""Internal registry mapping language codes to :class:`LanguageRules`."""


def register(rules: LanguageRules) -> None:
    """Register a language's rules in the global registry.

    If a language with the same ``code`` already exists, it is overwritten.

    Args:
        rules: The :class:`LanguageRules` instance to register.

    Raises:
        ValueError: If ``rules.code`` is empty.

    Example:
        >>> from pluralio.registry import LanguageRules, register
        >>> register(LanguageRules(code="xx"))
    """
    if not rules.code or not rules.code.strip():
        raise ValueError("Language code cannot be empty")
    _REGISTRY[rules.code] = rules


def get_rules(lang: str) -> LanguageRules:
    """Retrieve the rules for a given language code.

    Args:
        lang: ISO 639-1 language code (e.g. ``"en"``, ``"es"``).

    Returns:
        The :class:`LanguageRules` instance for the requested language.

    Raises:
        ValueError: If ``lang`` is not registered. The error message
            includes the list of supported languages.

    Example:
        >>> from pluralio.registry import get_rules
        >>> rules = get_rules("en")
        >>> rules.code
        'en'
    """
    if lang not in _REGISTRY:
        raise ValueError(
            f"Unsupported language: {lang!r}. Supported: {sorted(_REGISTRY)}"
        )
    return _REGISTRY[lang]


def supported_languages() -> list[str]:
    """Return a sorted list of all registered language codes.

    Returns:
        Sorted list of ISO 639-1 codes (e.g. ``["en", "es", "fr", "it", "pt"]``).

    Example:
        >>> from pluralio.registry import supported_languages
        >>> supported_languages()
        ['en', 'es', 'fr', 'it', 'pt']
    """
    return sorted(_REGISTRY)


def snapshot() -> dict[str, LanguageRules]:
    """Return a deep copy of the current registry state.

    Useful for test isolation — call :func:`restore` with the returned
    value to roll back any mutations made by tests.

    Returns:
        A deep copy of the internal ``_REGISTRY`` dict.

    Example:
        >>> from pluralio.registry import snapshot, restore
        >>> state = snapshot()
        >>> # ... mutations happen ...
        >>> restore(state)
    """
    return copy.deepcopy(_REGISTRY)


def restore(state: dict[str, LanguageRules]) -> None:
    """Replace the current registry with a previously snapshotted state.

    Args:
        state: A dict previously returned by :func:`snapshot`.
    """
    _REGISTRY.clear()
    _REGISTRY.update(state)
