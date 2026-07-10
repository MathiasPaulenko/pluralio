"""Core pluralization and singularization engine.

This module implements the main algorithm that transforms a word
between its singular and plural forms. The algorithm follows a
three-step priority chain for each word:

1. **Uncountable check** — if the word is in the language's
   ``uncountable`` set, it is returned unchanged.
2. **Irregular lookup** — if the word appears in the irregular
   mapping (``irregular_plurals`` or ``irregular_singles``),
   the mapped form is returned.
3. **Regex rules** — the first matching regex rule in the
   ordered list is applied. If no rule matches, the word is
   returned unchanged.

Additional features handled here:

- **Case preservation**: the output mirrors the casing of the
  input (title case, all caps, lowercase).
- **Hyphenated words**: only the first segment is transformed
  (e.g. ``"mother-in-law"`` → ``"mothers-in-law"``).
- **Count-aware pluralization**: when ``count == 1`` the word
  is returned in singular form regardless of other rules.
- **Input validation**: non-string inputs raise ``TypeError``;
  empty or whitespace-only strings are returned as-is.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, get_rules


def _match_case(source: str, target: str) -> str:
    """Apply the casing pattern of ``source`` to ``target``.

    Three modes are supported:
    - **All caps**: if ``source`` is entirely uppercase, ``target``
      is returned in uppercase.
    - **Title case**: if only the first character of ``source`` is
      uppercase, ``target`` is capitalized on its first character.
    - **Lowercase**: otherwise ``target`` is returned unchanged.

    Args:
        source: The original word whose casing pattern to replicate.
        target: The transformed word to re-case.

    Returns:
        ``target`` with the casing of ``source`` applied.

    Example:
        >>> _match_case("Library", "libraries")
        'Libraries'
        >>> _match_case("LIBRARY", "libraries")
        'LIBRARIES'
        >>> _match_case("library", "libraries")
        'libraries'
    """
    if source.isupper():
        return target.upper()
    if source[0].isupper():
        return target[0].upper() + target[1:]
    return target


def _apply_rules(
    word: str,
    rules: LanguageRules,
    irregulars: dict[str, str],
    rule_list: list[tuple[re.Pattern[str], str]],
) -> str:
    """Apply the three-step transformation chain to a single word.

    This is the shared inner logic used by both :func:`pluralize` and
    :func:`singularize`. It checks uncountables first, then irregulars,
    then regex rules, preserving the input casing in the result.

    Args:
        word: The word to transform (already stripped, no hyphens).
        rules: The :class:`LanguageRules` for the target language.
        irregulars: Either ``irregular_plurals`` or ``irregular_singles``
            from the language rules, depending on direction.
        rule_list: Either ``plural_rules`` or ``singular_rules`` from
            the language rules, depending on direction.

    Returns:
        The transformed word with original casing preserved.
    """
    lower = word.lower()
    if lower in rules.uncountable:
        return word
    if lower in irregulars:
        return _match_case(word, irregulars[lower])
    for pattern, replacement in rule_list:
        if pattern.search(lower):
            return _match_case(word, pattern.sub(replacement, lower, count=1))
    return word


def _pluralize_hyphenated(word: str, lang: str, count: int | None) -> str:
    """Pluralize only the first segment of a hyphenated word.

    Args:
        word: The hyphenated word (e.g. ``"mother-in-law"``).
        lang: Language code to pass through.
        count: Count value to pass through for count-aware behavior.

    Returns:
        The word with its first segment pluralized
        (e.g. ``"mothers-in-law"``).
    """
    parts = word.split("-")
    parts[0] = pluralize(parts[0], lang=lang, count=count)
    return "-".join(parts)


def _singularize_hyphenated(word: str, lang: str) -> str:
    """Singularize only the first segment of a hyphenated word.

    Args:
        word: The hyphenated word (e.g. ``"mothers-in-law"``).
        lang: Language code to pass through.

    Returns:
        The word with its first segment singularized
        (e.g. ``"mother-in-law"``).
    """
    parts = word.split("-")
    parts[0] = singularize(parts[0], lang=lang)
    return "-".join(parts)


def pluralize(word: str, lang: str = "en", count: int | None = None) -> str:
    """Convert a word to its plural form.

    The function follows the three-step priority chain
    (uncountable → irregular → regex) and preserves the input
    casing in the output.

    Args:
        word: The singular word to pluralize.
        lang: ISO 639-1 language code. Defaults to ``"en"``.
        count: Optional integer count. When ``count == 1`` the word
            is returned unchanged (singular form). Any other value
            (including ``0``, negative numbers, and ``None``) produces
            the plural form.

    Returns:
        The plural form of ``word``, with original casing preserved.

    Raises:
        TypeError: If ``word`` is not a string.
        ValueError: If ``lang`` is not a registered language.

    Example:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("box")
        'boxes'
        >>> pluralize("child")
        'children'
        >>> pluralize("gato", lang="es")
        'gatos'
        >>> pluralize("item", count=1)
        'item'
        >>> pluralize("Library")
        'Libraries'
        >>> pluralize("mother-in-law")
        'mothers-in-law'
    """
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    stripped = word.strip()
    if not stripped:
        return word
    if count is not None and count == 1:
        return word
    rules = get_rules(lang)
    if "-" in stripped:
        return _pluralize_hyphenated(stripped, lang, count)
    return _apply_rules(stripped, rules, rules.irregular_plurals, rules.plural_rules)


def singularize(word: str, lang: str = "en") -> str:
    """Convert a word to its singular form.

    The function follows the three-step priority chain
    (uncountable → irregular → regex) and preserves the input
    casing in the output.

    Args:
        word: The plural word to singularize.
        lang: ISO 639-1 language code. Defaults to ``"en"``.

    Returns:
        The singular form of ``word``, with original casing preserved.

    Raises:
        TypeError: If ``word`` is not a string.
        ValueError: If ``lang`` is not a registered language.

    Example:
        >>> singularize("cities")
        'city'
        >>> singularize("mice")
        'mouse'
        >>> singularize("lápices", lang="es")
        'lápiz'
        >>> singularize("Libraries")
        'Library'
        >>> singularize("mothers-in-law")
        'mother-in-law'
    """
    if not isinstance(word, str):
        raise TypeError(f"word must be str, got {type(word).__name__}")
    stripped = word.strip()
    if not stripped:
        return word
    rules = get_rules(lang)
    if "-" in stripped:
        return _singularize_hyphenated(stripped, lang)
    return _apply_rules(stripped, rules, rules.irregular_singles, rules.singular_rules)
