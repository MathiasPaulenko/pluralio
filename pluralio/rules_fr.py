"""French pluralization and singularization rules.

This module defines the complete set of French pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``fr`` language in the global registry.

The rules are organized into four categories:

1. **Irregular plurals**: Words that do not follow regex patterns
   and must be memorized. This includes ``-al`` words that take
   ``-als`` instead of the default ``-aux`` (e.g. ``"bal" →
   "bals"``, ``"festival" → "festivals"``), ``-ail`` words that
   take ``-aux`` (e.g. ``"travail" → "travaux"``), ``-ou`` words
   that take ``-oux`` (e.g. ``"bijou" → "bijoux"``), special
   plurals (``"œil" → "yeux"``, ``"monsieur" → "messieurs"``),
   and foreign loanwords (e.g. ``"weekend" → "weekends"``). The
   inverse mapping (plural → singular) is auto-generated.

2. **Extra singulars**: Additional plural → singular mappings that
   cannot be derived from the irregular plurals. These handle
   cases where the singular form requires a different ending than
   the regex would produce (e.g. ``"travaux" → "travail"``
   instead of ``"traval"``, ``"yeux" → "œil"``).

3. **Regex rules**: Ordered patterns applied to words that are not
   in the irregular or uncountable lists. The first matching rule
   wins. Rules cover common French pluralization patterns:
   - ``al`` → ``aux``, ``eau`` → ``eaux``, ``eu`` → ``eux``
   - ``s``/``x``/``z`` → invariable, default → add ``s``

4. **Uncountable words**: Words that are invariable — their plural
   form is identical to their singular form. This includes abstract
   nouns (``information``, ``courage``), materials (``or``, ``fer``),
   foods (``pain``, ``lait``), invariable ``-s``/``-x``/``-z`` words
   (``fois``, ``croix``, ``nez``), and foreign loanwords (``jazz``,
   ``rock``).

Known limitations:

- **``-aux`` ambiguity**: ``travaux → travail`` (should be ``-ail``,
  not ``-al``). Covered by ``_EXTRA_SINGLES`` for common words.
  Obscure ``-ail`` plurals will singularize to ``-al``.
- **``-ou`` vs ``-oux``**: Most ``-ou`` words take ``+s``
  (``trou → trous``). The ``-oux`` exceptions (``bijou → bijoux``)
  are in irregulars. Singularization of ``-oux`` → ``-ou`` is NOT
  in regex; handled by irregulars only.
- **``-al`` vs ``-als``**: Most ``-al`` words take ``-aux``, but
  ~7 exceptions take ``-als`` (``bal → bals``). These are in
  irregulars.

Reference: ``ref/rules.md`` for the full rules documentation.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_IRREGULAR_PLURALS: dict[str, str] = {
    # ── -al → -als (exceptions to the -aux rule) ──────────────────
    "bal": "bals", "festival": "festivals", "carnaval": "carnavals",
    "récital": "récitals", "cal": "cals", "pal": "pals",
    "narval": "narvals", "régal": "régals",
    "fatal": "fatals",
    "étal": "étals", "val": "vals",
    "gal": "gals", "recal": "recals",
    # ── -ail → -aux (exceptions to the +s rule) ───────────────────
    "travail": "travaux", "vitrail": "vitraux",
    "soupirail": "soupiraux", "corail": "coraux",
    "émail": "émaux", "fermail": "fermaux",
    "ventail": "ventaux",
    "bail": "baux",
    # ── -ou → -oux (exceptions to the +s rule) ────────────────────
    "bijou": "bijoux", "caillou": "cailloux", "hibou": "hiboux",
    "chou": "choux", "genou": "genoux", "pou": "poux",
    "joujou": "joujoux", "ripou": "ripoux",
    "gnou": "gnoux", "bayou": "bayoux",
    # ── -au → -aux (common words needing explicit mapping) ────────
    "tuyau": "tuyaux", "noyau": "noyaux", "boyau": "boyaux",
    "sarrau": "sarraux",
    # ── -eu → -eux (exceptions: most -eu words take -eux, but some take +s) ──
    "jeu": "jeux", "feu": "feux", "vœu": "vœux",
    # ── -eu → +s (exceptions to the -eux rule) ───────────────────
    "bleu": "bleus", "pneu": "pneus", "émeu": "émeus",
    # ── Special plurals (completely irregular) ────────────────────
    "œil": "yeux", "ciel": "cieux",
    "monsieur": "messieurs", "madame": "mesdames",
    "mademoiselle": "mesdemoiselles",
    "cour": "cours",
    # ── -al → -aux (common words needing explicit mapping) ────────
    "cheval": "chevaux", "animal": "animaux",
    "journal": "journaux", "général": "généraux",
    "hôpital": "hôpitaux", "capital": "capitaux",
    "signal": "signaux", "idéal": "idéaux",
    "bocal": "bocaux", "local": "locaux",
    "natal": "nataux", "royal": "royaux",
    "amiral": "amiraux", "rival": "rivaux",
    "cristal": "cristaux", "métal": "métaux",
    "principal": "principaux", "social": "sociaux",
    "spécial": "spéciaux", "normal": "normaux",
    "national": "nationaux", "rational": "rationaux",
    "international": "internationaux",
    "canal": "canaux",
    # ── Foreign loanwords (+s, regular but listed for safety) ──────
    "weekend": "weekends", "parking": "parkings",
    "shopping": "shoppings", "meeting": "meetings",
    "club": "clubs", "leader": "leaders",
    "record": "records", "star": "stars",
    "test": "tests", "sandwich": "sandwichs",
    "ketchup": "ketchups", "byte": "bytes",
    "code": "codes", "bug": "bugs",
    "script": "scripts", "server": "servers",
    "framework": "frameworks", "endpoint": "endpoints",
    "callback": "callbacks", "middleware": "middlewares",
    "pipeline": "pipelines", "token": "tokens",
    "container": "containers", "docker": "dockers",
}
"""Mapping of singular → plural for irregular French words.

Includes ``-al`` words that take ``-als`` instead of ``-aux``,
``-ail`` words that take ``-aux``, ``-ou`` words that take
``-oux``, special plurals (``œil → yeux``, ``monsieur →
messieurs``), and foreign loanwords. All keys and values are
lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_EXTRA_SINGLES: dict[str, str] = {
    # -aux → -ail (regex gives -al, but some come from -ail)
    "travaux": "travail", "vitraux": "vitrail",
    "soupiraux": "soupirail", "coraux": "corail",
    "émaux": "émail", "fermaux": "fermail",
    "ventaux": "ventail",
    "baux": "bail",
    # -aux → -au (regex gives -al, but these come from -au)
    "tuyaux": "tuyau", "noyaux": "noyau", "boyaux": "boyau",
    "sarraux": "sarrau",
    # Special
    "yeux": "œil", "cieux": "ciel",
    "messieurs": "monsieur", "mesdames": "madame",
    "mesdemoiselles": "mademoiselle",
    # -aux → -al (for words where singularization regex might not catch)
    "nationaux": "national", "rationaux": "rational",
    "internationaux": "international",
    # Accentless variants for robustness
    "ideaux": "ideal", "emaux": "email",
    "generaux": "general", "hopitaux": "hopital",
    "metaux": "metal", "signaux": "signal",
    "regaux": "regal", "recitaux": "recital",
    "voeux": "voeu",
    # Compound component: "aux" from "au" (e.g. pots-aux-feux → pot-au-feu)
    "aux": "au",
}
"""Additional plural → singular mappings for French.

These handle cases where the singular form requires a different
ending than the regex would produce. For example, ``"travaux"``
should singularize to ``"travail"`` (not ``"traval"``), and
``"yeux"`` should singularize to ``"œil"`` (not ``"yeul"``).
"""

_IRREGULAR_SINGLES.update(_EXTRA_SINGLES)

for _plural, _singular in _EXTRA_SINGLES.items():
    _IRREGULAR_PLURALS.setdefault(_singular, _plural)

_PLURAL_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"al$"), "aux"),
    (re.compile(r"eau$"), "eaux"),
    (re.compile(r"au$"), "aux"),
    (re.compile(r"eu$"), "eux"),
    (re.compile(r"([sxz])$"), r"\1"),
    (re.compile(r"$"), "s"),
]
"""Ordered French pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``al`` → replace with ``aux`` (cheval → chevaux;
   exceptions like bal → bals in irregulars).
2. Words ending in ``eau`` → replace with ``eaux`` (bateau → bateaux).
3. Words ending in ``au`` → replace with ``aux`` (tuyau → tuyaux).
   Must come after ``eau$`` to avoid double-matching.
4. Words ending in ``eu`` → replace with ``eux`` (jeu → jeux;
   exceptions like bleu → bleus in irregulars).
5. Words ending in ``s``, ``x``, or ``z`` → invariable (no change).
6. Default → append ``s`` (chat → chats, livre → livres).
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"eaux$"), "eau"),
    (re.compile(r"aux$"), "al"),
    (re.compile(r"eux$"), "eu"),
    (re.compile(r"s$"), ""),
]
"""Ordered French singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``eaux`` → replace with ``eau`` (bateaux → bateau).
   Must come before ``-aux`` rule.
2. Words ending in ``aux`` → replace with ``al`` (chevaux → cheval;
   ``-ail`` words handled by extra singles).
3. Words ending in ``eux`` → replace with ``eu`` (jeux → jeu).
4. Default: strip trailing ``s`` (chats → chat, maisons → maison).
"""

_UNCOUNTABLE: set[str] = {
    # Abstract/uncountable nouns
    "information", "recherche", "violence", "patience",
    "courage", "liberté", "justice", "beauté",
    "jeunesse", "vieillesse", "faiblesse", "sagesse",
    "richesse", "santé", "faim", "soif",
    "peur", "joie", "tristesse", "colère",
    "amour", "haine", "espoir", "désespoir",
    "temps", "argent", "or", "fer",
    "cuivre", "plomb", "bois", "verre",
    "papier", "cuir", "plastique", "caoutchouc",
    # Foods (uncountable)
    "pain", "lait", "beurre", "fromage",
    "sucre", "sel", "poivre", "riz",
    "farine", "viande", "porc", "jambon",
    # -s invariable
    "fois", "souris", "brebis",
    "poids", "rhinocéros", "virus",
    # -x invariable
    "croix", "voix", "noix",
    "choix", "prix",
    # -z invariable
    "nez",
    # Foreign (invariable)
    "jazz", "rock", "punk", "flash",
    # Always plural (pluralia tantum)
    "obsèques", "fiançailles", "ténèbres",
    "archives", "mathématiques",
    "fils", "ciseaux", "lunettes", "jumelles",
    "pincettes", "arrérages", "ambages",
    "fraîtures", "mœurs",
    "condoléances", "frais", "gens",
}
"""Set of French uncountable/invariable words.

Includes abstract nouns (``information``, ``courage``,
``liberté``), materials (``or``, ``fer``, ``cuivre``), foods
(``pain``, ``lait``, ``riz``), invariable ``-s`` words (``fois``,
``souris``, ``virus``), invariable ``-x`` words (``croix``,
``voix``, ``choix``), invariable ``-z`` words (``nez``), and
foreign loanwords (``jazz``, ``rock``, ``punk``, ``flash``).
"""

_RULES = LanguageRules(
    code="fr",
    irregular_plurals=_IRREGULAR_PLURALS,
    irregular_singles=_IRREGULAR_SINGLES,
    plural_rules=_PLURAL_RULES,
    singular_rules=_SINGULAR_RULES,
    uncountable=_UNCOUNTABLE,
)
"""French :class:`LanguageRules` instance registered as ``"fr"``."""

register(_RULES)
