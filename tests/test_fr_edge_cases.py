"""French edge cases for pluralization and singularization."""
from __future__ import annotations

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestFrCasePreservation:
    """French case preservation for pluralization."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("Cheval", "Chevaux"),
        ("CHEVAL", "CHEVAUX"),
        ("Bateau", "Bateaux"),
        ("BATEAU", "BATEAUX"),
        ("Chat", "Chats"),
        ("CHAT", "CHATS"),
        ("Animal", "Animaux"),
        ("ANIMAL", "ANIMAUX"),
    ])
    def test_fr_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("Chevaux", "Cheval"),
        ("CHEVAUX", "CHEVAL"),
        ("Bateaux", "Bateau"),
        ("BATEAUX", "BATEAU"),
        ("Chats", "Chat"),
        ("CHATS", "CHAT"),
    ])
    def test_fr_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="fr") == expected



class TestFrMixedCase:
    """French mixed case preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhone", "iPhones"),
        ("McDonald", "McDonalds"),
    ])
    def test_fr_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected



class TestFrHyphenated:
    """French hyphenated compound words."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("café-théâtre", "cafés-théâtres"),
        ("eau-de-vie", "eaux-de-vie"),
        ("garde-manger", "gardes-mangers"),
        ("chou-fleur", "choux-fleurs"),
        ("pot-au-feu", "pots-aux-feux"),
        ("arc-en-ciel", "arcs-en-ciel"),
    ])
    def test_fr_hyphenated_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("cafés-théâtres", "café-théâtre"),
        ("eaux-de-vie", "eau-de-vie"),
        ("gardes-mangers", "garde-manger"),
        ("choux-fleurs", "chou-fleur"),
        ("pots-aux-feux", "pot-au-feu"),
        ("arcs-en-ciel", "arc-en-ciel"),
    ])
    def test_fr_hyphenated_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="fr") == expected



class TestFrIdempotency:
    """French already-plural words should be unchanged by pluralize."""

    @pytest.mark.parametrize("word", [
        "chats", "livres", "maisons", "bateaux", "chevaux",
        "animaux", "journaux", "hôpitaux", "bocaux", "travaux",
        "bijoux", "cailloux", "jeux", "feux", "yeux",
        "messieurs", "mesdames", "weekends", "parkings",
        "ciseaux", "lunettes", "jumelles", "fils",
    ])
    def test_fr_already_plural_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="fr") == word



class TestFrRoundTrip:
    """French round-trip: singularize(pluralize(x)) == x."""

    @pytest.mark.parametrize("word", [
        "chat", "livre", "maison", "arbre", "détail",
        "trou", "bateau", "chapeau", "manteau", "rideau",
        "cheval", "animal", "journal", "hôpital", "bocal",
        "bal", "festival", "carnaval", "récital", "fatal",
        "travail", "vitrail", "corail", "émail",
        "bijou", "caillou", "hibou", "chou", "genou",
        "jeu", "feu", "vœu", "bleu", "pneu",
        "œil", "ciel", "monsieur", "madame", "mademoiselle",
        "canal", "capital", "signal", "social", "spécial",
        "normal", "national", "international",
        "tuyau", "noyau", "boyau", "bail",
        "cour", "étal", "val", "gnou", "bayou",
        "weekend", "parking", "club", "leader", "test",
    ])
    def test_fr_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word, lang="fr"), lang="fr") == word



class TestFrCountAware:
    """French count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "chat", "livre", "maison", "cheval", "bateau",
        "animal", "journal", "travail", "bijou", "jeu",
        "œil", "monsieur", "canal", "weekend", "club",
    ])
    def test_fr_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, lang="fr", count=1) == word

    @pytest.mark.parametrize("word", [
        "chat", "livre", "maison", "cheval", "bateau",
        "animal", "journal", "travail", "bijou", "jeu",
        "œil", "monsieur", "canal", "weekend", "club",
    ])
    def test_fr_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="fr", count=0) == pluralize(word, lang="fr")

    @pytest.mark.parametrize("word", [
        "chat", "livre", "maison", "cheval", "bateau",
        "animal", "journal", "travail", "bijou", "jeu",
        "œil", "monsieur", "canal", "weekend", "club",
    ])
    def test_fr_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="fr", count=2) == pluralize(word, lang="fr")



class TestFrWhitespace:
    """French whitespace preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        (" chat", " chats"),
        ("chat ", "chats "),
        (" chat ", " chats "),
        ("  cheval  ", "  chevaux  "),
    ])
    def test_fr_whitespace_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        (" chats", " chat"),
        ("chats ", "chat "),
        (" chats ", " chat "),
        ("  chevaux  ", "  cheval  "),
    ])
    def test_fr_whitespace_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="fr") == expected



class TestFrSingleLetter:
    """French single letters and boundary cases."""

    def test_fr_single_letter_a(self) -> None:
        assert pluralize("a", lang="fr") == "as"

    def test_fr_single_letter_a_uppercase(self) -> None:
        assert pluralize("A", lang="fr") == "AS"

    def test_fr_empty_string(self) -> None:
        assert pluralize("", lang="fr") == ""
        assert singularize("", lang="fr") == ""

    def test_fr_whitespace_only(self) -> None:
        assert pluralize("   ", lang="fr") == "   "
        assert singularize("   ", lang="fr") == "   "



class TestFrUncountableConsistency:
    """French uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "information", "recherche", "violence", "patience",
        "courage", "liberté", "justice", "beauté",
        "jeunesse", "vieillesse", "faiblesse", "sagesse",
        "richesse", "santé", "faim", "soif",
        "peur", "joie", "tristesse", "colère",
        "amour", "haine", "espoir", "désespoir",
        "temps", "argent", "or", "fer",
        "cuivre", "plomb", "bois", "verre",
        "papier", "cuir", "plastique", "caoutchouc",
        "pain", "lait", "beurre", "fromage",
        "sucre", "sel", "poivre", "riz",
        "farine", "viande", "porc", "jambon",
        "fois", "souris", "brebis",
        "poids", "rhinocéros", "virus",
        "croix", "voix", "noix",
        "choix", "prix",
        "nez",
        "jazz", "rock", "punk", "flash",
        "obsèques", "fiançailles", "ténèbres",
        "archives", "mathématiques", "fils",
        "ciseaux", "lunettes", "jumelles",
        "pincettes", "arrérages", "ambages",
        "fraîtures", "mœurs",
        "condoléances", "frais", "gens",
    ])
    def test_fr_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="fr") == word
        assert singularize(word, lang="fr") == word



class TestFrIsSingularIsPlural:
    """French is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "chat", "livre", "maison", "cheval", "bateau",
        "animal", "journal", "travail", "bijou", "jeu",
        "œil", "monsieur", "canal", "weekend", "club",
    ])
    def test_fr_singular_words(self, word: str) -> None:
        assert is_singular(word, lang="fr") is True
        assert is_plural(word, lang="fr") is False

    @pytest.mark.parametrize("word", [
        "chats", "livres", "maisons", "chevaux", "bateaux",
        "animaux", "journaux", "travaux", "bijoux", "jeux",
        "yeux", "messieurs", "canaux", "weekends", "clubs",
    ])
    def test_fr_plural_words(self, word: str) -> None:
        assert is_plural(word, lang="fr") is True
        assert is_singular(word, lang="fr") is False

    @pytest.mark.parametrize("word", [
        "information", "temps", "argent", "riz",
        "fois", "souris", "croix", "voix", "nez",
        "jazz", "rock", "obsèques", "archives",
    ])
    def test_fr_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="fr") is True
        assert is_plural(word, lang="fr") is True


# ---------------------------------------------------------------------------
# Italian edge cases
# ---------------------------------------------------------------------------



