from __future__ import annotations

import pytest

import pluralio
from pluralio import join, ordinal, template


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

    def test_string_input(self) -> None:
        assert ordinal("5") == "5th"

    def test_string_input_ordinal(self) -> None:
        assert ordinal("21") == "21st"

    def test_large_number(self) -> None:
        assert ordinal(1000) == "1000th"

    def test_111_to_120_all_th(self) -> None:
        for n in range(111, 121):
            assert ordinal(n) == f"{n}th"

    def test_invalid_string(self) -> None:
        with pytest.raises(ValueError, match="invalid literal"):
            ordinal("abc")


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
