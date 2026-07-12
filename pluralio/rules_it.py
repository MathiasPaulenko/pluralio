"""Italian pluralization and singularization rules.

This module defines the complete set of Italian pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``it`` language in the global registry.

The rules are organized into four categories:

1. **Irregular plurals**: Words that do not follow regex patterns
   and must be memorized. This includes sdrucciola ``-co`` → ``-ci``
   (e.g. ``"amico" → "amici"``), sdrucciola ``-go`` → ``-gi``
   (e.g. ``"asparago" → "asparagi"``), piana ``-go`` → ``-ghi``
   explicit mappings (e.g. ``"lago" → "laghi"``), completely
   irregular words (e.g. ``"uomo" → "uomini"``, ``"dio" → "dei"``),
   and foreign loanwords (e.g. ``"film" → "film"``).
   The inverse mapping (plural → singular) is auto-generated.

2. **Extra singulars**: Additional plural → singular mappings that
   cannot be derived from the irregular plurals. These handle cases
   where the singular form requires a different ending than the
   regex would produce (e.g. ``"amici" → "amico"``, ``"uova" → "uovo"``).

3. **Regex rules**: Ordered patterns applied to words that are not
   in the irregular or uncountable lists. The first matching rule
   wins. Rules cover common Italian pluralization patterns:
   - ``-ca`` → ``-che``, ``-ga`` → ``-ghe`` (feminine)
   - ``-co`` → ``-chi``, ``-go`` → ``-ghi`` (piana)
   - ``-io`` → ``-i``, ``-o`` → ``-i``, ``-a`` → ``-e``, ``-e`` → ``-i``
   - ``-s``/``-x`` → invariable, default → ``+i``

4. **Uncountable words**: Words that are invariable — their plural
   form is identical to their singular form. This includes foreign
   loanwords (``film``, ``bar``, ``computer``), Greek-origin forms
   in ``-i`` (``analisi``, ``crisi``), pluralia tantum (``occhiali``,
   ``forbici``), and truncated forms (``foto``, ``auto``).

Known limitations:

- **``-i`` ambiguity**: ``-i`` can come from ``-o`` (``libri → libro``),
  ``-e`` (``cani → cane``), or ``-io`` (``vizi → vizio``). Regex
  defaults to ``-o``; ``-e`` and ``-io`` words are in irregulars/
  extra singles for common cases.
- **``-co``/``-go`` split**: Regex always produces ``-chi``/``-ghi``
  (piana). Sdrucciola words (``amico → amici``) are in irregulars.
- **``-ci``/``-gi`` singularization**: Regex gives ``-ce``/``-ge``
  (``luci → luce``), but ``-co``/``-go`` words (``amici → amico``)
  need extra singles.
- **Stress detection**: Italian stress is not marked orthographically.
  Regex can't detect stress position, so the ``-co``/``-go`` split
  relies on irregulars.

Reference: ``ref/rules.md`` for the full rules documentation.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_IRREGULAR_PLURALS: dict[str, str] = {
    "amico": "amici", "medico": "medici", "nemico": "nemici",
    "logico": "logici", "magico": "magici", "tragico": "tragici",
    "comico": "comici", "filosofico": "filosofici",
    "storico": "storici", "geografico": "geografici",
    "biologo": "biologi", "psicologo": "psicologi",
    "teologo": "teologi", "archeologo": "archeologi",
    "tecnico": "tecnici", "politico": "politici",
    "pratico": "pratici", "identico": "identici",
    "simpatico": "simpatici", "dinamico": "dinamici",
    "romantico": "romantici", "sintatico": "sintatici",
    "pubblico": "pubblici", "tedesco": "tedeschi",
    "asparago": "asparagi",
    "lago": "laghi", "fuoco": "fuochi",
    "luogo": "luoghi", "gioco": "giochi",
    "porco": "porci",
    "uomo": "uomini", "moglie": "mogli",
    "dio": "dei", "tempio": "templi",
    "bue": "buoi", "ala": "ali",
    "arma": "armi", "dito": "dita",
    "osso": "ossa", "labbro": "labbra",
    "ginocchio": "ginocchia", "occhio": "occhi",
    "orecchio": "orecchi", "uovo": "uova",
    "paio": "paia", "miglio": "miglia",
    "centinaio": "centinaia", "migliaio": "migliaia",
    "cane": "cani", "fiore": "fiori", "pane": "pani", "amore": "amori",
    "vizio": "vizi", "figlio": "figli", "orologio": "orologi", "inizio": "inizi",
    "film": "film", "bar": "bar", "bus": "bus",
    "computer": "computer", "sport": "sport",
    "taxi": "taxi", "metro": "metro",
    "weekend": "weekend", "meeting": "meeting",
    "club": "club", "leader": "leader",
    "test": "test", "code": "code",
    "server": "server", "framework": "framework",
    "token": "token", "container": "container",
    "docker": "docker", "script": "script",
}
"""Mapping of singular → plural for irregular Italian words.

Includes sdrucciola ``-co`` → ``-ci`` and ``-go`` → ``-gi`` words,
piana ``-go`` → ``-ghi`` explicit mappings, completely irregular
words, and foreign loanwords. All keys and values are lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_EXTRA_SINGLES: dict[str, str] = {
    "giochi": "gioco", "fuochi": "fuoco",
    "luoghi": "luogo",
    "laghi": "lago",
    "amici": "amico", "medici": "medico",
    "nemici": "nemico",
    "asparagi": "asparago",
    "uomini": "uomo", "buoi": "bue",
    "mogli": "moglie", "templi": "tempio",
    "uova": "uovo", "ossa": "osso",
    "dita": "dito", "paia": "paio",
    "centinaia": "centinaio", "migliaia": "migliaio",
}
"""Additional plural → singular mappings for Italian.

These handle cases where the singular form requires a different
ending than the regex would produce. For example, ``"amici"``
should singularize to ``"amico"`` (not ``"amice"``), and
``"uova"`` should singularize to ``"uovo"`` (not ``"uova"``).
"""

_IRREGULAR_SINGLES.update(_EXTRA_SINGLES)

for _plural, _singular in _EXTRA_SINGLES.items():
    _IRREGULAR_PLURALS.setdefault(_singular, _plural)

_PLURAL_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"ca$"), "che"),
    (re.compile(r"ga$"), "ghe"),
    (re.compile(r"co$"), "chi"),
    (re.compile(r"go$"), "ghi"),
    (re.compile(r"che$"), r"\g<0>"),
    (re.compile(r"ghe$"), r"\g<0>"),
    (re.compile(r"chi$"), r"\g<0>"),
    (re.compile(r"ghi$"), r"\g<0>"),
    (re.compile(r"io$"), "i"),
    (re.compile(r"o$"), "i"),
    (re.compile(r"a$"), "e"),
    (re.compile(r"e$"), "i"),
    (re.compile(r"i$"), r"\g<0>"),
    (re.compile(r"[sx]$"), r"\g<0>"),
    (re.compile(r"$"), "i"),
]
"""Ordered Italian pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``ca`` → replace with ``che`` (amica → amiche).
2. Words ending in ``ga`` → replace with ``ghe`` (lega → leghe).
3. Words ending in ``co`` → replace with ``chi`` (banco → banchi;
   sdrucciola exceptions in irregulars).
4. Words ending in ``go`` → replace with ``ghi`` (lago → laghi;
   sdrucciola exceptions in irregulars).
5-8. Words ending in ``che``, ``ghe``, ``chi``, ``ghi`` → invariable
   (already plural, idempotency).
9. Words ending in ``io`` → replace with ``i`` (vizio → vizi).
10. Words ending in ``o`` → replace with ``i`` (libro → libri).
11. Words ending in ``a`` → replace with ``e`` (casa → case).
12. Words ending in ``e`` → replace with ``i`` (cane → cani).
13. Words ending in ``i`` → invariable (already plural, idempotency).
14. Words ending in ``s`` or ``x`` → invariable (no change).
15. Default → append ``i``.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"che$"), "ca"),
    (re.compile(r"ghe$"), "ga"),
    (re.compile(r"chi$"), "co"),
    (re.compile(r"ghi$"), "go"),
    (re.compile(r"ci$"), "ce"),
    (re.compile(r"gi$"), "ge"),
    (re.compile(r"i$"), "o"),
    (re.compile(r"e$"), "a"),
]
"""Ordered Italian singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``che`` → replace with ``ca`` (amiche → amica).
2. Words ending in ``ghe`` → replace with ``ga`` (leghe → lega).
3. Words ending in ``chi`` → replace with ``co`` (banchi → banco).
4. Words ending in ``ghi`` → replace with ``go`` (laghi → lago).
5. Words ending in ``ci`` → replace with ``ce`` (luci → luce;
   ``-co`` words handled by extra singles).
6. Words ending in ``gi`` → replace with ``ge``.
7. Words ending in ``i`` → replace with ``o`` (libri → libro;
   ``-e`` and ``-io`` words handled by extra singles).
8. Words ending in ``e`` → replace with ``a`` (case → casa).
"""

_UNCOUNTABLE: set[str] = {
    "film", "bar", "bus", "computer", "sport",
    "taxi", "metro", "weekend", "meeting",
    "club", "leader", "test", "code",
    "server", "framework", "token", "container",
    "docker", "script", "software", "hardware",
    "web", "blog", "chat", "spam",
    "jazz", "rock", "punk", "flash",
    "brindisi", "analisi", "tesi", "crisi",
    "oasi", "sintesi", "ipotesi", "diagnosi",
    "paralisi", "catarsi",
    "specie", "serie", "voce",
    "caffè",
    "occhiali", "forbici", "pantaloni",
    "soldi", "nozze", "stoviglie",
    "vettovaglie",
    "foto", "moto", "radio", "cinema",
    "auto", "biliardo",
}
"""Set of Italian uncountable/invariable words.

Includes foreign loanwords (``film``, ``bar``, ``computer``),
Greek-origin forms in ``-i`` (``analisi``, ``crisi``, ``tesi``),
pluralia tantum (``occhiali``, ``forbici``, ``pantaloni``),
invariable ``-e`` words (``specie``, ``serie``, ``voce``),
and truncated forms (``foto``, ``moto``, ``auto``).
"""

_RULES = LanguageRules(
    code="it",
    irregular_plurals=_IRREGULAR_PLURALS,
    irregular_singles=_IRREGULAR_SINGLES,
    plural_rules=_PLURAL_RULES,
    singular_rules=_SINGULAR_RULES,
    uncountable=_UNCOUNTABLE,
)
"""Italian :class:`LanguageRules` instance registered as ``"it"``."""

register(_RULES)
