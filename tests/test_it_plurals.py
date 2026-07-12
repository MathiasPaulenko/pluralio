from __future__ import annotations

import pytest

from pluralio import pluralize


class TestItalianPluralRules:
    def test_o_to_i(self) -> None:
        for singular, plural in [("libro", "libri"), ("gatto", "gatti"),
                                 ("tavolo", "tavoli"), ("amore", "amori")]:
            assert pluralize(singular, lang="it") == plural

    def test_a_to_e(self) -> None:
        for singular, plural in [("casa", "case"), ("gatta", "gatte"),
                                 ("scuola", "scuole"), ("banana", "banane")]:
            assert pluralize(singular, lang="it") == plural

    def test_e_to_i(self) -> None:
        for singular, plural in [("cane", "cani"), ("fiore", "fiori"),
                                 ("pane", "pani"), ("notte", "notti")]:
            assert pluralize(singular, lang="it") == plural

    def test_ca_to_che(self) -> None:
        for singular, plural in [("amica", "amiche"), ("banca", "banche"),
                                 ("mucca", "mucche"), ("tica", "tiche")]:
            assert pluralize(singular, lang="it") == plural

    def test_ga_to_ghe(self) -> None:
        for singular, plural in [("lega", "leghe"), ("riga", "righe"),
                                 ("piaga", "piaghe"), ("droga", "droghe")]:
            assert pluralize(singular, lang="it") == plural

    def test_co_to_chi(self) -> None:
        for singular, plural in [("banco", "banchi"), ("pacco", "pacchi"),
                                 ("fuoco", "fuochi"), ("gioco", "giochi")]:
            assert pluralize(singular, lang="it") == plural

    def test_go_to_ghi(self) -> None:
        for singular, plural in [("lago", "laghi"), ("luogo", "luoghi"),
                                 ("ago", "aghi"), ("fungo", "funghi")]:
            assert pluralize(singular, lang="it") == plural

    def test_io_to_i(self) -> None:
        for singular, plural in [("vizio", "vizi"), ("figlio", "figli"),
                                 ("orologio", "orologi"), ("inizio", "inizi")]:
            assert pluralize(singular, lang="it") == plural

    def test_s_invariable(self) -> None:
        for word in ["brindisi", "analisi", "crisi", "tesi"]:
            assert pluralize(word, lang="it") == word

    def test_default_plus_i(self) -> None:
        for singular, plural in [("ct", "cti")]:
            assert pluralize(singular, lang="it") == plural

    def test_already_plural_unchanged(self) -> None:
        for word in ["libri", "cani", "banchi", "amiche",
                     "amici", "uomini", "uova"]:
            assert pluralize(word, lang="it") == word


class TestItalianIrregularPlurals:
    @pytest.mark.parametrize("singular,plural", [
        ("amico", "amici"), ("medico", "medici"), ("nemico", "nemici"),
        ("logico", "logici"), ("magico", "magici"), ("tragico", "tragici"),
        ("comico", "comici"), ("filosofico", "filosofici"),
        ("storico", "storici"), ("geografico", "geografici"),
        ("biologo", "biologi"), ("psicologo", "psicologi"),
        ("teologo", "teologi"), ("archeologo", "archeologi"),
        ("tecnico", "tecnici"), ("politico", "politici"),
        ("pratico", "pratici"), ("identico", "identici"),
        ("simpatico", "simpatici"), ("dinamico", "dinamici"),
        ("romantico", "romantici"), ("sintatico", "sintatici"),
        ("pubblico", "pubblici"), ("tedesco", "tedeschi"),
        ("asparago", "asparagi"),
        ("lago", "laghi"), ("fuoco", "fuochi"),
        ("luogo", "luoghi"), ("gioco", "giochi"),
        ("porco", "porci"),
        ("uomo", "uomini"), ("moglie", "mogli"),
        ("dio", "dei"), ("tempio", "templi"),
        ("bue", "buoi"), ("ala", "ali"),
        ("arma", "armi"), ("dito", "dita"),
        ("osso", "ossa"), ("labbro", "labbra"),
        ("ginocchio", "ginocchia"), ("occhio", "occhi"),
        ("orecchio", "orecchi"), ("uovo", "uova"),
        ("paio", "paia"), ("miglio", "miglia"),
        ("centinaio", "centinaia"), ("migliaio", "migliaia"),
        ("cane", "cani"), ("fiore", "fiori"), ("pane", "pani"), ("amore", "amori"),
        ("vizio", "vizi"), ("figlio", "figli"), ("orologio", "orologi"), ("inizio", "inizi"),
        ("notte", "notti"), ("mente", "menti"), ("fronte", "fronti"),
        ("sede", "sedi"), ("parte", "parti"), ("classe", "classi"),
        ("noce", "noci"), ("fede", "fedi"), ("pace", "paci"),
        ("croce", "croci"), ("gente", "genti"), ("nave", "navi"),
        ("valle", "valli"), ("parete", "pareti"), ("radice", "radici"),
        ("voce", "voci"),
        ("bacio", "baci"), ("spazio", "spazi"), ("ufficio", "uffici"),
        ("socio", "soci"), ("cambio", "cambi"), ("esempio", "esempi"),
        ("principio", "principi"), ("stadio", "stadi"), ("negozio", "negozi"),
        ("formaggio", "formaggi"), ("viaggio", "viaggi"), ("raggio", "raggi"),
        ("coraggio", "coraggi"), ("passaggio", "passaggi"), ("messaggio", "messaggi"),
        ("casa", "case"), ("scuola", "scuole"), ("banana", "banane"),
        ("gatta", "gatte"), ("pasta", "paste"), ("pianta", "piante"),
        ("famiglia", "famiglie"), ("squadra", "squadre"), ("festa", "feste"),
        ("donna", "donne"), ("ragazza", "ragazze"), ("macchina", "macchine"),
        ("piazza", "piazze"), ("pizza", "pizze"), ("bambina", "bambine"),
        ("film", "film"), ("bar", "bar"), ("bus", "bus"),
        ("computer", "computer"), ("sport", "sport"),
        ("taxi", "taxi"), ("metro", "metro"),
        ("weekend", "weekend"), ("meeting", "meeting"),
        ("club", "club"), ("leader", "leader"),
        ("test", "test"), ("code", "code"),
        ("server", "server"), ("framework", "framework"),
        ("token", "token"), ("container", "container"),
        ("docker", "docker"), ("script", "script"),
    ])
    def test_irregular_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="it") == plural


class TestItalianUncountable:
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
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="it") == word
