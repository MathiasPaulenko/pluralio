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
    # e-ending words (two-consonant cluster rule)
    "noche", "leche", "frente", "mente", "gente", "arte", "parte",
    "calle", "valle", "coche", "bloque", "cheque", "choque", "mueble",
    "breve", "cable", "doble", "pobre", "chiste", "coste", "poste",
    "oeste", "corte", "muerte", "suerte", "puerta", "fuerte", "cine",
    "deporte", "reporte", "soporte", "cliente", "fuente", "puente",
    "ambiente", "incidente", "presidente", "paciente", "agente",
    "urgente", "torrente", "caliente", "lente", "diente", "nombre",
    "hombre", "diamante", "elefante", "gigante", "creciente",
    "potente", "violente", "serpiente",
    # tes rule
    "machete", "billete", "paquete", "bote", "lote", "mote",
    "coyote", "chocolate", "petate", "chupete",
    # jes rule
    "reloj", "garaje", "viaje", "peaje", "coraje", "paisaje",
    "mensaje", "rodaje", "montaje", "homenaje",
    # accent restoration
    "huracán", "mandarín",
    # ce+s words
    "príncipe", "índice", "vértice", "múltiple", "pirámide", "códice",
    # other e-ending words
    "base", "clase", "fase", "frase", "llave", "clave", "nave",
    "nube", "nieve", "adobe", "pibe", "nene", "mole",
    # compás fix
    "compás",
    # -é words (idempotency fix)
    "café", "té", "bebé", "puré", "cliché", "paté",
    "rosé", "bidé", "frappé",
    # -y words
    "ley", "rey", "buey", "hoy", "convoy",
    # loanwords -r
    "monitor", "scanner", "manager", "browser", "printer", "computer",
    "editor", "visitor", "sponsor", "partner", "provider", "supplier",
    "investor", "founder", "developer", "sender", "receiver",
    # accent restoration
    "caimán", "guardián", "sotán", "comodín", "edén",
    "limón", "melón", "dragón", "campeón",
    # non-tech loanwords
    "sandwich", "whisky", "ponche", "parche",
]


PORTUGUESE_WORDS = [
    # Regular vowel
    "casa", "livro", "gato",
    # -ão → -ões
    "coração", "canção", "balão",
    # -ão → -ães
    "cão", "pão", "alemão",
    # -ão → -ãos
    "irmão", "mão", "chão",
    # -m → -ns
    "homem", "jardim",
    # -l → -is
    "animal", "azul",
    # -el → -éis
    "papel", "nível",
    # -ol → -óis
    "sol", "farol",
    # -r → -res
    "flor", "motor",
    # -z → -zes
    "luz", "rapaz",
    # -s → -ses (irregular)
    "português", "japonês", "gás", "país", "deus",
    # consonant + e
    "nome", "filme", "noite", "leite", "sede", "rede",
    "parede", "cobre", "pobre", "pele", "vale", "arte",
    "morte", "parte", "elefante", "dificuldade",
    # vowel + is (invariable or strip s)
    "lei", "rei",
    # -il words
    "cantil", "barril", "funil",
    # -el → -éis (accent)
    "mel", "fiel",
    # vowel + consonant + e
    "árvore",
    # consonant + e (e-ending words with consonant before e)
    "chave", "chefe", "peixe",
    # -ão → -ãos (additional)
    "grão", "são",
    # Uncountable
    "tórax", "lápis", "três", "mais", "cais", "dois",
    "nós", "vós",
    # Loanwords
    "club", "chip", "email", "server",
]


class TestRoundTrip:
    @pytest.mark.parametrize("word", ENGLISH_WORDS)
    def test_en_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word)) == word

    @pytest.mark.parametrize("word", SPANISH_WORDS)
    def test_es_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word, lang="es"), lang="es") == word

    @pytest.mark.parametrize("word", PORTUGUESE_WORDS)
    def test_pt_singularize_pluralize(self, word: str) -> None:
        assert singularize(pluralize(word, lang="pt"), lang="pt") == word
