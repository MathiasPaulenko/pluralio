"""pluralio — Pluralization and singularization for Python.

Public API:
    - :func:`pluralize`: Convert a word to plural form.
    - :func:`singularize`: Convert a word to singular form.
    - :func:`supported_languages`: List registered language codes.
    - :func:`add_irregular`: Add an irregular word pair (both directions).
    - :func:`add_plural`: Add only the singular→plural direction.
    - :func:`add_singular`: Add only the plural→singular direction.
    - :func:`add_uncountable`: Mark a word as invariable.
    - :func:`add_plural_rule`: Insert a pluralization regex rule.
    - :func:`add_singular_rule`: Insert a singularization regex rule.
    - :func:`register_language`: Register a new language with its rules.
    - :func:`is_plural`: Check if a word is in plural form.
    - :func:`is_singular`: Check if a word is in singular form.
    - :class:`LanguageRules`: Dataclass for custom language rules.
    - :func:`register`: Low-level registry registration.
    - :func:`get_rules`: Low-level registry lookup.

Supported languages (built-in):
    - English (``en``)
    - Spanish (``es``)
    - Portuguese (``pt``)
    - French (``fr``)
    - Italian (``it``)

.. note::
    Language rules are registered as a side effect of importing this
    package. Always use ``import pluralio`` (or
    ``from pluralio import pluralize``) rather than importing from
    submodules directly, e.g. avoid ``from pluralio.core import pluralize``,
    because the latter bypasses registration and will raise
    ``ValueError`` for any non-default language.

Example:
    >>> import pluralio
    >>> pluralio.pluralize("cat")
    'cats'
    >>> pluralio.pluralize("gato", lang="es")
    'gatos'
    >>> pluralio.singularize("cities")
    'city'
"""

import re
import unicodedata
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pluralio import rules as _rules  # noqa: F401 — triggers registration
from pluralio.core import _clear_regex_cache, pluralize, singularize
from pluralio.registry import (
    LanguageRules,
    get_rules,
    register,
    supported_languages,
)


def _read_version() -> str:
    try:
        return version("pluralio")
    except PackageNotFoundError:
        pass
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(), re.M)
        if match:
            return match.group(1)
    return "0.0.0+unknown"


__version__ = _read_version()
"""Package version string (read from installed package metadata or pyproject.toml)."""

__all__ = [
    "pluralize",
    "singularize",
    "supported_languages",
    "LanguageRules",
    "register",
    "get_rules",
    "add_irregular",
    "add_plural",
    "add_singular",
    "add_uncountable",
    "add_plural_rule",
    "add_singular_rule",
    "register_language",
    "is_plural",
    "is_singular",
    "__version__",
]


def add_irregular(singular: str, plural: str, lang: str = "en") -> None:
    """Add an irregular word pair for both pluralize and singularize.

    This registers the word in both ``irregular_plurals``
    (singular → plural) and ``irregular_singles`` (plural → singular),
    so that both :func:`pluralize` and :func:`singularize` use the
    mapping. The entries are stored in lowercase for case-insensitive
    matching.

    Args:
        singular: The singular form of the word.
        plural: The plural form of the word.
        lang: Language code to register the pair in. Defaults to ``"en"``.

    Example:
        >>> add_irregular("person", "people")
        >>> pluralize("person")
        'people'
        >>> singularize("people")
        'person'
    """
    rules = get_rules(lang)
    rules.irregular_plurals[singular.lower()] = plural.lower()
    rules.irregular_singles[plural.lower()] = singular.lower()
    _clear_regex_cache()


def add_plural(singular: str, plural: str, lang: str = "en") -> None:
    """Add only the singular→plural direction for an irregular word.

    Unlike :func:`add_irregular`, this only affects :func:`pluralize`.
    :func:`singularize` will not know about the inverse mapping.

    This is useful when the plural→singular direction follows a
    different rule or needs a separate entry (e.g. Spanish accent
    restoration).

    Args:
        singular: The singular form of the word.
        plural: The plural form of the word.
        lang: Language code. Defaults to ``"en"``.

    Example:
        >>> add_plural("joven", "jóvenes", lang="es")
        >>> pluralize("joven", lang="es")
        'jóvenes'
    """
    rules = get_rules(lang)
    rules.irregular_plurals[singular.lower()] = plural.lower()
    _clear_regex_cache()


def add_singular(plural: str, singular: str, lang: str = "en") -> None:
    """Add only the plural→singular direction for an irregular word.

    Unlike :func:`add_irregular`, this only affects :func:`singularize`.
    :func:`pluralize` will not know about the forward mapping.

    This is useful for Spanish accent restoration where the plural
    form has a predictable ending but the singular requires an accent
    that the regex rules cannot infer.

    Args:
        plural: The plural form of the word.
        singular: The singular form of the word.
        lang: Language code. Defaults to ``"en"``.

    Example:
        >>> add_singular("alemanes", "alemán", lang="es")
        >>> singularize("alemanes", lang="es")
        'alemán'
    """
    rules = get_rules(lang)
    rules.irregular_singles[plural.lower()] = singular.lower()
    _clear_regex_cache()


def add_uncountable(word: str, lang: str = "en") -> None:
    """Mark a word as uncountable (invariable).

    Uncountable words are returned unchanged by both :func:`pluralize`
    and :func:`singularize`. They are checked **before** irregulars
    and regex rules, so they take highest priority.

    Args:
        word: The word to mark as uncountable.
        lang: Language code. Defaults to ``"en"``.

    Example:
        >>> add_uncountable("data")
        >>> pluralize("data")
        'data'
        >>> singularize("data")
        'data'
    """
    rules = get_rules(lang)
    rules.uncountable.add(word.lower())
    _clear_regex_cache()


def add_plural_rule(pattern: str, replacement: str, lang: str = "en") -> None:
    """Insert a pluralization regex rule at the top (highest priority).

    Rules are checked in order, and the first match wins. By inserting
    at position 0, the new rule takes priority over all existing rules.

    Args:
        pattern: Regular expression pattern to match (string, will be
            compiled internally).
        replacement: Replacement string for ``re.sub``.
        lang: Language code. Defaults to ``"en"``.

    Example:
        >>> add_plural_rule(r"us$", "i")
        >>> pluralize("cactus")
        'cacti'
    """
    rules = get_rules(lang)
    rules.plural_rules.insert(0, (re.compile(pattern), replacement))
    _clear_regex_cache()


def add_singular_rule(pattern: str, replacement: str, lang: str = "en") -> None:
    """Insert a singularization regex rule at the top (highest priority).

    Rules are checked in order, and the first match wins. By inserting
    at position 0, the new rule takes priority over all existing rules.

    Args:
        pattern: Regular expression pattern to match (string, will be
            compiled internally).
        replacement: Replacement string for ``re.sub``.
        lang: Language code. Defaults to ``"en"``.

    Example:
        >>> add_singular_rule(r"i$", "us")
        >>> singularize("cacti")
        'cactus'
    """
    rules = get_rules(lang)
    rules.singular_rules.insert(0, (re.compile(pattern), replacement))
    _clear_regex_cache()


def register_language(
    lang: str,
    *,
    plural_rules: list[tuple[str, str]] | None = None,
    singular_rules: list[tuple[str, str]] | None = None,
    irregular_plurals: dict[str, str] | None = None,
    irregular_singles: dict[str, str] | None = None,
    uncountable: set[str] | None = None,
) -> None:
    """Register a new language with its pluralization rules.

    This is the high-level API for adding a completely new language.
    It compiles the regex patterns, normalizes keys to lowercase,
    auto-generates inverse irregular mappings, and registers the
    resulting :class:`LanguageRules` in the global registry.

    If ``plural_rules`` is omitted, a default rule of ``(r"$", "s")``
    is used (append ``s``).
    If ``singular_rules`` is omitted, a default rule of ``(r"s$", "")``
    is used (strip trailing ``s``).

    For every entry in ``irregular_plurals``, the inverse is
    automatically added to ``irregular_singles`` unless an explicit
    entry already exists.

    Args:
        lang: ISO 639-1 language code for the new language.
        plural_rules: List of ``(pattern, replacement)`` string tuples
            for pluralization. Checked in order; first match wins.
        singular_rules: List of ``(pattern, replacement)`` string tuples
            for singularization. Checked in order; first match wins.
        irregular_plurals: Mapping of singular → plural for irregular
            words. Keys and values are normalized to lowercase.
        irregular_singles: Mapping of plural → singular for irregular
            words. Keys and values are normalized to lowercase.
            Auto-populated from ``irregular_plurals`` where possible.
        uncountable: Set of invariable words. Normalized to lowercase.

    Example:
        >>> register_language(
        ...     "fr",
        ...     plural_rules=[(r"$", "s")],
        ...     singular_rules=[(r"s$", "")],
        ...     irregular_plurals={"cheval": "chevaux"},
        ...     uncountable={"information"},
        ... )
        >>> pluralize("chat", lang="fr")
        'chats'
        >>> pluralize("cheval", lang="fr")
        'chevaux'
        >>> singularize("chevaux", lang="fr")
        'cheval'
        >>> pluralize("information", lang="fr")
        'information'
    """
    plurals = {k.lower(): v.lower() for k, v in (irregular_plurals or {}).items()}
    singles = {k.lower(): v.lower() for k, v in (irregular_singles or {}).items()}
    for singular, plural in plurals.items():
        singles.setdefault(plural, singular)

    compiled_plural = [(re.compile(p), r) for p, r in (plural_rules or [(r"$", "s")])]
    compiled_singular = [(re.compile(p), r) for p, r in (singular_rules or [(r"s$", "")])]

    register(LanguageRules(
        code=lang,
        irregular_plurals=plurals,
        irregular_singles=singles,
        plural_rules=compiled_plural,
        singular_rules=compiled_singular,
        uncountable={w.lower() for w in (uncountable or set())},
    ))
    _clear_regex_cache()


def is_plural(word: str, lang: str = "en") -> bool:
    """Check if a word is in its plural form.

    A word is considered plural if singularizing it produces a
    different word. Uncountable (invariable) words are valid as
    both singular and plural, so they return ``True``.

    Args:
        word: The word to check.
        lang: ISO 639-1 language code. Defaults to ``"en"``.

    Returns:
        ``True`` if the word is in plural form (or is uncountable),
        ``False`` otherwise.

    Raises:
        TypeError: If ``word`` is not a string.
        ValueError: If ``lang`` is not a registered language.

    Example:
        >>> is_plural("cats")
        True
        >>> is_plural("cat")
        False
        >>> is_plural("sheep")
        True
        >>> is_plural("gatos", lang="es")
        True
    """
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    stripped = unicodedata.normalize("NFC", word.strip())
    if not stripped:
        return False
    if stripped.lower() in get_rules(lang).uncountable:
        return True
    return singularize(stripped, lang=lang).lower() != stripped.lower()


def is_singular(word: str, lang: str = "en") -> bool:
    """Check if a word is in its singular form.

    A word is considered singular if pluralizing it produces a
    different word. Uncountable (invariable) words are valid as
    both singular and plural, so they return ``True``.

    Args:
        word: The word to check.
        lang: ISO 639-1 language code. Defaults to ``"en"``.

    Returns:
        ``True`` if the word is in singular form (or is uncountable),
        ``False`` otherwise.

    Raises:
        TypeError: If ``word`` is not a string.
        ValueError: If ``lang`` is not a registered language.

    Example:
        >>> is_singular("cat")
        True
        >>> is_singular("cats")
        False
        >>> is_singular("sheep")
        True
        >>> is_singular("gato", lang="es")
        True
    """
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    stripped = unicodedata.normalize("NFC", word.strip())
    if not stripped:
        return False
    if stripped.lower() in get_rules(lang).uncountable:
        return True
    return pluralize(stripped, lang=lang).lower() != stripped.lower()
