from __future__ import annotations

import pytest

from pluralio import pluralize, singularize


class TestItalianSingularRules:
    def test_che_to_ca(self) -> None:
        for plural, singular in [("amiche", "amica"), ("banche", "banca"),
                                 ("mucche", "mucca"), ("tiche", "tica")]:
            assert singularize(plural, lang="it") == singular

    def test_ghe_to_ga(self) -> None:
        for plural, singular in [("leghe", "lega"), ("righe", "riga"),
                                 ("piaghe", "piaga"), ("droghe", "droga")]:
            assert singularize(plural, lang="it") == singular

    def test_chi_to_co(self) -> None:
        for plural, singular in [("banchi", "banco"), ("pacchi", "pacco"),
                                 ("aghi", "ago"), ("funghi", "fungo")]:
            assert singularize(plural, lang="it") == singular

    def test_ghi_to_go(self) -> None:
        for plural, singular in [("laghi", "lago"), ("luoghi", "luogo")]:
            assert singularize(plural, lang="it") == singular

    def test_ci_to_ce(self) -> None:
        for plural, singular in [("luci", "luce"), ("voci", "voce")]:
            assert singularize(plural, lang="it") == singular

    def test_i_to_o(self) -> None:
        for plural, singular in [("libri", "libro"), ("gatti", "gatto"),
                                 ("tavoli", "tavolo"), ("amori", "amore")]:
            assert singularize(plural, lang="it") == singular

    def test_e_to_a(self) -> None:
        for plural, singular in [("case", "casa"), ("gatte", "gatta"),
                                 ("scuole", "scuola"), ("banane", "banana")]:
            assert singularize(plural, lang="it") == singular


class TestItalianIrregularSingles:
    @pytest.mark.parametrize("plural,singular", [
        ("amici", "amico"), ("medici", "medico"), ("nemici", "nemico"),
        ("logici", "logico"), ("magici", "magico"), ("tragici", "tragico"),
        ("comici", "comico"), ("filosofici", "filosofico"),
        ("storici", "storico"), ("geografici", "geografico"),
        ("biologi", "biologo"), ("psicologi", "psicologo"),
        ("teologi", "teologo"), ("archeologi", "archeologo"),
        ("tecnici", "tecnico"), ("politici", "politico"),
        ("pratici", "pratico"), ("identici", "identico"),
        ("simpatici", "simpatico"), ("dinamici", "dinamico"),
        ("romantici", "romantico"), ("sintatici", "sintatico"),
        ("pubblici", "pubblico"), ("tedeschi", "tedesco"),
        ("asparagi", "asparago"),
        ("laghi", "lago"), ("fuochi", "fuoco"),
        ("luoghi", "luogo"), ("giochi", "gioco"),
        ("porci", "porco"),
        ("uomini", "uomo"), ("mogli", "moglie"),
        ("dei", "dio"), ("templi", "tempio"),
        ("buoi", "bue"), ("ali", "ala"),
        ("armi", "arma"), ("dita", "dito"),
        ("ossa", "osso"), ("labbra", "labbro"),
        ("ginocchia", "ginocchio"), ("occhi", "occhio"),
        ("orecchi", "orecchio"), ("uova", "uovo"),
        ("paia", "paio"), ("miglia", "miglio"),
        ("centinaia", "centinaio"), ("migliaia", "migliaio"),
        ("cani", "cane"), ("fiori", "fiore"), ("pani", "pane"), ("amori", "amore"),
        ("notti", "notte"), ("menti", "mente"), ("fronti", "fronte"),
        ("sedi", "sede"), ("parti", "parte"), ("classi", "classe"),
        ("noci", "noce"), ("fedi", "fede"), ("paci", "pace"),
        ("croci", "croce"), ("genti", "gente"), ("navi", "nave"),
        ("valli", "valle"), ("pareti", "parete"), ("radici", "radice"),
        ("voci", "voce"),
        ("baci", "bacio"), ("spazi", "spazio"), ("uffici", "ufficio"),
        ("soci", "socio"), ("cambi", "cambio"), ("esempi", "esempio"),
        ("principi", "principio"), ("stadi", "stadio"), ("negozi", "negozio"),
        ("formaggi", "formaggio"), ("viaggi", "viaggio"), ("raggi", "raggio"),
        ("coraggi", "coraggio"), ("passaggi", "passaggio"), ("messaggi", "messaggio"),
        ("case", "casa"), ("scuole", "scuola"), ("banane", "banana"),
        ("gatte", "gatta"), ("paste", "pasta"), ("piante", "pianta"),
        ("famiglie", "famiglia"), ("squadre", "squadra"), ("feste", "festa"),
        ("donne", "donna"), ("ragazze", "ragazza"), ("macchine", "macchina"),
        ("piazze", "piazza"), ("pizze", "pizza"), ("bambine", "bambina"),
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
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="it") == singular


class TestItalianRoundTrip:
    """Round-trip: singularize(pluralize(x)) == x for common words."""

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
    ])
    def test_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word, lang="it"), lang="it") == word
