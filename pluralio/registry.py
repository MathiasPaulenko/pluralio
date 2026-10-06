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
    ['en', 'eo', 'es', 'fr', 'it', 'pt']
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field, replace

__all__ = ["LanguageRules", "register", "get_rules", "supported_languages", "snapshot", "restore"]


@dataclass(frozen=True)
class LanguageRules:
    """Container for all pluralization/singularization rules of a language.

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
    """ISO 639-1 language code (e.g. ``"en"``, ``"es"``, ``"fr"``)."""

    irregular_plurals: dict[str, str] = field(default_factory=dict)
    """Singular → plural mapping for words that do not follow regex rules.
    Keys and values are lowercase. Checked **before** regex rules during
    pluralization."""

    irregular_singles: dict[str, str] = field(default_factory=dict)
    """Plural → singular mapping for words that do not follow regex rules.
    Keys and values are lowercase. Checked **before** regex rules during
    singularization. Typically the inverse of ``irregular_plurals``, but
    may include extra entries (e.g. Spanish accent restoration)."""

    plural_rules: list[tuple[re.Pattern[str], str]] = field(default_factory=list)
    """Ordered ``(compiled_regex, replacement)`` tuples applied during
    pluralization. First match wins."""

    singular_rules: list[tuple[re.Pattern[str], str]] = field(default_factory=list)
    """Ordered ``(compiled_regex, replacement)`` tuples applied during
    singularization. First match wins."""

    uncountable: set[str] = field(default_factory=set)
    """Lowercase invariable words — both ``pluralize`` and ``singularize``
    return them unchanged. Checked **first**, before irregulars and regex."""


_REGISTRY: dict[str, LanguageRules] = {}
"""Internal registry mapping language codes to :class:`LanguageRules`."""


def register(rules: LanguageRules) -> None:
    """Register a language's rules in the global registry.

    If a language with the same ``code`` already exists, it is overwritten.
    The regex application cache is cleared to prevent stale results.

    The code is normalized (stripped and lowercased) before registration,
    so ``LanguageRules(code=" EN ")`` is registered as ``"en"``. When the
    code needs normalization, a normalized copy of ``rules`` is stored.

    Args:
        rules: The :class:`LanguageRules` instance to register.

    Raises:
        ValueError: If ``rules.code`` is empty or whitespace-only.

    Example:
        >>> from pluralio.registry import LanguageRules, register
        >>> state = snapshot()
        >>> register(LanguageRules(code="xx"))
        >>> "xx" in supported_languages()
        True
        >>> restore(state)
    """
    code = rules.code.strip().lower() if isinstance(rules.code, str) else rules.code
    if not code:
        raise ValueError("Language code cannot be empty")
    _REGISTRY[code] = rules if rules.code == code else replace(rules, code=code)
    from pluralio.core import _clear_regex_cache

    _clear_regex_cache()


def get_rules(lang: str) -> LanguageRules:
    """Retrieve the rules for a given language code.

    The lookup is normalized the same way as :func:`register` —
    ``get_rules(" EN ")`` resolves to ``"en"``.

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
    key = lang.strip().lower() if isinstance(lang, str) else lang
    if key not in _REGISTRY:
        raise ValueError(
            f"Unsupported language: {lang!r}. Supported: {sorted(_REGISTRY)}"
        )
    return _REGISTRY[key]


def supported_languages() -> list[str]:
    """Return a sorted list of all registered language codes.

    Returns:
        Sorted list of ISO 639-1 codes (e.g. ``["en", "eo", "es", "fr", "it", "pt"]``).

    Example:
        >>> from pluralio.registry import supported_languages
        >>> supported_languages()
        ['en', 'eo', 'es', 'fr', 'it', 'pt']
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

    Clears the regex application cache to prevent stale results after
    restoration. This is critical for test isolation — :mod:`conftest`
    uses ``snapshot`` / ``restore`` around every test.

    Args:
        state: A dict previously returned by :func:`snapshot`.

    Example:
        >>> from pluralio.registry import snapshot, restore
        >>> state = snapshot()
        >>> # ... mutations happen ...
        >>> restore(state)
    """
    _REGISTRY.clear()
    _REGISTRY.update(state)
    from pluralio.core import _clear_regex_cache

    _clear_regex_cache()
