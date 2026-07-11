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
        ("annexes", "annexe"), ("pickaxes", "pickaxe"),
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
