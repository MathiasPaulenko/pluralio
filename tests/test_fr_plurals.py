from __future__ import annotations

import pytest

from pluralio import pluralize


class TestFrenchPluralRules:
    def test_al_to_aux(self) -> None:
        for singular, plural in [("cheval", "chevaux"), ("animal", "animaux"),
                                 ("journal", "journaux"), ("hôpital", "hôpitaux"),
                                 ("bocal", "bocaux"), ("local", "locaux")]:
            assert pluralize(singular, lang="fr") == plural

    def test_eau_to_eaux(self) -> None:
        for singular, plural in [("bateau", "bateaux"), ("chapeau", "chapeaux"),
                                 ("manteau", "manteaux"), ("rideau", "rideaux")]:
            assert pluralize(singular, lang="fr") == plural

    def test_eu_to_eux(self) -> None:
        for singular, plural in [("jeu", "jeux"), ("feu", "feux"),
                                 ("vœu", "vœux")]:
            assert pluralize(singular, lang="fr") == plural

    def test_eu_plus_s_exceptions(self) -> None:
        for singular, plural in [("bleu", "bleus"), ("pneu", "pneus"),
                                 ("émeu", "émeus")]:
            assert pluralize(singular, lang="fr") == plural

    def test_au_to_aux(self) -> None:
        for singular, plural in [("tuyau", "tuyaux"), ("noyau", "noyaux"),
                                 ("boyau", "boyaux"), ("sarrau", "sarraux")]:
            assert pluralize(singular, lang="fr") == plural

    def test_s_invariable(self) -> None:
        for word in ["fois", "souris", "brebis", "cours", "poids"]:
            assert pluralize(word, lang="fr") == word

    def test_x_invariable(self) -> None:
        for word in ["croix", "voix", "noix", "choix", "prix"]:
            assert pluralize(word, lang="fr") == word

    def test_z_invariable(self) -> None:
        for word in ["nez"]:
            assert pluralize(word, lang="fr") == word

    def test_default_plus_s(self) -> None:
        for singular, plural in [("chat", "chats"), ("livre", "livres"),
                                 ("maison", "maisons"), ("détail", "détails"),
                                 ("trou", "trous"), ("arbre", "arbres")]:
            assert pluralize(singular, lang="fr") == plural

    def test_already_plural_unchanged(self) -> None:
        for word in ["chats", "livres", "maisons", "bateaux", "chevaux"]:
            assert pluralize(word, lang="fr") == word


class TestFrenchIrregularPlurals:
    @pytest.mark.parametrize("singular,plural", [
        # -al → -als (exceptions to the -aux rule)
        ("bal", "bals"), ("festival", "festivals"), ("carnaval", "carnavals"),
        ("récital", "récitals"), ("cal", "cals"), ("pal", "pals"),
        ("narval", "narvals"), ("régal", "régals"),
        ("fatal", "fatals"),
        # -ail → -aux (exceptions to the +s rule)
        ("travail", "travaux"), ("vitrail", "vitraux"),
        ("soupirail", "soupiraux"), ("corail", "coraux"),
        ("émail", "émaux"), ("fermail", "fermaux"),
        ("ventail", "ventaux"), ("bail", "baux"),
        # -ou → -oux (exceptions to the +s rule)
        ("bijou", "bijoux"), ("caillou", "cailloux"), ("hibou", "hiboux"),
        ("chou", "choux"), ("genou", "genoux"), ("pou", "poux"),
        ("joujou", "joujoux"), ("ripou", "ripoux"),
        # -au → -aux (common words needing explicit mapping)
        ("tuyau", "tuyaux"), ("noyau", "noyaux"), ("boyau", "boyaux"),
        ("sarrau", "sarraux"),
        # -eu → -eux (exceptions: most -eu words take -eux)
        ("jeu", "jeux"), ("feu", "feux"), ("vœu", "vœux"),
        # -eu → +s (exceptions to the -eux rule)
        ("bleu", "bleus"), ("pneu", "pneus"), ("émeu", "émeus"),
        # Special plurals (completely irregular)
        ("œil", "yeux"), ("ciel", "cieux"),
        ("monsieur", "messieurs"), ("madame", "mesdames"),
        ("mademoiselle", "mesdemoiselles"),
        # -al → -aux (common words needing explicit mapping)
        ("cheval", "chevaux"), ("animal", "animaux"),
        ("journal", "journaux"), ("général", "généraux"),
        ("hôpital", "hôpitaux"), ("capital", "capitaux"),
        ("signal", "signaux"), ("idéal", "idéaux"),
        ("bocal", "bocaux"), ("local", "locaux"),
        ("natal", "nataux"), ("royal", "royaux"),
        ("amiral", "amiraux"), ("rival", "rivaux"),
        ("cristal", "cristaux"), ("métal", "métaux"),
        ("principal", "principaux"), ("social", "sociaux"),
        ("spécial", "spéciaux"), ("normal", "normaux"),
        ("national", "nationaux"), ("rational", "rationaux"),
        ("international", "internationaux"),
        ("canal", "canaux"),
        # Foreign loanwords (+s, regular but listed for safety)
        ("weekend", "weekends"), ("parking", "parkings"),
        ("shopping", "shoppings"), ("meeting", "meetings"),
        ("club", "clubs"), ("leader", "leaders"),
        ("record", "records"), ("star", "stars"),
        ("test", "tests"), ("sandwich", "sandwichs"),
        ("ketchup", "ketchups"), ("byte", "bytes"),
        ("code", "codes"), ("bug", "bugs"),
        ("script", "scripts"), ("server", "servers"),
        ("framework", "frameworks"), ("endpoint", "endpoints"),
        ("callback", "callbacks"), ("middleware", "middlewares"),
        ("pipeline", "pipelines"), ("token", "tokens"),
        ("container", "containers"), ("docker", "dockers"),
    ])
    def test_irregular_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="fr") == plural


class TestFrenchUncountable:
    @pytest.mark.parametrize("word", [
        # Abstract/uncountable nouns
        "information", "recherche", "violence", "patience",
        "courage", "liberté", "justice", "beauté",
        "jeunesse", "vieillesse", "faiblesse", "sagesse",
        "richesse", "santé", "faim", "soif",
        "peur", "joie", "tristesse", "colère",
        "amour", "haine", "espoir", "désespoir",
        "temps", "argent", "or", "fer",
        "cuivre", "plomb", "bois", "verre",
        "papier", "cuir", "plastique", "caoutchouc",
        # Foods (uncountable)
        "pain", "lait", "beurre", "fromage",
        "sucre", "sel", "poivre", "riz",
        "farine", "viande", "porc", "jambon",
        # -s invariable
        "fois", "souris", "brebis", "cours",
        "poids", "rhinocéros", "virus",
        # -x invariable
        "croix", "voix", "noix",
        "choix", "prix",
        # -z invariable
        "nez",
        # Foreign (invariable)
        "jazz", "rock", "punk", "flash",
        # Always plural (pluralia tantum)
        "obsèques", "fiançailles", "ténèbres",
        "archives", "mathématiques",
    ])
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="fr") == word
