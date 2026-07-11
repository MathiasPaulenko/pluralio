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
    "hoof": "hooves", "behalf": "behalves", "wharf": "wharves",
    "scarf": "scarves",
    # Proper nouns ending in -clive (protected from compound lives$ rule)
    "baronclive": "baronclives", "robertclive": "robertclives",
    # -is -> -es (Greek)
    "ellipsis": "ellipses", "neurosis": "neuroses",
    "synopsis": "synopses", "emphasis": "emphases",
    "paralysis": "paralyses",
    # More Latin/Greek irregulars
    "louse": "lice", "agendum": "agenda",
    "erratum": "errata", "ovum": "ova",
    "helix": "helices", "codex": "codices",
    "radix": "radices", "cortex": "cortices",
    "vortex": "vortices", "apex": "apices",
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
    "serf": "serfs", "surf": "surfs", "zarf": "zarfs",
    # Exceptions to fe → ves rule (just add s)
    "strife": "strifes", "fife": "fifes",
    # vowel + life compounds (not caught by [^aeiou]lives$ rule)
    "lovelife": "lovelives", "righttolife": "righttolives",
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
    "avocado": "avocados",
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
    # consonant + f exceptions (just add s)
    "gulf": "gulfs", "reef": "reefs", "scurf": "scurfs",
    # -f → -ves irregulars (need explicit entry for singularize)
    "elf": "elves",
    # Words ending in -che (singularize would strip ch+es, leaving wrong stem)
    # Most -che words are now handled by the ([aeiou])ches$ -> \1che regex rule.
    # These remain for explicit singular protection:
    "cache": "caches", "niche": "niches", "creche": "creches",
    "apache": "apaches", "machete": "machetes",
    "mustache": "mustaches", "moustache": "moustaches",
    "avalanche": "avalanches",
    # -che words not caught by ([aeiou])ches$ regex (consonant+y before ches)
    "psyche": "psyches", "demarche": "demarches",
    "thelarche": "thelarches", "tranche": "tranches",
    # Words ending in -ie (singularize ies->y would give wrong stem)
    "brownie": "brownies", "calorie": "calories",
    "auntie": "aunties", "aussie": "aussies",
    "beanie": "beanies", "birdie": "birdies",
    "bogie": "bogies", "collie": "collies",
    "groupie": "groupies", "hippie": "hippies",
    "indie": "indies", "junkie": "junkies",
    "lassie": "lassies", "newbie": "newbies",
    "pixie": "pixies", "pinkie": "pinkies",
    "preppie": "preppies", "yuppie": "yuppies",
    "sweetie": "sweeties", "toughie": "toughies",
    "quickie": "quickies", "smoothie": "smoothies",
    "veggie": "veggies", "barrie": "barries",
    "baddie": "baddies", "brassie": "brassies",
    "coldie": "coldies", "coolie": "coolies",
    "townie": "townies", "wreckie": "wreckies",
    # qu + y → quies (qu acts as consonant unit)
    "soliloquy": "soliloquies",
    # Singular words ending in ss (singularize must not strip s)
    "class": "classes", "kiss": "kisses", "mass": "masses",
    "press": "presses", "moss": "mosses", "toss": "tosses",
    "stress": "stresses", "address": "addresses", "access": "accesses",
    "process": "processes", "success": "successes",
    # Singular words ending in us (Latin/Greek origin)
    "discus": "discuses", "census": "censuses",
    "plexus": "plexuses", "sinus": "sinuses",
    "thermos": "thermoses", "abacus": "abaci",
    "corpus": "corpora", "genus": "genera", "opus": "opera",
    # Singular words ending in s (not ss) that need +es
    "atlas": "atlases",
    "canvas": "canvases", "bias": "biases", "bonus": "bonuses",
    "campus": "campuses", "chorus": "choruses", "circus": "circuses",
    "consensus": "consensuses", "crocus": "crocuses",
    "octopus": "octopuses", "pelvis": "pelvises",
    "rebus": "rebuses", "trellis": "trellises",
    "hippopotamus": "hippopotamuses", "platypus": "platypuses",
    "minibus": "minibuses", "omnibus": "omnibuses",
    # Greek -on → -a
    "automaton": "automata",
    # Compound without hyphen
    "passerby": "passersby",
    # Words ending in s (not ss) that need +es
    "walrus": "walruses", "iris": "irises",
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
    (re.compile(r"(ss|sh|ch|x|z)$"), r"\1es"),
    (re.compile(r"([^aeiou])y$"), r"\1ies"),
    # Compound exceptions to f→ves: just add s
    (re.compile(r"(.+)(dwarf|golf|gulf|turf|strife)$"), r"\1\2s"),
    (re.compile(r"fe$"), "ves"),
    (re.compile(r"([^aeiou])(?<!f)f$"), r"\1ves"),
    (re.compile(r"([^aeiou])o$"), r"\1oes"),
    (re.compile(r"([^s])$"), r"\1s"),
]
"""Ordered English pluralization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``s``, ``ss``, ``sh``, ``ch``, ``x``, ``z`` → add ``es``.
2. Words ending in consonant + ``y`` → replace ``y`` with ``ies``.
3. Compound ``f``-exceptions (``dwarf``, ``golf``, ``gulf``, ``turf``,
   ``strife``) → just add ``s``. Base words handled by irregulars.
4. Words ending in ``fe`` → replace with ``ves``.
5. Words ending in consonant + ``f`` → replace ``f`` with ``ves``.
6. Words ending in consonant + ``o`` → replace ``o`` with ``oes``.
7. Default: append ``s``.
"""

_SINGULAR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(.+)([^aeiou])ies$"), r"\1\2y"),
    # vowel + che + s → vowel + che (ache→aches, cache→caches, niche→niches)
    (re.compile(r"([aeiou])ches$"), r"\1che"),
    (re.compile(r"(ss|sh|ch|x|zz)es$"), r"\1"),
    (re.compile(r"ses$"), "se"),
    (re.compile(r"zes$"), "ze"),
    (re.compile(r"([^aeiou])oes$"), r"\1o"),
    # Protect Latin/Greek singular endings from having s stripped
    (re.compile(r"(is|us|ness)$"), r"\1"),
    # Compound f→ves singularization (base words handled by irregulars)
    # The [^aeiou] guard on lives$ prevents false positives like olive→olife
    (re.compile(r"(.+)([^aeiou])lives$"), r"\1\2life"),
    (re.compile(r"(.+)wives$"), r"\1wife"),
    (re.compile(r"(.+)knives$"), r"\1knife"),
    (re.compile(r"(.+)wolves$"), r"\1wolf"),
    (re.compile(r"(.+)halves$"), r"\1half"),
    (re.compile(r"(.+)selves$"), r"\1self"),
    (re.compile(r"(.+)shelves$"), r"\1shelf"),
    (re.compile(r"(.+)loaves$"), r"\1loaf"),
    (re.compile(r"(.+)thieves$"), r"\1thief"),
    (re.compile(r"(.+)calves$"), r"\1calf"),
    (re.compile(r"(.+)scarves$"), r"\1scarf"),
    (re.compile(r"(.+)hooves$"), r"\1hoof"),
    (re.compile(r"(.+)behalves$"), r"\1behalf"),
    (re.compile(r"(.+)wharves$"), r"\1wharf"),
    (re.compile(r"(ss)$"), r"\1"),
    (re.compile(r"s$"), ""),
]
"""Ordered English singularization regex rules (first match wins).

Order matters: more specific patterns must come before generic ones.
1. Words ending in ``ies`` → replace with ``y``.
2. Words ending in vowel + ``ches`` → replace with vowel + ``che``
   (e.g. ``"aches" → "ache"``, ``"caches" → "cache"``).
3. Words ending in ``s``, ``ss``, ``sh``, ``ch``, ``x``, ``z`` + ``es``
   → strip ``es``.
4. Words ending in ``ses`` → replace with ``se``.
5. Words ending in ``zes`` → replace with ``ze``.
6. Words ending in consonant + ``oes`` → replace with consonant + ``o``.
7. Words ending in ``is``, ``us``, ``ness`` → unchanged (Latin/Greek singular).
8. Compound ``f→ves`` words → singularize back to ``f`` form
   (e.g. ``"afterlives" → "afterlife"``, ``"housewives" → "housewife"``).
   Base words (``life``, ``wife``, etc.) are handled by irregulars.
   The ``[^aeiou]`` guard on ``lives$`` prevents false positives
   like ``"olives" → "olife"``.
9. Words ending in ``ss`` → unchanged (already singular, e.g. ``"glass"``,
   ``"dress"``, ``"loss"``).
10. Default: strip trailing ``s``.

Note:
    The ``ves → f`` rule was removed because it caused false positives
    (e.g. ``"hives" → "hif"``). All legitimate ``f/fe → ves`` words are
    handled by the irregular lookup, which takes priority over regex rules.
    Compound ``f→ves`` words are handled by the dedicated regex rules
    in item 8 above. The ``oes → o`` rule uses a consonant prefix
    (``([^aeiou])oes``) to avoid matching ``-e`` words like ``"shoes"``
    (handled by irregulars).
"""

_UNCOUNTABLE: set[str] = {
    "sheep", "deer", "fish", "moose", "salmon", "trout",
    "rice", "bread", "beef", "pork", "milk", "cheese",
    "butter", "coffee", "tea", "juice", "water", "fruit",
    "sugar", "salt", "pepper", "soup", "pasta",
    "gold", "silver", "iron", "steel", "wood",
    "plastic", "rubber", "leather", "paper", "cotton", "wool",
    "information", "equipment", "news", "furniture", "luggage",
    "money", "advice", "knowledge", "research", "evidence",
    "education", "traffic", "music", "literature",
    "physics", "mathematics", "chemistry", "economics",
    "tuberculosis", "psoriasis", "rabies", "mumps",
    "jeans", "scissors", "glasses", "trousers", "pants",
    "series", "species", "police", "cattle", "offspring",
    "measles", "diabetes", "chaos", "staff", "personnel",
    "means", "aircraft", "spacecraft", "watercraft", "hovercraft",
    "baggage",
    # Plural-only nouns ending in -es (would be broken by vowel+ches rule)
    "riches", "breeches", "britches",
    "jodhpurbreeches", "kneebreeches", "ridingbreeches",
    # Common non-noun words ending in s (should not be singularized)
    "is", "this", "was", "has", "us", "as", "thus",
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
