from __future__ import annotations

import pytest

from pluralio import pluralize, singularize


class TestEsperantoSingularRules:
    def test_basic_j_strip(self) -> None:
        for plural, singular in [("libroj", "libro"), ("hundoj", "hundo"),
                                 ("katoj", "kato"), ("floroj", "floro"),
                                 ("domoj", "domo"), ("akvoj", "akvo")]:
            assert singularize(plural, lang="eo") == singular

    def test_accusative_jn_to_n(self) -> None:
        for plural, singular in [("librojn", "libron"), ("hundojn", "hundon"),
                                 ("katojn", "katon"), ("domojn", "domon")]:
            assert singularize(plural, lang="eo") == singular

    def test_adjective_j_strip(self) -> None:
        for plural, singular in [("bonaj", "bona"), ("grandaj", "granda"),
                                 ("malgrandaj", "malgranda")]:
            assert singularize(plural, lang="eo") == singular

    def test_adjective_accusative(self) -> None:
        for plural, singular in [("bonajn", "bonan"), ("grandajn", "grandan")]:
            assert singularize(plural, lang="eo") == singular

    def test_pronouns_invariable(self) -> None:
        for word in ["mi", "vi", "li", "ŝi", "ĝi", "ni", "ili", "oni", "si"]:
            assert singularize(word, lang="eo") == word

    def test_case_preservation(self) -> None:
        assert singularize("Libroj", lang="eo") == "Libro"
        assert singularize("LIBROJ", lang="eo") == "LIBRO"
        assert singularize("Hundoj", lang="eo") == "Hundo"


class TestEsperantoRoundTrip:
    @pytest.mark.parametrize("word", [
        "libro", "hundo", "kato", "floro", "domo", "akvo",
        "bona", "granda", "malgranda",
        "libron", "hundon", "bonan", "grandan",
        "pano", "kafo", "teksto", "lingvo",
        "amiko", "familio", "urbo", "lando",
        "instruisto", "studento", "lernejo", "laboro",
    ])
    def test_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word, lang="eo"), lang="eo") == word
