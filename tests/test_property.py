"""Property-based tests using Hypothesis for invariant verification."""
from __future__ import annotations

import unicodedata

from hypothesis import given, settings
from hypothesis import strategies as st

from pluralio import pluralize, singularize

# Strategies for generating test words from known vocabulary
en_words = st.sampled_from([
    "cat", "dog", "house", "book", "city", "story", "baby", "lady",
    "wolf", "leaf", "knife", "wife", "life", "half", "calf",
    "box", "fox", "bus", "gas", "class", "boss", "kiss", "mass",
    "hero", "potato", "tomato", "photo", "piano", "radio",
    "man", "woman", "child", "tooth", "foot", "goose", "mouse",
    "ox", "person", "die", "penny", "cactus", "nucleus", "alumnus",
    "datum", "medium", "curriculum", "phenomenon", "criterion",
    "analysis", "crisis", "matrix", "index", "appendix", "vertex",
    "sheep", "deer", "fish", "series", "species", "moose",
    "cache", "niche", "diff", "history", "biology",
    "cuff", "stuff", "bluff", "fluff", "puff", "scoff", "stiff",
    "elf", "dwarf", "hoof", "thief", "shelf", "self",
    "boy", "toy", "key", "day", "way", "monkey", "honey",
    "church", "dish", "brush", "crash", "flash", "watch",
    "status", "virus", "atlas", "canvas", "bias", "bonus",
    "octopus", "platypus", "minibus", "omnibus",
    "ellipsis", "neurosis", "synopsis", "emphasis", "paralysis",
    "louse", "agendum", "erratum", "ovum", "helix", "codex",
    "radix", "cortex", "vortex", "apex",
    "tuberculosis", "psoriasis", "rabies", "mumps",
    "function", "variable", "object", "method",
    "server", "client", "router", "container", "token",
])

es_words = st.sampled_from([
    "gato", "perro", "casa", "libro", "ciudad", "verdad",
    "canción", "corazón", "botón", "limón", "camión", "razón",
    "estación", "emoción", "nación", "región", "sesión",
    "lápiz", "voz", "luz", "capaz", "feliz", "pez",
    "árbol", "papel", "flor", "color", "error", "dolor",
    "motor", "autor", "actor", "doctor", "factor", "sector",
    "club", "álbum", "clic", "email", "chip", "bit",
    "examen", "joven", "imagen", "crimen", "origen", "régimen",
    "volumen", "resumen", "germen", "margen",
    "rubí", "tabú", "champú", "maniquí", "bisturí", "jabalí",
    "alemán", "inglés", "francés", "japonés",
    "framework", "server", "router", "token", "driver",
    "buffer", "proxy", "header", "script", "backlog",
    "scrum", "review", "merge", "fork", "log", "bug",
    "cache", "hash", "url", "widget", "plugin", "addon",
    "test", "stub", "spy", "alert", "event", "message",
    "user", "account", "profile", "role", "group", "team",
    "project", "issue", "plan", "tier", "quota", "limit",
])


class TestEnIdempotency:
    """pluralize(pluralize(x)) == pluralize(x) for known English words."""

    @given(en_words)
    @settings(max_examples=500)
    def test_pluralize_idempotent(self, word: str) -> None:
        p1 = pluralize(word)
        p2 = pluralize(p1)
        assert p2 == p1, f"pluralize not idempotent: {word} -> {p1} -> {p2}"

    @given(en_words)
    @settings(max_examples=500)
    def test_singularize_idempotent(self, word: str) -> None:
        s1 = singularize(word)
        s2 = singularize(s1)
        assert s2 == s1, f"singularize not idempotent: {word} -> {s1} -> {s2}"


class TestEsIdempotency:
    """pluralize(pluralize(x)) == pluralize(x) for known Spanish words."""

    @given(es_words)
    @settings(max_examples=500)
    def test_pluralize_idempotent(self, word: str) -> None:
        p1 = pluralize(word, lang="es")
        p2 = pluralize(p1, lang="es")
        assert p2 == p1, f"ES pluralize not idempotent: {word} -> {p1} -> {p2}"

    @given(es_words)
    @settings(max_examples=500)
    def test_singularize_idempotent(self, word: str) -> None:
        s1 = singularize(word, lang="es")
        s2 = singularize(s1, lang="es")
        assert s2 == s1, f"ES singularize not idempotent: {word} -> {s1} -> {s2}"


class TestRoundTrip:
    """singularize(pluralize(x)) == x for known singular words."""

    @given(en_words)
    @settings(max_examples=500)
    def test_en_roundtrip(self, word: str) -> None:
        p = pluralize(word)
        s = singularize(p)
        assert s == word, f"EN round-trip failed: {word} -> {p} -> {s}"

    @given(es_words)
    @settings(max_examples=500)
    def test_es_roundtrip(self, word: str) -> None:
        p = pluralize(word, lang="es")
        s = singularize(p, lang="es")
        assert s == word, f"ES round-trip failed: {word} -> {p} -> {s}"


class TestCasePreservation:
    """pluralize preserves case patterns for known words."""

    @given(en_words)
    @settings(max_examples=300)
    def test_en_all_caps(self, word: str) -> None:
        upper = word.upper()
        p = pluralize(upper)
        assert p == p.upper(), f"Case not preserved: {upper} -> {p}"

    @given(en_words)
    @settings(max_examples=300)
    def test_en_title_case(self, word: str) -> None:
        title = word.capitalize()
        p = pluralize(title)
        assert p == p.capitalize(), f"Title case not preserved: {title} -> {p}"

    @given(es_words)
    @settings(max_examples=300)
    def test_es_all_caps(self, word: str) -> None:
        upper = word.upper()
        p = pluralize(upper, lang="es")
        assert p == p.upper(), f"ES case not preserved: {upper} -> {p}"

    @given(es_words)
    @settings(max_examples=300)
    def test_es_title_case(self, word: str) -> None:
        title = word.capitalize()
        p = pluralize(title, lang="es")
        assert p == p.capitalize(), f"ES title case not preserved: {title} -> {p}"


class TestUnicodeNormalization:
    """Inputs are NFC-normalized on entry."""

    @given(es_words)
    @settings(max_examples=200)
    def test_nfc_normalized(self, word: str) -> None:
        nfc = unicodedata.normalize("NFC", word)
        nfd = unicodedata.normalize("NFD", word)
        assert pluralize(nfc, lang="es") == pluralize(nfd, lang="es")
