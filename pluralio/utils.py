"""Utility functions for pluralio.

This module provides helper functions that complement the core
pluralization/singularization API:

- :func:`join`: Join words into a natural-language list.
- :func:`ordinal`: Convert a number to its ordinal string (``1`` → ``"1st"``).
- :func:`template`: Interpolate pluralize/singularize into string templates.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from pluralio.core import pluralize, singularize

__all__ = ["join", "ordinal", "template"]


def join(
    words: Iterable[str],
    *,
    conjunction: str = "and",
    final_sep: str = ", ",
    sep: str = ", ",
) -> str:
    """Join words into a natural-language list.

    Args:
        words: Iterable of strings to join.
        conjunction: Conjunction word for the last item. Defaults to ``"and"``.
        final_sep: Separator before the conjunction. Defaults to ``", "``.
            Pass ``""`` for no comma before the conjunction (Oxford comma
            removal).
        sep: Separator between items (except before the conjunction).
            Defaults to ``", "``.

    Returns:
        A natural-language string joining all words.

    Example:
        >>> join(["apple"])
        'apple'
        >>> join(["apple", "banana"])
        'apple and banana'
        >>> join(["apple", "banana", "carrot"])
        'apple, banana, and carrot'
        >>> join(["apple", "banana", "carrot"], final_sep="")
        'apple, banana and carrot'
        >>> join(["apple", "banana", "carrot"], conjunction="or")
        'apple, banana, or carrot'
    """
    items = list(words)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} {conjunction} {items[1]}"
    head = sep.join(items[:-1])
    if final_sep:
        return f"{head}{final_sep}{conjunction} {items[-1]}"
    return f"{head} {conjunction} {items[-1]}"


def ordinal(number: int | str) -> str:
    """Convert a number to its ordinal string representation.

    Args:
        number: An integer or a string representation of an integer.

    Returns:
        The ordinal string (e.g. ``"1st"``, ``"2nd"``, ``"3rd"``, ``"11th"``).

    Raises:
        ValueError: If ``number`` cannot be converted to an integer.

    Example:
        >>> ordinal(1)
        '1st'
        >>> ordinal(2)
        '2nd'
        >>> ordinal(3)
        '3rd'
        >>> ordinal(11)
        '11th'
        >>> ordinal(21)
        '21st'
        >>> ordinal("101")
        '101st'
        >>> ordinal(0)
        '0th'
    """
    n = int(number)
    abs_n = abs(n)
    suffix = "th" if 10 <= abs_n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(abs_n % 10, "th")
    return f"{n}{suffix}"


_TEMPLATE_PATTERN = re.compile(
    r"\{(\w+)(?::(pluralize|singularize)(?::(\w+))?)?\}"
)


def template(text: str, **kwargs: object) -> str:
    """Interpolate pluralize/singularize into a string template.

    Placeholders use the syntax ``{name}``, ``{name:pluralize}``, or
    ``{name:singularize}``. When ``:pluralize`` is used, the function
    looks for a ``count`` key in ``kwargs`` (or a custom count variable
    specified as ``{name:pluralize:count_var}``) to enable count-aware
    pluralization.

    Args:
        text: Template string with placeholders.
        **kwargs: Values for placeholder substitution. If a ``count`` key
            is present, it is used for count-aware pluralization. A custom
            count variable can be specified in the placeholder syntax
            (e.g. ``{word:pluralize:n}`` uses ``kwargs["n"]`` as the count).

    Returns:
        The interpolated string.

    Raises:
        KeyError: If a placeholder name is not found in ``kwargs``.

    Example:
        >>> template("I have {count} {word:pluralize}", count=5, word="cat")
        'I have 5 cats'
        >>> template("I have {count} {word:pluralize}", count=1, word="cat")
        'I have 1 cat'
        >>> template("The {word:singularize} is here", word="mice")
        'The mouse is here'
        >>> template("{n} {word:pluralize} arrived", n=3, word="box")
        '3 boxes arrived'
    """

    def _replace(match: re.Match[str]) -> str:
        name = match.group(1)
        transform = match.group(2)
        count_var = match.group(3)

        if name not in kwargs:
            raise KeyError(f"Template placeholder {{{name}}} not found in kwargs")

        value = kwargs[name]
        if not isinstance(value, str):
            value = str(value)

        if transform is None:
            return value

        if transform == "pluralize":
            count: int | None = None
            if count_var and count_var in kwargs:
                count = int(str(kwargs[count_var]))
            elif "count" in kwargs:
                count = int(str(kwargs["count"]))
            return pluralize(value, count=count)

        if transform == "singularize":
            return singularize(value)

        return value  # pragma: no cover - unreachable, regex only captures pluralize|singularize

    return _TEMPLATE_PATTERN.sub(_replace, text)
