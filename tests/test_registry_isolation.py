from __future__ import annotations

from pluralio import (
    add_irregular,
    add_plural,
    add_plural_rule,
    add_singular,
    add_singular_rule,
    add_uncountable,
    pluralize,
    register_language,
    singularize,
    supported_languages,
)
from pluralio.registry import LanguageRules, register


class TestRegistryIsolation:
    def test_registering_in_test_does_not_leak(self) -> None:
        register(LanguageRules(code="temp"))
        assert "temp" in supported_languages()

    def test_supported_languages_stable_across_tests(self) -> None:
        langs = supported_languages()
        assert "en" in langs
        assert "es" in langs
        assert "temp" not in langs

    def test_custom_language_register_and_use(self) -> None:
        register_language("xx", plural_rules=[(r"$", "s")])
        assert pluralize("word", lang="xx") == "words"


class TestAddIrregular:
    def test_both_directions(self) -> None:
        add_irregular("foo", "foobars")
        assert pluralize("foo") == "foobars"
        assert singularize("foobars") == "foo"

    def test_case_insensitive(self) -> None:
        add_irregular("Foo", "Bars")
        assert pluralize("foo") == "bars"
        assert singularize("bars") == "foo"

    def test_spanish(self) -> None:
        add_irregular("miword", "miswords", lang="es")
        assert pluralize("miword", lang="es") == "miswords"
        assert singularize("miswords", lang="es") == "miword"

    def test_overrides_regex(self) -> None:
        add_irregular("special", "specials_custom")
        assert pluralize("special") == "specials_custom"


class TestAddPluralOnly:
    def test_only_plural_direction(self) -> None:
        add_plural("xyz", "xyzfoo")
        assert pluralize("xyz") == "xyzfoo"
        assert singularize("xyzfoo") != "xyz"

    def test_spanish_accent_case(self) -> None:
        add_plural("joven", "jóvenes", lang="es")
        assert pluralize("joven", lang="es") == "jóvenes"


class TestAddSingularOnly:
    def test_only_singular_direction(self) -> None:
        add_singular("xyzfoo", "xyz")
        assert singularize("xyzfoo") == "xyz"
        assert pluralize("xyz") != "xyzfoo"

    def test_spanish_accent_restoration(self) -> None:
        add_singular("alemanes", "alemán", lang="es")
        assert singularize("alemanes", lang="es") == "alemán"


class TestAddUncountable:
    def test_pluralize_returns_same(self) -> None:
        add_uncountable("foobar")
        assert pluralize("foobar") == "foobar"

    def test_singularize_returns_same(self) -> None:
        add_uncountable("foobar")
        assert singularize("foobar") == "foobar"

    def test_case_insensitive(self) -> None:
        add_uncountable("FooBar")
        assert pluralize("foobar") == "foobar"
        assert singularize("foobar") == "foobar"

    def test_spanish(self) -> None:
        add_uncountable("miword", lang="es")
        assert pluralize("miword", lang="es") == "miword"


class TestAddPluralRule:
    def test_custom_rule_priority(self) -> None:
        add_plural_rule(r"foo$", "foobars")
        assert pluralize("foo") == "foobars"

    def test_rule_inserted_at_top(self) -> None:
        add_plural_rule(r"z$", "zzzes")
        assert pluralize("fizz") == "fizzzzes"

    def test_spanish(self) -> None:
        add_plural_rule(r"abc$", "abcxyz", lang="es")
        assert pluralize("abc", lang="es") == "abcxyz"


class TestAddSingularRule:
    def test_custom_rule_priority(self) -> None:
        add_singular_rule(r"foobars$", "foo")
        assert singularize("foobars") == "foo"

    def test_rule_inserted_at_top(self) -> None:
        add_singular_rule(r"zzzes$", "z")
        assert singularize("quizzzes") == "quiz"

    def test_spanish(self) -> None:
        add_singular_rule(r"xyz$", "", lang="es")
        assert singularize("abcxyz", lang="es") == "abc"


class TestRegisterLanguage:
    def test_new_language(self) -> None:
        register_language(
            "fr",
            plural_rules=[(r"$", "s")],
            singular_rules=[(r"s$", "")],
            irregular_plurals={"cheval": "chevaux"},
            uncountable={"information"},
        )
        assert "fr" in supported_languages()
        assert pluralize("chat", lang="fr") == "chats"
        assert singularize("chats", lang="fr") == "chat"
        assert pluralize("cheval", lang="fr") == "chevaux"
        assert singularize("chevaux", lang="fr") == "cheval"
        assert pluralize("information", lang="fr") == "information"

    def test_defaults_when_empty(self) -> None:
        register_language("xx")
        assert pluralize("word", lang="xx") == "words"
        assert singularize("words", lang="xx") == "word"

    def test_register_clears_regex_cache(self) -> None:
        import re

        from pluralio.registry import restore, snapshot

        state = snapshot()
        # Populate cache with default English rules
        assert pluralize("cat") == "cats"
        # Replace English rules with a custom pattern
        register(LanguageRules(code="en", plural_rules=[(re.compile(r"$"), "XYZ")]))
        # Cache must be cleared — should use new rules, not stale result
        assert pluralize("cat") == "catXYZ"
        restore(state)

    def test_restore_clears_regex_cache(self) -> None:
        from pluralio.registry import restore, snapshot

        state = snapshot()
        # Populate cache with default English rules
        assert pluralize("foo") == "foos"
        # Add custom rule and populate cache with it
        add_plural_rule(r"foo$", "FOOBAR")
        assert pluralize("foo") == "FOOBAR"
        # Restore should clear cache — foo should go back to "foos"
        restore(state)
        assert pluralize("foo") == "foos"


class TestMatchCaseEdgeCases:
    def test_empty_target_lowercase_source(self) -> None:
        add_irregular("testword", "")
        assert pluralize("testword") == ""

    def test_empty_target_title_case_source(self) -> None:
        add_irregular("TestWord", "")
        assert pluralize("TestWord") == ""

    def test_empty_target_all_caps_source(self) -> None:
        add_irregular("TESTWORD", "")
        assert pluralize("TESTWORD") == ""

    def test_digit_only_source_preserves_target_case(self) -> None:
        from pluralio.core import _match_case

        assert _match_case("123", "ABC") == "ABC"
        assert _match_case("42", "Hello") == "Hello"
