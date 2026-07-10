from __future__ import annotations

import pytest

import pluralio
from pluralio import add_irregular, add_uncountable, is_plural, is_singular


class TestIsPlural:
    def test_plural_word(self) -> None:
        assert is_plural("cats") is True

    def test_singular_word(self) -> None:
        assert is_plural("cat") is False

    def test_irregular_plural(self) -> None:
        assert is_plural("children") is True

    def test_irregular_singular(self) -> None:
        assert is_plural("child") is False

    def test_uncountable_returns_false(self) -> None:
        assert is_plural("sheep") is False
        assert is_plural("information") is False

    def test_empty_string_returns_false(self) -> None:
        assert is_plural("") is False

    def test_whitespace_only_returns_false(self) -> None:
        assert is_plural("   ") is False

    def test_strips_whitespace(self) -> None:
        assert is_plural("  cats  ") is True

    def test_case_insensitive(self) -> None:
        assert is_plural("CATS") is True
        assert is_plural("Cats") is True

    def test_spanish_plural(self) -> None:
        assert is_plural("gatos", lang="es") is True

    def test_spanish_singular(self) -> None:
        assert is_plural("gato", lang="es") is False

    def test_spanish_irregular_plural(self) -> None:
        assert is_plural("ratones", lang="es") is True

    def test_spanish_uncountable(self) -> None:
        assert is_plural("lunes", lang="es") is False

    def test_non_string_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            is_plural(123)  # type: ignore[arg-type]

    def test_none_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            is_plural(None)  # type: ignore[arg-type]

    def test_unsupported_lang_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            is_plural("cats", lang="zz")

    def test_custom_irregular(self) -> None:
        add_irregular("foo", "foobars")
        assert is_plural("foobars") is True
        assert is_plural("foo") is False

    def test_custom_uncountable(self) -> None:
        add_uncountable("foobar")
        assert is_plural("foobar") is False


class TestIsSingular:
    def test_singular_word(self) -> None:
        assert is_singular("cat") is True

    def test_plural_word(self) -> None:
        assert is_singular("cats") is False

    def test_irregular_singular(self) -> None:
        assert is_singular("child") is True

    def test_irregular_plural(self) -> None:
        assert is_singular("children") is False

    def test_uncountable_returns_false(self) -> None:
        assert is_singular("sheep") is False
        assert is_singular("information") is False

    def test_empty_string_returns_false(self) -> None:
        assert is_singular("") is False

    def test_whitespace_only_returns_false(self) -> None:
        assert is_singular("   ") is False

    def test_strips_whitespace(self) -> None:
        assert is_singular("  cat  ") is True

    def test_case_insensitive(self) -> None:
        assert is_singular("Cat") is True
        assert is_singular("CAT") is True

    def test_spanish_singular(self) -> None:
        assert is_singular("gato", lang="es") is True

    def test_spanish_plural(self) -> None:
        assert is_singular("gatos", lang="es") is False

    def test_spanish_irregular_singular(self) -> None:
        assert is_singular("ratón", lang="es") is True

    def test_spanish_uncountable(self) -> None:
        assert is_singular("lunes", lang="es") is False

    def test_non_string_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            is_singular(123)  # type: ignore[arg-type]

    def test_none_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            is_singular(None)  # type: ignore[arg-type]

    def test_unsupported_lang_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            is_singular("cat", lang="zz")

    def test_custom_irregular(self) -> None:
        add_irregular("barfoo", "barfoos")
        assert is_singular("barfoo") is True
        assert is_singular("barfoos") is False

    def test_custom_uncountable(self) -> None:
        add_uncountable("barbaz")
        assert is_singular("barbaz") is False


class TestIsPluralIsSingularConsistency:
    @pytest.mark.parametrize("word", [
        "cat", "cats", "child", "children", "city", "cities",
        "box", "boxes", "mouse", "mice", "sheep", "information",
    ])
    def test_mutually_exclusive_for_countable(self, word: str) -> None:
        if is_plural(word):
            assert not is_singular(word)
        elif is_singular(word):
            assert not is_plural(word)

    @pytest.mark.parametrize("word", ["sheep", "information", "news"])
    def test_both_false_for_uncountable(self, word: str) -> None:
        assert is_plural(word) is False
        assert is_singular(word) is False


class TestVersion:
    def test_version_is_string(self) -> None:
        assert isinstance(pluralio.__version__, str)

    def test_version_not_empty(self) -> None:
        assert pluralio.__version__ != ""

    def test_version_in_all(self) -> None:
        assert "__version__" in pluralio.__all__
