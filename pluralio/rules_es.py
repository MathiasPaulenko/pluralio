"""Spanish pluralization and singularization rules.

This module defines the complete set of Spanish pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``es`` language in the global registry.

The rules are organized into four categories:

1. **Irregular plurals**: Words that do not follow regex patterns
   and must be memorized. This includes words ending in a stressed
   vowel + ``í`` or ``ú`` (e.g. ``"rubí" → "rubíes"``), words with
   accent shifts (e.g. ``"joven" → "jóvenes"``, ``"examen" → "exámenes"``),
   and foreign loanwords (e.g. ``"club" → "clubs"``).
   The inverse mapping (plural → singular) is auto-generated.

2. **Extra singulars**: Additional plural → singular mappings that
   cannot be derived from the irregular plurals. These handle cases
   where the singular form requires an accent that the plural does
   not have (e.g. ``"alemanes" → "alemán"``, ``"inglés" → "ingleses"``).

3. **Regex rules**: Ordered patterns applied to words that are not
   in the irregular or uncountable lists. The first matching rule
   wins. Rules cover common Spanish pluralization patterns:
   - ``z`` → ``ces``
   - ``ión`` → ``iones``, ``ón`` → ``ones``, etc.
   - Vowel ending → add ``s``
   - Consonant ending → add ``es``

4. **Uncountable words**: Words that are invariable — their plural
   form is identical to their singular form. This includes days of
   the week ending in ``s``, words ending in ``x``, Greek-origin
   words ending in ``is``, compound words, and foreign loanwords.

Reference: ``ref/rules.md`` for the full rules documentation.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_IRREGULAR_PLURALS: dict[str, str] = {
    "rubí": "rubíes", "tabú": "tabúes", "champú": "champúes",
    "maniquí": "maniquíes", "bisturí": "bisturíes",
    "jabalí": "jabalíes", "tisú": "tisúes",
    "bambú": "bambúes", "hindú": "hindúes",
    "carmesí": "carmesíes", "israelí": "israelíes",
    "marroquí": "marroquíes", "popurrí": "popurríes",
    "nazarí": "nazaríes", "irakí": "irakíes",
    "paquistaní": "paquistaníes", "saharauí": "saharauíes",
    "magrebí": "magrebíes", "vadí": "vadíes",
    "bengalí": "bengalíes", "alhelí": "alhelíes",
    "joven": "jóvenes", "examen": "exámenes",
    "origen": "orígenes", "régimen": "regímenes",
    "imagen": "imágenes", "volumen": "volúmenes",
    "resumen": "resúmenes", "crimen": "crímenes",
    "germen": "gérmenes", "margen": "márgenes",
    "virgen": "vírgenes", "orden": "órdenes",
    "carácter": "caracteres", "espécimen": "especímenes",
    "club": "clubs", "álbum": "álbumes",
    "clic": "clics", "tic": "tics",
    "email": "emails", "modem": "modems",
    "chip": "chips", "bit": "bits",
    "fan": "fans", "jet": "jets",
    "link": "links", "ring": "rings",
    "boicot": "boicots", "banner": "banners",
    "snob": "snobs", "stand": "stands",
    "thriller": "thrillers", "poster": "posters",
    "record": "records", "sprint": "sprints",
    "guion": "guiones",
    "bien": "bienes", "sien": "sienes",
    "sí": "síes", "yo": "yoes", "no": "noes",
}
"""Mapping of singular → plural for irregular Spanish words.

Includes words with stressed ``í``/``ú`` endings, accent shifts,
and foreign loanwords. All keys and values are lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_EXTRA_SINGLES: dict[str, str] = {
    "alemanes": "alemán", "capitanes": "capitán",
    "champanes": "champán", "charlatanes": "charlatán",
    "sultanes": "sultán", "gavilanes": "gavilán",
    "truhanes": "truhán", "fulanes": "fulán",
    "rufianes": "rufián",
    "calcetines": "calcetín", "jardines": "jardín",
    "desatines": "desatín", "chiquitines": "chiquitín",
    "sambenines": "sambenín", "baladines": "baladín",
    "chapines": "chapín", "festines": "festín",
    "ingleses": "inglés", "franceses": "francés",
    "portugueses": "portugués", "japoneses": "japonés",
    "holandeses": "holandés", "daneses": "danés",
    "irlandeses": "irlandés", "aragoneses": "aragonés",
    "leoneses": "leonés", "cordobeses": "cordobés",
    "corteses": "cortés", "intereses": "interés",
    "monteses": "montés", "burgaleses": "burgalés",
    "logroñeses": "logroñés", "tarraconeses": "tarraconés",
    "alaveses": "alavés",
}
"""Additional plural → singular mappings for Spanish.

These handle accent restoration cases where the singular form
requires an accent mark that the plural form does not have.
For example, ``"alemán"`` → ``"alemanes"`` (plural loses the accent),
so the reverse mapping ``"alemanes" → "alemán"`` must be explicit.
"""

_IRREGULAR_SINGLES.update(_EXTRA_SINGLES)

_PLURAL_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"z$"), "ces"),
    (re.compile(r"ión$"), "iones"),
    (re.compile(r"ón$"), "ones"),
    (re.compile(r"án$"), "anes"),
    (re.compile(r"ín$"), "ines"),
    (re.compile(r"és$"), "eses"),
    (re.compile(r"x$"), ""),
    (re.compile(r"([aeiouáéíóú])$"), r"\1s"),
    (re.compile(r"([^aeiouáéíóúx])$"), r"\1es"),
]
"""Ordered Spanish pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``z`` → replace with ``ces``.
2. Words ending in ``ión`` → replace with ``iones``.
3. Words ending in ``ón`` → replace with ``ones``.
4. Words ending in ``án`` → replace with ``anes``.
5. Words ending in ``ín`` → replace with ``ines``.
6. Words ending in ``és`` → replace with ``eses``.
7. Words ending in ``x`` → invariable (no change).
8. Words ending in a vowel (including accented) → append ``s``.
9. Default (consonant ending, not ``x``) → append ``es``.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"iones$"), "ión"),
    (re.compile(r"(.{3,})ones$"), r"\1ón"),
    (re.compile(r"ces$"), "z"),
    (re.compile(r"([^aeiouáéíóú])es$"), r"\1"),
    (re.compile(r"s$"), ""),
]
"""Ordered Spanish singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``iones`` → replace with ``ión``.
2. Words ending in ``ones`` (3+ chars before) → replace with ``ón``.
3. Words ending in ``ces`` → replace with ``z``.
4. Words ending in consonant + ``es`` → strip ``es``.
5. Default: strip trailing ``s``.
"""

_UNCOUNTABLE: set[str] = {
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
}
"""Set of Spanish uncountable/invariable words.

Includes days of the week (``lunes``, ``martes``, ...), Greek-origin
words ending in ``is`` (``crisis``, ``análisis``, ...), words ending
in ``x`` (``tórax``, ``fax``, ...), compound words (``paraguas``,
``saltamontes``, ...), and foreign loanwords (``software``, ``web``,
``jazz``, ...).
"""

_RULES = LanguageRules(
    code="es",
    irregular_plurals=_IRREGULAR_PLURALS,
    irregular_singles=_IRREGULAR_SINGLES,
    plural_rules=_PLURAL_RULES,
    singular_rules=_SINGULAR_RULES,
    uncountable=_UNCOUNTABLE,
)
"""Spanish :class:`LanguageRules` instance registered as ``"es"``."""

register(_RULES)
