"""English edge cases for pluralization and singularization."""
from __future__ import annotations

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestEnSEndingIrregulars:
    @pytest.mark.parametrize(("singular", "plural"), [
        ("atlas", "atlases"), ("canvas", "canvases"), ("bias", "biases"),
        ("bonus", "bonuses"), ("campus", "campuses"),
        ("chorus", "choruses"), ("circus", "circuses"),
        ("consensus", "consensuses"), ("crocus", "crocuses"),
        ("octopus", "octopuses"), ("pelvis", "pelvises"),
        ("rebus", "rebuses"), ("trellis", "trellises"),
        ("platypus", "platypuses"), ("minibus", "minibuses"),
        ("omnibus", "omnibuses"),
    ])
    def test_s_ending_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural



class TestEnCrossCheckFixes:
    @pytest.mark.parametrize(("singular", "plural"), [
        # -is -> -es (Greek)
        ("ellipsis", "ellipses"), ("neurosis", "neuroses"),
        ("synopsis", "synopses"), ("emphasis", "emphases"),
        ("paralysis", "paralyses"),
        # Latin/Greek irregulars
        ("louse", "lice"), ("agendum", "agenda"),
        ("erratum", "errata"), ("ovum", "ova"),
        ("helix", "helices"), ("codex", "codices"),
        ("radix", "radices"), ("cortex", "cortices"),
        ("vortex", "vortices"), ("apex", "apices"),
    ])
    def test_is_and_latin_irregulars(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural

    @pytest.mark.parametrize(("word", "expected"), [
        ("cuff", "cuffs"), ("stuff", "stuffs"), ("bluff", "bluffs"),
        ("fluff", "fluffs"), ("chuff", "chuffs"), ("puff", "puffs"),
        ("quaff", "quaffs"), ("duff", "duffs"), ("muff", "muffs"),
        ("scoff", "scoffs"), ("snuff", "snuffs"), ("scurf", "scurfs"),
        ("whiff", "whiffs"), ("skiff", "skiffs"), ("stiff", "stiffs"),
        ("gruff", "gruffs"), ("scruff", "scruffs"),
    ])
    def test_ff_words(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected
        assert singularize(expected) == word

    @pytest.mark.parametrize("word", [
        "tuberculosis", "psoriasis", "rabies", "mumps",
    ])
    def test_disease_uncountables(self, word: str) -> None:
        assert pluralize(word) == word
        assert singularize(word) == word

    @pytest.mark.parametrize(("singular", "plural"), [
        ("history", "histories"), ("biology", "biologies"),
    ])
    def test_history_biology_countable(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
        ("diff", "diffs"), ("cache", "caches"),
        ("niche", "niches"), ("machete", "machetes"),
    ])
    def test_tech_word_fixes(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert pluralize(plural) == plural



class TestEnSingularProtection:
    @pytest.mark.parametrize("word", [
        "status", "virus", "campus", "corpus", "genus",
        "opus", "radius", "focus", "fungus", "census",
        "apparatus", "plexus", "sinus", "consensus",
    ])
    def test_us_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "analysis", "crisis", "thesis", "basis", "oasis",
        "parenthesis", "ellipsis", "neurosis", "synopsis",
        "emphasis", "paralysis", "diagnosis", "prognosis",
    ])
    def test_is_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "darkness", "happiness", "kindness", "weakness",
        "fitness", "illness", "sadness", "madness",
        "awareness", "carelessness", "thoughtlessness",
    ])
    def test_ness_singular_unchanged(self, word: str) -> None:
        assert singularize(word) == word



class TestEnOesSingularRule:
    @pytest.mark.parametrize(("singular", "plural"), [
        ("ado", "adoes"), ("tango", "tangoes"),
        ("cargo", "cargoes"), ("judo", "judoes"), ("motto", "mottoes"),
        ("bravado", "bravadoes"),
        ("fresco", "frescoes"),
    ])
    def test_oes_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnFvesRoundTrip:
    @pytest.mark.parametrize(("singular", "plural"), [
        ("behalf", "behalves"), ("wharf", "wharves"), ("scarf", "scarves"),
        ("wolf", "wolves"), ("half", "halves"), ("elf", "elves"),
        ("shelf", "shelves"), ("self", "selves"),
    ])
    def test_fves_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnCheRegexRule:
    """Words ending in vowel+che handled by the ([aeiou])ches$ regex rule."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("ache", "aches"), ("cache", "caches"), ("niche", "niches"),
        ("cliche", "cliches"), ("quiche", "quiches"), ("panache", "panaches"),
        ("brioche", "brioches"), ("pastiche", "pastiches"),
        ("headache", "headaches"), ("earache", "earaches"),
        ("toothache", "toothaches"), ("backache", "backaches"),
        ("heartache", "heartaches"), ("stomachache", "stomachaches"),
        ("douche", "douches"), ("gouache", "gouaches"),
        ("cloche", "cloches"), ("barouche", "barouches"),
        ("cartouche", "cartouches"), ("caliche", "caliches"),
        ("huarache", "huaraches"), ("seiche", "seiches"),
        ("troche", "troches"), ("microfiche", "microfiches"),
        ("attache", "attaches"), ("synecdoche", "synecdoches"),
    ])
    def test_che_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular

    @pytest.mark.parametrize("word", [
        "matches", "catches", "hatches", "patches", "batches",
        "latches", "witches", "switches", "ditches",
    ])
    def test_ch_words_not_broken(self, word: str) -> None:
        assert singularize(word) == word[:-2]

    @pytest.mark.parametrize("word", ["riches", "breeches", "britches"])
    def test_plural_only_uncountable(self, word: str) -> None:
        assert singularize(word) == word
        assert pluralize(word) == word



class TestEnIeIrregulars:
    """Words ending in -ie that need irregular entries for correct singularization."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("brownie", "brownies"), ("calorie", "calories"),
        ("cookie", "cookies"), ("movie", "movies"),
        ("auntie", "aunties"), ("aussie", "aussies"),
        ("beanie", "beanies"), ("birdie", "birdies"),
        ("collie", "collies"), ("groupie", "groupies"),
        ("hippie", "hippies"), ("indie", "indies"),
        ("junkie", "junkies"), ("lassie", "lassies"),
        ("newbie", "newbies"), ("pixie", "pixies"),
        ("pinkie", "pinkies"), ("smoothie", "smoothies"),
        ("sweetie", "sweeties"), ("townie", "townies"),
    ])
    def test_ie_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnCompoundFves:
    """Compound f→ves words handled by singularization regex rules.

    Base words (life, wife, knife, wolf, etc.) are in irregulars.
    Compounds are handled by dedicated regex rules like
    ``(.+)([^aeiou])lives$`` → ``\\1\\2life``.
    """

    @pytest.mark.parametrize(("singular", "plural"), [
        ("afterlife", "afterlives"), ("halflife", "halflives"),
        ("nightlife", "nightlives"), ("housewife", "housewives"),
        ("midwife", "midwives"), ("bookshelf", "bookshelves"),
        ("headscarf", "headscarves"), ("aardwolf", "aardwolves"),
        ("lonewolf", "lonewolves"), ("bowieknife", "bowieknives"),
        ("pocketknife", "pocketknives"), ("jackknife", "jackknives"),
        ("betterhalf", "betterhalves"), ("boxcalf", "boxcalves"),
        ("businesslife", "businesslives"), ("eternallife", "eternallives"),
        ("reallife", "reallives"), ("wildlife", "wildlives"),
        ("werewolf", "werewolves"), ("redwolf", "redwolves"),
        ("timberwolf", "timberwolves"), ("steakknife", "steakknives"),
        ("drawknife", "drawknives"), ("penknife", "penknives"),
        ("firsthalf", "firsthalves"), ("secondhalf", "secondhalves"),
        ("continentalshelf", "continentalshelves"),
        ("goldencalf", "goldencalves"),
        ("manandwife", "manandwives"), ("oldwife", "oldwives"),
    ])
    def test_compound_fves_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnCompoundFexceptions:
    """Compound f-exception words that just add ``s`` (not ``ves``).

    Base words (dwarf, golf, gulf, turf, strife) are in irregulars.
    Compounds are handled by the plural exception regex rule
    ``(.+)(dwarf|golf|gulf|turf|strife)$`` → ``\\1\\2s``.
    """

    @pytest.mark.parametrize(("singular", "plural"), [
        ("reddwarf", "reddwarfs"), ("whitedwarf", "whitedwarfs"),
        ("yellowdwarf", "yellowdwarfs"), ("truedwarf", "truedwarfs"),
        ("miniaturegolf", "miniaturegolfs"),
        ("professionalgolf", "professionalgolfs"),
        ("arabiangulf", "arabiangulfs"), ("persiangulf", "persiangulfs"),
        ("lilyturf", "lilyturfs"),
        ("loosestrife", "loosestrifes"),
        ("purpleloosestrife", "purpleloosestrifes"),
        ("spikedloosestrife", "spikedloosestrifes"),
    ])
    def test_compound_fexception_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnFexceptionIrregulars:
    """Base f-exception words that just add ``s`` (not ``ves``)."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("serf", "serfs"), ("surf", "surfs"), ("zarf", "zarfs"),
        ("strife", "strifes"), ("fife", "fifes"),
    ])
    def test_fexception_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnVowelLifeCompounds:
    """vowel + life compounds not caught by ``[^aeiou]lives$`` rule.

    These need irregular entries because the consonant guard
    prevents the regex from matching.
    """

    @pytest.mark.parametrize(("singular", "plural"), [
        ("lovelife", "lovelives"), ("righttolife", "righttolives"),
    ])
    def test_vowel_life_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnLivesRuleGuard:
    """The ``([^aeiou])lives$`` guard prevents false positives."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("olive", "olives"), ("clive", "clives"),
        ("baronclive", "baronclives"), ("robertclive", "robertclives"),
    ])
    def test_olive_not_broken(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular



class TestEnSsSingularization:
    """Words ending in -ss should not lose an s when singularized."""

    @pytest.mark.parametrize("word", [
        "glass", "dress", "loss", "miss", "pass", "fuss",
        "class", "kiss", "press", "moss", "toss", "stress",
        "boss", "cross", "floss", "gross",
    ])
    def test_ss_singular_is_self(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize(("word", "expected"), [
        ("dresses", "dress"), ("losses", "loss"),
        ("classes", "class"), ("kisses", "kiss"), ("presses", "press"),
        ("bosses", "boss"), ("crosses", "cross"),
    ])
    def test_ss_plural_singularizes(self, word: str, expected: str) -> None:
        assert singularize(word) == expected



class TestEnNewIrregulars:
    """Tests for newly added irregular plurals."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
        ("walrus", "walruses"),
        ("automaton", "automata"),
        ("tornado", "tornadoes"),
        ("passerby", "passersby"),
        ("iris", "irises"),
    ])
    def test_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural



class TestEnGlassCountable:
    """glass is now countable (a drinking glass), not uncountable."""

    def test_pluralize_glass(self) -> None:
        assert pluralize("glass") == "glasses"

    def test_glass_not_uncountable(self) -> None:
        assert is_singular("glass") is True
        assert is_plural("glass") is False

    def test_glasses_still_uncountable(self) -> None:
        """'glasses' (eyeglasses) remains uncountable."""
        assert singularize("glasses") == "glasses"
        assert pluralize("glasses") == "glasses"



class TestEnChSingularization:
    """Words ending in -ch (not -che) must singularize correctly.

    The old ([aeiou])ches$ rule broke words like beach, teach, coach
    by returning beache, teache, coache. Now they use the standard
    (ss|sh|ch|x|zz)es$ rule.
    """

    @pytest.mark.parametrize("word", [
        "beach", "peach", "reach", "teach", "preach", "bleach",
        "coach", "approach", "broach", "encroach", "crouch",
        "lunch", "crunch", "bunch", "punch", "hunch",
        "branch", "ranch", "starch", "march", "torch", "porch",
    ])
    def test_ch_roundtrip(self, word: str) -> None:
        plural = pluralize(word)
        assert singularize(plural) == word

    @pytest.mark.parametrize(("word", "expected"), [
        ("beaches", "beach"), ("peaches", "peach"), ("reaches", "reach"),
        ("teaches", "teach"), ("coaches", "coach"), ("approaches", "approach"),
        ("lunches", "lunch"), ("branches", "branch"), ("torches", "torch"),
    ])
    def test_ch_plural_singularizes(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    @pytest.mark.parametrize("word", [
        "ache", "cache", "niche", "apache", "creche", "machete",
        "mustache", "moustache", "avalanche", "psyche", "demarche",
        "tranche", "thelarche",
    ])
    def test_che_roundtrip(self, word: str) -> None:
        plural = pluralize(word)
        assert singularize(plural) == word



class TestEnHyphenatedPrefixes:
    """Hyphenated words with prefix first segments pluralize the last segment."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("re-analysis", "re-analyses"),
        ("pre-screening", "pre-screenings"),
        ("anti-inflammatory", "anti-inflammatories"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
        ("non-intervention", "non-interventions"),
        ("sub-committee", "sub-committees"),
        ("inter-agency", "inter-agencies"),
    ])
    def test_prefix_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("re-analysis", "re-analyses"),
        ("pre-screening", "pre-screenings"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
    ])
    def test_prefix_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
        ("meta-analysis", "meta-analyses"),
        ("post-analysis", "post-analyses"),
        ("co-pilot", "co-pilots"),
        ("ex-president", "ex-presidents"),
    ])
    def test_prefix_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural



class TestEnDemonyms:
    """Demonyms ending in -ese are invariable (same singular and plural)."""

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "burmese", "lebanese",
        "portuguese", "javanese", "sundanese", "senegalese", "congolese",
        "sudanese", "maltese", "siamese",
    ])
    def test_demonym_pluralize_unchanged(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese", "lebanese",
    ])
    def test_demonym_singularize_unchanged(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_demonym_is_singular(self, word: str) -> None:
        assert is_singular(word) is True

    @pytest.mark.parametrize("word", [
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_demonym_is_plural(self, word: str) -> None:
        assert is_plural(word) is True



class TestEnLatinGreekIrregulars:
    """Round-trip tests for Latin/Greek classical irregular plurals (Fase 1)."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("desideratum", "desiderata"),
        ("maximum", "maxima"),
        ("millennium", "millennia"),
        ("anathema", "anathemata"),
        ("schema", "schemata"),
        ("alumna", "alumnae"),
        ("formula", "formulae"),
        ("nebula", "nebulae"),
        ("stamen", "stamina"),
        ("ephemeris", "ephemerides"),
        ("arthritis", "arthritides"),
        ("hepatitis", "hepatitides"),
        ("perihelion", "perihelia"),
        ("oxymoron", "oxymora"),
        ("murex", "murices"),
        ("latex", "latices"),
        ("goy", "goyim"),
        ("afrit", "afriti"),
        ("mythos", "mythoi"),
        ("beef", "beefs"),
        ("money", "monies"),
        ("numen", "numina"),
        ("carmen", "carmina"),
        ("genie", "genies"),
    ])
    def test_latin_greek_roundtrip(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural
        assert singularize(plural) == singular
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    def test_graffito_pluralize_only(self) -> None:
        assert pluralize("graffito") == "graffiti"
        assert singularize("graffiti") == "graffiti"



class TestEnNewUncountables:
    """Uncountable words from Fase 2 — pluralize(x) == x and singularize(x) == x."""

    @pytest.mark.parametrize("word", [
        "bison", "buffalo", "caribou", "elk", "swine", "wildebeest", "eland",
        "cod", "flounder", "grouse", "haddock", "hake", "halibut", "herring",
        "mackerel", "pike", "roe", "shad", "snipe", "teal", "turbot",
        "bream", "carp", "dace", "pickerel",
        "graffiti", "djinn", "pence", "quid", "hertz", "chassis", "corps",
        "debris", "siemens", "contretemps", "mews", "haggis", "innings",
        "proceedings", "jackanapes", "zucchini", "quinoa",
        "amoyese", "borghese", "congoese", "faroese", "foochowese",
        "genevese", "genoese", "gilbertese", "hottentotese", "kiplingese",
        "kongoese", "lucchese", "nankingese", "niasese", "pekingese",
        "piedmontese", "pistoiese", "sarawakese", "shavese", "vermontese",
        "wenchowese", "yengeese",
        "blowfish", "angelfish", "jellyfish", "catfish", "swordfish",
        "goldfish", "starfish", "pufferfish", "sunfish", "bluefish",
        "blackfish", "codfish", "dogfish", "flatfish", "monkfish",
        "reeffish", "sawfish", "stonefish", "toadfish", "whitefish",
        "chickenpox", "smallpox", "cowpox", "foxpox", "gerbilpox",
        "monkeypox", "mousepox", "rabbitpox", "raccoonpox", "skunkpox",
    ])
    def test_uncountable_pluralize(self, word: str) -> None:
        assert pluralize(word) == word

    @pytest.mark.parametrize("word", [
        "bison", "buffalo", "caribou", "elk", "swine", "wildebeest", "eland",
        "cod", "flounder", "grouse", "haddock", "hake", "halibut", "herring",
        "mackerel", "pike", "roe", "shad", "snipe", "teal", "turbot",
        "bream", "carp", "dace", "pickerel",
        "graffiti", "djinn", "pence", "quid", "hertz", "chassis", "corps",
        "debris", "siemens", "contretemps", "mews", "haggis", "innings",
        "proceedings", "jackanapes", "zucchini", "quinoa",
        "amoyese", "borghese", "congoese", "faroese", "foochowese",
        "genevese", "genoese", "gilbertese", "hottentotese", "kiplingese",
        "kongoese", "lucchese", "nankingese", "niasese", "pekingese",
        "piedmontese", "pistoiese", "sarawakese", "shavese", "vermontese",
        "wenchowese", "yengeese",
        "blowfish", "angelfish", "jellyfish", "catfish", "swordfish",
        "goldfish", "starfish", "pufferfish", "sunfish", "bluefish",
        "blackfish", "codfish", "dogfish", "flatfish", "monkfish",
        "reeffish", "sawfish", "stonefish", "toadfish", "whitefish",
        "chickenpox", "smallpox", "cowpox", "foxpox", "gerbilpox",
        "monkeypox", "mousepox", "rabbitpox", "raccoonpox", "skunkpox",
    ])
    def test_uncountable_singularize(self, word: str) -> None:
        assert singularize(word) == word

    @pytest.mark.parametrize("word", [
        "amoyese", "pekingese", "yengeese", "lucchese", "piedmontese",
        "blowfish", "catfish", "goldfish", "starfish", "swordfish",
        "chickenpox", "smallpox", "monkeypox", "mousepox", "skunkpox",
    ])
    def test_uncountable_is_singular_and_plural(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is True



class TestEnForeignOWords:
    """Fase 4: Foreign -o words that pluralize with -os (not -oes)."""

    @pytest.mark.parametrize(("singular", "plural"), [
        # Animales
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("hippo", "hippos"), ("rhino", "rhinos"),
        # Instrumentos
        ("allegro", "allegros"), ("bolero", "boleros"),
        ("bongo", "bongos"), ("canto", "cantos"),
        ("falsetto", "falsettos"), ("intermezzo", "intermezzos"),
        ("rondo", "rondos"), ("staccato", "staccatos"),
        ("tremolo", "tremolos"), ("vibrato", "vibratos"),
        ("violoncello", "violoncellos"), ("timpano", "timpanos"),
        # Comida/bebida
        ("cappuccino", "cappuccinos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"),
        # Objetos
        ("archipelago", "archipelagos"), ("bingo", "bingos"),
        ("commando", "commandos"), ("ditto", "dittos"),
        ("fiasco", "fiascos"), ("gizmo", "gizmos"),
        ("hairdo", "hairdos"), ("manifesto", "manifestos"),
        ("stucco", "stuccos"), ("torso", "torsos"), ("ufo", "ufos"),
        # Otros
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("cappuccino", "cappuccinos"), ("allegro", "allegros"),
        ("bolero", "boleros"), ("bongo", "bongos"),
        ("canto", "cantos"), ("falsetto", "falsettos"),
        ("intermezzo", "intermezzos"), ("rondo", "rondos"),
        ("staccato", "staccatos"), ("tremolo", "tremolos"),
        ("vibrato", "vibratos"), ("violoncello", "violoncellos"),
        ("timpano", "timpanos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"), ("hippo", "hippos"),
        ("rhino", "rhinos"), ("archipelago", "archipelagos"),
        ("bingo", "bingos"), ("commando", "commandos"),
        ("ditto", "dittos"), ("fiasco", "fiascos"),
        ("gizmo", "gizmos"), ("hairdo", "hairdos"),
        ("manifesto", "manifestos"), ("stucco", "stuccos"),
        ("torso", "torsos"), ("ufo", "ufos"),
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
        ("albino", "albinos"), ("armadillo", "armadillos"),
        ("cappuccino", "cappuccinos"), ("allegro", "allegros"),
        ("bolero", "boleros"), ("bongo", "bongos"),
        ("canto", "cantos"), ("falsetto", "falsettos"),
        ("intermezzo", "intermezzos"), ("rondo", "rondos"),
        ("staccato", "staccatos"), ("tremolo", "tremolos"),
        ("vibrato", "vibratos"), ("violoncello", "violoncellos"),
        ("timpano", "timpanos"), ("cilantro", "cilantros"),
        ("coco", "cocos"), ("espresso", "espressos"),
        ("gyro", "gyros"), ("oregano", "oreganos"),
        ("pimento", "pimentos"), ("pinto", "pintos"),
        ("risotto", "risottos"), ("tobacco", "tobaccos"),
        ("burro", "burros"), ("hippo", "hippos"),
        ("rhino", "rhinos"), ("archipelago", "archipelagos"),
        ("bingo", "bingos"), ("commando", "commandos"),
        ("ditto", "dittos"), ("fiasco", "fiascos"),
        ("gizmo", "gizmos"), ("hairdo", "hairdos"),
        ("manifesto", "manifestos"), ("stucco", "stuccos"),
        ("torso", "torsos"), ("ufo", "ufos"),
        ("aficionado", "aficionados"), ("credo", "credos"),
        ("demo", "demos"), ("euro", "euros"),
        ("gringo", "gringos"), ("info", "infos"),
        ("macho", "machos"), ("macro", "macros"),
        ("micro", "micros"), ("neutrino", "neutrinos"),
        ("polo", "polos"), ("psycho", "psychos"),
        ("pueblo", "pueblos"), ("quarto", "quartos"),
        ("repo", "repos"), ("typo", "typos"),
        ("weirdo", "weirdos"), ("zero", "zeros"),
        ("yo-yo", "yo-yos"),
    ])
    def test_o_words_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    def test_not_oes(self) -> None:
        assert pluralize("albino") != "albinoes"
        assert pluralize("armadillo") != "armadilloes"
        assert pluralize("cappuccino") != "cappuccinoes"



class TestEnFase3InverseSingularization:
    """Fase 3: explicit inverse singularization entries."""

    @pytest.mark.parametrize(("plural", "singular"), [
        ("abuses", "abuse"), ("clauses", "clause"), ("excuses", "excuse"),
        ("fuses", "fuse"), ("uses", "use"), ("pauses", "pause"),
        ("spouses", "spouse"), ("reuses", "reuse"), ("misuses", "misuse"),
    ])
    def test_uses_to_use(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("plural", "singular"), [
        ("aeries", "aerie"), ("belies", "belie"), ("bookies", "bookie"),
        ("cooties", "cootie"), ("freebies", "freebie"), ("goalies", "goalie"),
        ("lies", "lie"), ("magpies", "magpie"), ("neckties", "necktie"),
        ("oldies", "oldie"), ("prairies", "prairie"), ("rookies", "rookie"),
        ("sorties", "sortie"), ("vies", "vie"), ("zombies", "zombie"),
    ])
    def test_ies_to_ie_comunes(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("plural", "singular"), [
        ("addies", "addie"), ("archies", "archie"), ("barbies", "barbie"),
        ("charlies", "charlie"), ("eddies", "eddie"), ("julies", "julie"),
        ("katies", "katie"), ("maggies", "maggie"), ("sophies", "sophie"),
        ("trekkies", "trekkie"), ("valkyries", "valkyrie"), ("yorkies", "yorkie"),
    ])
    def test_ies_to_ie_proper_nouns(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("plural", "singular"), [
        ("antitheses", "antithesis"), ("catalyses", "catalysis"),
        ("diagnoses", "diagnosis"), ("geneses", "genesis"),
        ("metamorphoses", "metamorphosis"), ("mitoses", "mitosis"),
        ("nemeses", "nemesis"), ("prognoses", "prognosis"),
        ("psychoses", "psychosis"), ("syntheses", "synthesis"),
        ("taxes", "tax"), ("thromboses", "thrombosis"),
    ])
    def test_es_to_is(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("plural", "singular"), [
        ("backhoes", "backhoe"), ("floes", "floe"),
        ("mistletoes", "mistletoe"), ("tiptoes", "tiptoe"),
        ("woes", "woe"),
    ])
    def test_oes_to_oe(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("plural", "singular"), [
        ("blanches", "blanche"), ("porsches", "porsche"),
        ("hesses", "hesse"), ("matisses", "matisse"),
        ("clives", "clive"), ("palmolives", "palmolive"),
        ("annexes", "annex"), ("pickaxes", "pickaxe"),
        ("buzzes", "buzz"), ("fizzes", "fizz"),
        ("bolshois", "bolshoi"), ("hanois", "hanoi"),
    ])
    def test_minor_subphases(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular



class TestEnProperNounCasePreservation:
    """Fase 5: Proper nouns ending in -ie with case preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("Barbie", "Barbies"), ("Charlie", "Charlies"),
        ("BILLIE", "BILLIES"), ("barbie", "barbies"),
        ("charlie", "charlies"), ("Billie", "Billies"),
        ("Annie", "Annies"), ("ANNIE", "ANNIES"),
        ("Archie", "Archies"), ("artie", "arties"),
        ("ARTIE", "ARTIES"), ("Bessie", "Bessies"),
        ("BESSIE", "BESSIES"), ("bessie", "bessies"),
        ("Betty", "Betties"), ("BETTY", "BETTIES"),
        ("betty", "betties"), ("Bobbie", "Bobbies"),
        ("Connie", "Connies"), ("connie", "connies"),
        ("Curie", "Curies"), ("CURIE", "CURIES"),
        ("Debbie", "Debbies"), ("Eddie", "Eddies"),
        ("EDDIE", "EDDIES"), ("Ellie", "Ellies"),
        ("Frankie", "Frankies"), ("Gracie", "Gracies"),
        ("Jackie", "Jackies"), ("Jamie", "Jamies"),
        ("Julie", "Julies"), ("JULIE", "JULIES"),
        ("Katie", "Katies"), ("katie", "katies"),
        ("KATIE", "KATIES"), ("Leslie", "Leslies"),
        ("Maggie", "Maggies"), ("Millie", "Millies"),
        ("Nellie", "Nellies"), ("nellie", "nellies"),
        ("NELLIE", "NELLIES"), ("Ollie", "Ollies"),
        ("Reggie", "Reggies"), ("Richie", "Richies"),
        ("Rosie", "Rosies"), ("Sadie", "Sadies"),
        ("sophie", "sophies"), ("Sophie", "Sophies"),
        ("SOPHIE", "SOPHIES"), ("Susie", "Susies"),
        ("Tommie", "Tommies"), ("Willie", "Willies"),
        ("Winnie", "Winnies"), ("Yorkie", "Yorkies"),
        ("yorkie", "yorkies"), ("YORKIE", "YORKIES"),
        ("Sherry", "Sherries"), ("sherry", "sherries"),
        ("SHERRY", "SHERRIES"),
    ])
    def test_proper_noun_pluralize_case(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("Barbies", "Barbie"), ("Charlies", "Charlie"),
        ("BILLIES", "BILLIE"), ("barbies", "barbie"),
        ("charlies", "charlie"), ("Billies", "Billie"),
        ("Annies", "Annie"), ("ANNIES", "ANNIE"),
        ("Archies", "Archie"), ("Bessies", "Bessie"),
        ("BESSIES", "BESSIE"), ("bessies", "bessie"),
        ("Betties", "Betty"), ("BETTIES", "BETTY"),
        ("betties", "betty"), ("Bobbies", "Bobbie"),
        ("Connies", "Connie"), ("Curies", "Curie"),
        ("CURIES", "CURIE"), ("Debbies", "Debbie"),
        ("Eddies", "Eddie"), ("EDDIES", "EDDIE"),
        ("Ellies", "Ellie"), ("Frankies", "Frankie"),
        ("Gracies", "Gracie"), ("Jackies", "Jackie"),
        ("Jamies", "Jamie"), ("Julies", "Julie"),
        ("JULIES", "JULIE"), ("Katies", "Katie"),
        ("katies", "katie"), ("KATIES", "KATIE"),
        ("Leslies", "Leslie"), ("Maggies", "Maggie"),
        ("Millies", "Millie"), ("Nellies", "Nellie"),
        ("nellies", "nellie"), ("NELLIES", "NELLIE"),
        ("Ollies", "Ollie"), ("Reggies", "Reggie"),
        ("Richies", "Richie"), ("Rosies", "Rosie"),
        ("Sadies", "Sadie"), ("sophies", "sophie"),
        ("Sophies", "Sophie"), ("SOPHIES", "SOPHIE"),
        ("Susies", "Susie"), ("Tommies", "Tommie"),
        ("Willies", "Willie"), ("Winnies", "Winnie"),
        ("Yorkies", "Yorkie"), ("yorkies", "yorkie"),
        ("YORKIES", "YORKIE"), ("Sherries", "Sherry"),
        ("sherries", "sherry"), ("SHERRIES", "SHERRY"),
    ])
    def test_proper_noun_singularize_case(self, word: str, expected: str) -> None:
        assert singularize(word) == expected

    @pytest.mark.parametrize(("singular", "plural"), [
        ("Barbie", "Barbies"), ("Charlie", "Charlies"),
        ("Billie", "Billies"), ("Annie", "Annies"),
        ("Bessie", "Bessies"), ("Betty", "Betties"),
        ("Curie", "Curies"), ("Eddie", "Eddies"),
        ("Julie", "Julies"), ("Katie", "Katies"),
        ("Maggie", "Maggies"), ("Nellie", "Nellies"),
        ("Reggie", "Reggies"), ("Sophie", "Sophies"),
        ("Willie", "Willies"), ("Yorkie", "Yorkies"),
        ("Sherry", "Sherries"), ("Bobbie", "Bobbies"),
        ("Connie", "Connies"), ("Gracie", "Gracies"),
    ])
    def test_proper_noun_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural



class TestEnSingularSComplete:
    """Fase 6: Singular words ending in -s that need +es pluralization."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural) == singular

    @pytest.mark.parametrize(("singular", "plural"), [
        ("acropolis", "acropolises"),
        ("aegis", "aegises"),
        ("alias", "aliases"),
        ("asbestos", "asbestoses"),
        ("bathos", "bathoses"),
        ("caddis", "caddises"),
        ("cannabis", "cannabises"),
        ("cosmos", "cosmoses"),
        ("dais", "daises"),
        ("digitalis", "digitalises"),
        ("epidermis", "epidermises"),
        ("ethos", "ethoses"),
        ("eyas", "eyases"),
        ("glottis", "glottises"),
        ("hubris", "hubrises"),
        ("ibis", "ibises"),
        ("mantis", "mantises"),
        ("marquis", "marquises"),
        ("metropolis", "metropolises"),
        ("pathos", "pathoses"),
        ("polis", "polises"),
        ("sassafras", "sassafrases"),
    ])
    def test_singular_s_roundtrip(self, singular: str, plural: str) -> None:
        assert singularize(pluralize(singular)) == singular
        assert pluralize(singularize(plural)) == plural

    @pytest.mark.parametrize("plural", [
        "acropolises", "aegises", "aliases", "asbestoses", "bathoses",
        "caddises", "cannabises", "cosmoses", "daises", "digitalises",
        "epidermises", "ethoses", "eyases", "glottises", "hubrises",
        "ibises", "mantises", "marquises", "metropolises", "pathoses",
        "polises", "sassafrases",
    ])
    def test_singular_s_already_plural(self, plural: str) -> None:
        assert pluralize(plural) == plural



class TestEnAnnexRoundTrip:
    """annex should round-trip correctly (American English)."""

    def test_pluralize_annex(self) -> None:
        assert pluralize("annex") == "annexes"

    def test_singularize_annexes(self) -> None:
        assert singularize("annexes") == "annex"

    def test_round_trip(self) -> None:
        assert singularize(pluralize("annex")) == "annex"



class TestEnFinesseBellyache:
    """finesse and bellyache should round-trip correctly."""

    def test_finesse(self) -> None:
        assert pluralize("finesse") == "finesses"
        assert singularize("finesses") == "finesse"

    def test_bellyache(self) -> None:
        assert pluralize("bellyache") == "bellyaches"
        assert singularize("bellyaches") == "bellyache"



class TestEnCountAware:
    """English count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, count=1) == word

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, count=0) == pluralize(word)

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
        "framework", "endpoint", "callback",
    ])
    def test_en_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, count=2) == pluralize(word)



class TestEnMixedCase:
    """English mixed case preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhone", "iPhones"),
        ("McDonald", "McDonalds"),
        ("WordPress", "WordPresses"),
    ])
    def test_en_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word) == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhones", "iPhone"),
        ("McDonalds", "McDonald"),
        ("WordPresses", "WordPress"),
    ])
    def test_en_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word) == expected



class TestEnSingleLetterAndEdge:
    """English single letters and boundary cases."""

    def test_en_single_letter_a(self) -> None:
        assert pluralize("a") == "as"

    def test_en_single_letter_a_uppercase(self) -> None:
        assert pluralize("A") == "AS"

    def test_en_empty_string(self) -> None:
        assert pluralize("") == ""
        assert singularize("") == ""

    def test_en_whitespace_only(self) -> None:
        assert pluralize("   ") == "   "
        assert singularize("   ") == "   "



class TestEnUncountableConsistency:
    """English uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "sheep", "fish", "deer", "moose", "swine",
        "series", "species", "news", "scissors",
        "trousers", "pants", "glasses",
        "bison", "buffalo", "caribou", "elk", "wildebeest",
        "cod", "salmon", "trout", "pike", "herring",
        "graffiti", "djinn", "pence", "quid",
        "hertz", "chassis", "corps", "debris", "siemens",
        "contretemps", "mews", "haggis", "innings", "proceedings",
        "japanese", "chinese", "vietnamese", "portuguese",
    ])
    def test_en_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word) == word
        assert singularize(word) == word



class TestEnIsSingularIsPlural:
    """English is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "cat", "dog", "house", "child", "mouse",
        "goose", "foot", "tooth", "man", "woman",
        "person", "ox", "cactus", "nucleus", "fungus",
    ])
    def test_en_singular_words(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is False

    @pytest.mark.parametrize("word", [
        "cats", "dogs", "houses", "children", "mice",
        "geese", "feet", "teeth", "men", "women",
        "people", "oxen", "cacti", "nuclei", "fungi",
    ])
    def test_en_plural_words(self, word: str) -> None:
        assert is_plural(word) is True
        assert is_singular(word) is False

    @pytest.mark.parametrize("word", [
        "sheep", "fish", "deer", "series", "species",
        "news", "scissors", "bison", "graffiti",
    ])
    def test_en_uncountable_both(self, word: str) -> None:
        assert is_singular(word) is True
        assert is_plural(word) is True



class TestEnHyphenatedRoundTrip:
    """English hyphenated compound round-trip identity."""

    @pytest.mark.parametrize("word", [
        "mother-in-law", "father-in-law", "brother-in-law",
        "sister-in-law", "daughter-in-law", "son-in-law",
        "attorney-general", "court-martial", "editor-in-chief",
        "forget-me-not", "merry-go-round",
        "meta-analysis", "post-modernism",
    ])
    def test_en_hyphenated_roundtrip(self, word: str) -> None:
        assert singularize(pluralize(word)) == word


# ---------------------------------------------------------------------------
# French edge cases
# ---------------------------------------------------------------------------



