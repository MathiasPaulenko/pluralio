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

    def test_two_consonant_es_to_e(self) -> None:
        for plural, singular in [
            ("clientes", "cliente"), ("noches", "noche"),
            ("hombres", "hombre"), ("frentes", "frente"),
            ("cortes", "corte"), ("puertas", "puerta"),
            ("muertes", "muerte"), ("suertes", "suerte"),
            ("fuentes", "fuente"), ("puentes", "puente"),
            ("agentes", "agente"), ("calientes", "caliente"),
            ("dientes", "diente"), ("nombres", "nombre"),
            ("diamantes", "diamante"), ("elefantes", "elefante"),
        ]:
            assert singularize(plural, lang="es") == singular

    def test_tes_to_te(self) -> None:
        for plural, singular in [
            ("machetes", "machete"), ("billetes", "billete"),
            ("paquetes", "paquete"), ("botes", "bote"),
            ("lotes", "lote"), ("motes", "mote"),
            ("coyotes", "coyote"), ("chocolates", "chocolate"),
            ("petates", "petate"), ("chupetes", "chupete"),
            ("boletes", "bolete"),
        ]:
            assert singularize(plural, lang="es") == singular

    def test_jes_to_je(self) -> None:
        for plural, singular in [
            ("relojes", "reloj"), ("garajes", "garaje"),
            ("viajes", "viaje"), ("peajes", "peaje"),
            ("corajes", "coraje"), ("paisajes", "paisaje"),
            ("mensajes", "mensaje"), ("rodajes", "rodaje"),
            ("montajes", "montaje"), ("homenajes", "homenaje"),
        ]:
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
        ("huracanes", "huracán"), ("mandarines", "mandarín"),
        ("fases", "fase"), ("bases", "base"), ("clases", "clase"),
        ("frases", "frase"), ("llaves", "llave"), ("claves", "clave"),
        ("naves", "nave"), ("breves", "breve"), ("nieves", "nieve"),
        ("nubes", "nube"), ("adobes", "adobe"), ("cines", "cine"),
        ("príncipes", "príncipe"), ("pirámides", "pirámide"),
        ("índices", "índice"), ("vértices", "vértice"), ("códices", "códice"),
        ("pibes", "pibe"), ("nenes", "nene"), ("moles", "mole"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="es") == singular
