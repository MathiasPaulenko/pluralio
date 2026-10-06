from __future__ import annotations

import pytest

from pluralio import add_singular_rule
from pluralio.core import pluralize, singularize
from pluralio.registry import LanguageRules, register


class TestPluralize:
    def test_count_one_returns_singular(self) -> None:
        assert pluralize("item", count=1) == "item"

    def test_count_none_returns_plural(self) -> None:
        assert pluralize("item") == "items"

    def test_count_zero_returns_plural(self) -> None:
        assert pluralize("item", count=0) == "items"

    def test_count_negative_returns_plural(self) -> None:
        assert pluralize("item", count=-1) == "items"

    def test_count_two_returns_plural(self) -> None:
        assert pluralize("item", count=2) == "items"

    def test_count_string_one_returns_singular(self) -> None:
        assert pluralize("item", count="1") == "item"  # type: ignore[arg-type]

    def test_invalid_lang_raises_on_empty_word(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            pluralize("", lang="zz")

    def test_uncountable_returns_unchanged(self) -> None:
        assert pluralize("sheep") == "sheep"

    def test_irregular_plural_lookup(self) -> None:
        assert pluralize("man") == "men"

    def test_first_matching_regex_rule_wins(self) -> None:
        assert pluralize("box") == "boxes"
        assert pluralize("city") == "cities"
        assert pluralize("cat") == "cats"

    def test_no_rule_matches_returns_unchanged(self) -> None:
        register(LanguageRules(code="empty"))
        assert pluralize("word", lang="empty") == "word"

    def test_empty_string_returns_empty(self) -> None:
        assert pluralize("") == ""


class TestSingularize:
    def test_irregular_single_lookup(self) -> None:
        assert singularize("men") == "man"

    def test_uncountable_returns_unchanged(self) -> None:
        assert singularize("sheep") == "sheep"

    def test_first_matching_regex_rule_wins(self) -> None:
        assert singularize("cities") == "city"
        assert singularize("boxes") == "box"
        assert singularize("cats") == "cat"

    def test_no_rule_matches_returns_unchanged(self) -> None:
        register(LanguageRules(code="empty"))
        assert singularize("word", lang="empty") == "word"

    def test_empty_string_returns_empty(self) -> None:
        assert singularize("") == ""

    def test_invalid_lang_raises_on_empty_word(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            singularize("", lang="zz")

    def test_rule_producing_empty_string_is_honored(self) -> None:
        add_singular_rule(r"onlys$", "")
        assert singularize("onlys") == ""
