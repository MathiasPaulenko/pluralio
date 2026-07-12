from __future__ import annotations

import pytest

from pluralio import pluralize, singularize


class TestFrenchSingularRules:
    def test_eaux_to_eau(self) -> None:
        for plural, singular in [("bateaux", "bateau"), ("chapeaux", "chapeau"),
                                 ("manteaux", "manteau"), ("rideaux", "rideau")]:
            assert singularize(plural, lang="fr") == singular

    def test_aux_to_al(self) -> None:
        for plural, singular in [("chevaux", "cheval"), ("animaux", "animal"),
                                 ("journaux", "journal"), ("bocaux", "bocal")]:
            assert singularize(plural, lang="fr") == singular

    def test_eux_to_eu(self) -> None:
        for plural, singular in [("jeux", "jeu"), ("feux", "feu")]:
            assert singularize(plural, lang="fr") == singular

    def test_s_strip(self) -> None:
        for plural, singular in [("chats", "chat"), ("livres", "livre"),
                                 ("maisons", "maison"), ("détails", "détail"),
                                 ("trous", "trou"), ("arbres", "arbre")]:
            assert singularize(plural, lang="fr") == singular


class TestFrenchIrregularSingles:
    @pytest.mark.parametrize("plural,singular", [
        # -als → -al (exceptions to the -aux rule)
        ("bals", "bal"), ("festivals", "festival"), ("carnavals", "carnaval"),
        ("récitals", "récital"), ("cals", "cal"), ("pals", "pal"),
        ("narvals", "narval"), ("régals", "régal"),
        ("fatals", "fatal"),
        # -aux → -ail (exceptions: regex gives -al, but these come from -ail)
        ("travaux", "travail"), ("vitraux", "vitrail"),
        ("soupiraux", "soupirail"), ("coraux", "corail"),
        ("émaux", "émail"), ("fermaux", "fermail"),
        ("ventaux", "ventail"), ("baux", "bail"),
        # -aux → -au (regex gives -al, but these come from -au)
        ("tuyaux", "tuyau"), ("noyaux", "noyau"), ("boyaux", "boyau"),
        ("sarraux", "sarrau"),
        # -oux → -ou (irregulars only, not in regex)
        ("bijoux", "bijou"), ("cailloux", "caillou"), ("hiboux", "hibou"),
        ("choux", "chou"), ("genoux", "genou"), ("poux", "pou"),
        ("joujoux", "joujou"), ("ripoux", "ripou"),
        # -eux → -eu (irregulars for singularization safety)
        ("jeux", "jeu"), ("feux", "feu"), ("vœux", "vœu"),
        # -eus → -eu (regular +s plurals)
        ("bleus", "bleu"), ("pneus", "pneu"), ("émeus", "émeu"),
        # Special plurals
        ("yeux", "œil"), ("cieux", "ciel"),
        ("messieurs", "monsieur"), ("mesdames", "madame"),
        ("mesdemoiselles", "mademoiselle"),
        # -aux → -al (common words)
        ("chevaux", "cheval"), ("animaux", "animal"),
        ("journaux", "journal"), ("généraux", "général"),
        ("hôpitaux", "hôpital"), ("capitaux", "capital"),
        ("signaux", "signal"), ("idéaux", "idéal"),
        ("bocaux", "bocal"), ("locaux", "local"),
        ("nataux", "natal"), ("royaux", "royal"),
        ("amiraux", "amiral"), ("rivaux", "rival"),
        ("cristaux", "cristal"), ("métaux", "métal"),
        ("principaux", "principal"), ("sociaux", "social"),
        ("spéciaux", "spécial"), ("normaux", "normal"),
        ("nationaux", "national"), ("rationaux", "rational"),
        ("internationaux", "international"),
        # Accentless variants
        ("ideaux", "ideal"), ("emaux", "email"),
        ("canaux", "canal"),
        # Foreign loanwords
        ("weekends", "weekend"), ("parkings", "parking"),
        ("shoppings", "shopping"), ("meetings", "meeting"),
        ("clubs", "club"), ("leaders", "leader"),
        ("records", "record"), ("stars", "star"),
        ("tests", "test"), ("sandwichs", "sandwich"),
        ("ketchups", "ketchup"), ("bytes", "byte"),
        ("codes", "code"), ("bugs", "bug"),
        ("scripts", "script"), ("servers", "server"),
        ("frameworks", "framework"), ("endpoints", "endpoint"),
        ("callbacks", "callback"), ("middlewares", "middleware"),
        ("pipelines", "pipeline"), ("tokens", "token"),
        ("containers", "container"), ("dockers", "docker"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="fr") == singular


class TestFrenchRoundTrip:
    """Round-trip: singularize(pluralize(x)) == x for common words."""

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
        "tuyau", "noyau", "boyau",
        "bail",
        "weekend", "parking", "club", "leader", "test",
    ])
    def test_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word, lang="fr"), lang="fr") == word
