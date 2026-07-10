from __future__ import annotations

import pytest

from pluralio import pluralize, singularize


class TestInputValidation:
    def test_empty_string_pluralize(self) -> None:
        assert pluralize("") == ""

    def test_empty_string_singularize(self) -> None:
        assert singularize("") == ""

    def test_none_raises_typeerror_pluralize(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            pluralize(None)  # type: ignore[arg-type]

    def test_none_raises_typeerror_singularize(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            singularize(None)  # type: ignore[arg-type]

    def test_non_string_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            pluralize(123)  # type: ignore[arg-type]

    def test_int_input_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            singularize(42)  # type: ignore[arg-type]


class TestCasePreservation:
    @pytest.mark.parametrize("word,expected", [
        ("Library", "Libraries"),
        ("LIBRARY", "LIBRARIES"),
        ("Box", "Boxes"),
        ("BOX", "BOXES"),
        ("Child", "Children"),
        ("CHILD", "CHILDREN"),
        ("City", "Cities"),
        ("CITY", "CITIES"),
    ])
    def test_title_case_preserved(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("Libraries", "Library"),
        ("LIBRARIES", "LIBRARY"),
        ("Boxes", "Box"),
        ("Children", "Child"),
    ])
    def test_singularize_case_preserved(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestHyphenatedWords:
    def test_mother_in_law(self) -> None:
        assert pluralize("mother-in-law") == "mothers-in-law"

    def test_runner_up(self) -> None:
        assert pluralize("runner-up") == "runners-up"

    def test_singularize_hyphenated(self) -> None:
        assert singularize("mothers-in-law") == "mother-in-law"

    def test_spanish_hyphenated(self) -> None:
        assert pluralize("café-bar", lang="es") == "cafés-bar"


class TestWordsWithNumbers:
    def test_word_with_trailing_number(self) -> None:
        assert pluralize("item42") == "item42s"

    def test_word_with_leading_number(self) -> None:
        assert pluralize("42item") == "42items"


class TestWhitespaceHandling:
    def test_strips_whitespace_pluralize(self) -> None:
        assert pluralize("  cat  ") == "cats"

    def test_strips_whitespace_singularize(self) -> None:
        assert singularize("  cats  ") == "cat"

    def test_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ") == "   "
        assert singularize("   ") == "   "
