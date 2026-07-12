from __future__ import annotations

from pluralio import pluralize


class TestEsperantoPluralRules:
    def test_basic_j(self) -> None:
        for singular, plural in [("libro", "libroj"), ("hundo", "hundoj"),
                                 ("kato", "katoj"), ("floro", "floroj"),
                                 ("domo", "domoj"), ("akvo", "akvoj")]:
            assert pluralize(singular, lang="eo") == plural

    def test_accusative_n_to_jn(self) -> None:
        for singular, plural in [("libron", "librojn"), ("hundon", "hundojn"),
                                 ("katon", "katojn"), ("domon", "domojn")]:
            assert pluralize(singular, lang="eo") == plural

    def test_adjective_j(self) -> None:
        for singular, plural in [("bona", "bonaj"), ("granda", "grandaj"),
                                 ("malgranda", "malgrandaj")]:
            assert pluralize(singular, lang="eo") == plural

    def test_adjective_accusative(self) -> None:
        for singular, plural in [("bonan", "bonajn"), ("grandan", "grandajn")]:
            assert pluralize(singular, lang="eo") == plural

    def test_pronouns_invariable(self) -> None:
        for word in ["mi", "vi", "li", "ŝi", "ĝi", "ni", "ili", "oni", "si"]:
            assert pluralize(word, lang="eo") == word

    def test_correlatives_invariable(self) -> None:
        for word in ["kio", "tio", "ĉio", "nenio", "iom"]:
            assert pluralize(word, lang="eo") == word

    def test_particles_invariable(self) -> None:
        for word in ["kaj", "aŭ", "sed", "la", "en", "sur", "de", "al"]:
            assert pluralize(word, lang="eo") == word

    def test_case_preservation(self) -> None:
        assert pluralize("Libro", lang="eo") == "Libroj"
        assert pluralize("LIBRO", lang="eo") == "LIBROJ"
        assert pluralize("Hundo", lang="eo") == "Hundoj"

    def test_count_aware(self) -> None:
        assert pluralize("libro", lang="eo", count=1) == "libro"
        assert pluralize("libro", lang="eo", count=2) == "libroj"

    def test_already_plural_accusative_invariable(self) -> None:
        for word in ["librojn", "hundojn", "katojn", "bonajn", "grandajn"]:
            assert pluralize(word, lang="eo") == word

    def test_already_plural_nominative_adds_nothing(self) -> None:
        for word in ["libroj", "hundoj", "katoj", "bonaj"]:
            assert pluralize(word, lang="eo") == word
