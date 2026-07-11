from __future__ import annotations

import pytest

from pluralio import pluralize


class TestEnglishPluralRules:
    def test_consonant_plus_y_to_ies(self) -> None:
        for singular, plural in [
            ("city", "cities"), ("library", "libraries"), ("party", "parties"),
        ]:
            assert pluralize(singular) == plural

    def test_vowel_plus_y_to_ys(self) -> None:
        for singular, plural in [("boy", "boys"), ("key", "keys"), ("day", "days")]:
            assert pluralize(singular) == plural

    def test_s_ss_sh_ch_x_z_to_es(self) -> None:
        for singular, plural in [("box", "boxes"), ("church", "churches"), ("bus", "buses"),
                                  ("class", "classes"), ("brush", "brushes"), ("dish", "dishes")]:
            assert pluralize(singular) == plural

    def test_default_plus_s(self) -> None:
        for singular, plural in [("book", "books"), ("car", "cars"), ("cat", "cats"),
                                  ("shoe", "shoes")]:
            assert pluralize(singular) == plural

    def test_fe_to_ves(self) -> None:
        for singular, plural in [("knife", "knives"), ("wife", "wives"), ("life", "lives")]:
            assert pluralize(singular) == plural

    def test_consonant_f_to_ves(self) -> None:
        for singular, plural in [("wolf", "wolves"), ("leaf", "leaves"), ("calf", "calves"),
                                  ("loaf", "loaves"), ("thief", "thieves"),
                                  ("shelf", "shelves"), ("self", "selves"),
                                  ("half", "halves")]:
            assert pluralize(singular) == plural
    def test_consonant_o_to_oes(self) -> None:
        for singular, plural in [("potato", "potatoes"), ("tomato", "tomatoes"),
                                  ("hero", "heroes"), ("echo", "echoes"),
                                  ("veto", "vetoes"), ("torpedo", "torpedoes"),
                                  ("mosquito", "mosquitoes"), ("volcano", "volcanoes")]:
            assert pluralize(singular) == plural

    def test_o_exceptions_just_s(self) -> None:
        for singular, plural in [
            ("photo", "photos"), ("piano", "pianos"), ("halo", "halos"),
            ("solo", "solos"), ("cello", "cellos"), ("disco", "discos"),
            ("memo", "memos"), ("auto", "autos"), ("ego", "egos"),
            ("kilo", "kilos"), ("tempo", "tempos"), ("turbo", "turbos"),
            ("logo", "logos"), ("pro", "pros"), ("combo", "combos"),
            ("casino", "casinos"), ("taco", "tacos"), ("burrito", "burritos"),
            ("poncho", "ponchos"), ("sombrero", "sombreros"),
            ("flamingo", "flamingos"),
            ("avocado", "avocados"),
        ]:
            assert pluralize(singular) == plural

    def test_fe_exceptions_just_s(self) -> None:
        for singular, plural in [("cafe", "cafes"), ("safe", "safes"), ("giraffe", "giraffes"),
                                  ("strafe", "strafes")]:
            assert pluralize(singular) == plural

    def test_f_exceptions_just_s(self) -> None:
        for singular, plural in [
            ("turf", "turfs"), ("golf", "golfs"), ("dwarf", "dwarfs"),
            ("brief", "briefs"), ("chief", "chiefs"), ("roof", "roofs"),
            ("proof", "proofs"), ("belief", "beliefs"), ("relief", "reliefs"),
        ]:
            assert pluralize(singular) == plural


class TestEnglishIrregularPlurals:
    @pytest.mark.parametrize("singular,plural", [
        ("man", "men"), ("woman", "women"), ("child", "children"),
        ("person", "people"), ("mouse", "mice"), ("goose", "geese"),
        ("foot", "feet"), ("tooth", "teeth"), ("ox", "oxen"),
        ("die", "dice"), ("yes", "yeses"),
        ("cactus", "cacti"), ("nucleus", "nuclei"), ("alumnus", "alumni"),
        ("radius", "radii"), ("focus", "foci"), ("fungus", "fungi"),
        ("stimulus", "stimuli"), ("syllabus", "syllabi"),
        ("phenomenon", "phenomena"), ("criterion", "criteria"),
        ("datum", "data"), ("medium", "media"), ("bacterium", "bacteria"),
        ("curriculum", "curricula"), ("memorandum", "memoranda"),
        ("spectrum", "spectra"), ("stratum", "strata"),
        ("analysis", "analyses"), ("basis", "bases"), ("crisis", "crises"),
        ("diagnosis", "diagnoses"), ("hypothesis", "hypotheses"),
        ("oasis", "oases"), ("parenthesis", "parentheses"),
        ("thesis", "theses"), ("axis", "axes"),
        ("matrix", "matrices"), ("index", "indices"),
        ("appendix", "appendices"), ("vertex", "vertices"),
        ("wolf", "wolves"), ("half", "halves"), ("calf", "calves"),
        ("leaf", "leaves"), ("loaf", "loaves"), ("thief", "thieves"),
        ("self", "selves"), ("shelf", "shelves"),
        ("wife", "wives"), ("knife", "knives"), ("life", "lives"),
        ("potato", "potatoes"), ("tomato", "tomatoes"), ("hero", "heroes"),
        ("echo", "echoes"), ("veto", "vetoes"), ("torpedo", "torpedoes"),
        ("mosquito", "mosquitoes"), ("volcano", "volcanoes"),
        ("photo", "photos"), ("piano", "pianos"), ("halo", "halos"),
        ("pie", "pies"), ("tie", "ties"), ("movie", "movies"),
        ("cookie", "cookies"), ("selfie", "selfies"),
        ("bus", "buses"), ("quiz", "quizzes"),
        ("status", "statuses"), ("virus", "viruses"),
        ("cafe", "cafes"), ("safe", "safes"), ("giraffe", "giraffes"),
        ("strafe", "strafes"), ("turf", "turfs"), ("golf", "golfs"),
        ("solo", "solos"), ("cello", "cellos"), ("disco", "discos"),
        ("memo", "memos"), ("auto", "autos"), ("ego", "egos"),
        ("kilo", "kilos"), ("tempo", "tempos"), ("turbo", "turbos"),
        ("dynamo", "dynamos"), ("lasso", "lassos"), ("jumbo", "jumbos"),
        ("memento", "mementos"), ("logo", "logos"), ("embryo", "embryos"),
        ("ghetto", "ghettos"), ("concerto", "concertos"), ("soprano", "sopranos"),
        ("combo", "combos"), ("pro", "pros"),
        ("shoe", "shoes"), ("foe", "foes"), ("hoe", "hoes"),
        ("toe", "toes"), ("doe", "does"),
        ("go", "goes"), ("no", "noes"), ("so", "sos"), ("do", "does"),
        ("hoof", "hooves"), ("dwarf", "dwarfs"),
        ("brief", "briefs"), ("chief", "chiefs"), ("roof", "roofs"),
        ("proof", "proofs"), ("belief", "beliefs"), ("relief", "reliefs"),
        ("casino", "casinos"), ("taco", "tacos"), ("burrito", "burritos"),
        ("poncho", "ponchos"), ("sombrero", "sombreros"),
        ("flamingo", "flamingos"),
        ("avocado", "avocados"),
        ("aloe", "aloes"), ("oboe", "oboes"), ("canoe", "canoes"),
        ("gas", "gases"), ("boss", "bosses"),
        ("lens", "lenses"), ("cross", "crosses"),
    ])
    def test_irregular_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular) == plural


class TestEnglishUncountable:
    @pytest.mark.parametrize("word", [
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
        "politics", "ethics", "gymnastics", "linguistics", "athletics",
        "civics", "statistics", "informatics", "classics", "mechanics",
        "dynamics", "genetics", "obstetrics", "pediatrics", "psychiatrics",
        "orthopaedics", "academics", "logistics", "hysterics",
        "billiards", "darts", "checkers", "craps",
    ])
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word) == word
