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

import unicodedata
from functools import lru_cache

from pluralio.registry import LanguageRules, get_rules


def _match_case(source: str, target: str) -> str:
    """Apply the casing pattern of ``source`` to ``target``.

    Four modes are supported:
    - **All caps**: if ``source`` is entirely uppercase, ``target``
      is returned in uppercase.
    - **Title case**: if only the first character of ``source`` is
      uppercase and the rest are lowercase, ``target`` is capitalized
      on its first character.
    - **Mixed case**: if ``source`` has uppercase letters beyond the
      first character but is not all caps, each character position in
      ``target`` mirrors the case of the corresponding position in
      ``source``. Extra characters in ``target`` default to lowercase.
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
        >>> _match_case("McDonald", "mcdonalds")
        'McDonalds'
        >>> _match_case("iPhone", "iphones")
        'iPhones'
    """
    first_upper = source[0].isupper()
    # Single pass: detect all-upper, title case, or mixed
    all_upper = first_upper
    has_upper_after_first = False
    for c in source[1:]:
        if c.isupper():
            has_upper_after_first = True
        else:
            all_upper = False
    # Fast path: all lowercase
    if not first_upper and not has_upper_after_first:
        return target
    if all_upper:
        return target.upper()
    if first_upper and not has_upper_after_first:
        # Title case: first upper, rest lower
        return target[0].upper() + target[1:]
    # Mixed case: mirror each position
    result = []
    for i, char in enumerate(target):
        if i < len(source):
            result.append(char.upper() if source[i].isupper() else char.lower())
        else:
            result.append(char.lower())
    return "".join(result)


@lru_cache(maxsize=4096)
def _apply_regex_to_word(lower: str, lang: str, is_plural: bool) -> str:
    """Apply regex rules to a lowercase word and return the result.

    This is the cached inner loop of :func:`_apply_rules`. Only the
    regex iteration is cached — uncountable and irregular lookups
    remain in the uncached caller because they are O(1) dict checks.

    Args:
        lower: The lowercase word to transform.
        lang: Language code for rule lookup.
        is_plural: ``True`` for pluralization rules, ``False`` for
            singularization rules.

    Returns:
        The transformed lowercase word, or the original word if no
            rule matches.
    """
    rules = get_rules(lang)
    rule_list = rules.plural_rules if is_plural else rules.singular_rules
    for pattern, replacement in rule_list:
        if pattern.search(lower):
            return pattern.sub(replacement, lower, count=1)
    return lower


def _clear_regex_cache() -> None:
    """Clear the regex application cache.

    Must be called whenever language rules are modified at runtime
    (e.g. via :func:`add_irregular`, :func:`add_plural_rule`, etc.)
    to prevent stale cached results.
    """
    _apply_regex_to_word.cache_clear()


def _apply_rules(
    word: str,
    lower: str,
    rules: LanguageRules,
    is_plural: bool,
) -> str:
    """Apply the three-step transformation chain to a single word.

    This is the shared inner logic used by both :func:`pluralize` and
    :func:`singularize`. It applies regex rules and preserves the
    input casing in the result. Uncountable and irregular checks
    are performed by the caller before reaching this function.

    Args:
        word: The original word (with original casing).
        lower: The lowercase version of ``word``.
        rules: The :class:`LanguageRules` for the target language.
        is_plural: ``True`` for pluralization rules, ``False`` for
            singularization rules.

    Returns:
        The transformed word with original casing preserved.
    """
    result = _apply_regex_to_word(lower, rules.code, is_plural)
    if not result or result == lower:
        return word
    return _match_case(word, result)


def _split_whitespace(word: str) -> tuple[str, str, str]:
    """Split a word into leading whitespace, core, and trailing whitespace.

    Args:
        word: The string to split.

    Returns:
        A tuple of (leading, core, trailing) where core is the
        stripped content. If the word is entirely whitespace,
        core is empty.
    """
    # Fast path: no surrounding whitespace (common case)
    if word and not word[0].isspace() and not word[-1].isspace():
        return "", word, ""
    stripped = word.strip()
    if not stripped:
        return "", "", ""
    start = len(word) - len(word.lstrip())
    end = len(word.rstrip())
    return word[:start], stripped, word[end:]


# First segments that indicate the LAST segment should be pluralized
# (these are verbs, adjectives, or function words, not head nouns)
_LAST_SEGMENT_PLURAL_FIRST_WORDS: frozenset[str] = frozenset({
    "forget", "merry",
    # Prefixes where the head noun is the last segment
    "meta", "post", "re", "pre", "anti", "pro", "non", "sub",
    "co", "ex", "inter", "intra", "multi", "semi", "pseudo",
    "proto", "neo",
})


def _pluralize_hyphenated(word: str, lang: str, count: int | None) -> str:
    """Pluralize the appropriate segment(s) of a hyphenated word.

    For most English compounds the head noun is the first segment
    (e.g. ``"mother-in-law"`` → ``"mothers-in-law"``).
    For some compounds the head noun is the last segment
    (e.g. ``"forget-me-not"`` → ``"forget-me-nots"``).

    Args:
        word: The hyphenated word (e.g. ``"mother-in-law"``).
        lang: Language code to pass through.
        count: Count value to pass through for count-aware behavior.

    Returns:
        The word with the appropriate segment pluralized.
    """
    parts = word.split("-")
    # Find the first non-empty segment.
    idx = 0
    while idx < len(parts) and not parts[idx]:
        idx += 1
    if idx >= len(parts):
        return word

    first = parts[idx].lower()

    # Check if the last segment should be pluralized instead of the first
    if first in _LAST_SEGMENT_PLURAL_FIRST_WORDS:
        last_idx = len(parts) - 1
        while last_idx >= 0 and not parts[last_idx]:
            last_idx -= 1
        if last_idx >= 0:
            parts[last_idx] = pluralize(parts[last_idx], lang=lang, count=count)
        return "-".join(parts)

    parts[idx] = pluralize(parts[idx], lang=lang, count=count)
    return "-".join(parts)


def _singularize_hyphenated(word: str, lang: str) -> str:
    """Singularize the appropriate segment of a hyphenated word.

    For most compounds the first segment was pluralized
    (e.g. ``"mothers-in-law"`` → ``"mother-in-law"``).
    For last-segment compounds the last segment was pluralized
    (e.g. ``"forget-me-nots"`` → ``"forget-me-not"``).

    Args:
        word: The hyphenated word (e.g. ``"mothers-in-law"``).
        lang: Language code to pass through.

    Returns:
        The word with the appropriate segment singularized.
    """
    parts = word.split("-")
    # Find the first non-empty segment.
    idx = 0
    while idx < len(parts) and not parts[idx]:
        idx += 1
    if idx >= len(parts):
        return word

    first = parts[idx].lower()

    # If the first word indicates last-segment pluralization,
    # singularize the last non-empty segment instead.
    if first in _LAST_SEGMENT_PLURAL_FIRST_WORDS:
        last_idx = len(parts) - 1
        while last_idx >= 0 and not parts[last_idx]:
            last_idx -= 1
        if last_idx >= 0:
            parts[last_idx] = singularize(parts[last_idx], lang=lang)
        return "-".join(parts)

    if idx < len(parts):
        parts[idx] = singularize(parts[idx], lang=lang)
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
    leading, stripped, trailing = _split_whitespace(word)
    if not stripped:
        return word
    if not stripped.isascii():
        stripped = unicodedata.normalize("NFC", stripped)
    if count is not None and count == 1:
        return leading + stripped + trailing
    rules = get_rules(lang)
    lower = stripped if stripped.islower() else stripped.lower()
    if lower in rules.uncountable:
        return leading + stripped + trailing
    if lower in rules.irregular_plurals:
        result = _match_case(stripped, rules.irregular_plurals[lower])
        return leading + result + trailing
    if lower in rules.irregular_singles:
        return leading + stripped + trailing
    if "-" in stripped:
        result = _pluralize_hyphenated(stripped, lang, count)
        return leading + result + trailing
    result = _apply_rules(stripped, lower, rules, is_plural=True)
    return leading + result + trailing


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
    leading, stripped, trailing = _split_whitespace(word)
    if not stripped:
        return word
    if not stripped.isascii():
        stripped = unicodedata.normalize("NFC", stripped)
    rules = get_rules(lang)
    lower = stripped if stripped.islower() else stripped.lower()
    if lower in rules.uncountable:
        return leading + stripped + trailing
    if lower in rules.irregular_singles:
        result = _match_case(stripped, rules.irregular_singles[lower])
        return leading + result + trailing
    if lower in rules.irregular_plurals:
        return leading + stripped + trailing
    if "-" in stripped:
        result = _singularize_hyphenated(stripped, lang)
        return leading + result + trailing
    result = _apply_rules(stripped, lower, rules, is_plural=False)
    return leading + result + trailing
