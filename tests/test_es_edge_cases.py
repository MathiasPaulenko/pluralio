"""Spanish edge cases for pluralization and singularization."""
from __future__ import annotations

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestEsNewFixes:
    def test_zigzag_uncountable(self) -> None:
        assert pluralize("zigzag", lang="es") == "zigzag"
        assert singularize("zigzag", lang="es") == "zigzag"

    def test_himenes_accent(self) -> None:
        assert pluralize("himen", lang="es") == "hímenes"
        assert singularize("hímenes", lang="es") == "himen"

    @pytest.mark.parametrize(("singular", "plural"), [
        ("dios", "dioses"), ("tos", "toses"),
        ("gas", "gases"), ("bus", "buses"), ("vals", "valses"),
    ])
    def test_es_s_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular
        assert pluralize(plural, lang="es") == plural



class TestEsTechLoanwords:
    @pytest.mark.parametrize(("singular", "plural"), [
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



class TestEsCrossCheckFixes:
    @pytest.mark.parametrize(("singular", "plural"), [
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

    @pytest.mark.parametrize(("singular", "plural"), [
        ("espermatozoide", "espermatozoides"),
        ("asteroide", "asteroides"),
        ("androide", "androides"),
    ])
    def test_es_oide_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural
        assert singularize(plural, lang="es") == singular



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



class TestEsPeineRoundTrip:
    """peine should round-trip correctly (vowel+consonant+e pattern)."""

    def test_pluralize_peine(self) -> None:
        assert pluralize("peine", lang="es") == "peines"

    def test_singularize_peines(self) -> None:
        assert singularize("peines", lang="es") == "peine"

    def test_round_trip(self) -> None:
        assert singularize(pluralize("peine", lang="es"), lang="es") == "peine"



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



class TestEsCasePreservation:
    """Spanish case preservation for irregulars and regex words."""

    @pytest.mark.parametrize(("word", "expected"), [
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

    @pytest.mark.parametrize(("word", "expected"), [
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

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhone", "iPhones"),
    ])
    def test_es_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="es") == expected



class TestEsHyphenatedWords:
    """Spanish hyphenated word pluralization."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("café-bar", "cafés-bar"),
        ("teórico-práctico", "teóricos-práctico"),
        ("económico-social", "económicos-social"),
        ("físico-químico", "físicos-químico"),
        ("histórico-artístico", "históricos-artístico"),
    ])
    def test_es_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural

    @pytest.mark.parametrize(("singular", "plural"), [
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



