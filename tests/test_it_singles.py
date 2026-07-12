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
        ("sedie", "sedia"), ("chiavi", "chiave"), ("isole", "isola"),
        ("forchette", "forchetta"), ("spine", "spina"), ("pietre", "pietra"),
        ("robe", "roba"), ("camicie", "camicia"), ("montagne", "montagna"),
        ("stelle", "stella"), ("barche", "barca"),
        ("cuori", "cuore"), ("studenti", "studente"), ("denti", "dente"),
        ("nomi", "nome"), ("soli", "sole"), ("colori", "colore"), ("valori", "valore"),
        ("dottori", "dottore"), ("signori", "signore"), ("attori", "attore"),
        ("professori", "professore"), ("imperatori", "imperatore"),
        ("scultori", "scultore"), ("pittori", "pittore"), ("scrittori", "scrittore"),
        ("superfici", "superficie"), ("effigi", "effigie"),
        ("studi", "studio"), ("esercizi", "esercizio"),
        ("piogge", "pioggia"), ("valigie", "valigia"),
        ("rocce", "roccia"), ("fasce", "fascia"), ("asce", "ascia"),
        ("problemi", "problema"), ("temi", "tema"), ("sistemi", "sistema"),
        ("poemi", "poema"), ("climi", "clima"), ("drammi", "dramma"),
        ("programmi", "programma"), ("telegrammi", "telegramma"),
        ("schemi", "schema"), ("dogmi", "dogma"), ("emblemi", "emblema"),
        ("idiomi", "idioma"), ("fantasmi", "fantasma"), ("pirati", "pirata"),
        ("poeti", "poeta"), ("colleghi", "collega"), ("atleti", "atleta"),
        ("artisti", "artista"), ("autisti", "autista"), ("giornalisti", "giornalista"),
        ("linguisti", "linguista"), ("turisti", "turista"), ("astronauti", "astronauta"),
        ("fiumi", "fiume"), ("ponti", "ponte"), ("clienti", "cliente"),
        ("residenti", "residente"), ("presidenti", "presidente"),
        ("generali", "generale"), ("animali", "animale"), ("fossili", "fossile"),
        ("fucili", "fucile"), ("cortili", "cortile"), ("volgari", "volgare"),
        ("regolari", "regolare"), ("singolari", "singolare"), ("particolari", "particolare"),
        ("borse", "borsa"), ("coppie", "coppia"), ("porte", "porta"),
        ("torte", "torta"), ("tazze", "tazza"), ("sale", "sala"),
        ("ruote", "ruota"), ("penne", "penna"), ("palle", "palla"),
        ("tele", "tela"), ("sorelle", "sorella"), ("fruste", "frusta"),
        ("braccia", "braccio"), ("lenzuola", "lenzuolo"), ("ciglia", "ciglio"),
        ("lacci", "laccio"), ("stracci", "straccio"), ("sacrifici", "sacrificio"),
        ("abbracci", "abbraccio"), ("obblighi", "obbligo"),
        ("torri", "torre"), ("corti", "corte"), ("sorti", "sorte"),
        ("morti", "morte"), ("canzoni", "canzone"),
        ("bicchieri", "bicchiere"), ("giornali", "giornale"), ("mari", "mare"),
        ("padri", "padre"), ("madri", "madre"), ("rei", "re"),
        ("zii", "zio"), ("zie", "zia"),
        ("fratelli", "fratello"), ("nonni", "nonno"), ("nonne", "nonna"),
        ("cugini", "cugino"), ("cugine", "cugina"),
        ("piedi", "piede"), ("fini", "fine"), ("margini", "margine"),
        ("bottoni", "bottone"), ("giganti", "gigante"), ("santoni", "santone"),
        ("difensori", "difensore"), ("attaccanti", "attaccante"),
        ("esemplari", "esemplare"), ("necessari", "necessario"),
        ("sufficienti", "sufficiente"), ("importanti", "importante"),
        ("evidenti", "evidente"), ("intelligenti", "intelligente"),
        ("potenti", "potente"), ("urgenti", "urgente"),
        ("simili", "simile"), ("facili", "facile"), ("difficili", "difficile"),
        ("utili", "utile"), ("inutili", "inutile"),
        ("possibili", "possibile"), ("impossibili", "impossibile"),
        ("probabili", "probabile"), ("improbabili", "improbabile"),
        ("portatili", "portatile"), ("turbini", "turbine"),
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
        "notte", "mente", "fronte", "sede", "parte", "classe",
        "noce", "fede", "pace", "croce", "gente", "nave",
        "valle", "parete", "radice", "voce",
        "bacio", "spazio", "ufficio", "socio", "cambio", "esempio",
        "principio", "stadio", "negozio",
        "formaggio", "viaggio", "raggio", "coraggio",
        "passaggio", "messaggio",
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
    def test_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word, lang="it"), lang="it") == word
