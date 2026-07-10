from __future__ import annotations

import pytest

from pluralio import pluralize, singularize

ENGLISH_WORDS = [
    "book", "city", "box", "child", "mouse", "library",
    "knife", "wolf", "potato", "party", "church", "bus",
    "cat", "dog", "shoe", "boy", "key", "day",
    "man", "woman", "person", "foot", "tooth", "goose",
    "cactus", "nucleus", "phenomenon", "criterion", "analysis", "crisis",
    "matrix", "index", "appendix", "vertex",
    "half", "leaf", "loaf", "thief", "self", "shelf",
    "wife", "life", "hero", "echo", "veto",
    "photo", "piano", "halo", "pie", "tie", "movie",
    "cookie", "selfie", "quiz", "status", "virus",
    # New regex rule exceptions
    "cafe", "safe", "giraffe", "strafe",
    "turf", "golf", "dwarf", "brief", "chief", "roof",
    "proof", "belief", "relief", "hoof",
    "solo", "cello", "disco", "memo", "auto", "ego",
    "kilo", "tempo", "turbo", "logo", "pro", "combo",
    "casino", "taco", "burrito", "poncho", "sombrero",
    "flamingo", "tornado", "avocado",
    "foe", "hoe", "toe",
    "aloe", "oboe", "canoe",
    # Words ending in s (plural adds es)
    "gas", "boss", "lens", "cross",
    # ves false positive words (just add s)
    "hive", "drive", "valve", "solve", "twelve",
    "carve", "curve", "nerve", "serve", "starve",
    "resolve", "evolve", "involve",
    # Short o-ending words
    "go", "no", "so", "do",
]

SPANISH_WORDS = [
    "libro", "casa", "lápiz", "ratón", "árbol", "canción",
    "joven", "examen", "color", "voz", "luz", "papel",
    "limón", "corazón", "botón", "alemán", "capitán", "jardín",
    "inglés", "francés", "rubí", "tabú", "maniquí",
    "imagen", "volumen", "resumen", "crimen", "germen", "margen",
    "club", "álbum", "email", "fan", "guion",
    "sí", "no", "carácter", "espécimen",
    # Accent shift words
    "origen", "régimen", "virgen", "orden",
    "bien", "sien",
    "champú", "bisturí", "jabalí", "bambú", "hindú",
    "portugués", "japonés", "holandés", "danés",
    "champán", "charlatán", "sultán", "gavilán",
    "calcetín", "desatín", "festín",
]


class TestRoundTrip:
    @pytest.mark.parametrize("word", ENGLISH_WORDS)
    def test_en_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word)) == word

    @pytest.mark.parametrize("word", SPANISH_WORDS)
    def test_es_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word, lang="es"), lang="es") == word
