"""English pluralization and singularization rules.

This module defines the complete set of English pluralization
rules used by pluralio. It is imported automatically when
``import pluralio`` is executed, which triggers the registration
of the ``en`` language in the global registry.

The rules are organized into three categories:

1. **Irregular plurals**: Words that do not follow any regex pattern
   and must be memorized (e.g. ``"man" → "men"``, ``"child" → "children"``).
   The inverse mapping (plural → singular) is auto-generated.

2. **Regex rules**: Ordered patterns applied to words that are not
   in the irregular or uncountable lists. The first matching rule
   wins. Rules are ordered from most specific to least specific.

3. **Uncountable words**: Words that are invariable — their plural
   form is identical to their singular form (e.g. ``"sheep"``,
   ``"information"``, ``"rice"``).

Reference: ``ref/rules.md`` for the full rules documentation.
"""

from __future__ import annotations

import re

from pluralio.registry import LanguageRules, register

_IRREGULAR_PLURALS: dict[str, str] = {
    "man": "men", "woman": "women", "child": "children",
    "person": "people", "mouse": "mice", "goose": "geese",
    "foot": "feet", "tooth": "teeth", "ox": "oxen",
    "die": "dice", "yes": "yeses",
    "cactus": "cacti", "nucleus": "nuclei", "alumnus": "alumni",
    "radius": "radii", "focus": "foci", "fungus": "fungi",
    "stimulus": "stimuli", "syllabus": "syllabi",
    "phenomenon": "phenomena", "criterion": "criteria",
    "datum": "data", "medium": "media", "bacterium": "bacteria",
    "curriculum": "curricula", "memorandum": "memoranda",
    "spectrum": "spectra", "stratum": "strata",
    "analysis": "analyses", "basis": "bases", "crisis": "crises",
    "diagnosis": "diagnoses", "hypothesis": "hypotheses",
    "oasis": "oases", "parenthesis": "parentheses",
    "thesis": "theses", "axis": "axes",
    "matrix": "matrices", "index": "indices",
    "appendix": "appendices", "vertex": "vertices",
    "wolf": "wolves", "half": "halves", "calf": "calves",
    "leaf": "leaves", "loaf": "loaves", "thief": "thieves",
    "self": "selves", "shelf": "shelves",
    "wife": "wives", "knife": "knives", "life": "lives",
    "hoof": "hooves",
    "potato": "potatoes", "tomato": "tomatoes", "hero": "heroes",
    "echo": "echoes", "veto": "vetoes", "torpedo": "torpedoes",
    "mosquito": "mosquitoes", "volcano": "volcanoes",
    "photo": "photos", "piano": "pianos", "halo": "halos",
    "pie": "pies", "tie": "ties", "movie": "movies",
    "cookie": "cookies", "selfie": "selfies",
    "bus": "buses", "quiz": "quizzes",
    "status": "statuses", "virus": "viruses",
    # Exceptions to fe → ves rule (just add s)
    "cafe": "cafes", "safe": "safes", "giraffe": "giraffes",
    "strafe": "strafes",
    # Exceptions to consonant+f → ves rule (just add s)
    "turf": "turfs", "golf": "golfs", "dwarf": "dwarfs",
    "brief": "briefs", "chief": "chiefs", "roof": "roofs",
    "proof": "proofs", "belief": "beliefs", "relief": "reliefs",
    # Exceptions to consonant+o → oes rule (just add s)
    "solo": "solos", "cello": "cellos", "disco": "discos",
    "memo": "memos", "auto": "autos", "ego": "egos",
    "kilo": "kilos", "tempo": "tempos", "turbo": "turbos",
    "dynamo": "dynamos", "lasso": "lassos", "jumbo": "jumbos",
    "memento": "mementos", "logo": "logos", "embryo": "embryos",
    "ghetto": "ghettos", "concerto": "concertos", "soprano": "sopranos",
    "combo": "combos", "pro": "pros",
    "casino": "casinos", "taco": "tacos", "burrito": "burritos",
    "poncho": "ponchos", "sombrero": "sombreros", "flamingo": "flamingos",
    "tornado": "tornados", "avocado": "avocados",
    # Exceptions to oes → o singular rule (strip s only)
    "shoe": "shoes", "foe": "foes", "hoe": "hoes",
    "toe": "toes", "doe": "does",
    "aloe": "aloes", "oboe": "oboes", "canoe": "canoes",
    # Words where singular ends in s (plural adds es, singular must strip es)
    "gas": "gases", "boss": "bosses",
    "lens": "lenses", "plus": "pluses", "cross": "crosses",
    # Short words ending in o (need irregular for correct singularization)
    "go": "goes", "so": "sos", "no": "noes",
    # do → does (placed after doe → does so do wins in _IRREGULAR_SINGLES)
    "do": "does",
}
"""Mapping of singular → plural for irregular English words.

These words do not follow any regex pattern and must be looked up
directly. All keys and values are lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_IRREGULAR_SINGLES["dwarves"] = "dwarf"
"""Additional singular for ``dwarves`` (alternative plural of ``dwarf``)."""

_PLURAL_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(s|ss|sh|ch|x|z)$"), r"\1es"),
    (re.compile(r"([^aeiou])y$"), r"\1ies"),
    (re.compile(r"fe$"), "ves"),
    (re.compile(r"([^aeiou])f$"), r"\1ves"),
    (re.compile(r"([^aeiou])o$"), r"\1oes"),
    (re.compile(r"$"), "s"),
]
"""Ordered English pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``s``, ``ss``, ``sh``, ``ch``, ``x``, ``z`` → add ``es``.
2. Words ending in consonant + ``y`` → replace ``y`` with ``ies``.
3. Words ending in ``fe`` → replace with ``ves``.
4. Words ending in consonant + ``f`` → replace ``f`` with ``ves``.
5. Words ending in consonant + ``o`` → replace ``o`` with ``oes``.
6. Default: append ``s``.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"ies$"), "y"),
    (re.compile(r"(ss|sh|ch|x|z|s)es$"), r"\1"),
    (re.compile(r"s$"), ""),
]
"""Ordered English singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``ies`` → replace with ``y``.
2. Words ending in ``s``, ``ss``, ``sh``, ``ch``, ``x``, ``z`` + ``es``
   → strip ``es``.
3. Default: strip trailing ``s``.

Note:
    The ``ves → f`` and ``oes → o`` rules were removed because they
    caused false positives (e.g. ``"hives" → "hif"``, ``"aloes" → "alo"``).
    All legitimate ``f/fe → ves`` and ``o → oes`` words are handled by
    the irregular lookup, which takes priority over regex rules.
"""

_UNCOUNTABLE: set[str] = {
    "sheep", "deer", "fish", "moose", "salmon", "trout",
    "rice", "bread", "beef", "pork", "milk", "cheese",
    "butter", "coffee", "tea", "juice", "water", "fruit",
    "sugar", "salt", "pepper", "soup", "pasta",
    "gold", "silver", "iron", "steel", "wood", "glass",
    "plastic", "rubber", "leather", "paper", "cotton", "wool",
    "information", "equipment", "news", "furniture", "luggage",
    "money", "advice", "knowledge", "research", "evidence",
    "education", "traffic", "music", "literature", "history",
    "physics", "mathematics", "chemistry", "biology", "economics",
    "jeans", "scissors", "glasses", "trousers", "pants",
    "series", "species", "police", "cattle", "offspring",
    "measles", "diabetes", "chaos", "staff", "personnel",
    "means", "aircraft", "spacecraft", "watercraft", "hovercraft",
    "baggage",
}
"""Set of English uncountable/invariable words.

These words have the same form in singular and plural.
They are checked first, before irregulars and regex rules.
"""

_RULES = LanguageRules(
    code="en",
    irregular_plurals=_IRREGULAR_PLURALS,
    irregular_singles=_IRREGULAR_SINGLES,
    plural_rules=_PLURAL_RULES,
    singular_rules=_SINGULAR_RULES,
    uncountable=_UNCOUNTABLE,
)
"""English :class:`LanguageRules` instance registered as ``"en"``."""

register(_RULES)
