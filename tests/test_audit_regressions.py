"""Regression tests for bugs found and fixed during the stabilization audit.

Each test pins a specific defect that was repaired; if any of these
fail, a previously fixed bug has returned.
"""

from __future__ import annotations

import pytest

from pluralio import (
    add_irregular,
    add_plural,
    add_plural_rule,
    add_singular,
    add_singular_rule,
    add_uncountable,
    is_plural,
    is_singular,
    join,
    ordinal,
    pluralize,
    register_language,
    singularize,
    template,
)
from pluralio.registry import (
    LanguageRules,
    get_rules,
    register,
    restore,
    snapshot,
    supported_languages,
)


class TestEnUsEsWords:
    """-us nouns whose plural is +es (genius → geniuses)."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("geniuses", "genius"),
        ("focuses", "focus"),
        ("apparatuses", "apparatus"),
        ("hiatuses", "hiatus"),
        ("impetuses", "impetus"),
        ("thesauruses", "thesaurus"),
        ("prospectuses", "prospectus"),
        ("rhombuses", "rhombus"),
        ("papyruses", "papyrus"),
        ("citruses", "citrus"),
        ("calluses", "callus"),
        ("toruses", "torus"),
        ("cumuluses", "cumulus"),
        ("cirruses", "cirrus"),
        ("boluses", "bolus"),
        ("taluses", "talus"),
        ("umbilicuses", "umbilicus"),
        ("succubuses", "succubus"),
        ("incubuses", "incubus"),
        ("rumpuses", "rumpus"),
        ("tumuluses", "tumulus"),
        ("nexuses", "nexus"),
        ("phosphoruses", "phosphorus"),
        ("ignoramuses", "ignoramus"),
        ("eucalyptuses", "eucalyptus"),
        ("humuses", "humus"),
        ("surpluses", "surplus"),
        ("tarsuses", "tarsus"),
        ("carpuses", "carpus"),
        ("bronchuses", "bronchus"),
        ("cactuses", "cactus"),
        ("nucleuses", "nucleus"),
        ("radiuses", "radius"),
        ("alumnuses", "alumnus"),
        ("funguses", "fungus"),
        ("stimuluses", "stimulus"),
        ("syllabuses", "syllabus"),
        ("abacuses", "abacus"),
    ])
    def test_singularize_us_es(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("genius", "geniuses"),
        ("apparatus", "apparatuses"),
        ("hiatus", "hiatuses"),
        ("impetus", "impetuses"),
        ("thesaurus", "thesauruses"),
        ("prospectus", "prospectuses"),
        ("rhombus", "rhombuses"),
        ("papyrus", "papyruses"),
        ("citrus", "citruses"),
        ("callus", "calluses"),
        ("torus", "toruses"),
        ("cumulus", "cumuluses"),
        ("cirrus", "cirruses"),
        ("bolus", "boluses"),
        ("talus", "taluses"),
        ("umbilicus", "umbilicuses"),
        ("succubus", "succubuses"),
        ("incubus", "incubuses"),
        ("rumpus", "rumpuses"),
        ("tumulus", "tumuluses"),
        ("nexus", "nexuses"),
        ("phosphorus", "phosphoruses"),
        ("ignoramus", "ignoramuses"),
        ("eucalyptus", "eucalyptuses"),
        ("humus", "humuses"),
        ("surplus", "surpluses"),
        ("tarsus", "tarsuses"),
        ("carpus", "carpuses"),
        ("bronchus", "bronchuses"),
        ("asparagus", "asparaguses"),
    ])
    def test_pluralize_us(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    def test_menu_takes_plain_s(self) -> None:
        assert pluralize("menu") == "menus"
        assert singularize("menus") == "menu"

    def test_kudos_invariable(self) -> None:
        assert pluralize("kudos") == "kudos"
        assert singularize("kudos") == "kudos"
        assert is_plural("kudos")
        assert is_singular("kudos")


class TestEnUseWordsProtected:
    """-use words ending in 'uses' must not be hit by the uses$ → us rule."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("houses", "house"),
        ("amuses", "amuse"),
        ("bemuses", "bemuse"),
        ("confuses", "confuse"),
        ("refuses", "refuse"),
        ("diffuses", "diffuse"),
        ("infuses", "infuse"),
        ("defuses", "defuse"),
        ("effuses", "effuse"),
        ("accuses", "accuse"),
        ("arouses", "arouse"),
        ("rouses", "rouse"),
        ("espouses", "espouse"),
        ("disuses", "disuse"),
        ("louses", "louse"),
        ("mouses", "mouse"),
        ("uses", "use"),
        ("excuses", "excuse"),
        ("spouses", "spouse"),
        ("causes", "cause"),
        ("pauses", "pause"),
        ("clauses", "clause"),
        ("applauses", "applause"),
        ("blouses", "blouse"),
        ("fuses", "fuse"),
        ("muses", "muse"),
        ("ruses", "ruse"),
        ("abuses", "abuse"),
    ])
    def test_singularize_use_words(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestEnShoesCompounds:
    """Compound -shoe words take +s; the oes rule must not eat the 'e'."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("horseshoes", "horseshoe"),
        ("snowshoes", "snowshoe"),
        ("gumshoes", "gumshoe"),
        ("overshoes", "overshoe"),
    ])
    def test_singularize_shoes_compounds(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    def test_round_trip(self) -> None:
        assert pluralize("horseshoe") == "horseshoes"
        assert singularize(pluralize("horseshoe")) == "horseshoe"


class TestEnFeWords:
    """-afe words take +s; only l+f takes -ves."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("carafe", "carafes"),
        ("chafe", "chafes"),
        ("safe", "safes"),
        ("cafe", "cafes"),
        ("giraffe", "giraffes"),
        ("strafe", "strafes"),
    ])
    def test_pluralize_afe(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("barf", "barfs"),
        ("nerf", "nerfs"),
        ("snarf", "snarfs"),
        ("serf", "serfs"),
        ("surf", "surfs"),
        ("cliff", "cliffs"),
        ("sheriff", "sheriffs"),
    ])
    def test_pluralize_consonant_f_takes_s(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("wolf", "wolves"),
        ("self", "selves"),
        ("shelf", "shelves"),
        ("bookshelf", "bookshelves"),
        ("werewolf", "werewolves"),
        ("headscarf", "headscarves"),
    ])
    def test_pluralize_ves_class(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    def test_ves_round_trip(self) -> None:
        assert singularize(pluralize("bookshelf")) == "bookshelf"
        assert singularize(pluralize("werewolf")) == "werewolf"


class TestEnConsonantOExceptions:
    """Consonant + o loanwords that take plain +s."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("limo", "limos"),
        ("nacho", "nachos"),
        ("bimbo", "bimbos"),
        ("bro", "bros"),
        ("promo", "promos"),
        ("jello", "jellos"),
        ("afro", "afros"),
        ("mambo", "mambos"),
        ("matzo", "matzos"),
    ])
    def test_pluralize_o_exceptions(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("hero", "heroes"),
        ("echo", "echoes"),
        ("potato", "potatoes"),
        ("tomato", "tomatoes"),
        ("domino", "dominoes"),
        ("mango", "mangoes"),
    ])
    def test_pluralize_oes_still_works(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected


class TestEnMisc:
    def test_taxies_singularize(self) -> None:
        assert singularize("taxies") == "taxi"
        assert singularize("taxis") == "taxi"

    def test_inspect_with_us_words(self) -> None:
        assert is_plural("geniuses")
        assert is_singular("genius")
        assert not is_plural("genius")
        assert is_plural("menus")
        assert is_singular("menu")


class TestFrRegressions:
    def test_pot_au_feu_compound(self) -> None:
        assert pluralize("pot-au-feu", lang="fr") == "pots-au-feu"
        assert singularize("pots-au-feu", lang="fr") == "pot-au-feu"
        # already-singular compound is idempotent
        assert singularize("pot-au-feu", lang="fr") == "pot-au-feu"

    def test_coq_au_vin_compound(self) -> None:
        assert pluralize("coq-au-vin", lang="fr") == "coqs-au-vin"
        assert singularize("coqs-au-vin", lang="fr") == "coq-au-vin"

    def test_landau_regular_plural(self) -> None:
        assert pluralize("landau", lang="fr") == "landaus"

    @pytest.mark.parametrize("word", [
        "mois", "relais", "repas", "matelas", "os", "obus", "vernis",
        "puits", "châssis", "maquis", "dais", "débris", "autobus",
        "bus", "iris",
    ])
    def test_s_invariable_nouns(self, word: str) -> None:
        assert pluralize(word, lang="fr") == word
        assert singularize(word, lang="fr") == word


class TestItRegressions:
    @pytest.mark.parametrize(("word", "expected"), [
        ("sindaco", "sindaci"),
        ("chimico", "chimici"),
        ("fisico", "fisici"),
        ("critico", "critici"),
        ("tipico", "tipici"),
        ("classico", "classici"),
        ("cattolico", "cattolici"),
        ("alcolico", "alcolici"),
        ("epico", "epici"),
        ("etnico", "etnici"),
        ("lirico", "lirici"),
        ("arsenico", "arsenici"),
        ("greco", "greci"),
        ("geologo", "geologi"),
        ("antropologo", "antropologi"),
        ("etnologo", "etnologi"),
        ("astrologo", "astrologi"),
        ("cosmologo", "cosmologi"),
        ("diploma", "diplomi"),
        ("sintoma", "sintomi"),
        ("idiota", "idioti"),
    ])
    def test_pluralize_sdrucciola_and_greek(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="it") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("pianista", "pianisti"),
        ("dentista", "dentisti"),
        ("barista", "baristi"),
        ("ciclista", "ciclisti"),
        ("tassista", "tassisti"),
        ("chitarrista", "chitarristi"),
        ("violinista", "violinisti"),
        ("cellista", "cellisti"),
        ("solista", "solisti"),
        ("ottimista", "ottimisti"),
        ("pessimista", "pessimisti"),
        ("fascista", "fascisti"),
        ("comunista", "comunisti"),
        ("capitalista", "capitalisti"),
        ("socialista", "socialisti"),
        ("materialista", "materialisti"),
        ("idealista", "idealisti"),
        ("arrivista", "arrivisti"),
        ("animista", "animisti"),
    ])
    def test_pluralize_ista(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="it") == expected

    def test_ista_round_trip(self) -> None:
        assert singularize("pianisti", lang="it") == "pianista"
        assert singularize("baristi", lang="it") == "barista"

    def test_bracci_and_pesi(self) -> None:
        assert singularize("bracci", lang="it") == "braccio"
        assert singularize("pesi", lang="it") == "peso"

    @pytest.mark.parametrize("word", [
        "video", "sms", "pc", "tv", "cd", "dvd", "grù", "cento",
        "venti", "trenta", "undici", "novanta",
    ])
    def test_invariable_additions(self, word: str) -> None:
        assert pluralize(word, lang="it") == word
        assert singularize(word, lang="it") == word


class TestEsRegressions:
    def test_jersey(self) -> None:
        assert pluralize("jersey", lang="es") == "jerséis"
        assert singularize("jerséis", lang="es") == "jersey"
        assert singularize("jerseis", lang="es") == "jersey"
        # the plural form must be idempotent
        assert pluralize("jerséis", lang="es") == "jerséis"

    def test_peones_accent_restoration(self) -> None:
        assert singularize("peones", lang="es") == "peón"
        assert pluralize("peón", lang="es") == "peones"


class TestCountHandling:
    def test_string_counts_normalized(self) -> None:
        assert pluralize("cat", count="1") == "cat"  # type: ignore[arg-type]
        assert pluralize("cat", count=" 1 ") == "cat"  # type: ignore[arg-type]
        assert pluralize("cat", count="01") == "cat"  # type: ignore[arg-type]
        assert pluralize("cat", count="2") == "cats"  # type: ignore[arg-type]
        assert pluralize("cat", count="abc") == "cats"  # type: ignore[arg-type]

    def test_numeric_counts(self) -> None:
        assert pluralize("cat", count=1) == "cat"
        assert pluralize("cat", count=0) == "cats"
        assert pluralize("cat", count=2) == "cats"
        assert pluralize("cat", count=None) == "cats"


class TestRegistryValidation:
    def test_register_non_str_code_raises(self) -> None:
        state = snapshot()
        try:
            with pytest.raises(TypeError, match="must be str"):
                register(LanguageRules(code=5))  # type: ignore[arg-type]
        finally:
            restore(state)
        # registry must not be poisoned by the failed registration
        assert supported_languages() == ["en", "eo", "es", "fr", "it", "pt"]

    def test_get_rules_non_str_lang_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            get_rules([])  # type: ignore[arg-type]

    def test_get_rules_none_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            get_rules(None)  # type: ignore[arg-type]


class TestExtensibilityValidation:
    @pytest.mark.parametrize(("kwargs", "match"), [
        ({"singular": None, "plural": "x"}, "singular must be str"),
        ({"singular": "x", "plural": 5}, "plural must be str"),
    ])
    def test_add_irregular_validates(
        self, kwargs: dict[str, object], match: str
    ) -> None:
        with pytest.raises(TypeError, match=match):
            add_irregular(**kwargs)  # type: ignore[arg-type]

    def test_add_plural_validates(self) -> None:
        with pytest.raises(TypeError, match="must be str"):
            add_plural(1, "x")  # type: ignore[arg-type]

    def test_add_singular_validates(self) -> None:
        with pytest.raises(TypeError, match="must be str"):
            add_singular(1, "x")  # type: ignore[arg-type]

    def test_add_uncountable_validates(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            add_uncountable(1)  # type: ignore[arg-type]

    def test_add_plural_rule_validates(self) -> None:
        with pytest.raises(TypeError, match="pattern must be str"):
            add_plural_rule(1, "x")  # type: ignore[arg-type]

    def test_add_singular_rule_validates(self) -> None:
        with pytest.raises(TypeError, match="replacement must be str"):
            add_singular_rule("x$", 1)  # type: ignore[arg-type]


class TestRegisterLanguageEmptyRules:
    def test_empty_rules_lists_mean_no_rules(self) -> None:
        state = snapshot()
        try:
            register_language("xx", plural_rules=[], singular_rules=[])
            # explicitly empty rule lists are honored (no default injected)
            assert pluralize("cat", lang="xx") == "cat"
            assert singularize("cats", lang="xx") == "cats"
        finally:
            restore(state)

    def test_omitted_rules_get_defaults(self) -> None:
        state = snapshot()
        try:
            register_language("yy")
            assert pluralize("cat", lang="yy") == "cats"
            assert singularize("cats", lang="yy") == "cat"
        finally:
            restore(state)


class TestUtilsRegressions:
    def test_ordinal_none_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="requires an integer"):
            ordinal(None)  # type: ignore[arg-type]

    def test_ordinal_infinity_raises_valueerror(self) -> None:
        with pytest.raises(ValueError, match="requires an integer"):
            ordinal(float("inf"))  # type: ignore[arg-type]

    def test_ordinal_non_integral_float_raises(self) -> None:
        with pytest.raises(ValueError, match="requires an integer"):
            ordinal(1.5)  # type: ignore[arg-type]

    def test_template_count_none_pluralizes(self) -> None:
        assert template("{w:pluralize}", w="cat", count=None) == "cats"

    def test_template_count_int(self) -> None:
        assert template("{w:pluralize}", w="cat", count=1) == "cat"
        assert template("{w:pluralize}", w="cat", count=2) == "cats"

    def test_template_custom_count_var(self) -> None:
        assert template("{w:pluralize:n}", w="cat", n=1) == "cat"

    def test_join_empty_conjunction_two_items(self) -> None:
        assert join(["a", "b"], conjunction="") == "a b"

    def test_join_empty_conjunction_three_items(self) -> None:
        assert join(["a", "b", "c"], conjunction="") == "a, b, c"

    def test_join_empty_conjunction_and_final_sep(self) -> None:
        assert join(["a", "b", "c"], conjunction="", final_sep="") == "a, b c"

    def test_join_default_behavior_unchanged(self) -> None:
        assert join(["a", "b"]) == "a and b"
        assert join(["a", "b", "c"]) == "a, b, and c"
        assert join(["a", "b", "c"], final_sep="") == "a, b and c"
