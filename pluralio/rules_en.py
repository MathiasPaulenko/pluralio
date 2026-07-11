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
    # Fase 4: Foreign -o words pluralized with -os (not -oes)
    # Instrumentos
    "allegro": "allegros", "bolero": "boleros", "bongo": "bongos",
    "canto": "cantos", "falsetto": "falsettos", "intermezzo": "intermezzos",
    "rondo": "rondos", "staccato": "staccatos", "tremolo": "tremolos",
    "vibrato": "vibratos", "violoncello": "violoncellos", "timpano": "timpanos",
    # Comida/bebida
    "cappuccino": "cappuccinos", "cilantro": "cilantros", "coco": "cocos",
    "espresso": "espressos", "gyro": "gyros", "oregano": "oreganos",
    "pimento": "pimentos", "pinto": "pintos", "risotto": "risottos",
    "tobacco": "tobaccos", "burro": "burros",
    # Animales
    "albino": "albinos", "armadillo": "armadillos", "hippo": "hippos",
    "rhino": "rhinos",
    # Objetos
    "archipelago": "archipelagos", "bingo": "bingos", "commando": "commandos",
    "ditto": "dittos", "fiasco": "fiascos", "gizmo": "gizmos",
    "hairdo": "hairdos", "lumbago": "lumbagos", "magneto": "magnetos",
    "manifesto": "manifestos", "sterno": "sternos", "stucco": "stuccos",
    "terrazzo": "terrazzos", "torso": "torsos", "ufo": "ufos",
    # Otros
    "aficionado": "aficionados", "aggro": "aggros", "ammo": "ammos",
    "credo": "credos", "crescendo": "crescendos", "cyano": "cyanos",
    "demo": "demos", "euro": "euros", "flamenco": "flamencos",
    "furioso": "furiosos", "generalissimo": "generalissimos", "gigolo": "gigolos",
    "gringo": "gringos", "guano": "guanos", "gumbo": "gumbos",
    "impetigo": "impetigos", "info": "infos", "lingo": "lingos",
    "lino": "linos", "livedo": "livedos", "loco": "locos",
    "macho": "machos", "macro": "macros", "mafioso": "mafiosos",
    "magnifico": "magnificos", "medico": "medicos", "metro": "metros",
    "micro": "micros", "neutrino": "neutrinos", "octavo": "octavos",
    "pedalo": "pedalos", "pleco": "plecos", "polo": "polos",
    "psycho": "psychos", "pueblo": "pueblos", "quarto": "quartos",
    "repo": "repos", "rococo": "rococos", "saddo": "saddos",
    "sago": "sagos", "salvo": "salvos", "sirocco": "siroccos",
    "stylo": "stylos", "sumo": "sumos", "techno": "technos",
    "testudo": "testudos", "tiro": "tiros", "torero": "toreros",
    "typo": "typos", "tyro": "tyros", "vaquero": "vaqueros",
    "vermicelli": "vermicellis", "verso": "versos", "weirdo": "weirdos",
    "yo-yo": "yo-yos", "zero": "zeros",
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
    # Words ending in -che (singular ends in -che, plural adds -s)
    # Must be explicit because (ss|sh|ch|x|zz)es$ rule would strip -es
    # leaving wrong stem (e.g. caches -> cach instead of cache)
    "ache": "aches",
    "cache": "caches", "niche": "niches", "creche": "creches",
    "apache": "apaches", "machete": "machetes",
    "mustache": "mustaches", "moustache": "moustaches",
    "avalanche": "avalanches",
    "psyche": "psyches", "demarche": "demarches",
    "thelarche": "thelarches", "tranche": "tranches",
    "cliche": "cliches", "quiche": "quiches", "panache": "panaches",
    "brioche": "brioches", "pastiche": "pastiches",
    "douche": "douches", "gouache": "gouaches",
    "cloche": "cloches", "barouche": "barouches",
    "cartouche": "cartouches", "caliche": "caliches",
    "huarache": "huaraches", "seiche": "seiches",
    "troche": "troches", "microfiche": "microfiches",
    "attache": "attaches", "synecdoche": "synecdoches",
    # Compound -ache words (headache, earache, etc.)
    "headache": "headaches", "earache": "earaches",
    "toothache": "toothaches", "backache": "backaches",
    "heartache": "heartaches", "stomachache": "stomachaches",
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
    # Fase 6: Additional singular -s words that need +es
    "acropolis": "acropolises", "aegis": "aegises", "alias": "aliases",
    "asbestos": "asbestoses", "bathos": "bathoses", "caddis": "caddises",
    "cannabis": "cannabises", "cosmos": "cosmoses", "dais": "daises",
    "digitalis": "digitalises", "epidermis": "epidermises",
    "ethos": "ethoses", "eyas": "eyases", "glottis": "glottises",
    "hubris": "hubrises", "ibis": "ibises", "mantis": "mantises",
    "marquis": "marquises", "metropolis": "metropolises",
    "pathos": "pathoses", "polis": "polises", "sassafras": "sassafrases",
    # 1.1 -um → -a (unconditional)
    "desideratum": "desiderata", "extremum": "extrema",
    "candelabrum": "candelabra",
    # 1.2 -um → -a (classical)
    "maximum": "maxima", "minimum": "minima", "momentum": "momenta",
    "optimum": "optima", "quantum": "quanta", "cranium": "crania",
    "dictum": "dicta", "phylum": "phyla", "aquarium": "aquaria",
    "compendium": "compendia", "emporium": "emporia", "encomium": "encomia",
    "gymnasium": "gymnasia", "honorarium": "honoraria", "interregnum": "interregna",
    "lustrum": "lustra", "millennium": "millennia", "rostrum": "rostra",
    "speculum": "specula", "stadium": "stadia", "trapezium": "trapezia",
    "ultimatum": "ultimata", "vacuum": "vacua", "velum": "vela",
    "consortium": "consortia", "arboretum": "arboreta",
    # 1.3 -a → -ata (classical)
    "anathema": "anathemata", "bema": "bemata", "carcinoma": "carcinomata",
    "charisma": "charismata", "diploma": "diplomata", "dogma": "dogmata",
    "drama": "dramata", "edema": "edemata", "enema": "enemata",
    "enigma": "enigmata", "lemma": "lemmata", "lymphoma": "lymphomata",
    "magma": "magmata", "melisma": "melismata", "miasma": "miasmata",
    "oedema": "oedemata", "sarcoma": "sarcomata", "schema": "schemata",
    "soma": "somata", "stigma": "stigmata", "stoma": "stomata",
    "trauma": "traumata", "gumma": "gummata", "pragma": "pragmata",
    # 1.4 -a → -ae (unconditional)
    "alumna": "alumnae", "alga": "algae", "vertebra": "vertebrae",
    "persona": "personae", "vita": "vitae",
    # 1.5 -a → -ae (classical)
    "amoeba": "amoebae", "antenna": "antennae", "formula": "formulae",
    "hyperbola": "hyperbolae", "medusa": "medusae", "nebula": "nebulae",
    "parabola": "parabolae", "abscissa": "abscissae", "hydra": "hydrae",
    "nova": "novae", "lacuna": "lacunae", "aurora": "aurorae",
    "umbra": "umbrae", "flora": "florae", "fauna": "faunae",
    # 1.6 -en → -ina (classical)
    "stamen": "stamina", "foramen": "foramina", "lumen": "lumina",
    # 1.7 -is → -ides (classical)
    "ephemeris": "ephemerides", "clitoris": "clitorides",
    "chrysalis": "chrysalides", "epididymis": "epididymides",
    # 1.8 -itis → -itides
    "arthritis": "arthritides", "bronchitis": "bronchitides",
    "bursitis": "bursitides", "colitis": "colitides",
    "dermatitis": "dermatitides", "encephalitis": "encephalitides",
    "gastroenteritis": "gastroenteritides", "hepatitis": "hepatitides",
    "meningitis": "meningitides", "neuritis": "neuritides",
    "peritonitis": "peritonitides", "pharyngitis": "pharyngitides",
    "sinusitis": "sinusitides", "tonsillitis": "tonsillitides",
    "vasculitis": "vasculitides",
    # 1.11 -on → -a (unconditional)
    "perihelion": "perihelia", "aphelion": "aphelia",
    "prolegomenon": "prolegomena", "noumenon": "noumena",
    "organon": "organa", "asyndeton": "asyndeta", "hyperbaton": "hyperbata",
    # 1.12 -on → -a (classical)
    "oxymoron": "oxymora",
    # 1.13 -ix/ex → -ices (unconditional)
    "murex": "murices", "silex": "silices",
    # 1.14 -ix/ex → -ices (classical)
    "latex": "latices", "pontifex": "pontifices", "simplex": "simplices",
    # 1.15 Hebrew → -im
    "goy": "goyim", "seraph": "seraphim", "cherub": "cherubim",
    # 1.16 Arabic → -i
    "afrit": "afriti", "afreet": "afreeti", "efreet": "efreeti",
    # 1.17 Other irregulars
    "mythos": "mythoi", "penis": "penises", "testis": "testes",
    "chili": "chilis", "brother": "brothers", "infinity": "infinities",
    "lore": "lores", "beef": "beefs", "money": "monies",
    "mongoose": "mongooses", "cow": "cows", "graffito": "graffiti",
    "genie": "genies", "ganglion": "ganglions", "trilby": "trilbys",
    "numen": "numina", "atman": "atmas", "occiput": "occiputs",
    "sabretooth": "sabretooths", "sabertooth": "sabertooths",
    "lowlife": "lowlifes", "flatfoot": "flatfoots", "tenderfoot": "tenderfoots",
    "romany": "romanies", "jerry": "jerries", "mary": "maries",
    "rom": "roma", "carmen": "carmina",
    # Proper nouns ending in -ie (lowercase, case preserved by engine)
    "addie": "addies", "aggie": "aggies", "allie": "allies",
    "amie": "amies", "angie": "angies", "annie": "annies",
    "annmarie": "annmaries", "archie": "archies", "artie": "arties",
    "barbie": "barbies", "basie": "basies", "bennie": "bennies",
    "bernie": "bernies", "bertie": "berties", "bessie": "bessies",
    "betty": "betties", "billie": "billies", "bobbie": "bobbies",
    "bonnie": "bonnies", "bowie": "bowies", "brandie": "brandies",
    "brie": "bries", "callie": "callies", "carnegie": "carnegies",
    "carrie": "carries", "cassie": "cassies", "charlie": "charlies",
    "cherie": "cheries", "christie": "christies", "connie": "connies",
    "curie": "curies", "dannie": "dannies", "debbie": "debbies",
    "dollie": "dollies", "donnie": "donnies", "drambuie": "drambuies",
    "eddie": "eddies", "effie": "effies", "ellie": "ellies",
    "elsie": "elsies", "erie": "eries", "ernie": "ernies",
    "essie": "essies", "eugenie": "eugenies", "fannie": "fannies",
    "flossie": "flossies", "frankie": "frankies", "freddie": "freddies",
    "gillespie": "gillespies", "goldie": "goldies", "gracie": "gracies",
    "guthrie": "guthries", "hallie": "hallies", "hattie": "hatties",
    "hettie": "hetties", "hollie": "hollies", "jackie": "jackies",
    "jamie": "jamies", "janie": "janies", "jannie": "jannies",
    "jeanie": "jeanies", "jeannie": "jeannies", "jennie": "jennies",
    "jessie": "jessies", "jimmie": "jimmies", "jodie": "jodies",
    "johnie": "johnies", "johnnie": "johnnies", "josie": "josies",
    "julie": "julies", "kalgoorlie": "kalgoorlies", "kathie": "kathies",
    "katie": "katies", "kellie": "kellies", "kewpie": "kewpies",
    "kristie": "kristies", "laramie": "laramies", "laurie": "lauries",
    "leslie": "leslies", "lessie": "lessies", "lillie": "lillies",
    "lizzie": "lizzies", "lonnie": "lonnies", "lorie": "lories",
    "lorrie": "lorries", "lottie": "lotties", "louie": "louies",
    "mackenzie": "mackenzies", "maggie": "maggies", "maisie": "maisies",
    "mamie": "mamies", "marcie": "marcies", "margie": "margies",
    "marie": "maries", "marjorie": "marjories", "mattie": "matties",
    "mckenzie": "mckenzies", "melanie": "melanies", "mickie": "mickies",
    "millie": "millies", "minnie": "minnies", "mollie": "mollies",
    "mountie": "mounties", "nannie": "nannies", "natalie": "natalies",
    "nellie": "nellies", "nettie": "netties", "ollie": "ollies",
    "ozzie": "ozzies", "pearlie": "pearlies", "pottawatomie": "pottawatomies",
    "reggie": "reggies", "richie": "richies", "rickie": "rickies",
    "robbie": "robbies", "ronnie": "ronnies", "rosalie": "rosalies",
    "rosemarie": "rosemaries", "rosie": "rosies", "roxie": "roxies",
    "rushdie": "rushdies", "ruthie": "ruthies", "sadie": "sadies",
    "sallie": "sallies", "sammie": "sammies", "scottie": "scotties",
    "selassie": "selassies", "sherry": "sherries", "sophie": "sophies",
    "stacie": "stacies", "stefanie": "stefanies", "stephanie": "stephanies",
    "stevie": "stevies", "susie": "susies", "sylvie": "sylvies",
    "tammie": "tammies", "terrie": "terries", "tessie": "tessies",
    "tommie": "tommies", "tracie": "tracies", "trekkie": "trekkies",
    "valarie": "valaries", "valerie": "valeries", "valkyrie": "valkyries",
    "vickie": "vickies", "virgie": "virgies", "willie": "willies",
    "winnie": "winnies", "wylie": "wylies", "yorkie": "yorkies",
}
"""Mapping of singular → plural for irregular English words.

These words do not follow any regex pattern and must be looked up
directly. All keys and values are lowercase.
"""

_IRREGULAR_SINGLES: dict[str, str] = {v: k for k, v in _IRREGULAR_PLURALS.items()}
"""Auto-generated inverse mapping (plural → singular) for irregulars."""

_IRREGULAR_SINGLES["dwarves"] = "dwarf"
"""Additional singular for ``dwarves`` (alternative plural of ``dwarf``)."""

# === Fase 3: Singularización inversa explícita ===

_EXTRA_SINGLES: dict[str, str] = {
    # uses → use
    "abuses": "abuse",
    "applauses": "applause",
    "blouses": "blouse",
    "carouses": "carouse",
    "causes": "cause",
    "chartreuses": "chartreuse",
    "clauses": "clause",
    "contuses": "contuse",
    "douses": "douse",
    "excuses": "excuse",
    "fuses": "fuse",
    "hypotenuses": "hypotenuse",
    "masseuses": "masseuse",
    "menopauses": "menopause",
    "misuses": "misuse",
    "muses": "muse",
    "overuses": "overuse",
    "pauses": "pause",
    "peruses": "peruse",
    "profuses": "profuse",
    "recluses": "recluse",
    "reuses": "reuse",
    "ruses": "ruse",
    "souses": "souse",
    "spouses": "spouse",
    "suffuses": "suffuse",
    "transfuses": "transfuse",
    "uses": "use",
    # ies → ie (comunes)
    "aeries": "aerie",
    "baggies": "baggie",
    "belies": "belie",
    "biggies": "biggie",
    "bonnies": "bonnie",
    "boogies": "boogie",
    "bookies": "bookie",
    "bourgeoisies": "bourgeoisie",
    "budgies": "budgie",
    "caddies": "caddie",
    "camaraderies": "camaraderie",
    "cockamamies": "cockamamie",
    "cooties": "cootie",
    "coteries": "coterie",
    "crappies": "crappie",
    "curies": "curie",
    "cutesies": "cutesie",
    "dogies": "dogie",
    "eyries": "eyrie",
    "floozies": "floozie",
    "footsies": "footsie",
    "freebies": "freebie",
    "goalies": "goalie",
    "hies": "hie",
    "jalousies": "jalousie",
    "kiddies": "kiddie",
    "laddies": "laddie",
    "lies": "lie",
    "lingeries": "lingerie",
    "magpies": "magpie",
    "menageries": "menagerie",
    "mommies": "mommie",
    "neckties": "necktie",
    "nighties": "nightie",
    "oldies": "oldie",
    "organdies": "organdie",
    "overlies": "overlie",
    "potpies": "potpie",
    "prairies": "prairie",
    "reveries": "reverie",
    "rookies": "rookie",
    "rotisseries": "rotisserie",
    "softies": "softie",
    "sorties": "sortie",
    "stymies": "stymie",
    "underlies": "underlie",
    "unties": "untie",
    "vies": "vie",
    "zombies": "zombie",
    # ies → ie (nombres propios, lowercase)
    "addies": "addie",
    "aggies": "aggie",
    "allies": "allie",
    "amies": "amie",
    "angies": "angie",
    "annies": "annie",
    "annmaries": "annmarie",
    "archies": "archie",
    "arties": "artie",
    "barbies": "barbie",
    "basies": "basie",
    "bennies": "bennie",
    "bernies": "bernie",
    "berties": "bertie",
    "bessies": "bessie",
    "betties": "betty",
    "billies": "billie",
    "blondies": "blondie",
    "bowies": "bowie",
    "brandies": "brandie",
    "bries": "brie",
    "callies": "callie",
    "carnegies": "carnegie",
    "carries": "carrie",
    "cassies": "cassie",
    "charlies": "charlie",
    "cheries": "cherie",
    "christies": "christie",
    "connies": "connie",
    "dannies": "dannie",
    "debbies": "debbie",
    "dixies": "dixie",
    "dollies": "dollie",
    "donnies": "donnie",
    "drambuies": "drambuie",
    "eddies": "eddie",
    "effies": "effie",
    "ellies": "ellie",
    "elsies": "elsie",
    "eries": "erie",
    "ernies": "ernie",
    "essies": "essie",
    "eugenies": "eugenie",
    "fannies": "fannie",
    "flossies": "flossie",
    "frankies": "frankie",
    "freddies": "freddie",
    "gillespies": "gillespie",
    "goldies": "goldie",
    "gracies": "gracie",
    "guthries": "guthrie",
    "hallies": "hallie",
    "hatties": "hattie",
    "hetties": "hettie",
    "hollies": "hollie",
    "jackies": "jackie",
    "jamies": "jamie",
    "janies": "janie",
    "jannies": "jannie",
    "jeanies": "jeanie",
    "jeannies": "jeannie",
    "jennies": "jennie",
    "jessies": "jessie",
    "jimmies": "jimmie",
    "jodies": "jodie",
    "johnies": "johnie",
    "johnnies": "johnnie",
    "josies": "josie",
    "julies": "julie",
    "kalgoorlies": "kalgoorlie",
    "kathies": "kathie",
    "katies": "katie",
    "kellies": "kellie",
    "kewpies": "kewpie",
    "kristies": "kristie",
    "laramies": "laramie",
    "lauries": "laurie",
    "leslies": "leslie",
    "lessies": "lessie",
    "lillies": "lillie",
    "lizzies": "lizzie",
    "lonnies": "lonnie",
    "lories": "lorie",
    "lorries": "lorrie",
    "lotties": "lottie",
    "louies": "louie",
    "mackenzies": "mackenzie",
    "maggies": "maggie",
    "maisies": "maisie",
    "mamies": "mamie",
    "marcies": "marcie",
    "margies": "margie",
    "marjories": "marjorie",
    "matties": "mattie",
    "mckenzies": "mckenzie",
    "melanies": "melanie",
    "mickies": "mickie",
    "millies": "millie",
    "minnies": "minnie",
    "mollies": "mollie",
    "mounties": "mountie",
    "nannies": "nannie",
    "natalies": "natalie",
    "nellies": "nellie",
    "netties": "nettie",
    "ollies": "ollie",
    "ozzies": "ozzie",
    "pearlies": "pearlie",
    "pottawatomies": "pottawatomie",
    "reggies": "reggie",
    "richies": "richie",
    "rickies": "rickie",
    "robbies": "robbie",
    "ronnies": "ronnie",
    "rosalies": "rosalie",
    "rosemaries": "rosemarie",
    "rosies": "rosie",
    "roxies": "roxie",
    "rushdies": "rushdie",
    "ruthies": "ruthie",
    "sadies": "sadie",
    "sallies": "sallie",
    "sammies": "sammie",
    "scotties": "scottie",
    "selassies": "selassie",
    "sherries": "sherry",
    "sophies": "sophie",
    "stacies": "stacie",
    "stefanies": "stefanie",
    "stephanies": "stephanie",
    "stevies": "stevie",
    "susies": "susie",
    "sylvies": "sylvie",
    "tammies": "tammie",
    "terries": "terrie",
    "tessies": "tessie",
    "tommies": "tommie",
    "tracies": "tracie",
    "trekkies": "trekkie",
    "valaries": "valarie",
    "valeries": "valerie",
    "valkyries": "valkyrie",
    "vickies": "vickie",
    "virgies": "virgie",
    "willies": "willie",
    "winnies": "winnie",
    "wylies": "wylie",
    "yorkies": "yorkie",
    # es → is
    "amanuenses": "amanuensis",
    "amniocenteses": "amniocentesis",
    "antitheses": "antithesis",
    "apotheoses": "apotheosis",
    "arterioscleroses": "arteriosclerosis",
    "atheroscleroses": "atherosclerosis",
    "catalyses": "catalysis",
    "catharses": "catharsis",
    "cirrhoses": "cirrhosis",
    "cocces": "coccus",
    "dialyses": "dialysis",
    "diereses": "dieresis",
    "electrolyses": "electrolysis",
    "exegeses": "exegesis",
    "geneses": "genesis",
    "halitoses": "halitosis",
    "hydrolyses": "hydrolysis",
    "hypnoses": "hypnosis",
    "hystereses": "hysteresis",
    "metamorphoses": "metamorphosis",
    "metastases": "metastasis",
    "misdiagnoses": "misdiagnosis",
    "mitoses": "mitosis",
    "mononucleoses": "mononucleosis",
    "narcoses": "narcosis",
    "necroses": "necrosis",
    "nemeses": "nemesis",
    "osmoses": "osmosis",
    "osteoporoses": "osteoporosis",
    "parthenogeneses": "parthenogenesis",
    "periphrases": "periphrasis",
    "photosyntheses": "photosynthesis",
    "preces": "prex",
    "probosces": "proboscis",
    "prognoses": "prognosis",
    "prophylaxes": "prophylaxis",
    "prostheses": "prosthesis",
    "psychoanalyses": "psychoanalysis",
    "psychokineses": "psychokinesis",
    "psychoses": "psychosis",
    "scleroses": "sclerosis",
    "scolioses": "scoliosis",
    "sepses": "sepsis",
    "silicoses": "silicosis",
    "symbioses": "symbiosis",
    "syntheses": "synthesis",
    "taxes": "tax",
    "telekineses": "telekinesis",
    "thromboses": "thrombosis",
    "urinalyses": "urinalysis",
    # oes → oe
    "backhoes": "backhoe",
    "floes": "floe",
    "mistletoes": "mistletoe",
    "pekoes": "pekoe",
    "sloes": "sloe",
    "throes": "throe",
    "tiptoes": "tiptoe",
    "woes": "woe",
    # ches → che (nombres propios, lowercase)
    "andromaches": "andromache",
    "blanches": "blanche",
    "comanches": "comanche",
    "nietzsches": "nietzsche",
    "porsches": "porsche",
    "roches": "roche",
    # sses → sse (nombres propios, lowercase)
    "hesses": "hesse",
    "jesses": "jesse",
    "larousses": "larousse",
    "matisses": "matisse",
    # ves → ve (nombres propios, lowercase)
    "clives": "clive",
    "palmolives": "palmolive",
    # xes → xe
    "annexes": "annexe",
    "deluxes": "deluxe",
    "pickaxes": "pickaxe",
    # zzes → zz
    "buzzes": "buzz",
    "fizzes": "fizz",
    "frizzes": "frizz",
    "razzes": "razz",
    # ois → oi (nombres propios, lowercase)
    "bolshois": "bolshoi",
    "hanois": "hanoi",
}
_IRREGULAR_SINGLES.update(_EXTRA_SINGLES)

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
2. Words ending in ``s``, ``ss``, ``sh``, ``ch``, ``x``, ``z`` + ``es``
   → strip ``es`` (e.g. ``"beaches" → "beach"``, ``"boxes" → "box"``).
   Words ending in ``-che`` (e.g. ``"caches"``) are handled by
   irregulars, not this rule.
3. Words ending in ``ses`` → replace with ``se``.
4. Words ending in ``zes`` → replace with ``ze``.
5. Words ending in consonant + ``oes`` → replace with consonant + ``o``.
6. Words ending in ``is``, ``us``, ``ness`` → unchanged (Latin/Greek singular).
7. Compound ``f→ves`` words → singularize back to ``f`` form
   (e.g. ``"afterlives" → "afterlife"``, ``"housewives" → "housewife"``).
   Base words (``life``, ``wife``, etc.) are handled by irregulars.
   The ``[^aeiou]`` guard on ``lives$`` prevents false positives
   like ``"olives" → "olife"``.
8. Words ending in ``ss`` → unchanged (already singular, e.g. ``"glass"``,
   ``"dress"``, ``"loss"``).
9. Default: strip trailing ``s``.

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
    "rice", "bread", "pork", "milk", "cheese",
    "butter", "coffee", "tea", "juice", "water", "fruit",
    "sugar", "salt", "pepper", "soup", "pasta",
    "gold", "silver", "iron", "steel", "wood",
    "plastic", "rubber", "leather", "paper", "cotton", "wool",
    "information", "equipment", "news", "furniture", "luggage",
    "advice", "knowledge", "research", "evidence",
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
    # Demonyms ending in -ese (invariable: same for singular and plural)
    "japanese", "chinese", "vietnamese", "burmese", "lebanese",
    "portuguese", "javanese", "sundanese", "senegalese", "congolese",
    "sudanese", "maltese", "siamese",
    # 2.1 Animals/herd (invariable)
    "bison", "buffalo", "caribou", "elk", "swine", "wildebeest", "eland",
    # 2.2 Fish (invariable)
    "cod", "flounder", "grouse", "haddock", "hake", "halibut", "herring",
    "mackerel", "pike", "roe", "shad", "snipe", "teal", "turbot",
    "bream", "carp", "dace", "pickerel",
    # 2.3 Other uncountables
    "graffiti", "djinn", "pence", "quid", "hertz", "chassis", "corps",
    "debris", "siemens", "contretemps", "mews", "haggis", "innings",
    "proceedings", "jackanapes", "zucchini", "quinoa",
    # 7.1 Additional demonyms ending in -ese
    "amoyese", "borghese", "congoese", "faroese", "foochowese",
    "genevese", "genoese", "gilbertese", "hottentotese", "kiplingese",
    "kongoese", "lucchese", "nankingese", "niasese", "pekingese",
    "piedmontese", "pistoiese", "sarawakese", "shavese", "vermontese",
    "wenchowese", "yengeese",
    # 7.2 Additional fish (invariable)
    "blowfish", "angelfish", "jellyfish", "catfish", "swordfish",
    "goldfish", "starfish", "pufferfish", "sunfish", "bluefish",
    "blackfish", "codfish", "dogfish", "flatfish", "monkfish",
    "reeffish", "sawfish", "stonefish", "toadfish", "whitefish",
    # 7.3 Pox diseases (invariable)
    "chickenpox", "smallpox", "cowpox", "foxpox", "gerbilpox",
    "monkeypox", "mousepox", "rabbitpox", "raccoonpox", "skunkpox",
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
