from __future__ import annotations

import pytest

from pluralio import pluralize


class TestSpanishPluralRules:
    def test_vowel_plus_s(self) -> None:
        for singular, plural in [("libro", "libros"), ("casa", "casas"), ("mesa", "mesas")]:
            assert pluralize(singular, lang="es") == plural

    def test_consonant_plus_es(self) -> None:
        for singular, plural in [("árbol", "árboles"), ("papel", "papeles"), ("color", "colores")]:
            assert pluralize(singular, lang="es") == plural

    def test_z_to_ces(self) -> None:
        for singular, plural in [("lápiz", "lápices"), ("voz", "voces"), ("luz", "luces")]:
            assert pluralize(singular, lang="es") == plural

    def test_ion_to_iones(self) -> None:
        for singular, plural in [("canción", "canciones"), ("región", "regiones")]:
            assert pluralize(singular, lang="es") == plural

    def test_invariable_s_x(self) -> None:
        for word in ["lunes", "tórax", "crisis"]:
            assert pluralize(word, lang="es") == word


class TestSpanishAccentShift:
    @pytest.mark.parametrize("singular,plural", [
        ("joven", "jóvenes"), ("examen", "exámenes"),
        ("origen", "orígenes"), ("régimen", "regímenes"),
        ("imagen", "imágenes"), ("volumen", "volúmenes"),
        ("resumen", "resúmenes"), ("crimen", "crímenes"),
        ("germen", "gérmenes"), ("margen", "márgenes"),
        ("virgen", "vírgenes"), ("orden", "órdenes"),
        ("carácter", "caracteres"), ("espécimen", "especímenes"),
    ])
    def test_accent_shift_on_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural


class TestSpanishIrregularPlurals:
    @pytest.mark.parametrize("singular,plural", [
        ("rubí", "rubíes"), ("tabú", "tabúes"), ("champú", "champúes"),
        ("maniquí", "maniquíes"), ("bisturí", "bisturíes"),
        ("jabalí", "jabalíes"), ("tisú", "tisúes"),
        ("bambú", "bambúes"), ("hindú", "hindúes"),
        ("carmesí", "carmesíes"), ("israelí", "israelíes"),
        ("marroquí", "marroquíes"), ("popurrí", "popurríes"),
        ("nazarí", "nazaríes"), ("irakí", "irakíes"),
        ("paquistaní", "paquistaníes"), ("saharauí", "saharauíes"),
        ("magrebí", "magrebíes"), ("vadí", "vadíes"),
        ("bengalí", "bengalíes"), ("alhelí", "alhelíes"),
        ("club", "clubs"), ("álbum", "álbumes"),
        ("clic", "clics"), ("tic", "tics"),
        ("email", "emails"), ("modem", "modems"),
        ("chip", "chips"), ("bit", "bits"),
        ("fan", "fans"), ("jet", "jets"),
        ("link", "links"), ("ring", "rings"),
        ("boicot", "boicots"), ("banner", "banners"),
        ("snob", "snobs"), ("stand", "stands"),
        ("thriller", "thrillers"), ("poster", "posters"),
        ("record", "records"), ("sprint", "sprints"),
        ("guion", "guiones"), ("bien", "bienes"), ("sien", "sienes"),
        ("sí", "síes"), ("yo", "yoes"), ("no", "noes"),
        ("compás", "compases"),
        ("café", "cafés"), ("té", "tés"), ("bebé", "bebés"),
        ("puré", "purés"), ("cliché", "clichés"), ("paté", "patés"),
        ("rosé", "rosés"), ("bidé", "bidés"), ("frappé", "frappés"),
        ("ley", "leyes"), ("rey", "reyes"), ("buey", "bueyes"),
        ("hoy", "hoyes"), ("convoy", "convoyes"),
        ("sandwich", "sandwiches"), ("whisky", "whiskies"),
        ("ponche", "ponches"), ("parche", "parches"),
        ("monitor", "monitors"), ("scanner", "scanners"),
        ("manager", "managers"), ("browser", "browsers"),
        ("printer", "printers"), ("computer", "computers"),
        ("editor", "editors"), ("visitor", "visitors"),
        ("sponsor", "sponsors"), ("partner", "partners"),
        ("provider", "providers"), ("supplier", "suppliers"),
        ("investor", "investors"), ("founder", "founders"),
        ("developer", "developers"), ("sender", "senders"),
        ("receiver", "receivers"),
    ])
    def test_irregular_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="es") == plural


class TestSpanishUncountable:
    @pytest.mark.parametrize("word", [
        "lunes", "martes", "miércoles", "jueves", "viernes",
        "crisis", "análisis", "síntesis", "tesis", "paréntesis",
        "éxtasis", "oasis", "sintaxis", "lisis",
        "tórax", "fax", "clímax", "suplex", "flex", "index",
        "latex", "matrix", "mix", "relax", "sex", "simplex",
        "complex", "duplex", "telex", "vortex", "prefix", "nexus",
        "virus", "chasis", "atlas", "series",
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
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="es") == word
