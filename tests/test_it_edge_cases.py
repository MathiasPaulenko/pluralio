"""Italian edge cases for pluralization and singularization."""
from __future__ import annotations

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestItCasePreservation:
    """Italian case preservation for irregulars and regex words."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("Libro", "Libri"),
        ("LIBRO", "LIBRI"),
        ("Casa", "Case"),
        ("CASA", "CASE"),
        ("Cane", "Cani"),
        ("CANE", "CANI"),
        ("Amico", "Amici"),
        ("AMICO", "AMICI"),
        ("Uomo", "Uomini"),
        ("UOMO", "UOMINI"),
        ("Banco", "Banchi"),
        ("BANCO", "BANCHI"),
        ("Amica", "Amiche"),
        ("AMICA", "AMICHE"),
    ])
    def test_it_title_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="it") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("Libri", "Libro"),
        ("LIBRI", "LIBRO"),
        ("Case", "Casa"),
        ("CASE", "CASA"),
        ("Cani", "Cane"),
        ("CANI", "CANE"),
        ("Amici", "Amico"),
        ("AMICI", "AMICO"),
        ("Uomini", "Uomo"),
        ("UOMINI", "UOMO"),
        ("Banchi", "Banco"),
        ("BANCHI", "BANCO"),
        ("Amiche", "Amica"),
        ("AMICHE", "AMICA"),
    ])
    def test_it_title_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="it") == expected



class TestItMixedCase:
    """Italian mixed case preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("McLibro", "McLibri"),
    ])
    def test_it_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="it") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("McLibri", "McLibro"),
    ])
    def test_it_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="it") == expected



class TestItHyphenatedWords:
    """Italian hyphenated word pluralization."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("caffè-bar", "caffè-bar"),
        ("film-club", "film-club"),
        ("auto-scuola", "auto-scuole"),
    ])
    def test_it_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="it") == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("auto-scuola", "auto-scuole"),
    ])
    def test_it_hyphenated_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural, lang="it") == singular

    def test_it_hyphenated_roundtrip(self) -> None:
        for word in ["auto-scuola"]:
            assert singularize(pluralize(word, lang="it"), lang="it") == word

    def test_it_leading_hyphen_pluralize(self) -> None:
        assert pluralize("-casa", lang="it") == "-case"

    def test_it_leading_hyphen_singularize(self) -> None:
        assert singularize("-case", lang="it") == "-casa"

    def test_it_hyphen_only(self) -> None:
        assert pluralize("-", lang="it") == "-"
        assert singularize("-", lang="it") == "-"

    def test_it_double_hyphen(self) -> None:
        assert pluralize("--", lang="it") == "--"
        assert singularize("--", lang="it") == "--"



class TestItIdempotency:
    """Italian pluralize of already-plural words should return unchanged."""

    @pytest.mark.parametrize("word", [
        "libri", "cani", "fiori", "pani",
        "banchi", "amiche", "leghe", "righe",
        "amici", "medici", "nemici", "logici",
        "biologi", "psicologi", "tecnici", "politici",
        "asparagi", "laghi", "fuochi", "luoghi", "giochi",
        "uomini", "mogli", "dei", "templi",
        "buoi", "ali", "armi", "dita", "ossa",
        "labbra", "ginocchia", "occhi", "orecchi",
        "uova", "paia", "miglia", "centinaia", "migliaia",
        "vizi", "figli", "orologi", "inizi",
        "notti", "menti", "fronti", "sedi", "parti", "classi",
        "noci", "fedi", "paci", "croci", "genti", "navi",
        "valli", "pareti", "radici", "voci",
        "baci", "spazi", "uffici", "soci", "cambi", "esempi",
        "principi", "stadi", "negozi",
        "formaggi", "viaggi", "raggi", "coraggi", "passaggi", "messaggi",
        "case", "scuole", "banane", "gatte", "paste", "piante",
        "famiglie", "squadre", "feste", "donne", "ragazze",
        "macchine", "piazze", "pizze", "bambine",
        "sedie", "chiavi", "isole", "stelle", "barche",
        "cuori", "studenti", "denti", "nomi", "soli",
        "colori", "dottori", "signori", "attori", "professori",
        "superfici", "effigi", "studi", "esercizi",
        "piogge", "valigie", "rocce", "fasce", "asce",
        "problemi", "temi", "sistemi", "climi", "drammi",
        "programmi", "telegrammi",
        "schemi", "dogmi", "emblemi", "idiomi", "fantasmi",
        "pirati", "poeti", "colleghi", "atleti", "artisti",
        "autisti", "giornalisti", "linguisti", "turisti", "astronauti",
        "fiumi", "ponti", "clienti", "residenti", "presidenti",
        "generali", "animali", "fossili", "fucili", "cortili",
        "volgari", "regolari", "singolari", "particolari",
        "borse", "coppie", "porte", "torte", "tazze",
        "sale", "ruote", "penne", "palle", "tele",
        "sorelle", "fruste", "braccia", "lenzuola", "ciglia",
        "lacci", "stracci", "sacrifici", "abbracci", "obblighi",
        "torri", "corti", "sorti", "morti", "canzoni",
        "bicchieri", "giornali", "mari",
        "padri", "madri", "rei",
        "zii", "zie",
        "fratelli", "nonni", "nonne",
        "cugini", "cugine",
        "piedi", "fini", "margini",
        "bottoni", "giganti", "santoni",
        "difensori", "attaccanti",
        "esemplari", "necessari",
        "sufficienti", "importanti",
        "evidenti", "intelligenti",
        "potenti", "urgenti",
        "simili", "facili", "difficili",
        "utili", "inutili",
        "possibili", "impossibili",
        "probabili", "improbabili",
        "portatili", "turbini",
        "film", "bar", "bus", "computer", "sport",
    ])
    def test_it_pluralize_already_plural(self, word: str) -> None:
        assert pluralize(word, lang="it") == word



class TestItRoundTrip:
    """Italian pluralize → singularize round-trip identity."""

    @pytest.mark.parametrize("word", [
        "libro", "casa", "cane", "fiore", "pane",
        "amica", "banca", "lega", "riga",
        "banco", "pacco", "ago", "fungo",
        "vizio", "figlio", "orologio", "inizio",
        "amico", "medico", "nemico", "logico",
        "biologo", "psicologo", "tecnico", "politico",
        "asparago", "lago", "fuoco", "luogo", "gioco",
        "porco", "uomo", "moglie", "dio", "tempio",
        "bue", "ala", "arma", "dito", "osso",
        "labbro", "ginocchio", "occhio", "orecchio",
        "uovo", "paio", "miglio", "centinaio", "migliaio",
        "film", "bar", "bus", "computer", "sport",
        "taxi", "metro", "weekend", "meeting",
        "club", "leader", "test", "code",
        "server", "framework", "token", "container",
        "docker", "script",
        "notte", "mente", "fronte", "sede", "parte", "classe",
        "noce", "fede", "pace", "croce", "gente", "nave",
        "valle", "parete", "radice", "voce",
        "bacio", "spazio", "ufficio", "socio", "cambio", "esempio",
        "principio", "stadio", "negozio",
        "formaggio", "viaggio", "raggio", "coraggio",
        "passaggio", "messaggio", "scuola", "banana", "gatta", "pasta", "pianta",
        "famiglia", "squadra", "festa", "donna", "ragazza",
        "macchina", "piazza", "pizza", "bambina",
        "sedia", "chiave", "isola", "stella", "barca",
        "cuore", "studente", "dente", "nome", "sole",
        "colore", "dottore", "signore", "attore", "professore",
        "superficie", "effigie", "studio", "esercizio",
        "pioggia", "valigia", "roccia", "fascia", "ascia",
        "problema", "tema", "sistema", "clima", "dramma",
        "programma", "telegramma",
        "schema", "dogma", "emblema", "idioma", "fantasma",
        "pirata", "poeta", "collega", "atleta", "artista",
        "autista", "giornalista", "linguista", "turista", "astronauta",
        "fiume", "ponte", "cliente", "residente", "presidente",
        "generale", "animale", "fossile", "fucile", "cortile",
        "volgare", "regolare", "singolare", "particolare",
        "borsa", "coppia", "porta", "torta", "tazza",
        "sala", "ruota", "penna", "palla", "tela",
        "sorella", "frusta", "braccio", "lenzuolo", "ciglio",
        "laccio", "straccio", "sacrificio", "abbraccio", "obbligo",
        "torre", "corte", "sorte", "morte", "canzone",
        "bicchiere", "giornale", "mare",
        "padre", "madre", "re",
        "zio", "zia",
        "fratello", "nonno", "nonna",
        "cugino", "cugina",
        "piede", "fine", "margine",
        "bottone", "gigante", "santone",
        "difensore", "attaccante",
        "esemplare", "necessario",
        "sufficiente", "importante",
        "evidente", "intelligente",
        "potente", "urgente",
        "simile", "facile", "difficile",
        "utile", "inutile",
        "possibile", "impossibile",
        "probabile", "improbabile",
        "portatile", "turbine",
    ])
    def test_it_roundtrip(self, word: str) -> None:
        plural = pluralize(word, lang="it")
        assert singularize(plural, lang="it") == word



class TestItCountAware:
    """Italian count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "libro", "casa", "cane", "amico", "uomo",
        "uovo", "banco", "amica", "vizio", "framework",
    ])
    def test_it_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, lang="it", count=1) == word

    @pytest.mark.parametrize("word", [
        "libro", "casa", "cane", "amico", "uomo",
        "uovo", "banco", "amica", "vizio", "framework",
    ])
    def test_it_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="it", count=0) == pluralize(word, lang="it")

    @pytest.mark.parametrize("word", [
        "libro", "casa", "cane", "amico", "uomo",
        "uovo", "banco", "amica", "vizio", "framework",
    ])
    def test_it_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="it", count=2) == pluralize(word, lang="it")



class TestItWhitespace:
    """Italian whitespace preservation."""

    def test_it_preserves_whitespace_pluralize(self) -> None:
        assert pluralize("  libro  ", lang="it") == "  libri  "

    def test_it_preserves_whitespace_singularize(self) -> None:
        assert singularize("  libri  ", lang="it") == "  libro  "

    def test_it_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ", lang="it") == "   "
        assert singularize("   ", lang="it") == "   "

    def test_it_count_one_preserves_whitespace(self) -> None:
        assert pluralize("  libro  ", lang="it", count=1) == "  libro  "



class TestItSingleLetterAndEdge:
    """Italian single letters and boundary cases."""

    def test_it_single_letter_a(self) -> None:
        assert pluralize("a", lang="it") == "e"
        assert singularize("e", lang="it") == "a"

    def test_it_single_letter_a_uppercase(self) -> None:
        assert pluralize("A", lang="it") == "E"
        assert singularize("E", lang="it") == "A"

    def test_it_empty_string(self) -> None:
        assert pluralize("", lang="it") == ""
        assert singularize("", lang="it") == ""

    def test_it_whitespace_only(self) -> None:
        assert pluralize("   ", lang="it") == "   "
        assert singularize("   ", lang="it") == "   "



class TestItUncountableConsistency:
    """Italian uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "film", "bar", "bus", "computer", "sport",
        "taxi", "metro", "weekend", "meeting",
        "club", "leader", "test", "code",
        "server", "framework", "token", "container",
        "docker", "script", "software", "hardware",
        "web", "blog", "chat", "spam",
        "jazz", "rock", "punk", "flash",
        "brindisi", "analisi", "tesi", "crisi",
        "oasi", "sintesi", "ipotesi", "diagnosi",
        "paralisi", "catarsi",
        "specie", "serie",
        "occhiali", "forbici", "pantaloni",
        "soldi", "nozze", "stoviglie",
        "vettovaglie",
        "foto", "moto", "radio", "cinema",
        "auto", "biliardo",
    ])
    def test_it_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="it") == word
        assert singularize(word, lang="it") == word



class TestItIsSingularIsPlural:
    """Italian is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "libro", "casa", "cane", "fiore", "pane",
        "amico", "uomo", "uovo", "banco", "amica",
    ])
    def test_it_singular_words(self, word: str) -> None:
        assert is_singular(word, lang="it") is True
        assert is_plural(word, lang="it") is False

    @pytest.mark.parametrize("word", [
        "libri", "case", "cani", "fiori", "pani",
        "amici", "uomini", "uova", "banchi", "amiche",
    ])
    def test_it_plural_words(self, word: str) -> None:
        assert is_plural(word, lang="it") is True
        assert is_singular(word, lang="it") is False

    @pytest.mark.parametrize("word", [
        "film", "bar", "analisi", "crisi", "occhiali",
        "foto", "auto", "specie", "serie",
    ])
    def test_it_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="it") is True
        assert is_plural(word, lang="it") is True

