from __future__ import annotations

import unicodedata

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestInputValidation:
    def test_empty_string_pluralize(self) -> None:
        assert pluralize("") == ""

    def test_empty_string_singularize(self) -> None:
        assert singularize("") == ""

    def test_none_raises_typeerror_pluralize(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            pluralize(None)  # type: ignore[arg-type]

    def test_none_raises_typeerror_singularize(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            singularize(None)  # type: ignore[arg-type]

    def test_non_string_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            pluralize(123)  # type: ignore[arg-type]

    def test_int_input_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="word must be str"):
            singularize(42)  # type: ignore[arg-type]


class TestCasePreservation:
    @pytest.mark.parametrize("word,expected", [
        ("Library", "Libraries"),
        ("LIBRARY", "LIBRARIES"),
        ("Box", "Boxes"),
        ("BOX", "BOXES"),
        ("Child", "Children"),
        ("CHILD", "CHILDREN"),
        ("City", "Cities"),
        ("CITY", "CITIES"),
    ])
    def test_title_case_preserved(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("Libraries", "Library"),
        ("LIBRARIES", "LIBRARY"),
        ("Boxes", "Box"),
        ("Children", "Child"),
    ])
    def test_singularize_case_preserved(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestHyphenatedWords:
    def test_mother_in_law(self) -> None:
        assert pluralize("mother-in-law") == "mothers-in-law"

    def test_runner_up(self) -> None:
        assert pluralize("runner-up") == "runners-up"

    def test_singularize_hyphenated(self) -> None:
        assert singularize("mothers-in-law") == "mother-in-law"

    def test_spanish_hyphenated(self) -> None:
        assert pluralize("café-bar", lang="es") == "cafés-bar"

    def test_leading_hyphen_pluralize(self) -> None:
        assert pluralize("-cat") == "-cats"

    def test_leading_hyphen_singularize(self) -> None:
        assert singularize("-cats") == "-cat"

    def test_multiple_hyphens(self) -> None:
        assert pluralize("mother-in-law") == "mothers-in-law"
        assert singularize("mothers-in-law") == "mother-in-law"

    def test_hyphen_only(self) -> None:
        assert pluralize("-") == "-"
        assert singularize("-") == "-"

    def test_double_hyphen(self) -> None:
        assert pluralize("--") == "--"
        assert singularize("--") == "--"


class TestCompoundLastSegment:
    """Compounds where the last segment is pluralized."""

    @pytest.mark.parametrize("singular,plural", [
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
    ])
    def test_last_segment_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize("singular,plural", [
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
    ])
    def test_last_segment_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
    ])
    def test_last_segment_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular

    def test_last_segment_trailing_hyphen(self) -> None:
        assert pluralize("forget-me-not-") == "forget-me-nots-"
        assert singularize("forget-me-nots-") == "forget-me-not-"


class TestCompoundComprehensive:
    """Comprehensive round-trip tests for compound words."""

    @pytest.mark.parametrize("singular,plural", [
        ("mother-in-law", "mothers-in-law"),
        ("father-in-law", "fathers-in-law"),
        ("sister-in-law", "sisters-in-law"),
        ("brother-in-law", "brothers-in-law"),
        ("runner-up", "runners-up"),
        ("passer-by", "passers-by"),
        ("hanger-on", "hangers-on"),
        ("attorney-general", "attorneys-general"),
        ("court-martial", "courts-martial"),
        ("editor-in-chief", "editors-in-chief"),
        ("man-of-war", "men-of-war"),
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
        ("jack-in-the-box", "jacks-in-the-box"),
    ])
    def test_en_compound_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("café-bar", "cafés-bar"),
        ("coche-cama", "coches-cama"),
        ("pequeño-burgués", "pequeños-burgueses"),
    ])
    def test_es_compound_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular


class TestWordsWithNumbers:
    def test_word_with_trailing_number(self) -> None:
        assert pluralize("item42") == "item42s"

    def test_word_with_leading_number(self) -> None:
        assert pluralize("42item") == "42items"


class TestWhitespaceHandling:
    def test_preserves_whitespace_pluralize(self) -> None:
        assert pluralize("  cat  ") == "  cats  "

    def test_preserves_whitespace_singularize(self) -> None:
        assert singularize("  cats  ") == "  cat  "

    def test_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ") == "   "
        assert singularize("   ") == "   "

    def test_count_one_preserves_whitespace(self) -> None:
        assert pluralize("  cat  ", count=1) == "  cat  "


class TestMixedCase:
    @pytest.mark.parametrize("word,expected", [
        ("McDonald", "McDonalds"),
        ("iPhone", "iPhones"),
        ("McBox", "McBoxes"),
    ])
    def test_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("McDonalds", "McDonald"),
        ("iPhones", "iPhone"),
    ])
    def test_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestSingleLetterWords:
    def test_singularize_single_s(self) -> None:
        assert singularize("s") == "s"

    def test_singularize_single_s_uppercase(self) -> None:
        assert singularize("S") == "S"

    def test_pluralize_single_letter(self) -> None:
        assert pluralize("a") == "as"
        assert pluralize("A") == "AS"


class TestIsSingularIsPlural:
    @pytest.mark.parametrize("word", [
        "bus", "gas", "boss", "lens", "cross", "status", "virus",
        "cactus", "nucleus", "analysis", "crisis", "thesis", "basis",
        "alumnus", "radius", "focus", "fungus", "stimulus", "syllabus",
        "axis", "diagnosis", "hypothesis", "oasis", "parenthesis",
        "plus", "yes",
    ])
    def test_en_singular_ending_s(self, word: str) -> None:
        assert is_singular(word, lang="en") is True
        assert is_plural(word, lang="en") is False

    @pytest.mark.parametrize("word", [
        "buses", "gases", "bosses", "lenses", "crosses",
        "statuses", "viruses", "analyses", "crises", "theses",
        "cacti", "nuclei", "alumni", "radii", "foci",
    ])
    def test_en_plural_ending_s(self, word: str) -> None:
        assert is_plural(word, lang="en") is True
        assert is_singular(word, lang="en") is False

    @pytest.mark.parametrize("word", [
        "inglés", "francés", "portugués", "japonés", "holandés",
        "danés", "irlandés", "aragonés", "leonés", "cordobés",
        "cortés", "interés", "montés", "burgalés", "logroñés",
        "tarraconés", "alavés", "mes",
    ])
    def test_es_singular_ending_s(self, word: str) -> None:
        assert is_singular(word, lang="es") is True
        assert is_plural(word, lang="es") is False

    @pytest.mark.parametrize("word", [
        "ingleses", "franceses", "portugueses", "japoneses",
        "holandeses", "daneses", "meses", "libros", "casas",
    ])
    def test_es_plural_ending_s(self, word: str) -> None:
        assert is_plural(word, lang="es") is True
        assert is_singular(word, lang="es") is False

    @pytest.mark.parametrize("word", [
        "sheep", "fish", "information", "rice", "means", "aircraft",
        "baggage", "series", "species", "jeans",
    ])
    def test_en_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="en") is True
        assert is_plural(word, lang="en") is True

    @pytest.mark.parametrize("word", [
        "lunes", "martes", "crisis", "análisis", "tórax", "fax",
        "res", "software", "web",
    ])
    def test_es_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="es") is True
        assert is_plural(word, lang="es") is True

    @pytest.mark.parametrize("word", [
        "cat", "cats", "dog", "dogs", "bus", "buses",
        "child", "children", "box", "boxes",
        "knife", "knives", "city", "cities",
    ])
    def test_en_mutual_exclusivity(self, word: str) -> None:
        assert not (is_singular(word) and is_plural(word))

    @pytest.mark.parametrize("word", [
        "libro", "libros", "casa", "casas", "inglés", "ingleses",
        "mes", "meses",
    ])
    def test_es_mutual_exclusivity(self, word: str) -> None:
        assert not (is_singular(word, lang="es") and is_plural(word, lang="es"))


class TestIrregularIdempotency:
    @pytest.mark.parametrize("word", [
        "children", "mice", "geese", "feet", "teeth",
        "men", "women", "people", "oxen", "cacti", "nuclei",
        "alumni", "analyses", "crises", "matrices", "wolves",
        "knives", "potatoes", "heroes", "quizzes", "gases",
        "bosses", "goes", "does", "dwarves",
    ])
    def test_en_pluralize_already_plural_irregular(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "cats", "dogs", "houses", "horses", "noses", "cases",
        "phases", "vases", "roses", "tenses", "senses",
        "licenses", "promises", "surprises", "teases", "pleases",
        "releases", "decreases", "increases", "diseases",
        "cruises", "abuses", "excuses", "uses", "fuses", "muses",
        "causes", "pauses", "glimpses",
        "fizzes", "buzzes", "fuzzes",
        "boxes", "foxes", "axes", "mixes", "fixes",
        "boys", "toys", "joys", "keys", "days", "ways",
        "monkeys", "donkeys", "valleys", "honeys", "moneys", "journeys",
        "cities", "stories", "bodies", "copies", "pennies", "parties",
        "queries", "burglaries", "skies", "flies", "supplies", "replies",
        "babies", "ladies",
        "wolves", "halves", "calves", "leaves", "loaves", "thieves",
        "selves", "shelves", "wives", "knives", "lives", "hooves",
        "dwarfs", "chiefs", "roofs", "proofs", "beliefs", "reliefs",
        "briefs", "turfs", "golfs", "gulfs", "reefs",
        "cafes", "safes", "giraffes", "strafes",
        "heroes", "potatoes", "tomatoes", "echoes", "vetoes", "torpedoes",
        "mosquitoes", "volcanoes", "photos", "pianos", "halos",
        "solos", "cellos", "discos", "memos", "autos", "egos",
        "kilos", "tempos", "turbos", "dynamos", "lassos", "jumbos",
        "mementos", "logos", "embryos", "ghettos", "concertos",
        "sopranos", "combos", "pros", "casinos", "tacos", "burritos",
        "ponchos", "sombreros", "flamingos", "tornados", "avocados",
        "albinos", "armadillos", "cappuccinos", "allegros", "boleros",
        "bongos", "cantos", "falsettos", "intermezzos", "rondos",
        "staccatos", "tremolos", "vibratos", "violoncellos", "timpanos",
        "cilantros", "cocos", "espressos", "gyros", "oreganos",
        "pimentos", "pintos", "risottos", "tobaccos", "burros",
        "hippos", "rhinos", "archipelagos", "bingos", "commandos",
        "dittos", "fiascos", "gizmos", "hairdos", "lumbagos",
        "magnetos", "manifestos", "sternos", "stuccos", "terrazzos",
        "torsos", "ufos", "aficionados", "aggros", "ammos",
        "credos", "crescendos", "cyanos", "demos", "euros",
        "flamencos", "furiosos", "generalissimos", "gigolos", "gringos",
        "guanos", "gumbos", "impetigos", "infos", "lingos",
        "linos", "livedos", "locos", "machos", "macros", "mafiosos",
        "magnificos", "medicos", "metros", "micros", "neutrinos",
        "octavos", "pedalos", "plecos", "polos", "psychos", "pueblos",
        "quartos", "repos", "rococos", "saddos", "sagos", "salvos",
        "siroccos", "stylos", "sumos", "technos", "testudos", "tiros",
        "toreros", "typos", "tyros", "vaqueros", "vermicellis",
        "versos", "weirdos", "yo-yos", "zeros",
        "radios", "stereos", "videos", "studios", "ratios", "patios",
        "shoes", "foes", "hoes", "toes", "aloes", "oboes", "canoes",
        "pies", "ties", "movies", "cookies", "selfies",
        "soliloquies",
        "statuses", "viruses", "atlases", "canvases", "biases",
        "bonuses", "campuses", "choruses", "circuses",
        "consensuses", "crocuses", "octopuses", "pelvises",
        "rebuses", "trellises", "platypuses", "minibuses", "omnibuses",
    ])
    def test_en_pluralize_already_plural_regex(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "jóvenes", "exámenes", "imágenes", "volúmenes",
        "ingleses", "franceses", "rubíes", "clubs", "álbumes",
        "guiones", "meses", "huracanes", "índices", "vértices",
        "relojes",
        "canciones", "corazones", "botones", "limones", "camiones",
        "lápices", "voces", "luces", "capaces", "felices",
        "ciudades", "verdades", "hombres", "mujeres", "calles",
        "papeles", "flores", "colores", "errores", "motores",
        "casas", "mesas", "perros", "libros", "plumas",
        "planes", "panes",
    ])
    def test_es_pluralize_already_plural_irregular(self, word: str) -> None:
        assert pluralize(word, lang="es") == word


class TestUnicodeNormalization:
    @pytest.mark.parametrize("word", [
        "inglés", "huracán", "alemán", "lápiz", "canción",
        "examen", "joven", "rubí", "capitán",
    ])
    def test_nfd_pluralize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = pluralize(word, lang="es")
        nfd_result = pluralize(nfd, lang="es")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "ingleses", "huracanes", "alemanes", "lápices", "canciones",
        "exámenes", "jóvenes", "rubíes", "capitanes",
    ])
    def test_nfd_singularize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = singularize(word, lang="es")
        nfd_result = singularize(nfd, lang="es")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "inglés", "huracán", "examen", "joven",
    ])
    def test_nfd_is_singular(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_singular(nfd, lang="es") == is_singular(word, lang="es")

    @pytest.mark.parametrize("word", [
        "ingleses", "huracanes", "exámenes", "jóvenes",
    ])
    def test_nfd_is_plural(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_plural(nfd, lang="es") == is_plural(word, lang="es")


class TestIesSingularization:
    @pytest.mark.parametrize("plural,singular", [
        ("dies", "die"), ("lies", "lie"), ("vies", "vie"),
        ("cities", "city"), ("flies", "fly"), ("supplies", "supply"),
        ("replies", "reply"), ("babies", "baby"), ("ladies", "lady"),
        ("stories", "story"), ("bodies", "body"), ("copies", "copy"),
        ("pennies", "penny"), ("parties", "party"), ("queries", "query"),
        ("burglaries", "burglary"), ("skies", "sky"),
    ])
    def test_ies_singularize(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular


class TestUncountableNonNouns:
    @pytest.mark.parametrize("word", [
        "is", "this", "was", "has", "us", "as", "thus",
    ])
    def test_non_noun_singularize(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "is", "this", "was", "has", "us", "as", "thus",
    ])
    def test_non_noun_pluralize(self, word: str) -> None:
        assert pluralize(word) == word


class TestNewIrregulars:
    @pytest.mark.parametrize("singular,plural", [
        ("soliloquy", "soliloquies"),
        ("gulf", "gulfs"),
        ("reef", "reefs"),
    ])
    def test_new_en_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    def test_es_leones_accent(self) -> None:
        assert singularize("leones", lang="es") == "león"
        assert pluralize("león", lang="es") == "leones"


class TestSesZesSingularization:
    @pytest.mark.parametrize("plural,singular", [
        ("houses", "house"), ("horses", "horse"), ("noses", "nose"),
        ("cases", "case"), ("phases", "phase"), ("vases", "vase"),
        ("roses", "rose"), ("tenses", "tense"), ("senses", "sense"),
        ("licenses", "license"), ("promises", "promise"),
        ("surprises", "surprise"), ("teases", "tease"),
        ("pleases", "please"), ("releases", "release"),
        ("decreases", "decrease"), ("increases", "increase"),
        ("diseases", "disease"), ("cruises", "cruise"),
        ("abuses", "abuse"), ("excuses", "excuse"),
        ("uses", "use"), ("fuses", "fuse"), ("muses", "muse"),
        ("causes", "cause"), ("pauses", "pause"),
        ("glimpses", "glimpse"),
    ])
    def test_ses_singularize(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("fizzes", "fizz"), ("buzzes", "buzz"), ("fuzzes", "fuzz"),
    ])
    def test_zzes_singularize(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular


class TestSsUsIrregulars:
    @pytest.mark.parametrize("singular,plural", [
        ("class", "classes"), ("kiss", "kisses"), ("mass", "masses"),
        ("press", "presses"), ("moss", "mosses"), ("toss", "tosses"),
        ("stress", "stresses"), ("address", "addresses"),
        ("access", "accesses"), ("process", "processes"),
        ("success", "successes"),
    ])
    def test_ss_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert singularize(singular) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("discus", "discuses"), ("census", "censuses"),
        ("plexus", "plexuses"), ("sinus", "sinuses"),
        ("thermos", "thermoses"), ("abacus", "abaci"),
        ("corpus", "corpora"), ("genus", "genera"), ("opus", "opera"),
    ])
    def test_us_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert singularize(singular) == singular


class TestEsNewFixes:
    def test_zigzag_uncountable(self) -> None:
        assert pluralize("zigzag", lang="es") == "zigzag"
        assert singularize("zigzag", lang="es") == "zigzag"

    def test_himenes_accent(self) -> None:
        assert pluralize("himen", lang="es") == "hímenes"
        assert singularize("hímenes", lang="es") == "himen"

    @pytest.mark.parametrize("singular,plural", [
        ("dios", "dioses"), ("tos", "toses"),
        ("gas", "gases"), ("bus", "buses"), ("vals", "valses"),
    ])
    def test_es_s_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular
        assert pluralize(plural, lang="es") == plural


class TestEnSEndingIrregulars:
    @pytest.mark.parametrize("singular,plural", [
        ("atlas", "atlases"), ("canvas", "canvases"), ("bias", "biases"),
        ("bonus", "bonuses"), ("campus", "campuses"),
        ("chorus", "choruses"), ("circus", "circuses"),
        ("consensus", "consensuses"), ("crocus", "crocuses"),
        ("octopus", "octopuses"), ("pelvis", "pelvises"),
        ("rebus", "rebuses"), ("trellis", "trellises"),
        ("platypus", "platypuses"), ("minibus", "minibuses"),
        ("omnibus", "omnibuses"),
    ])
    def test_s_ending_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural


class TestEnCrossCheckFixes:
    @pytest.mark.parametrize("singular,plural", [
        # -is -> -es (Greek)
        ("ellipsis", "ellipses"), ("neurosis", "neuroses"),
        ("synopsis", "synopses"), ("emphasis", "emphases"),
        ("paralysis", "paralyses"),
        # Latin/Greek irregulars
        ("louse", "lice"), ("agendum", "agenda"),
        ("erratum", "errata"), ("ovum", "ova"),
        ("helix", "helices"), ("codex", "codices"),
        ("radix", "radices"), ("cortex", "cortices"),
        ("vortex", "vortices"), ("apex", "apices"),
    ])
    def test_is_and_latin_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural

    @pytest.mark.parametrize("word,expected", [
        ("cuff", "cuffs"), ("stuff", "stuffs"), ("bluff", "bluffs"),
        ("fluff", "fluffs"), ("chuff", "chuffs"), ("puff", "puffs"),
        ("quaff", "quaffs"), ("duff", "duffs"), ("muff", "muffs"),
        ("scoff", "scoffs"), ("snuff", "snuffs"), ("scurf", "scurfs"),
        ("whiff", "whiffs"), ("skiff", "skiffs"), ("stiff", "stiffs"),
        ("gruff", "gruffs"), ("scruff", "scruffs"),
    ])
    def test_ff_words(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected
        assert singularize(expected) == word

    @pytest.mark.parametrize("word", [
        "tuberculosis", "psoriasis", "rabies", "mumps",
    ])
    def test_disease_uncountables(self, word: str) -> None:
        assert pluralize(word) == word
        assert singularize(word) == word

    @pytest.mark.parametrize("singular,plural", [
        ("history", "histories"), ("biology", "biologies"),
    ])
    def test_history_biology_countable(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("diff", "diffs"), ("cache", "caches"),
        ("niche", "niches"), ("machete", "machetes"),
    ])
    def test_tech_word_fixes(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural


class TestEsTechLoanwords:
    @pytest.mark.parametrize("singular,plural", [
        ("framework", "frameworks"), ("endpoint", "endpoints"),
        ("callback", "callbacks"), ("middleware", "middlewares"),
        ("hash", "hashes"), ("url", "urls"), ("widget", "widgets"),
        ("bucket", "buckets"), ("pipeline", "pipelines"),
        ("build", "builds"), ("ticket", "tickets"), ("socket", "sockets"),
        ("fixture", "fixtures"), ("mock", "mocks"), ("diff", "diffs"),
        ("commit", "commits"), ("caché", "cachés"),
    ])
    def test_es_tech_loanwords(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular
        assert pluralize(plural, lang="es") == plural


class TestEnSingularProtection:
    @pytest.mark.parametrize("word", [
        "status", "virus", "campus", "corpus", "genus",
        "opus", "radius", "focus", "fungus", "census",
        "apparatus", "status", "plexus", "sinus", "consensus",
    ])
    def test_us_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "analysis", "crisis", "thesis", "basis", "oasis",
        "parenthesis", "ellipsis", "neurosis", "synopsis",
        "emphasis", "paralysis", "diagnosis", "prognosis",
    ])
    def test_is_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "darkness", "happiness", "kindness", "weakness",
        "fitness", "illness", "sadness", "madness",
        "awareness", "carelessness", "thoughtlessness",
    ])
    def test_ness_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word


class TestEnOesSingularRule:
    @pytest.mark.parametrize("singular,plural", [
        ("ado", "adoes"), ("tango", "tangoes"),
        ("cargo", "cargoes"), ("judo", "judoes"), ("motto", "mottoes"),
        ("bravado", "bravadoes"),
        ("fresco", "frescoes"),
    ])
    def test_oes_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnFvesRoundTrip:
    @pytest.mark.parametrize("singular,plural", [
        ("behalf", "behalves"), ("wharf", "wharves"), ("scarf", "scarves"),
        ("wolf", "wolves"), ("half", "halves"), ("elf", "elves"),
        ("shelf", "shelves"), ("self", "selves"),
    ])
    def test_fves_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEsCrossCheckFixes:
    @pytest.mark.parametrize("singular,plural", [
        ("país", "países"), ("revés", "reveses"),
        ("bistec", "bisteces"), ("coñac", "coñaces"),
    ])
    def test_es_irregular_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular

    @pytest.mark.parametrize("word", [
        "prótesis", "diagnosis", "crisis", "tesis",
        "síntesis", "paréntesis",
    ])
    def test_es_invariable(self, word: str) -> None:
        assert pluralize(word, lang="es") == word
        assert singularize(word, lang="es") == word

    @pytest.mark.parametrize("singular,plural", [
        ("espermatozoide", "espermatozoides"),
        ("asteroide", "asteroides"),
        ("androide", "androides"),
    ])
    def test_es_oide_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular


class TestEnCheRegexRule:
    """Words ending in vowel+che handled by the ([aeiou])ches$ regex rule."""

    @pytest.mark.parametrize("singular,plural", [
        ("ache", "aches"), ("cache", "caches"), ("niche", "niches"),
        ("cliche", "cliches"), ("quiche", "quiches"), ("panache", "panaches"),
        ("brioche", "brioches"), ("pastiche", "pastiches"),
        ("headache", "headaches"), ("earache", "earaches"),
        ("toothache", "toothaches"), ("backache", "backaches"),
        ("heartache", "heartaches"), ("stomachache", "stomachaches"),
        ("douche", "douches"), ("gouache", "gouaches"),
        ("cloche", "cloches"), ("barouche", "barouches"),
        ("cartouche", "cartouches"), ("caliche", "caliches"),
        ("huarache", "huaraches"), ("seiche", "seiches"),
        ("troche", "troches"), ("microfiche", "microfiches"),
        ("attache", "attaches"), ("synecdoche", "synecdoches"),
    ])
    def test_che_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    @pytest.mark.parametrize("word", [
        "matches", "catches", "hatches", "patches", "batches",
        "latches", "witches", "switches", "ditches",
    ])
    def test_ch_words_not_broken(self, word: str) -> None:
        assert singularize(word) == word[:-2]

    @pytest.mark.parametrize("word", ["riches", "breeches", "britches"])
    def test_plural_only_uncountable(self, word: str) -> None:
        assert singularize(word) == word
        assert pluralize(word) == word


class TestEnIeIrregulars:
    """Words ending in -ie that need irregular entries for correct singularization."""

    @pytest.mark.parametrize("singular,plural", [
        ("brownie", "brownies"), ("calorie", "calories"),
        ("cookie", "cookies"), ("movie", "movies"),
        ("auntie", "aunties"), ("aussie", "aussies"),
        ("beanie", "beanies"), ("birdie", "birdies"),
        ("collie", "collies"), ("groupie", "groupies"),
        ("hippie", "hippies"), ("indie", "indies"),
        ("junkie", "junkies"), ("lassie", "lassies"),
        ("newbie", "newbies"), ("pixie", "pixies"),
        ("pinkie", "pinkies"), ("smoothie", "smoothies"),
        ("sweetie", "sweeties"), ("townie", "townies"),
    ])
    def test_ie_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnCompoundFves:
    """Compound f→ves words handled by singularization regex rules.

    Base words (life, wife, knife, wolf, etc.) are in irregulars.
    Compounds are handled by dedicated regex rules like
    ``(.+)([^aeiou])lives$`` → ``\\1\\2life``.
    """

    @pytest.mark.parametrize("singular,plural", [
        ("afterlife", "afterlives"), ("halflife", "halflives"),
        ("nightlife", "nightlives"), ("housewife", "housewives"),
        ("midwife", "midwives"), ("bookshelf", "bookshelves"),
        ("headscarf", "headscarves"), ("aardwolf", "aardwolves"),
        ("lonewolf", "lonewolves"), ("bowieknife", "bowieknives"),
        ("pocketknife", "pocketknives"), ("jackknife", "jackknives"),
        ("betterhalf", "betterhalves"), ("boxcalf", "boxcalves"),
        ("businesslife", "businesslives"), ("eternallife", "eternallives"),
        ("reallife", "reallives"), ("wildlife", "wildlives"),
        ("werewolf", "werewolves"), ("redwolf", "redwolves"),
        ("timberwolf", "timberwolves"), ("steakknife", "steakknives"),
        ("drawknife", "drawknives"), ("penknife", "penknives"),
        ("firsthalf", "firsthalves"), ("secondhalf", "secondhalves"),
        ("continentalshelf", "continentalshelves"),
        ("goldencalf", "goldencalves"),
        ("manandwife", "manandwives"), ("oldwife", "oldwives"),
    ])
    def test_compound_fves_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnCompoundFexceptions:
    """Compound f-exception words that just add ``s`` (not ``ves``).

    Base words (dwarf, golf, gulf, turf, strife) are in irregulars.
    Compounds are handled by the plural exception regex rule
    ``(.+)(dwarf|golf|gulf|turf|strife)$`` → ``\\1\\2s``.
    """

    @pytest.mark.parametrize("singular,plural", [
        ("reddwarf", "reddwarfs"), ("whitedwarf", "whitedwarfs"),
        ("yellowdwarf", "yellowdwarfs"), ("truedwarf", "truedwarfs"),
        ("miniaturegolf", "miniaturegolfs"),
        ("professionalgolf", "professionalgolfs"),
        ("arabiangulf", "arabiangulfs"), ("persiangulf", "persiangulfs"),
        ("lilyturf", "lilyturfs"),
        ("loosestrife", "loosestrifes"),
        ("purpleloosestrife", "purpleloosestrifes"),
        ("spikedloosestrife", "spikedloosestrifes"),
    ])
    def test_compound_fexception_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnFexceptionIrregulars:
    """Base f-exception words that just add ``s`` (not ``ves``)."""

    @pytest.mark.parametrize("singular,plural", [
        ("serf", "serfs"), ("surf", "surfs"), ("zarf", "zarfs"),
        ("strife", "strifes"), ("fife", "fifes"),
    ])
    def test_fexception_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnVowelLifeCompounds:
    """vowel + life compounds not caught by ``[^aeiou]lives$`` rule.

    These need irregular entries because the consonant guard
    prevents the regex from matching.
    """

    @pytest.mark.parametrize("singular,plural", [
        ("lovelife", "lovelives"), ("righttolife", "righttolives"),
    ])
    def test_vowel_life_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnLivesRuleGuard:
    """The ``([^aeiou])lives$`` guard prevents false positives."""

    @pytest.mark.parametrize("singular,plural", [
        ("olive", "olives"), ("clive", "clives"),
        ("baronclive", "baronclives"), ("robertclive", "robertclives"),
    ])
    def test_olive_not_broken(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular


class TestEnSsSingularization:
    """Words ending in -ss should not lose an s when singularized."""

    @pytest.mark.parametrize("word", [
        "glass", "dress", "loss", "miss", "pass", "fuss",
        "class", "kiss", "press", "moss", "toss", "stress",
        "boss", "cross", "floss", "gross",
    ])
    def test_ss_singular_is_self(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word,expected", [
        ("dresses", "dress"), ("losses", "loss"),
        ("classes", "class"), ("kisses", "kiss"), ("presses", "press"),
        ("bosses", "boss"), ("crosses", "cross"),
    ])
    def test_ss_plural_singularizes(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestEnNewIrregulars:
    """Tests for newly added irregular plurals."""

    @pytest.mark.parametrize("singular,plural", [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize("singular,plural", [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural


class TestEnGlassCountable:
    """glass is now countable (a drinking glass), not uncountable."""

    def test_pluralize_glass(self) -> None:
        assert pluralize("glass") == "glasses"

    def test_glass_not_uncountable(self) -> None:
        assert is_singular("glass") is True
        assert is_plural("glass") is False

    def test_glasses_still_uncountable(self) -> None:
        """'glasses' (eyeglasses) remains uncountable."""
        assert singularize("glasses") == "glasses"
        assert pluralize("glasses") == "glasses"


class TestEsHipotesisUncountable:
    """hipótesis should be uncountable in Spanish."""

    def test_pluralize_unchanged(self) -> None:
        assert pluralize("hipótesis", lang="es") == "hipótesis"

    def test_singularize_unchanged(self) -> None:
        assert singularize("hipótesis", lang="es") == "hipótesis"

    def test_is_singular(self) -> None:
        assert is_singular("hipótesis", lang="es") is True

    def test_is_plural(self) -> None:
        assert is_plural("hipótesis", lang="es") is True


class TestEnChSingularization:
    """Words ending in -ch (not -che) must singularize correctly.

    The old ([aeiou])ches$ rule broke words like beach, teach, coach
    by returning beache, teache, coache. Now they use the standard
    (ss|sh|ch|x|zz)es$ rule.
    """

    @pytest.mark.parametrize("word", [
        "beach", "peach", "reach", "teach", "preach", "bleach",
        "coach", "approach", "broach", "encroach", "crouch",
        "lunch", "crunch", "bunch", "punch", "hunch",
        "branch", "ranch", "starch", "march", "torch", "porch",
    ])
    def test_ch_roundtrip(self, word: str) -> None:
        plural = pluralize(word)
        assert singularize(plural) == word

    @pytest.mark.parametrize("word,expected", [
        ("beaches", "beach"), ("peaches", "peach"), ("reaches", "reach"),
        ("teaches", "teach"), ("coaches", "coach"), ("approaches", "approach"),
        ("lunches", "lunch"), ("branches", "branch"), ("torches", "torch"),
    ])
    def test_ch_plural_singularizes(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    @pytest.mark.parametrize("word", [
        "ache", "cache", "niche", "apache", "creche", "machete",
        "mustache", "moustache", "avalanche", "psyche", "demarche",
        "tranche", "thelarche",
    ])
    def test_che_roundtrip(self, word: str) -> None:
        plural = pluralize(word)
        assert singularize(plural) == word


class TestWhitespacePreservation:
    """Leading/trailing whitespace must be preserved in output."""

    @pytest.mark.parametrize("word,expected", [
        ("  cat  ", "  cats  "),
        (" cat", " cats"),
        ("cat ", "cats "),
        ("\tcat\t", "\tcats\t"),
    ])
    def test_pluralize_whitespace(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("  cats  ", "  cat  "),
        (" cats", " cat"),
        ("cats ", "cat "),
        ("\tcats\t", "\tcat\t"),
    ])
    def test_singularize_whitespace(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    def test_count_1_preserves_whitespace(self) -> None:
        assert pluralize("  cat  ", count=1) == "  cat  "
        assert pluralize(" cat ", count=1) == " cat "

    def test_irregular_preserves_whitespace(self) -> None:
        assert pluralize("  child  ") == "  children  "
        assert singularize("  children  ") == "  child  "

    def test_uncountable_preserves_whitespace(self) -> None:
        assert pluralize("  sheep  ") == "  sheep  "
        assert singularize("  sheep  ") == "  sheep  "


class TestEnHyphenatedPrefixes:
    """Hyphenated words with prefix first segments pluralize the last segment."""

    @pytest.mark.parametrize("singular,plural", [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("re-analysis", "re-analyses"),
        ("pre-screening", "pre-screenings"),
        ("anti-inflammatory", "anti-inflammatories"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
        ("non-intervention", "non-interventions"),
        ("sub-committee", "sub-committees"),
        ("inter-agency", "inter-agencies"),
    ])
    def test_prefix_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize("singular,plural", [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("re-analysis", "re-analyses"),
        ("pre-screening", "pre-screenings"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
    ])
    def test_prefix_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
    ])
    def test_prefix_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural


class TestEnDemonyms:
    """Demonyms ending in -ese are invariable (same singular and plural)."""

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "burmese", "lebanese",
        "portuguese", "javanese", "sundanese", "senegalese", "congolese",
        "sudanese", "maltese", "siamese",
    ])
    def test_demonym_pluralize_unchanged(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese", "lebanese",
    ])
    def test_demonym_singularize_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_demonym_is_singular(self, word: str) -> None:
        assert is_singular(word) is True

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_demonym_is_plural(self, word: str) -> None:
        assert is_plural(word) is True


class TestEnLatinGreekIrregulars:
    """Round-trip tests for Latin/Greek classical irregular plurals (Fase 1)."""

    @pytest.mark.parametrize("singular,plural", [
        ("desideratum", "desiderata"),
        ("maximum", "maxima"),
        ("millennium", "millennia"),
        ("anathema", "anathemata"),
        ("schema", "schemata"),
        ("alumna", "alumnae"),
        ("formula", "formulae"),
        ("nebula", "nebulae"),
        ("stamen", "stamina"),
        ("ephemeris", "ephemerides"),
        ("arthritis", "arthritides"),
        ("hepatitis", "hepatitides"),
        ("perihelion", "perihelia"),
        ("oxymoron", "oxymora"),
        ("murex", "murices"),
        ("latex", "latices"),
        ("goy", "goyim"),
        ("afrit", "afriti"),
        ("mythos", "mythoi"),
        ("beef", "beefs"),
        ("money", "monies"),
        ("numen", "numina"),
        ("carmen", "carmina"),
        ("genie", "genies"),
    ])
    def test_latin_greek_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    def test_graffito_pluralize_only(self) -> None:
        assert pluralize("graffito") == "graffiti"
        assert singularize("graffiti") == "graffiti"


class TestEnNewUncountables:
    """Uncountable words from Fase 2 — pluralize(x) == x and singularize(x) == x."""

    @pytest.mark.parametrize("word", [
        "bison", "buffalo", "caribou", "elk", "swine", "wildebeest", "eland",
        "cod", "flounder", "grouse", "haddock", "hake", "halibut", "herring",
        "mackerel", "pike", "roe", "shad", "snipe", "teal", "turbot",
        "bream", "carp", "dace", "pickerel",
        "graffiti", "djinn", "pence", "quid", "hertz", "chassis", "corps",
        "debris", "siemens", "contretemps", "mews", "haggis", "innings",
        "proceedings", "jackanapes", "zucchini", "quinoa",
        "amoyese", "borghese", "congoese", "faroese", "foochowese",
        "genevese", "genoese", "gilbertese", "hottentotese", "kiplingese",
        "kongoese", "lucchese", "nankingese", "niasese", "pekingese",
        "piedmontese", "pistoiese", "sarawakese", "shavese", "vermontese",
        "wenchowese", "yengeese",
        "blowfish", "angelfish", "jellyfish", "catfish", "swordfish",
        "goldfish", "starfish", "pufferfish", "sunfish", "bluefish",
        "blackfish", "codfish", "dogfish", "flatfish", "monkfish",
        "reeffish", "sawfish", "stonefish", "toadfish", "whitefish",
        "chickenpox", "smallpox", "cowpox", "foxpox", "gerbilpox",
        "monkeypox", "mousepox", "rabbitpox", "raccoonpox", "skunkpox",
    ])
    def test_uncountable_pluralize(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "bison", "buffalo", "caribou", "elk", "swine", "wildebeest", "eland",
        "cod", "flounder", "grouse", "haddock", "hake", "halibut", "herring",
        "mackerel", "pike", "roe", "shad", "snipe", "teal", "turbot",
        "bream", "carp", "dace", "pickerel",
        "graffiti", "djinn", "pence", "quid", "hertz", "chassis", "corps",
        "debris", "siemens", "contretemps", "mews", "haggis", "innings",
        "proceedings", "jackanapes", "zucchini", "quinoa",
        "amoyese", "borghese", "congoese", "faroese", "foochowese",
        "genevese", "genoese", "gilbertese", "hottentotese", "kiplingese",
        "kongoese", "lucchese", "nankingese", "niasese", "pekingese",
        "piedmontese", "pistoiese", "sarawakese", "shavese", "vermontese",
        "wenchowese", "yengeese",
        "blowfish", "angelfish", "jellyfish", "catfish", "swordfish",
        "goldfish", "starfish", "pufferfish", "sunfish", "bluefish",
        "blackfish", "codfish", "dogfish", "flatfish", "monkfish",
        "reeffish", "sawfish", "stonefish", "toadfish", "whitefish",
        "chickenpox", "smallpox", "cowpox", "foxpox", "gerbilpox",
        "monkeypox", "mousepox", "rabbitpox", "raccoonpox", "skunkpox",
    ])
    def test_uncountable_singularize(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "amoyese", "pekingese", "yengeese", "lucchese", "piedmontese",
        "blowfish", "catfish", "goldfish", "starfish", "swordfish",
        "chickenpox", "smallpox", "monkeypox", "mousepox", "skunkpox",
    ])
    def test_uncountable_is_singular_and_plural(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is True


class TestEnForeignOWords:
    """Fase 4: Foreign -o words that pluralize with -os (not -oes)."""

    @pytest.mark.parametrize("singular,plural", [
        # Animales
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("hippo", "hippos"), ("rhino", "rhinos"),
        # Instrumentos
        ("allegro", "allegros"), ("bolero", "boleros"),
        ("bongo", "bongos"), ("canto", "cantos"),
        ("falsetto", "falsettos"), ("intermezzo", "intermezzos"),
        ("rondo", "rondos"), ("staccato", "staccatos"),
        ("tremolo", "tremolos"), ("vibrato", "vibratos"),
        ("violoncello", "violoncellos"), ("timpano", "timpanos"),
        # Comida/bebida
        ("cappuccino", "cappuccinos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"),
        # Objetos
        ("archipelago", "archipelagos"), ("bingo", "bingos"),
        ("commando", "commandos"), ("ditto", "dittos"),
        ("fiasco", "fiascos"), ("gizmo", "gizmos"),
        ("hairdo", "hairdos"), ("manifesto", "manifestos"),
        ("stucco", "stuccos"), ("torso", "torsos"), ("ufo", "ufos"),
        # Otros
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize("singular,plural", [
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("cappuccino", "cappuccinos"), ("allegro", "allegros"),
        ("bolero", "boleros"), ("bongo", "bongos"),
        ("canto", "cantos"), ("falsetto", "falsettos"),
        ("intermezzo", "intermezzos"), ("rondo", "rondos"),
        ("staccato", "staccatos"), ("tremolo", "tremolos"),
        ("vibrato", "vibratos"), ("violoncello", "violoncellos"),
        ("timpano", "timpanos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"), ("hippo", "hippos"),
        ("rhino", "rhinos"), ("archipelago", "archipelagos"),
        ("bingo", "bingos"), ("commando", "commandos"),
        ("ditto", "dittos"), ("fiasco", "fiascos"),
        ("gizmo", "gizmos"), ("hairdo", "hairdos"),
        ("manifesto", "manifestos"), ("stucco", "stuccos"),
        ("torso", "torsos"), ("ufo", "ufos"),
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("cappuccino", "cappuccinos"), ("allegro", "allegros"),
        ("bolero", "boleros"), ("bongo", "bongos"),
        ("canto", "cantos"), ("falsetto", "falsettos"),
        ("intermezzo", "intermezzos"), ("rondo", "rondos"),
        ("staccato", "staccatos"), ("tremolo", "tremolos"),
        ("vibrato", "vibratos"), ("violoncello", "violoncellos"),
        ("timpano", "timpanos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"), ("hippo", "hippos"),
        ("rhino", "rhinos"), ("archipelago", "archipelagos"),
        ("bingo", "bingos"), ("commando", "commandos"),
        ("ditto", "dittos"), ("fiasco", "fiascos"),
        ("gizmo", "gizmos"), ("hairdo", "hairdos"),
        ("manifesto", "manifestos"), ("stucco", "stuccos"),
        ("torso", "torsos"), ("ufo", "ufos"),
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    def test_not_oes(self) -> None:
        assert pluralize("albino") != "albinoes"
        assert pluralize("armadillo") != "armadilloes"
        assert pluralize("cappuccino") != "cappuccinoes"


class TestEnFase3InverseSingularization:
    """Fase 3: explicit inverse singularization entries."""

    @pytest.mark.parametrize("plural,singular", [
        ("abuses", "abuse"), ("clauses", "clause"), ("excuses", "excuse"),
        ("fuses", "fuse"), ("uses", "use"), ("pauses", "pause"),
        ("spouses", "spouse"), ("reuses", "reuse"), ("misuses", "misuse"),
    ])
    def test_uses_to_use(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("aeries", "aerie"), ("belies", "belie"), ("bookies", "bookie"),
        ("cooties", "cootie"), ("freebies", "freebie"), ("goalies", "goalie"),
        ("lies", "lie"), ("magpies", "magpie"), ("neckties", "necktie"),
        ("oldies", "oldie"), ("prairies", "prairie"), ("rookies", "rookie"),
        ("sorties", "sortie"), ("vies", "vie"), ("zombies", "zombie"),
    ])
    def test_ies_to_ie_comunes(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("addies", "addie"), ("archies", "archie"), ("barbies", "barbie"),
        ("charlies", "charlie"), ("eddies", "eddie"), ("julies", "julie"),
        ("katies", "katie"), ("maggies", "maggie"), ("sophies", "sophie"),
        ("trekkies", "trekkie"), ("valkyries", "valkyrie"), ("yorkies", "yorkie"),
    ])
    def test_ies_to_ie_proper_nouns(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("antitheses", "antithesis"), ("catalyses", "catalysis"),
        ("diagnoses", "diagnosis"), ("geneses", "genesis"),
        ("metamorphoses", "metamorphosis"), ("mitoses", "mitosis"),
        ("nemeses", "nemesis"), ("prognoses", "prognosis"),
        ("psychoses", "psychosis"), ("syntheses", "synthesis"),
        ("taxes", "tax"), ("thromboses", "thrombosis"),
    ])
    def test_es_to_is(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("backhoes", "backhoe"), ("floes", "floe"),
        ("mistletoes", "mistletoe"), ("tiptoes", "tiptoe"),
        ("woes", "woe"),
    ])
    def test_oes_to_oe(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("plural,singular", [
        ("blanches", "blanche"), ("porsches", "porsche"),
        ("hesses", "hesse"), ("matisses", "matisse"),
        ("clives", "clive"), ("palmolives", "palmolive"),
        ("annexes", "annex"), ("pickaxes", "pickaxe"),
        ("buzzes", "buzz"), ("fizzes", "fizz"),
        ("bolshois", "bolshoi"), ("hanois", "hanoi"),
    ])
    def test_minor_subphases(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular


class TestEnProperNounCasePreservation:
    """Fase 5: Proper nouns ending in -ie with case preservation."""

    @pytest.mark.parametrize("word,expected", [
        ("Barbie", "Barbies"), ("Charlie", "Charlies"),
        ("BILLIE", "BILLIES"), ("barbie", "barbies"),
        ("charlie", "charlies"), ("Billie", "Billies"),
        ("Annie", "Annies"), ("ANNIE", "ANNIES"),
        ("Archie", "Archies"), ("artie", "arties"),
        ("ARTIE", "ARTIES"), ("Bessie", "Bessies"),
        ("BESSIE", "BESSIES"), ("bessie", "bessies"),
        ("Betty", "Betties"), ("BETTY", "BETTIES"),
        ("betty", "betties"), ("Bobbie", "Bobbies"),
        ("Connie", "Connies"), ("connie", "connies"),
        ("Curie", "Curies"), ("CURIE", "CURIES"),
        ("Debbie", "Debbies"), ("Eddie", "Eddies"),
        ("EDDIE", "EDDIES"), ("Ellie", "Ellies"),
        ("Frankie", "Frankies"), ("Gracie", "Gracies"),
        ("Jackie", "Jackies"), ("Jamie", "Jamies"),
        ("Julie", "Julies"), ("JULIE", "JULIES"),
        ("Katie", "Katies"), ("katie", "katies"),
        ("KATIE", "KATIES"), ("Leslie", "Leslies"),
        ("Maggie", "Maggies"), ("Millie", "Millies"),
        ("Nellie", "Nellies"), ("nellie", "nellies"),
        ("NELLIE", "NELLIES"), ("Ollie", "Ollies"),
        ("Reggie", "Reggies"), ("Richie", "Richies"),
        ("Rosie", "Rosies"), ("Sadie", "Sadies"),
        ("sophie", "sophies"), ("Sophie", "Sophies"),
        ("SOPHIE", "SOPHIES"), ("Susie", "Susies"),
        ("Tommie", "Tommies"), ("Willie", "Willies"),
        ("Winnie", "Winnies"), ("Yorkie", "Yorkies"),
        ("yorkie", "yorkies"), ("YORKIE", "YORKIES"),
        ("Sherry", "Sherries"), ("sherry", "sherries"),
        ("SHERRY", "SHERRIES"),
    ])
    def test_proper_noun_pluralize_case(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("Barbies", "Barbie"), ("Charlies", "Charlie"),
        ("BILLIES", "BILLIE"), ("barbies", "barbie"),
        ("charlies", "charlie"), ("Billies", "Billie"),
        ("Annies", "Annie"), ("ANNIES", "ANNIE"),
        ("Archies", "Archie"), ("Bessies", "Bessie"),
        ("BESSIES", "BESSIE"), ("bessies", "bessie"),
        ("Betties", "Betty"), ("BETTIES", "BETTY"),
        ("betties", "betty"), ("Bobbies", "Bobbie"),
        ("Connies", "Connie"), ("Curies", "Curie"),
        ("CURIES", "CURIE"), ("Debbies", "Debbie"),
        ("Eddies", "Eddie"), ("EDDIES", "EDDIE"),
        ("Ellies", "Ellie"), ("Frankies", "Frankie"),
        ("Gracies", "Gracie"), ("Jackies", "Jackie"),
        ("Jamies", "Jamie"), ("Julies", "Julie"),
        ("JULIES", "JULIE"), ("Katies", "Katie"),
        ("katies", "katie"), ("KATIES", "KATIE"),
        ("Leslies", "Leslie"), ("Maggies", "Maggie"),
        ("Millies", "Millie"), ("Nellies", "Nellie"),
        ("nellies", "nellie"), ("NELLIES", "NELLIE"),
        ("Ollies", "Ollie"), ("Reggies", "Reggie"),
        ("Richies", "Richie"), ("Rosies", "Rosie"),
        ("Sadies", "Sadie"), ("sophies", "sophie"),
        ("Sophies", "Sophie"), ("SOPHIES", "SOPHIE"),
        ("Susies", "Susie"), ("Tommies", "Tommie"),
        ("Willies", "Willie"), ("Winnies", "Winnie"),
        ("Yorkies", "Yorkie"), ("yorkies", "yorkie"),
        ("YORKIES", "YORKIE"), ("Sherries", "Sherry"),
        ("sherries", "sherry"), ("SHERRIES", "SHERRY"),
    ])
    def test_proper_noun_singularize_case(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    @pytest.mark.parametrize("singular,plural", [
        ("Barbie", "Barbies"), ("Charlie", "Charlies"),
        ("Billie", "Billies"), ("Annie", "Annies"),
        ("Bessie", "Bessies"), ("Betty", "Betties"),
        ("Curie", "Curies"), ("Eddie", "Eddies"),
        ("Julie", "Julies"), ("Katie", "Katies"),
        ("Maggie", "Maggies"), ("Nellie", "Nellies"),
        ("Reggie", "Reggies"), ("Sophie", "Sophies"),
        ("Willie", "Willies"), ("Yorkie", "Yorkies"),
        ("Sherry", "Sherries"), ("Bobbie", "Bobbies"),
        ("Connie", "Connies"), ("Gracie", "Gracies"),
    ])
    def test_proper_noun_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural


class TestEnSingularSComplete:
    """Fase 6: Singular words ending in -s that need +es pluralization."""

    @pytest.mark.parametrize("singular,plural", [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize("singular,plural", [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize("singular,plural", [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    @pytest.mark.parametrize("plural", [
        "acropolises", "aegises", "aliases", "asbestoses", "bathoses",
        "caddises", "cannabises", "cosmoses", "daises", "digitalises",
        "epidermises", "ethoses", "eyases", "glottises", "hubrises",
        "ibises", "mantises", "marquises", "metropolises", "pathoses",
        "polises", "sassafrases",
    ])
    def test_singular_s_already_plural(self, plural: str) -> None:
        assert pluralize(plural) == plural


class TestEnAnnexRoundTrip:
    """annex should round-trip correctly (American English)."""

    def test_pluralize_annex(self) -> None:
        assert pluralize("annex") == "annexes"

    def test_singularize_annexes(self) -> None:
        assert singularize("annexes") == "annex"

    def test_round_trip(self) -> None:
        assert singularize(pluralize("annex")) == "annex"


class TestEsPeineRoundTrip:
    """peine should round-trip correctly (vowel+consonant+e pattern)."""

    def test_pluralize_peine(self) -> None:
        assert pluralize("peine", lang="es") == "peines"

    def test_singularize_peines(self) -> None:
        assert singularize("peines", lang="es") == "peine"

    def test_round_trip(self) -> None:
        assert singularize(pluralize("peine", lang="es"), lang="es") == "peine"


class TestEnFinesseBellyache:
    """finesse and bellyache should round-trip correctly."""

    def test_finesse(self) -> None:
        assert pluralize("finesse") == "finesses"
        assert singularize("finesses") == "finesse"

    def test_bellyache(self) -> None:
        assert pluralize("bellyache") == "bellyaches"
        assert singularize("bellyaches") == "bellyache"


class TestEsGrisRolCompounds:
    """gris (invariable), rol round-trip, compound uncountables."""

    def test_gris_uncountable(self) -> None:
        assert pluralize("gris", lang="es") == "gris"
        assert singularize("gris", lang="es") == "gris"

    def test_rol_round_trip(self) -> None:
        assert pluralize("rol", lang="es") == "roles"
        assert singularize("roles", lang="es") == "rol"

    @pytest.mark.parametrize("word", [
        "quitamanchas", "matasanos", "guardabosques", "guardacostas",
    ])
    def test_compound_uncountable(self, word: str) -> None:
        assert pluralize(word, lang="es") == word
        assert singularize(word, lang="es") == word


class TestPtCasePreservation:
    """Portuguese case preservation for irregulars and regex words."""

    @pytest.mark.parametrize("word,expected", [
        ("Coração", "Corações"),
        ("CORAÇÃO", "CORAÇÕES"),
        ("Papel", "Papéis"),
        ("PAPEL", "PAPÉIS"),
        ("Cão", "Cães"),
        ("CÃO", "CÃES"),
        ("Cidadão", "Cidadãos"),
        ("CIDADÃO", "CIDADÃOS"),
        ("Framework", "Frameworks"),
        ("FRAMEWORK", "FRAMEWORKS"),
        ("Bem", "Bens"),
        ("BEM", "BENS"),
    ])
    def test_pt_title_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="pt") == expected

    @pytest.mark.parametrize("word,expected", [
        ("Corações", "Coração"),
        ("CORAÇÕES", "CORAÇÃO"),
        ("Papéis", "Papel"),
        ("PAPÉIS", "PAPEL"),
        ("Cães", "Cão"),
        ("CÃES", "CÃO"),
        ("Cidadãos", "Cidadão"),
        ("CIDADÃOS", "CIDADÃO"),
    ])
    def test_pt_title_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="pt") == expected


class TestPtMixedCase:
    """Portuguese mixed case preservation."""

    @pytest.mark.parametrize("word,expected", [
        ("iPhone", "iPhones"),
    ])
    def test_pt_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="pt") == expected

    @pytest.mark.parametrize("word,expected", [
        ("iPhones", "iPhone"),
    ])
    def test_pt_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="pt") == expected


class TestPtHyphenatedWords:
    """Portuguese hyphenated word pluralization."""

    @pytest.mark.parametrize("singular,plural", [
        ("café-bar", "cafés-bar"),
        ("coração-de-leão", "corações-de-leão"),
        ("papel-moeda", "papéis-moeda"),
    ])
    def test_pt_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="pt") == plural

    @pytest.mark.parametrize("singular,plural", [
        ("café-bar", "cafés-bar"),
        ("coração-de-leão", "corações-de-leão"),
        ("papel-moeda", "papéis-moeda"),
    ])
    def test_pt_hyphenated_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural, lang="pt") == singular

    def test_pt_hyphenated_roundtrip(self) -> None:
        for word in ["café-bar", "coração-de-leão", "papel-moeda"]:
            assert singularize(pluralize(word, lang="pt"), lang="pt") == word

    def test_pt_verb_noun_compound_pluralize(self) -> None:
        for singular, plural in [
            ("quebra-cabeça", "quebra-cabeças"),
            ("guarda-chuva", "guarda-chuvas"),
            ("guarda-roupa", "guarda-roupas"),
            ("beija-flor", "beija-flores"),
            ("passa-tempo", "passa-tempos"),
            ("arranha-céu", "arranha-céus"),
            ("limpa-pára-brisa", "limpa-pára-brisas"),
            ("corta-caminho", "corta-caminhos"),
        ]:
            assert pluralize(singular, lang="pt") == plural

    def test_pt_verb_noun_compound_singularize(self) -> None:
        for singular, plural in [
            ("quebra-cabeça", "quebra-cabeças"),
            ("guarda-chuva", "guarda-chuvas"),
            ("guarda-roupa", "guarda-roupas"),
            ("beija-flor", "beija-flores"),
            ("passa-tempo", "passa-tempos"),
            ("arranha-céu", "arranha-céus"),
        ]:
            assert singularize(plural, lang="pt") == singular

    def test_pt_verb_noun_compound_roundtrip(self) -> None:
        for word in ["quebra-cabeça", "guarda-chuva", "guarda-roupa",
                      "beija-flor", "passa-tempo", "arranha-céu"]:
            assert singularize(pluralize(word, lang="pt"), lang="pt") == word

    def test_pt_leading_hyphen_pluralize(self) -> None:
        assert pluralize("-casa", lang="pt") == "-casas"

    def test_pt_leading_hyphen_singularize(self) -> None:
        assert singularize("-casas", lang="pt") == "-casa"

    def test_pt_hyphen_only(self) -> None:
        assert pluralize("-", lang="pt") == "-"
        assert singularize("-", lang="pt") == "-"

    def test_pt_double_hyphen(self) -> None:
        assert pluralize("--", lang="pt") == "--"
        assert singularize("--", lang="pt") == "--"


class TestPtIdempotency:
    """Portuguese pluralize of already-plural words should return unchanged."""

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "feijões", "limões", "leões",
        "botões", "estações", "nações", "relações", "funções",
        "criações", "emoções", "regiões", "questões", "lições",
        "intenções", "atenções", "conclusões", "decisões",
        "cães", "alemães", "capitães", "charlatães", "pães",
        "irmãos", "mãos", "chãos", "cristãos", "cidadãos", "órgãos",
        "papéis", "níveis", "anéis", "pincéis", "painéis", "pastéis",
        "sóis", "faróis", "anzóis", "caracóis", "lençóis",
        "gases", "países", "deuses", "portugueses", "japoneses",
        "ingleses", "franceses", "chineses",
        "meses", "leis", "reis", "pais",
        "frameworks", "endpoints", "callbacks", "middlewares",
        "hashes", "urls", "widgets", "buckets", "pipelines",
        "builds", "tickets", "sockets", "fixtures", "mocks", "diffs",
        "commits", "drivers", "buffers", "proxies", "headers",
        "branches", "forks", "pushes", "pulls", "tags",
        "logs", "bugs", "patches", "releases", "deploys",
        "backups", "snapshots", "dashboards", "plugins", "addons",
        "templates", "themes", "layouts", "forms", "inputs", "outputs",
        "flags", "switches", "toggles", "hooks", "triggers",
        "handlers", "listeners", "observers", "wrappers", "adapters",
        "parsers", "compilers", "debuggers", "runners", "workers",
        "nodes", "hosts", "peers", "clients", "brokers",
        "pods", "volumes", "images", "registries", "charts", "graphs",
        "tests", "suites", "cases", "stubs", "spies",
        "alerts", "events", "messages", "webhooks", "payloads",
        "requests", "responses", "sessions", "cookies",
        "queries", "cursors", "fields", "schemas", "migrations",
        "jobs", "tasks", "queues", "stacks", "heaps", "pools", "caches",
        "streams", "pipes", "ports", "channels", "signals", "beacons",
        "sensors", "devices", "badges", "cards", "menus", "tabs", "icons",
        "buttons", "labels", "filters", "sorts", "blocks", "sections",
        "items", "elements", "posts", "comments",
        "users", "accounts", "profiles", "roles", "groups", "teams",
        "projects", "issues", "plans", "tiers", "quotas", "limits",
        "invoices", "payments", "charges", "refunds",
        "licenses", "subscriptions", "monitors", "scanners",
        "managers", "browsers", "printers", "computers",
        "senders", "receivers", "editors", "visitors",
        "sponsors", "partners", "providers", "suppliers",
        "investors", "founders", "developers",
    ])
    def test_pt_pluralize_already_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word


class TestPtRoundTrip:
    """Portuguese pluralize → singularize round-trip identity."""

    @pytest.mark.parametrize("word", [
        "casa", "livro", "gato", "coração", "canção", "balão",
        "feijão", "limão", "leão", "botão", "estação", "nação",
        "cão", "alemão", "capitão", "charlatão", "pão",
        "irmão", "mão", "chão", "cidadão", "órgão",
        "papel", "nível", "mel", "fiel", "anel", "pincel",
        "sol", "farol", "anzol", "caracol", "lençol",
        "barril", "funil", "fuzil",
        "projétil", "fóssil", "míssil", "fácil", "réptil",
        "gás", "país", "deus", "português", "japonês",
        "inglês", "francês", "holandês", "chinês",
        "mês", "lei", "rei", "pai",
        "bem", "som", "flor", "cor", "mar", "paz", "luz",
        "framework", "endpoint", "callback", "middleware",
        "hash", "url", "widget", "bucket", "pipeline",
        "build", "ticket", "socket", "fixture", "mock", "diff",
        "commit", "driver", "buffer", "proxy", "header",
        "branch", "fork", "push", "pull", "tag",
        "log", "bug", "patch", "release", "deploy",
        "backup", "snapshot", "dashboard", "plugin", "addon",
        "template", "theme", "layout", "form", "input", "output",
        "flag", "switch", "toggle", "hook", "trigger",
        "handler", "listener", "observer", "wrapper", "adapter",
        "parser", "compiler", "debugger", "runner", "worker",
        "node", "host", "peer", "client", "broker",
        "pod", "volume", "image", "registry", "chart", "graph",
        "test", "suite", "case", "stub", "spy",
        "alert", "event", "message", "webhook", "payload",
        "request", "response", "session", "cookie",
        "query", "cursor", "field", "schema", "migration",
        "job", "task", "queue", "stack", "heap", "pool", "cache",
        "stream", "pipe", "port", "channel", "signal", "beacon",
        "sensor", "device", "badge", "card", "menu", "tab", "icon",
        "button", "label", "filter", "sort", "block", "section",
        "item", "element", "post", "comment",
        "user", "account", "profile", "role", "group", "team",
        "project", "issue", "plan", "tier", "quota", "limit",
        "invoice", "payment", "charge", "refund",
        "license", "subscription", "monitor", "scanner",
        "manager", "browser", "printer", "computer",
        "sender", "receiver", "editor", "visitor",
        "sponsor", "partner", "provider", "supplier",
        "investor", "founder", "developer",
    ])
    def test_pt_roundtrip(self, word: str) -> None:
        plural = pluralize(word, lang="pt")
        assert singularize(plural, lang="pt") == word


class TestPtUnicodeNormalization:
    """Portuguese NFD input should produce same result as NFC."""

    @pytest.mark.parametrize("word", [
        "coração", "canção", "balão", "leão", "estação",
        "cão", "alemão", "capitão", "pão",
        "papel", "nível", "mel", "fiel",
        "sol", "farol", "anzol", "lençol",
        "gás", "país", "português", "japonês",
        "mês", "árvore",
    ])
    def test_pt_nfd_pluralize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = pluralize(word, lang="pt")
        nfd_result = pluralize(nfd, lang="pt")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "leões", "estações",
        "cães", "alemães", "capitães", "pães",
        "papéis", "níveis", "fiéis",
        "sóis", "faróis", "anzóis", "lençóis",
        "gases", "países", "portugueses", "japoneses",
        "meses", "árvores",
    ])
    def test_pt_nfd_singularize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = singularize(word, lang="pt")
        nfd_result = singularize(nfd, lang="pt")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "gás", "português",
    ])
    def test_pt_nfd_is_singular(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_singular(nfd, lang="pt") == is_singular(word, lang="pt")

    @pytest.mark.parametrize("word", [
        "corações", "papéis", "cães", "gases", "portugueses",
    ])
    def test_pt_nfd_is_plural(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_plural(nfd, lang="pt") == is_plural(word, lang="pt")


class TestPtIsSingularIsPlural:
    """Portuguese is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "coração", "canção", "balão", "leão", "estação",
        "cão", "alemão", "capitão", "pão",
        "papel", "nível", "mel", "fiel",
        "sol", "farol", "anzol", "lençol",
        "gás", "país", "português", "japonês",
        "mês", "lei", "rei", "pai",
        "bem", "som", "flor", "cor", "mar", "paz", "luz",
        "framework", "endpoint", "callback", "middleware",
        "casa", "livro", "gato", "nome", "filme",
    ])
    def test_pt_singular_words(self, word: str) -> None:
        assert is_singular(word, lang="pt") is True
        assert is_plural(word, lang="pt") is False

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "leões", "estações",
        "cães", "alemães", "capitães", "pães",
        "papéis", "níveis", "fiéis",
        "sóis", "faróis", "anzóis", "lençóis",
        "gases", "países", "portugueses", "japoneses",
        "meses", "leis", "reis", "pais",
        "bens", "sons", "flores", "cores", "mares", "pazes", "luzes",
        "frameworks", "endpoints", "callbacks", "middlewares",
        "casas", "livros", "gatos", "nomes", "filmes",
    ])
    def test_pt_plural_words(self, word: str) -> None:
        assert is_plural(word, lang="pt") is True
        assert is_singular(word, lang="pt") is False

    @pytest.mark.parametrize("word", [
        "tórax", "látex", "lápis", "vírus", "óculos",
        "nós", "vós", "blues", "funk",
    ])
    def test_pt_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="pt") is True
        assert is_plural(word, lang="pt") is True


class TestPtCountAware:
    """Portuguese count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=1) == word

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=0) == pluralize(word, lang="pt")

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=2) == pluralize(word, lang="pt")


class TestPtWhitespace:
    """Portuguese whitespace preservation."""

    def test_pt_preserves_whitespace_pluralize(self) -> None:
        assert pluralize("  coração  ", lang="pt") == "  corações  "

    def test_pt_preserves_whitespace_singularize(self) -> None:
        assert singularize("  corações  ", lang="pt") == "  coração  "

    def test_pt_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ", lang="pt") == "   "
        assert singularize("   ", lang="pt") == "   "

    def test_pt_count_one_preserves_whitespace(self) -> None:
        assert pluralize("  coração  ", lang="pt", count=1) == "  coração  "


class TestPtSingleLetterAndEdge:
    """Portuguese single letters and boundary cases."""

    def test_pt_single_letter_a(self) -> None:
        assert pluralize("a", lang="pt") == "as"
        assert singularize("as", lang="pt") == "a"

    def test_pt_single_letter_a_uppercase(self) -> None:
        assert pluralize("A", lang="pt") == "AS"
        assert singularize("AS", lang="pt") == "A"

    def test_pt_empty_string(self) -> None:
        assert pluralize("", lang="pt") == ""
        assert singularize("", lang="pt") == ""

    def test_pt_whitespace_only(self) -> None:
        assert pluralize("   ", lang="pt") == "   "
        assert singularize("   ", lang="pt") == "   "


class TestPtUncountableConsistency:
    """Portuguese uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "tórax", "látex", "clímax", "sintaxe", "fax",
        "bíceps", "tríceps", "fórceps",
        "oásis", "gênesis",
        "lápis", "atlas", "vírus", "ônibus", "óculos",
        "férias", "núpcias", "cócegas", "afazeres",
        "três", "mais", "cais", "dois",
        "pires", "ourives", "cosmos", "seis",
        "menos", "jamais",
        "nós", "vós",
        "blues", "soul", "funk", "reggae", "folk", "metal",
        "software", "hardware", "web", "blog", "chat",
        "spam", "jazz", "rock", "punk", "flash",
        "marketing", "design", "streaming", "podcast",
        "feed", "shell", "kernel", "cloud",
        "backend", "frontend", "runtime", "workflow",
        "sandbox", "thread", "hub", "ping", "byte",
        "rugby", "skate", "poker", "darts",
        "hacker", "nerd", "geek",
        "download", "upload", "screenshot", "fallback",
    ])
    def test_pt_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word
        assert singularize(word, lang="pt") == word


# ---------------------------------------------------------------------------
# Spanish edge cases
# ---------------------------------------------------------------------------


class TestEsCasePreservation:
    """Spanish case preservation for irregulars and regex words."""

    @pytest.mark.parametrize("word,expected", [
        ("Lunes", "Lunes"),
        ("LUNES", "LUNES"),
        ("Crisis", "Crisis"),
        ("CRISIS", "CRISIS"),
        ("Rubí", "Rubíes"),
        ("RUBÍ", "RUBÍES"),
        ("Alemán", "Alemanes"),
        ("ALEMÁN", "ALEMANES"),
        ("Inglés", "Ingleses"),
        ("INGLÉS", "INGLESES"),
        ("Club", "Clubs"),
        ("CLUB", "CLUBS"),
        ("Framework", "Frameworks"),
        ("FRAMEWORK", "FRAMEWORKS"),
        ("País", "Países"),
        ("PAÍS", "PAÍSES"),
        ("Joven", "Jóvenes"),
        ("JOVEN", "JÓVENES"),
        ("Examen", "Exámenes"),
        ("EXAMEN", "EXÁMENES"),
    ])
    def test_es_title_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="es") == expected

    @pytest.mark.parametrize("word,expected", [
        ("Rubíes", "Rubí"),
        ("RUBÍES", "RUBÍ"),
        ("Alemanes", "Alemán"),
        ("ALEMANES", "ALEMÁN"),
        ("Ingleses", "Inglés"),
        ("INGLESES", "INGLÉS"),
        ("Clubs", "Club"),
        ("CLUBS", "CLUB"),
        ("Países", "País"),
        ("PAÍSES", "PAÍS"),
        ("Jóvenes", "Joven"),
        ("JÓVENES", "JOVEN"),
        ("Exámenes", "Examen"),
        ("EXÁMENES", "EXAMEN"),
    ])
    def test_es_title_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="es") == expected


class TestEsMixedCase:
    """Spanish mixed case preservation."""

    @pytest.mark.parametrize("word,expected", [
        ("iPhone", "iPhones"),
    ])
    def test_es_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="es") == expected


class TestEsHyphenatedWords:
    """Spanish hyphenated word pluralization."""

    @pytest.mark.parametrize("singular,plural", [
        ("café-bar", "cafés-bar"),
        ("teórico-práctico", "teóricos-práctico"),
        ("económico-social", "económicos-social"),
        ("físico-químico", "físicos-químico"),
        ("histórico-artístico", "históricos-artístico"),
    ])
    def test_es_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural

    @pytest.mark.parametrize("singular,plural", [
        ("café-bar", "cafés-bar"),
    ])
    def test_es_hyphenated_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural, lang="es") == singular

    def test_es_hyphenated_roundtrip(self) -> None:
        for word in ["café-bar"]:
            assert singularize(pluralize(word, lang="es"), lang="es") == word

    def test_es_leading_hyphen_pluralize(self) -> None:
        assert pluralize("-casa", lang="es") == "-casas"

    def test_es_leading_hyphen_singularize(self) -> None:
        assert singularize("-casas", lang="es") == "-casa"

    def test_es_hyphen_only(self) -> None:
        assert pluralize("-", lang="es") == "-"
        assert singularize("-", lang="es") == "-"

    def test_es_double_hyphen(self) -> None:
        assert pluralize("--", lang="es") == "--"
        assert singularize("--", lang="es") == "--"


class TestEsIdempotency:
    """Spanish pluralize of already-plural words should return unchanged."""

    @pytest.mark.parametrize("word", [
        "rubíes", "farolillos", "corrales", "pendones", "farones",
        "ingletes", "jóvenes", "exámenes", "resúmenes", "volúmenes",
        "alemanes", "ingleses", "franceses",
        "japoneses", "portugueses", "holandeses", "dinamarqueses",
        "clubs", "fraces", "álbumes", "cármenes", "especímenes",
        "caracteres", "lunes", "martes", "miércoles",
        "crisis", "análisis", "síntesis", "tesis",
        "países", "revéses", "bisteces", "coñaces",
        "frameworks", "endpoints", "callbacks", "middlewares",
        "hashes", "urls", "widgets", "buckets", "pipelines",
    ])
    def test_es_pluralize_already_plural(self, word: str) -> None:
        assert pluralize(word, lang="es") == word


class TestEsRoundTrip:
    """Spanish pluralize → singularize round-trip identity."""

    @pytest.mark.parametrize("word", [
        "casa", "libro", "gato", "perro", "mesa",
        "rubí", "farolillo", "corral", "pendón", "farón",
        "inglete", "joven", "examen", "resumen", "volumen",
        "alemán", "inglés", "francés", "japonés", "portugués",
        "holandés", "dinamarqués", "club", "frac", "álbum",
        "carmen", "espécimen", "carácter", "país", "revés",
        "bistec", "coñac", "framework", "endpoint", "callback",
        "middleware", "hash", "url", "widget", "bucket",
        "pipeline", "café", "té", "sofá", "papá",
    ])
    def test_es_roundtrip(self, word: str) -> None:
        plural = pluralize(word, lang="es")
        assert singularize(plural, lang="es") == word


class TestEsCountAware:
    """Spanish count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "casa", "libro", "rubí", "alemán", "framework",
        "joven", "examen", "país",
    ])
    def test_es_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, lang="es", count=1) == word

    @pytest.mark.parametrize("word", [
        "casa", "libro", "rubí", "alemán", "framework",
        "joven", "examen", "país",
    ])
    def test_es_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="es", count=0) == pluralize(word, lang="es")

    @pytest.mark.parametrize("word", [
        "casa", "libro", "rubí", "alemán", "framework",
        "joven", "examen", "país",
    ])
    def test_es_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="es", count=2) == pluralize(word, lang="es")


class TestEsWhitespace:
    """Spanish whitespace preservation."""

    def test_es_preserves_whitespace_pluralize(self) -> None:
        assert pluralize("  casa  ", lang="es") == "  casas  "

    def test_es_preserves_whitespace_singularize(self) -> None:
        assert singularize("  casas  ", lang="es") == "  casa  "

    def test_es_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ", lang="es") == "   "
        assert singularize("   ", lang="es") == "   "

    def test_es_count_one_preserves_whitespace(self) -> None:
        assert pluralize("  casa  ", lang="es", count=1) == "  casa  "


class TestEsSingleLetterAndEdge:
    """Spanish single letters and boundary cases."""

    def test_es_single_letter_a(self) -> None:
        assert pluralize("a", lang="es") == "as"
        assert singularize("as", lang="es") == "a"

    def test_es_single_letter_a_uppercase(self) -> None:
        assert pluralize("A", lang="es") == "AS"
        assert singularize("AS", lang="es") == "A"

    def test_es_empty_string(self) -> None:
        assert pluralize("", lang="es") == ""
        assert singularize("", lang="es") == ""

    def test_es_whitespace_only(self) -> None:
        assert pluralize("   ", lang="es") == "   "
        assert singularize("   ", lang="es") == "   "


class TestEsUncountableConsistency:
    """Spanish uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "lunes", "martes", "miércoles", "jueves", "viernes",
        "crisis", "análisis", "síntesis", "tesis", "paréntesis",
        "éxtasis", "oasis", "sintaxis", "lisis",
        "prótesis", "diagnosis", "hipótesis",
        "tórax", "fax", "clímax", "suplex", "flex", "index",
        "latex", "matrix", "mix", "relax", "sex", "simplex",
        "complex", "duplex", "telex", "vortex", "prefix", "nexus",
        "virus", "chasis", "atlas", "series",
        "res",
        "paraguas", "saltamontes", "cumpleaños", "rompecabezas",
        "sacacorchos", "parabrisas", "rascacielos",
        "software", "hardware", "web", "blog", "post", "chat",
        "spam", "parking", "marketing", "jazz", "rock", "punk",
        "gourmet", "piercing", "hobby", "flash", "cactus", "status", "clip",
        "zigzag",
        "parálisis", "tuberculosis", "psoriasis", "elefantiasis",
        "pediculosis", "rabies", "mumps",
        "génesis", "apocalipsis",
        "biceps", "triceps", "cuádriceps", "forceps",
        "lavacoches", "sacamuelas", "cortaplumas", "abrelatas",
        "parachoques", "rompecorazones", "sacaorchos",
        "quitamanchas", "matasanos", "guardabosques", "guardacostas",
        "gris",
    ])
    def test_es_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="es") == word
        assert singularize(word, lang="es") == word


class TestEsIsSingularIsPlural:
    """Spanish is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "casa", "libro", "gato", "perro", "mesa",
        "rubí", "joven", "examen", "alemán", "inglés",
        "club", "país", "framework", "endpoint",
    ])
    def test_es_singular_words(self, word: str) -> None:
        assert is_singular(word, lang="es") is True
        assert is_plural(word, lang="es") is False

    @pytest.mark.parametrize("word", [
        "casas", "libros", "gatos", "perros", "mesas",
        "rubíes", "jóvenes", "exámenes", "alemanes", "ingleses",
        "clubs", "países", "frameworks", "endpoints",
    ])
    def test_es_plural_words(self, word: str) -> None:
        assert is_plural(word, lang="es") is True
        assert is_singular(word, lang="es") is False

    @pytest.mark.parametrize("word", [
        "lunes", "martes", "crisis", "análisis", "tórax",
        "virus", "atlas", "paraguas", "software", "zigzag",
    ])
    def test_es_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="es") is True
        assert is_plural(word, lang="es") is True


# ---------------------------------------------------------------------------
# English edge cases
# ---------------------------------------------------------------------------


class TestEnCountAware:
    """English count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, count=1) == word

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, count=0) == pluralize(word)

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, count=2) == pluralize(word)


class TestEnMixedCase:
    """English mixed case preservation."""

    @pytest.mark.parametrize("word,expected", [
        ("iPhone", "iPhones"),
        ("McDonald", "McDonalds"),
        ("WordPress", "WordPresses"),
    ])
    def test_en_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize("word,expected", [
        ("iPhones", "iPhone"),
        ("McDonalds", "McDonald"),
        ("WordPresses", "WordPress"),
    ])
    def test_en_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word) == expected


class TestEnSingleLetterAndEdge:
    """English single letters and boundary cases."""

    def test_en_single_letter_a(self) -> None:
        assert pluralize("a") == "as"

    def test_en_single_letter_a_uppercase(self) -> None:
        assert pluralize("A") == "AS"

    def test_en_empty_string(self) -> None:
        assert pluralize("") == ""
        assert singularize("") == ""

    def test_en_whitespace_only(self) -> None:
        assert pluralize("   ") == "   "
        assert singularize("   ") == "   "


class TestEnUncountableConsistency:
    """English uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "sheep", "fish", "deer", "moose", "swine",
        "series", "species", "news", "scissors",
        "trousers", "pants", "glasses",
        "bison", "buffalo", "caribou", "elk", "wildebeest",
        "cod", "salmon", "trout", "pike", "herring",
        "graffiti", "djinn", "pence", "quid",
        "hertz", "chassis", "corps", "debris", "siemens",
        "contretemps", "mews", "haggis", "innings", "proceedings",
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_en_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word) == word
        assert singularize(word) == word


class TestEnIsSingularIsPlural:
    """English is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
    ])
    def test_en_singular_words(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is False

    @pytest.mark.parametrize("word", [
        "cats", "dogs", "houses", "children", "mice",
        "geese", "feet", "teeth", "men", "women",
        "people", "oxen", "cacti", "nuclei", "fungi",
    ])
    def test_en_plural_words(self, word: str) -> None:
        assert is_plural(word) is True
        assert is_singular(word) is False

    @pytest.mark.parametrize("word", [
        "sheep", "fish", "deer", "series", "species",
        "news", "scissors", "bison", "graffiti",
    ])
    def test_en_uncountable_both(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is True


class TestEnHyphenatedRoundTrip:
    """English hyphenated compound round-trip identity."""

    @pytest.mark.parametrize("word", [
        "mother-in-law", "father-in-law", "brother-in-law",
        "sister-in-law", "daughter-in-law", "son-in-law",
        "attorney-general", "court-martial", "editor-in-chief",
        "forget-me-not", "merry-go-round",
        "meta-analysis", "post-modernism",
    ])
    def test_en_hyphenated_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word)) == word


# ---------------------------------------------------------------------------
# French edge cases
# ---------------------------------------------------------------------------


class TestFrCasePreservation:
    """French case preservation for pluralization."""

    @pytest.mark.parametrize("word,expected", [
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

    @pytest.mark.parametrize("word,expected", [
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

    @pytest.mark.parametrize("word,expected", [
        ("iPhone", "iPhones"),
        ("McDonald", "McDonalds"),
    ])
    def test_fr_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected


class TestFrHyphenated:
    """French hyphenated compound words."""

    @pytest.mark.parametrize("word,expected", [
        ("café-théâtre", "cafés-théâtres"),
        ("eau-de-vie", "eaux-de-vie"),
        ("garde-manger", "gardes-mangers"),
        ("chou-fleur", "choux-fleurs"),
        ("pot-au-feu", "pots-aux-feux"),
        ("arc-en-ciel", "arcs-en-ciel"),
    ])
    def test_fr_hyphenated_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected

    @pytest.mark.parametrize("word,expected", [
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

    @pytest.mark.parametrize("word,expected", [
        (" chat", " chats"),
        ("chat ", "chats "),
        (" chat ", " chats "),
        ("  cheval  ", "  chevaux  "),
    ])
    def test_fr_whitespace_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="fr") == expected

    @pytest.mark.parametrize("word,expected", [
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


class TestItCasePreservation:
    """Italian case preservation for irregulars and regex words."""

    @pytest.mark.parametrize("word,expected", [
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

    @pytest.mark.parametrize("word,expected", [
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

    @pytest.mark.parametrize("word,expected", [
        ("McLibro", "McLibri"),
    ])
    def test_it_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="it") == expected

    @pytest.mark.parametrize("word,expected", [
        ("McLibri", "McLibro"),
    ])
    def test_it_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="it") == expected


class TestItHyphenatedWords:
    """Italian hyphenated word pluralization."""

    @pytest.mark.parametrize("singular,plural", [
        ("caffè-bar", "caffè-bar"),
        ("film-club", "film-club"),
        ("auto-scuola", "auto-scuole"),
    ])
    def test_it_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="it") == plural

    @pytest.mark.parametrize("singular,plural", [
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
        "passaggio", "messaggio",
        "casa", "scuola", "banana", "gatta", "pasta", "pianta",
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
