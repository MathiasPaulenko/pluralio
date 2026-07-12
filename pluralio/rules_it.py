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
    "notte": "notti", "mente": "menti", "fronte": "fronti",
    "sede": "sedi", "parte": "parti", "classe": "classi",
    "noce": "noci", "fede": "fedi", "pace": "paci",
    "croce": "croci", "gente": "genti", "nave": "navi",
    "valle": "valli", "parete": "pareti", "radice": "radici",
    "voce": "voci",
    "bacio": "baci", "spazio": "spazi", "ufficio": "uffici",
    "socio": "soci", "cambio": "cambi", "esempio": "esempi",
    "principio": "principi", "stadio": "stadi", "negozio": "negozi",
    "formaggio": "formaggi", "viaggio": "viaggi", "raggio": "raggi",
    "coraggio": "coraggi", "passaggio": "passaggi", "messaggio": "messaggi",
    "casa": "case", "scuola": "scuole", "banana": "banane",
    "gatta": "gatte", "pasta": "paste", "pianta": "piante",
    "famiglia": "famiglie", "squadra": "squadre", "festa": "feste",
    "donna": "donne", "ragazza": "ragazze", "macchina": "macchine",
    "piazza": "piazze", "pizza": "pizze", "bambina": "bambine",
    "sedia": "sedie", "chiave": "chiavi", "isola": "isole",
    "forchetta": "forchette", "spina": "spine", "pietra": "pietre",
    "roba": "robe", "camicia": "camicie", "montagna": "montagne",
    "stella": "stelle", "barca": "barche",
    "cuore": "cuori", "studente": "studenti", "dente": "denti",
    "nome": "nomi", "sole": "soli", "colore": "colori", "valore": "valori",
    "dottore": "dottori", "signore": "signori", "attore": "attori",
    "professore": "professori", "imperatore": "imperatori",
    "scultore": "scultori", "pittore": "pittori", "scrittore": "scrittori",
    "superficie": "superfici", "effigie": "effigi",
    "studio": "studi", "esercizio": "esercizi",
    "pioggia": "piogge", "valigia": "valigie",
    "roccia": "rocce", "fascia": "fasce", "ascia": "asce",
    "problema": "problemi", "tema": "temi", "sistema": "sistemi",
    "poema": "poemi", "clima": "climi", "dramma": "drammi",
    "programma": "programmi", "telegramma": "telegrammi",
    "schema": "schemi", "dogma": "dogmi", "emblema": "emblemi",
    "idioma": "idiomi", "fantasma": "fantasmi", "pirata": "pirati",
    "poeta": "poeti", "collega": "colleghi", "atleta": "atleti",
    "artista": "artisti", "autista": "autisti", "giornalista": "giornalisti",
    "linguista": "linguisti", "turista": "turisti", "astronauta": "astronauti",
    "fiume": "fiumi", "ponte": "ponti", "cliente": "clienti",
    "residente": "residenti", "presidente": "presidenti",
    "generale": "generali", "animale": "animali", "fossile": "fossili",
    "fucile": "fucili", "cortile": "cortili", "volgare": "volgari",
    "regolare": "regolari", "singolare": "singolari", "particolare": "particolari",
    "borsa": "borse", "coppia": "coppie", "porta": "porte",
    "torta": "torte", "tazza": "tazze", "sala": "sale",
    "ruota": "ruote", "penna": "penne", "palla": "palle",
    "tela": "tele", "sorella": "sorelle", "frusta": "fruste",
    "braccio": "braccia", "lenzuolo": "lenzuola", "ciglio": "ciglia",
    "laccio": "lacci", "straccio": "stracci", "sacrificio": "sacrifici",
    "abbraccio": "abbracci", "obbligo": "obblighi",
    "torre": "torri", "corte": "corti", "sorte": "sorti",
    "morte": "morti", "canzone": "canzoni",
}
"""Mapping of singular → plural for irregular Italian words.

Includes sdrucciola ``-co`` → ``-ci`` and ``-go`` → ``-gi`` words,
piana ``-go`` → ``-ghi`` explicit mappings, completely irregular
words, common feminine ``-e`` singulars, masculine ``-io``/``-cio``
/``-gio`` words, feminine ``-a`` words for plural idempotency,
masculine ``-e`` words for round-trip, Greek-origin masculine ``-a``
words, ``-ie`` feminine words, and additional feminine ``-a`` words
for plural idempotency. All keys and values are lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_EXTRA_SINGLES: dict[str, str] = {}
"""Additional plural → singular mappings for Italian.

All necessary mappings are auto-generated from the inverse of
``_IRREGULAR_PLURALS``. This dict is kept empty for structural
consistency with other language modules.
"""

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
    (re.compile(r"([bcdfghlmnpqrstvz])([cg])ia$"), r"\1\2e"),
    (re.compile(r"([aeiou])([cg])ia$"), r"\1\2ie"),
    (re.compile(r"a$"), "e"),
    (re.compile(r"ie$"), "i"),
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
10. Words ending in ``o`` → replace with ``i`` (libro → libri).
11. Consonant + ``ia`` → replace with ``e`` (pioggia → piogge).
12. Words ending in ``a`` → replace with ``e`` (casa → case).
13. Words ending in ``ie`` → replace with ``i`` (superficie → superfici).
14. Words ending in ``e`` → replace with ``i`` (cane → cani).
15. Words ending in ``i`` → invariable (already plural, idempotency).
16. Words ending in ``s`` or ``x`` → invariable (no change).
17. Default → append ``i``.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"che$"), "ca"),
    (re.compile(r"ghe$"), "ga"),
    (re.compile(r"chi$"), "co"),
    (re.compile(r"ghi$"), "go"),
    (re.compile(r"([bcdfghlmnpqrstvz])([cg])e$"), r"\1\2ia"),
    (re.compile(r"ci$"), "ce"),
    (re.compile(r"gi$"), "ge"),
    (re.compile(r"ioni$"), "ione"),
    (re.compile(r"tori$"), "tore"),
    (re.compile(r"i$"), "o"),
    (re.compile(r"e$"), "a"),
]
"""Ordered Italian singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``che`` → replace with ``ca`` (amiche → amica).
2. Words ending in ``ghe`` → replace with ``ga`` (leghe → lega).
3. Words ending in ``chi`` → replace with ``co`` (banchi → banco).
4. Words ending in ``ghi`` → replace with ``go`` (laghi → lago).
5. Consonant + ``ce`` → replace with ``cia`` (rocce → roccia).
6. Consonant + ``ge`` → replace with ``gia`` (piogge → pioggia).
7. Words ending in ``ci`` → replace with ``ce`` (luci → luce;
   ``-co`` words handled by extra singles).
8. Words ending in ``gi`` → replace with ``ge``.
9. Words ending in ``ioni`` → replace with ``ione`` (nazioni → nazione).
10. Words ending in ``tori`` → replace with ``tore`` (dottori → dottore).
11. Words ending in ``i`` → replace with ``o`` (libri → libro;
   ``-e`` and ``-io`` words handled by extra singles).
12. Words ending in ``e`` → replace with ``a`` (case → casa).
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
    "specie", "serie",
    "caffè", "noir",
    "occhiali", "forbici", "pantaloni",
    "soldi", "nozze", "stoviglie",
    "vettovaglie",
    "foto", "moto", "radio", "cinema",
    "auto", "biliardo",
    "streaming", "download", "upload", "post",
    "hashtag", "follower", "like", "share",
    "tweet", "link", "click", "login",
    "logout", "reset", "backup", "input",
    "output", "format", "record", "report",
    "budget", "shock", "stop", "start",
    "loop", "cross", "short", "spot",
    "sketch", "show", "preview", "trailer",
    "remake", "sequel", "break", "flop",
    "tennis", "golf", "hockey", "rugby",
    "match", "round", "ring", "volley",
    "sprint", "set", "staff",
    "città", "virtù", "tè", "perché",
    "cioè", "sé", "lunedì", "martedì",
    "mercoledì", "giovedì", "venerdì",
    "sabato", "domenica",
}
"""Set of Italian uncountable/invariable words.

Includes foreign loanwords (``film``, ``bar``, ``computer``, ``streaming``,
``download``, ``link``, ``click``), Greek-origin forms in ``-i``
(``analisi``, ``crisi``, ``tesi``), pluralia tantum (``occhiali``,
``forbici``, ``pantaloni``), invariable ``-e`` words (``specie``,
``serie``), truncated forms (``foto``, ``moto``, ``auto``), accented
invariables (``città``, ``virtù``, ``tè``, ``perché``), days of the week
(``lunedì``–``domenica``), and sports terms (``tennis``, ``golf``,
``hockey``, ``rugby``).
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
