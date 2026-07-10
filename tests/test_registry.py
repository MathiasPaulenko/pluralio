from __future__ import annotations

import pytest

from pluralio.registry import LanguageRules, get_rules, register, supported_languages


class TestRegister:
    def test_register_new_language(self) -> None:
        rules = LanguageRules(code="xx")
        register(rules)
        assert "xx" in supported_languages()

    def test_register_duplicate_overwrites(self) -> None:
        register(LanguageRules(code="xx", uncountable={"foo"}))
        register(LanguageRules(code="xx", uncountable={"bar"}))
        assert get_rules("xx").uncountable == {"bar"}

    def test_register_empty_code_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            register(LanguageRules(code=""))

    def test_register_whitespace_code_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            register(LanguageRules(code="   "))


class TestFrozenRules:
    def test_frozen_cannot_set_attribute(self) -> None:
        rules = LanguageRules(code="en")
        with pytest.raises(AttributeError):
            rules.code = "fr"  # type: ignore[misc]

    def test_frozen_cannot_add_to_uncountable(self) -> None:
        rules = LanguageRules(code="en")
        with pytest.raises(AttributeError):
            rules.uncountable = {"test"}  # type: ignore[misc]


class TestGetRules:
    def test_get_existing_language(self) -> None:
        rules = get_rules("en")
        assert rules.code == "en"

    def test_get_unsupported_language_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            get_rules("zz")

    def test_get_unsupported_error_message_lists_supported(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            get_rules("zz")
        msg = str(exc_info.value)
        assert "en" in msg
        assert "es" in msg


class TestSupportedLanguages:
    def test_returns_sorted_list(self) -> None:
        langs = supported_languages()
        assert langs == sorted(langs)

    def test_includes_en_and_es(self) -> None:
        langs = supported_languages()
        assert "en" in langs
        assert "es" in langs
