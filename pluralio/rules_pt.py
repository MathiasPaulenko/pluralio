"""Portuguese pluralization and singularization rules.

This module defines the complete set of Portuguese pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``pt`` language in the global registry.

The rules are organized into four categories:

1. **Irregular plurals**: Words that do not follow regex patterns
   and must be memorized. This includes words ending in ``-ão``
   that take ``-ães`` or ``-ãos`` instead of the default ``-ões``
   (e.g. ``"cão" → "cães"``, ``"irmão" → "irmãos"``), words with
   accent shifts in the plural (e.g. ``"papel" → "papéis"``,
   ``"sol" → "sóis"``), and foreign loanwords (e.g. ``"club" →
   "clubs"``). The inverse mapping (plural → singular) is
   auto-generated.

2. **Extra singulars**: Additional plural → singular mappings that
   cannot be derived from the irregular plurals. These handle
   cases where the singular form requires an accent that the
   plural does not have (e.g. ``"papéis" → "papel"``,
   ``"sóis" → "sol"``) or where the regex singularization would
   produce the wrong result (e.g. ``"portugueses" → "português"``).

3. **Regex rules**: Ordered patterns applied to words that are not
   in the irregular or uncountable lists. The first matching rule
   wins. Rules cover common Portuguese pluralization patterns:
   - ``ão`` → ``ões``, ``m`` → ``ns``, ``l`` → ``is``
   - ``r`` → ``res``, ``z`` → ``zes``
   - ``x`` → invariable, vowel ending → add ``s``

4. **Uncountable words**: Words that are invariable — their plural
   form is identical to their singular form. This includes words
   ending in ``x`` (``tórax``, ``látex``), invariable ``-s`` words
   (``lápis``, ``vírus``), compound words (``guarda-chuva``,
   ``beija-flor``), and foreign loanwords (``software``, ``web``,
   ``jazz``).

Known limitations:

- **Accent restoration**: ``-ões → -ão`` works via regex (tilde
  restored), but ``-éis → -el`` and ``-óis → -ol`` lose accents.
  Covered by ``_EXTRA_SINGLES`` for common words.
- **-ão split**: Regex always produces ``-ões``, but ~20% of
  ``-ão`` words take ``-ães`` or ``-ãos``. These are in
  irregulars.
- **-s ambiguity**: ``meses → mes`` (should be ``mês``). Covered
  by extra singles for common words.
- **-es → strip s**: ``portugueses → portuguê`` (should be
  ``português``). Covered by extra singles.

Reference: ``ref/rules.md`` for the full rules documentation.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_IRREGULAR_PLURALS: dict[str, str] = {
    # -ão → -ões (most common ~70%; also in irregulars for singularization)
    "coração": "corações", "canção": "canções", "balão": "balões",
    "feijão": "feijões", "limão": "limões", "leão": "leões",
    "botão": "botões", "feição": "feições", "travão": "travões",
    "estação": "estações", "nação": "nações", "opinião": "opiniões",
    "relação": "relações", "função": "funções", "instrução": "instruções",
    # -ão → -ães (smaller group, regex can't produce this)
    "cão": "cães", "alemão": "alemães", "capitão": "capitães",
    "charlatão": "charlatães", "sacristão": "sacristães",
    "escrivão": "escrivães", "pão": "pães",
    # -ão → -ãos (just +s, regex would give -ões)
    "irmão": "irmãos", "mão": "mãos", "chão": "chãos",
    "cristão": "cristãos", "cidadão": "cidadãos", "órgão": "órgãos",
    "grão": "grãos", "são": "sãos",
    # Accent ADDS in plural (-el → -éis)
    "papel": "papéis", "nível": "níveis", "fóssil": "fósseis",
    "fácil": "fáceis", "réptil": "répteis", "míssil": "mísseis",
    # Accent ADDS in plural (-ol → -óis)
    "sol": "sóis", "farol": "faróis", "anzol": "anzóis",
    "caracol": "caracóis", "lençol": "lençóis",
    # -il (oxítona) → -is (no accent change, regex handles -il → -is)
    "barril": "barris", "funil": "funis", "fuzil": "fuzis",
    # -el → -éis (accent, not in default regex)
    "mel": "méis", "fiel": "fiéis",
    # -il (paroxítona) → -eis (accent change, must be irregular)
    "projétil": "projéteis",
    # -s → -ses (accented singulars that need ses, not es)
    "gás": "gases", "país": "países", "deus": "deuses",
    # Monosyllables / special
    "bem": "bens",
    # Foreign loanwords (+s, not +es)
    "club": "clubs", "chip": "chips", "bit": "bits",
    "email": "emails", "link": "links", "banner": "banners",
    "server": "servers", "router": "routers", "token": "tokens",
    "docker": "dockers", "container": "containers",
}
"""Mapping of singular → plural for irregular Portuguese words.

Includes ``-ão`` words that take ``-ães`` or ``-ãos`` instead of
``-ões``, words with accent shifts in the plural (``-el → -éis``,
``-ol → -óis``), and foreign loanwords. All keys and values are
lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_EXTRA_SINGLES: dict[str, str] = {
    # -ões → -ão (regex ões → ão already restores tilde, but include for safety)
    "corações": "coração", "canções": "canção", "balões": "balão",
    "feijões": "feijão", "limões": "limão", "leões": "leão",
    "botões": "botão", "estações": "estação", "nações": "nação",
    "relações": "relação", "funções": "função",
    # -ães → -ão
    "cães": "cão", "alemães": "alemão", "capitães": "capitão",
    "pães": "pão", "charlatães": "charlatão",
    # -éis → -el (regex is → l loses accent)
    "papéis": "papel", "níveis": "nível",
    "méis": "mel", "fiéis": "fiel",
    # -óis → -ol (regex is → l loses accent)
    "sóis": "sol", "faróis": "farol", "anzóis": "anzol",
    "lençóis": "lençol", "caracóis": "caracol",
    # -es → -ês (accent restoration for -s words)
    "portugueses": "português", "japoneses": "japonês",
    # -s ambiguity (meses → mês, not mese)
    "meses": "mês",
    # vowel + is (not from -l, strip s not replace with l)
    "leis": "lei", "reis": "rei", "pais": "pai",
    # vowel + consonant + e (singularization gives consonant only)
    "árvores": "árvore",
}
"""Additional plural → singular mappings for Portuguese.

These handle accent restoration cases where the singular form
requires an accent mark that the plural form does not have, or
where the regex singularization would produce the wrong result.
For example, ``"papel"`` → ``"papéis"`` (plural adds accent), so
the reverse mapping ``"papéis" → "papel"`` must be explicit.
Also covers ``"portugueses" → "português"`` where the regex would
incorrectly produce ``"portuguese"``.
"""

_IRREGULAR_SINGLES.update(_EXTRA_SINGLES)

for _plural, _singular in _EXTRA_SINGLES.items():
    _IRREGULAR_PLURALS.setdefault(_singular, _plural)

_PLURAL_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"ão$"), "ões"),
    (re.compile(r"m$"), "ns"),
    (re.compile(r"il$"), "is"),
    (re.compile(r"l$"), "is"),
    (re.compile(r"r$"), "res"),
    (re.compile(r"z$"), "zes"),
    (re.compile(r"x$"), "x"),
    (re.compile(r"([aeiouáéíóúâêôãõ])$"), r"\1s"),
]
"""Ordered Portuguese pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``ão`` → replace with ``ões`` (most common ~70%).
2. Words ending in ``m`` → replace with ``ns``.
3. Words ending in ``il`` → replace with ``is`` (handles ``-il`` oxítona).
4. Words ending in ``l`` → replace with ``is`` (handles ``-al``, ``-ul``).
5. Words ending in ``r`` → append ``es`` (``r`` + ``es``).
6. Words ending in ``z`` → replace with ``zes``.
7. Words ending in ``x`` → invariable (no change).
8. Words ending in a vowel (including accented) → append ``s``.

Note: Words ending in ``s`` are handled by irregulars (accented
singulars like ``gás``, ``país``) or are already plural (``casas``,
``livros``) and returned unchanged by the engine.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"ões$"), "ão"),
    (re.compile(r"ães$"), "ão"),
    (re.compile(r"zes$"), "z"),
    (re.compile(r"ns$"), "m"),
    (re.compile(r"([^aeiouáéíóúâêôãõ])is$"), r"\1il"),
    (re.compile(r"is$"), "l"),
    (re.compile(r"([^aeiouáéíóúâêôãõs])([^aeiouáéíóúâêôãõs])es$"), r"\1\2e"),
    (re.compile(r"tes$"), "te"),
    (re.compile(r"des$"), "de"),
    (re.compile(r"mes$"), "me"),
    (re.compile(r"les$"), "le"),
    (re.compile(r"res$"), "r"),
    (re.compile(r"s$"), ""),
]
"""Ordered Portuguese singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``ões`` → replace with ``ão`` (restores tilde).
2. Words ending in ``ães`` → replace with ``ão``.
3. Words ending in ``zes`` → replace with ``z``.
4. Words ending in ``ns`` → replace with ``m``.
5. Words ending in consonant + ``is`` → replace with consonant + ``il``
   (handles ``-il`` words like ``cantil``, ``redil``).
6. Words ending in ``is`` → replace with ``l`` (handles ``-al``, ``-ul``;
   loses accent on ``-éis`` and ``-óis``; covered by ``_EXTRA_SINGLES``).
7. Words ending in two consonants + ``es`` → strip ``s`` only
   (handles ``e``-ending words like ``nome``, ``filme``, ``noite``).
8. Words ending in ``tes`` → strip ``s`` (handles ``te``-ending words).
9. Words ending in ``des`` → strip ``s`` (handles ``de``-ending words).
10. Words ending in ``mes`` → strip ``s`` (handles ``me``-ending words).
11. Words ending in ``les`` → strip ``s`` (handles ``le``-ending words).
12. Words ending in ``res`` → replace with ``r`` (handles ``-r`` words
   like ``flor``, ``motor`` that take ``-es`` in plural).
13. Default: strip trailing ``s``.
"""

_UNCOUNTABLE: set[str] = {
    # -x (invariable)
    "tórax", "látex", "clímax", "sintaxe",
    "fax", "xerox", "telex", "complex", "duplex",
    "simplex", "suplex", "sex", "mix", "index",
    "matrix", "flex",
    # -e (invariable slang)
    "fixe",
    # -ps (anatomical, invariable)
    "bíceps", "tríceps", "quadríceps", "fórceps",
    # Greek/biblical -is (invariable)
    "oásis", "gênesis",
    # -s (invariable)
    "lápis", "atlas", "vírus", "ônibus", "óculos",
    "férias", "núpcias", "cócegas", "afazeres",
    "três", "mais", "cais", "dois",
    "pires", "ourives", "cosmos", "seis",
    # Adverbs (invariable)
    "menos", "jamais",
    # Pronouns (invariable)
    "nós", "vós",
    # Compound words
    "guarda-chuva", "beija-flor", "passa-tempo",
    # Music genres (invariable)
    "blues", "soul", "funk", "reggae", "folk", "metal",
    # Foreign loanwords (invariable)
    "software", "hardware", "web", "blog", "chat",
    "spam", "jazz", "rock", "punk", "flash",
    "post", "marketing", "design", "streaming", "podcast",
    "feed", "cache", "cookie", "shell", "framework",
    "kernel", "cloud", "backend", "frontend", "deploy",
    "commit", "build", "runtime", "pipeline", "workflow",
    "sandbox", "socket", "proxy", "thread", "host",
    "node", "switch", "hub", "ping", "byte",
    # Sports/games (invariable)
    "rugby", "skate", "poker", "darts",
    # Culture (invariable)
    "hacker", "nerd", "geek",
    # Tech actions (invariable)
    "download", "upload", "screenshot", "backup", "fallback",
}
"""Set of Portuguese uncountable/invariable words.

Includes words ending in ``x`` (``tórax``, ``látex``, ``fax``,
``complex``), anatomical ``-ps`` words (``bíceps``, ``tríceps``,
``fórceps``), Greek/biblical ``-is`` words (``oásis``, ``gênesis``),
invariable ``-s`` words (``lápis``, ``vírus``, ``óculos``, ``férias``,
``pires``, ``ourives``), compound words (``guarda-chuva``,
``beija-flor``, ``passa-tempo``), music genres (``blues``, ``soul``,
``funk``, ``reggae``), and foreign loanwords (``software``, ``web``,
``jazz``, ``rock``, ``deploy``, ``commit``).
"""

_RULES = LanguageRules(
    code="pt",
    irregular_plurals=_IRREGULAR_PLURALS,
    irregular_singles=_IRREGULAR_SINGLES,
    plural_rules=_PLURAL_RULES,
    singular_rules=_SINGULAR_RULES,
    uncountable=_UNCOUNTABLE,
)
"""Portuguese :class:`LanguageRules` instance registered as ``"pt"``."""

register(_RULES)
