from __future__ import annotations

import pytest

from pluralio import singularize


class TestSpanishSingularRules:
    def test_iones_to_ion(self) -> None:
        for plural, singular in [("canciones", "canción"), ("regiones", "región")]:
            assert singularize(plural, lang="es") == singular

    def test_ces_to_z(self) -> None:
        for plural, singular in [("lápices", "lápiz"), ("voces", "voz"), ("luces", "luz")]:
            assert singularize(plural, lang="es") == singular

    def test_es_strip(self) -> None:
        for plural, singular in [("árboles", "árbol"), ("colores", "color")]:
            assert singularize(plural, lang="es") == singular

    def test_s_strip(self) -> None:
        for plural, singular in [("casas", "casa"), ("libros", "libro")]:
            assert singularize(plural, lang="es") == singular


class TestSpanishIrregularSingles:
    @pytest.mark.parametrize("plural,singular", [
        ("rubíes", "rubí"), ("tabúes", "tabú"), ("champúes", "champú"),
        ("maniquíes", "maniquí"), ("bisturíes", "bisturí"),
        ("jabalíes", "jabalí"), ("tisúes", "tisú"),
        ("bambúes", "bambú"), ("hindúes", "hindú"),
        ("carmesíes", "carmesí"), ("israelíes", "israelí"),
        ("marroquíes", "marroquí"), ("popurríes", "popurrí"),
        ("nazaríes", "nazarí"), ("irakíes", "irakí"),
        ("paquistaníes", "paquistaní"), ("saharauíes", "saharauí"),
        ("magrebíes", "magrebí"), ("vadíes", "vadí"),
        ("bengalíes", "bengalí"), ("alhelíes", "alhelí"),
        ("jóvenes", "joven"), ("exámenes", "examen"),
        ("orígenes", "origen"), ("regímenes", "régimen"),
        ("imágenes", "imagen"), ("volúmenes", "volumen"),
        ("resúmenes", "resumen"), ("crímenes", "crimen"),
        ("gérmenes", "germen"), ("márgenes", "margen"),
        ("vírgenes", "virgen"), ("órdenes", "orden"),
        ("caracteres", "carácter"), ("especímenes", "espécimen"),
        ("clubs", "club"), ("álbumes", "álbum"),
        ("clics", "clic"), ("tics", "tic"),
        ("emails", "email"), ("modems", "modem"),
        ("chips", "chip"), ("bits", "bit"),
        ("fans", "fan"), ("jets", "jet"),
        ("links", "link"), ("rings", "ring"),
        ("boicots", "boicot"), ("banners", "banner"),
        ("snobs", "snob"), ("stands", "stand"),
        ("thrillers", "thriller"), ("posters", "poster"),
        ("records", "record"), ("sprints", "sprint"),
        ("guiones", "guion"), ("bienes", "bien"), ("sienes", "sien"),
        ("síes", "sí"), ("yoes", "yo"), ("noes", "no"),
        ("alemanes", "alemán"), ("capitanes", "capitán"),
        ("champanes", "champán"), ("charlatanes", "charlatán"),
        ("sultanes", "sultán"), ("gavilanes", "gavilán"),
        ("truhanes", "truhán"), ("fulanes", "fulán"),
        ("rufianes", "rufián"),
        ("calcetines", "calcetín"), ("jardines", "jardín"),
        ("desatines", "desatín"), ("chiquitines", "chiquitín"),
        ("sambenines", "sambenín"), ("baladines", "baladín"),
        ("chapines", "chapín"), ("festines", "festín"),
        ("ingleses", "inglés"), ("franceses", "francés"),
        ("portugueses", "portugués"), ("japoneses", "japonés"),
        ("holandeses", "holandés"), ("daneses", "danés"),
        ("irlandeses", "irlandés"), ("aragoneses", "aragonés"),
        ("leoneses", "leonés"), ("cordobeses", "cordobés"),
        ("corteses", "cortés"), ("intereses", "interés"),
        ("monteses", "montés"), ("burgaleses", "burgalés"),
        ("logroñeses", "logroñés"), ("tarraconeses", "tarraconés"),
        ("alaveses", "alavés"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="es") == singular
