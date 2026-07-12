"""Cross-language edge cases for pluralization and singularization."""
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
    @pytest.mark.parametrize(("word", "expected"), [
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

    @pytest.mark.parametrize(("word", "expected"), [
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

    @pytest.mark.parametrize(("singular", "plural"), [
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
    ])
    def test_last_segment_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("forget-me-not", "forget-me-nots"),
        ("merry-go-round", "merry-go-rounds"),
    ])
    def test_last_segment_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
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

    @pytest.mark.parametrize(("singular", "plural"), [
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

    @pytest.mark.parametrize(("singular", "plural"), [
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
    @pytest.mark.parametrize(("word", "expected"), [
        ("McDonald", "McDonalds"),
        ("iPhone", "iPhones"),
        ("McBox", "McBoxes"),
    ])
    def test_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
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
    @pytest.mark.parametrize(("plural", "singular"), [
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
    @pytest.mark.parametrize(("singular", "plural"), [
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
    @pytest.mark.parametrize(("plural", "singular"), [
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

    @pytest.mark.parametrize(("plural", "singular"), [
        ("fizzes", "fizz"), ("buzzes", "buzz"), ("fuzzes", "fuzz"),
    ])
    def test_zzes_singularize(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular



class TestSsUsIrregulars:
    @pytest.mark.parametrize(("singular", "plural"), [
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

    @pytest.mark.parametrize(("singular", "plural"), [
        ("discus", "discuses"), ("census", "censuses"),
        ("plexus", "plexuses"), ("sinus", "sinuses"),
        ("thermos", "thermoses"), ("abacus", "abaci"),
        ("corpus", "corpora"), ("genus", "genera"), ("opus", "opera"),
    ])
    def test_us_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert singularize(singular) == singular



class TestWhitespacePreservation:
    """Leading/trailing whitespace must be preserved in output."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("  cat  ", "  cats  "),
        (" cat", " cats"),
        ("cat ", "cats "),
        ("\tcat\t", "\tcats\t"),
    ])
    def test_pluralize_whitespace(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
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



