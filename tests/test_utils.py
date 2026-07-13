from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

import pluralio
from pluralio import join, ordinal, template
from pluralio.utils import _TEMPLATE_PATTERN


class TestJoin:
    def test_single_item(self) -> None:
        assert join(["apple"]) == "apple"

    def test_two_items(self) -> None:
        assert join(["apple", "banana"]) == "apple and banana"

    def test_three_items(self) -> None:
        assert join(["apple", "banana", "carrot"]) == "apple, banana, and carrot"

    def test_empty_list(self) -> None:
        assert join([]) == ""

    def test_custom_conjunction(self) -> None:
        assert join(["a", "b", "c"], conjunction="or") == "a, b, or c"

    def test_no_oxford_comma(self) -> None:
        assert join(["a", "b", "c"], final_sep="") == "a, b and c"

    def test_custom_sep(self) -> None:
        assert join(["a", "b", "c"], sep="; ") == "a; b, and c"

    def test_iterable_input(self) -> None:
        assert join(iter(["a", "b"])) == "a and b"

    def test_many_items(self) -> None:
        items = ["a", "b", "c", "d", "e"]
        assert join(items) == "a, b, c, d, and e"

    def test_keyword_only(self) -> None:
        with pytest.raises(TypeError):
            join(["a", "b"], "or")  # type: ignore[misc]

    def test_empty_string_items(self) -> None:
        assert join(["", ""]) == " and "

    def test_single_empty_string(self) -> None:
        assert join([""]) == ""

    def test_generator_input(self) -> None:
        assert join(x for x in ["a", "b", "c"]) == "a, b, and c"

    def test_custom_all_params(self) -> None:
        result = join(["a", "b", "c"], conjunction="and even", final_sep="; ", sep=" / ")
        assert result == "a / b; and even c"

    def test_two_items_custom_conjunction(self) -> None:
        assert join(["a", "b"], conjunction="or") == "a or b"

    def test_two_items_ignores_sep_and_final_sep(self) -> None:
        assert join(["a", "b"], sep="; ", final_sep="!") == "a and b"

    def test_tuple_input(self) -> None:
        assert join(("a", "b", "c")) == "a, b, and c"

    def test_one_item_tuple(self) -> None:
        assert join(("only",)) == "only"

    def test_three_items_no_final_sep_with_custom_sep(self) -> None:
        assert join(["a", "b", "c"], sep="; ", final_sep="") == "a; b and c"

    @given(st.lists(st.text(min_size=1, max_size=10), min_size=3, max_size=20))  # type: ignore[untyped-decorator]
    def test_join_always_ends_with_last_item(self, items: list[str]) -> None:
        result = join(items)
        assert result.endswith(items[-1])

    @given(st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=20))  # type: ignore[untyped-decorator]
    def test_join_contains_all_items(self, items: list[str]) -> None:
        result = join(items)
        for item in items:
            assert item in result


class TestOrdinal:
    def test_first(self) -> None:
        assert ordinal(1) == "1st"

    def test_second(self) -> None:
        assert ordinal(2) == "2nd"

    def test_third(self) -> None:
        assert ordinal(3) == "3rd"

    def test_fourth(self) -> None:
        assert ordinal(4) == "4th"

    def test_eleventh(self) -> None:
        assert ordinal(11) == "11th"

    def test_twelfth(self) -> None:
        assert ordinal(12) == "12th"

    def test_thirteenth(self) -> None:
        assert ordinal(13) == "13th"

    def test_twenty_first(self) -> None:
        assert ordinal(21) == "21st"

    def test_twenty_second(self) -> None:
        assert ordinal(22) == "22nd"

    def test_twenty_third(self) -> None:
        assert ordinal(23) == "23rd"

    def test_one_hundred_first(self) -> None:
        assert ordinal(101) == "101st"

    def test_one_hundred_eleventh(self) -> None:
        assert ordinal(111) == "111th"

    def test_zero(self) -> None:
        assert ordinal(0) == "0th"

    def test_negative(self) -> None:
        assert ordinal(-1) == "-1st"

    def test_negative_two(self) -> None:
        assert ordinal(-2) == "-2nd"

    def test_negative_three(self) -> None:
        assert ordinal(-3) == "-3rd"

    def test_negative_eleven(self) -> None:
        assert ordinal(-11) == "-11th"

    def test_negative_111(self) -> None:
        assert ordinal(-111) == "-111th"

    def test_string_input(self) -> None:
        assert ordinal("5") == "5th"

    def test_string_input_ordinal(self) -> None:
        assert ordinal("21") == "21st"

    def test_large_number(self) -> None:
        assert ordinal(1000) == "1000th"

    def test_large_number_st(self) -> None:
        assert ordinal(1001) == "1001st"

    def test_111_to_120_all_th(self) -> None:
        for n in range(111, 121):
            assert ordinal(n) == f"{n}th"

    def test_invalid_string(self) -> None:
        with pytest.raises(ValueError, match="invalid literal"):
            ordinal("abc")

    def test_very_large_number(self) -> None:
        assert ordinal(10**6) == "1000000th"

    def test_very_large_number_st(self) -> None:
        assert ordinal(10**6 + 1) == "1000001st"

    @given(st.integers(min_value=0, max_value=10000))  # type: ignore[untyped-decorator]
    def test_ordinal_ends_with_valid_suffix(self, n: int) -> None:
        result = ordinal(n)
        assert result.endswith(("st", "nd", "rd", "th"))

    @given(st.integers(min_value=0, max_value=10000))  # type: ignore[untyped-decorator]
    def test_ordinal_starts_with_number(self, n: int) -> None:
        assert ordinal(n).startswith(str(n))

    @given(st.integers(min_value=4, max_value=20))  # type: ignore[untyped-decorator]
    def test_teens_are_all_th(self, n: int) -> None:
        assert ordinal(n) == f"{n}th"

    @given(st.integers(min_value=-10000, max_value=-1))  # type: ignore[untyped-decorator]
    def test_negative_ordinal_starts_with_number(self, n: int) -> None:
        assert ordinal(n).startswith(str(n))


class TestTemplate:
    def test_plain_substitution(self) -> None:
        assert template("Hello {name}", name="world") == "Hello world"

    def test_pluralize(self) -> None:
        assert template("{n} {word:pluralize}", n=5, word="cat") == "5 cats"

    def test_pluralize_count_1(self) -> None:
        assert template("{count} {word:pluralize}", count=1, word="cat") == "1 cat"

    def test_pluralize_count_0(self) -> None:
        assert template("{count} {word:pluralize}", count=0, word="cat") == "0 cats"

    def test_singularize(self) -> None:
        assert template("The {word:singularize}", word="mice") == "The mouse"

    def test_no_count_defaults_to_plural(self) -> None:
        assert template("{word:pluralize}", word="cat") == "cats"

    def test_multiple_placeholders(self) -> None:
        result = template("{n} {word:pluralize} arrived", n=3, word="box")
        assert result == "3 boxes arrived"

    def test_mixed_transforms(self) -> None:
        result = template(
            "{n} {plural:pluralize} and one {single:singularize}",
            n=5,
            plural="cat",
            single="mice",
        )
        assert result == "5 cats and one mouse"

    def test_custom_count_var(self) -> None:
        result = template("{num} {word:pluralize:num}", num=1, word="cat")
        assert result == "1 cat"

    def test_non_string_value(self) -> None:
        assert template("Count: {n}", n=42) == "Count: 42"

    def test_missing_key_raises(self) -> None:
        with pytest.raises(KeyError):
            template("{missing}")

    def test_no_placeholders(self) -> None:
        assert template("plain text") == "plain text"

    def test_multiple_same_placeholder(self) -> None:
        result = template("{word:pluralize} and {word:pluralize}", word="cat")
        assert result == "cats and cats"

    def test_count_as_string(self) -> None:
        result = template("{count} {word:pluralize}", count="5", word="cat")
        assert result == "5 cats"

    def test_count_string_one(self) -> None:
        result = template("{count} {word:pluralize}", count="1", word="cat")
        assert result == "1 cat"

    def test_custom_count_var_not_in_kwargs(self) -> None:
        result = template("{num} {word:pluralize:missing}", num=5, word="cat")
        assert result == "5 cats"

    def test_empty_template(self) -> None:
        assert template("") == ""

    def test_braces_not_placeholders(self) -> None:
        assert template("not a {placeholder}", placeholder="value") == "not a value"

    def test_int_value_pluralize(self) -> None:
        result = template("{word:pluralize}", word=123)
        assert result == "123s"

    def test_float_value_plain(self) -> None:
        result = template("Value: {v}", v=3.14)
        assert result == "Value: 3.14"

    def test_count_zero_is_plural(self) -> None:
        result = template("{count} {word:pluralize}", count=0, word="mouse")
        assert result == "0 mice"

    def test_negative_count_is_plural(self) -> None:
        result = template("{count} {word:pluralize}", count=-1, word="cat")
        assert result == "-1 cats"

    def test_template_with_irregular(self) -> None:
        result = template("{count} {word:pluralize}", count=2, word="child")
        assert result == "2 children"

    def test_template_singularize_irregular(self) -> None:
        result = template("The {word:singularize}", word="children")
        assert result == "The child"

    def test_template_pluralize_with_lang(self) -> None:
        result = template("{word:pluralize}", word="gato")
        # default lang is "en", so "gato" → "gatoes" (English rule)
        assert "gato" in result

    def test_mixed_plain_and_transform(self) -> None:
        result = template(
            "Dear {name}, you have {count} {word:pluralize}",
            name="Alice",
            count=3,
            word="message",
        )
        assert result == "Dear Alice, you have 3 messages"

    def test_adjacent_placeholders(self) -> None:
        result = template("{a}{b}", a="hello", b="world")
        assert result == "helloworld"

    def test_template_pattern_matches_pluralize(self) -> None:
        match = _TEMPLATE_PATTERN.match("{word:pluralize}")
        assert match is not None
        assert match.group(1) == "word"
        assert match.group(2) == "pluralize"

    def test_template_pattern_matches_singularize(self) -> None:
        match = _TEMPLATE_PATTERN.match("{word:singularize}")
        assert match is not None
        assert match.group(2) == "singularize"

    def test_template_pattern_matches_custom_count(self) -> None:
        match = _TEMPLATE_PATTERN.match("{word:pluralize:n}")
        assert match is not None
        assert match.group(3) == "n"

    def test_template_pattern_matches_plain(self) -> None:
        match = _TEMPLATE_PATTERN.match("{word}")
        assert match is not None
        assert match.group(2) is None

    def test_template_pattern_no_match_text(self) -> None:
        match = _TEMPLATE_PATTERN.match("plain text")
        assert match is None


class TestIntegration:
    def test_join_with_pluralize(self) -> None:
        words = [pluralio.pluralize(w) for w in ["cat", "dog", "child"]]
        assert join(words) == "cats, dogs, and children"

    def test_template_with_ordinal_and_pluralize(self) -> None:
        result = template(
            "The {pos} {word:pluralize} arrived",
            pos=ordinal(2),
            count=3,
            word="box",
        )
        assert result == "The 2nd boxes arrived"

    def test_join_with_template(self) -> None:
        items = [template("{word:pluralize}", word=w) for w in ["cat", "box"]]
        assert join(items) == "cats and boxes"

    def test_ordinal_in_template(self) -> None:
        result = template("The {pos} place", pos=ordinal(1))
        assert result == "The 1st place"

    def test_full_sentence_with_all_utils(self) -> None:
        items = [pluralio.pluralize(w) for w in ["cat", "box", "child"]]
        joined = join(items)
        result = template(
            "On the {pos} day, {count} {items} arrived",
            pos=ordinal(3),
            count=len(items),
            items=joined,
        )
        assert result == "On the 3rd day, 3 cats, boxes, and children arrived"

    def test_join_with_pluralize_count_aware(self) -> None:
        words = [pluralio.pluralize(w, count=c) for w, c in [("cat", 1), ("dog", 2)]]
        assert join(words) == "cat and dogs"

    def test_template_with_multilang_pluralize(self) -> None:
        result_es = pluralio.pluralize("gato", lang="es")
        result_en = pluralio.pluralize("cat")
        joined = join([result_es, result_en])
        assert joined == "gatos and cats"

