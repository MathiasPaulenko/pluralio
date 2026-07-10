from __future__ import annotations

import pytest

from pluralio import singularize


class TestEnglishSingularRules:
    def test_ies_to_y(self) -> None:
        for plural, singular in [
            ("cities", "city"), ("libraries", "library"), ("parties", "party"),
        ]:
            assert singularize(plural) == singular

    def test_sses_to_ss(self) -> None:
        assert singularize("classes") == "class"

    def test_shes_to_sh(self) -> None:
        assert singularize("brushes") == "brush"

    def test_ches_to_ch(self) -> None:
        assert singularize("churches") == "church"

    def test_xes_to_x(self) -> None:
        assert singularize("boxes") == "box"

    def test_default_strip_s(self) -> None:
        for plural, singular in [("cats", "cat"), ("dogs", "dog"), ("books", "book")]:
            assert singularize(plural) == singular

    def test_ves_to_f(self) -> None:
        for plural, singular in [("wolves", "wolf"), ("leaves", "leaf"), ("calves", "calf"),
                                  ("loaves", "loaf"), ("thieves", "thief"),
                                  ("shelves", "shelf"), ("selves", "self"),
                                  ("halves", "half"), ("hooves", "hoof"),
                                  ("knives", "knife"), ("wives", "wife"), ("lives", "life")]:
            assert singularize(plural) == singular

    def test_ves_false_positives(self) -> None:
        for plural, singular in [
            ("hives", "hive"), ("drives", "drive"), ("gives", "give"),
            ("moves", "move"), ("valves", "valve"), ("solves", "solve"),
            ("twelves", "twelve"), ("carves", "carve"), ("curves", "curve"),
            ("nerves", "nerve"), ("serves", "serve"), ("starves", "starve"),
            ("resolves", "resolve"), ("evolves", "evolve"),
            ("involves", "involve"),
            ("waves", "wave"), ("caves", "cave"), ("saves", "save"),
            ("dives", "dive"), ("fives", "five"),
        ]:
            assert singularize(plural) == singular

    def test_oes_to_o(self) -> None:
        for plural, singular in [("potatoes", "potato"), ("tomatoes", "tomato"),
                                  ("heroes", "hero"), ("echoes", "echo"),
                                  ("vetoes", "veto"), ("torpedoes", "torpedo"),
                                  ("mosquitoes", "mosquito"), ("volcanoes", "volcano")]:
            assert singularize(plural) == singular

    def test_oes_false_positives(self) -> None:
        for plural, singular in [("aloes", "aloe"), ("oboes", "oboe"), ("canoes", "canoe"),
                                  ("shoes", "shoe"), ("toes", "toe"), ("foes", "foe"),
                                  ("hoes", "hoe")]:
            assert singularize(plural) == singular

    def test_s_es_words(self) -> None:
        for plural, singular in [("gases", "gas"), ("buses", "bus"), ("bosses", "boss"),
                                  ("lenses", "lens"), ("crosses", "cross"),
                                  ("statuses", "status"), ("viruses", "virus")]:
            assert singularize(plural) == singular


class TestEnglishIrregularSingles:
    @pytest.mark.parametrize("plural,singular", [
        ("men", "man"), ("women", "woman"), ("children", "child"),
        ("people", "person"), ("mice", "mouse"), ("geese", "goose"),
        ("feet", "foot"), ("teeth", "tooth"), ("oxen", "ox"),
        ("dice", "die"), ("yeses", "yes"),
        ("cacti", "cactus"), ("nuclei", "nucleus"), ("alumni", "alumnus"),
        ("radii", "radius"), ("foci", "focus"), ("fungi", "fungus"),
        ("stimuli", "stimulus"), ("syllabi", "syllabus"),
        ("phenomena", "phenomenon"), ("criteria", "criterion"),
        ("data", "datum"), ("media", "medium"), ("bacteria", "bacterium"),
        ("curricula", "curriculum"), ("memoranda", "memorandum"),
        ("spectra", "spectrum"), ("strata", "stratum"),
        ("analyses", "analysis"), ("bases", "basis"), ("crises", "crisis"),
        ("diagnoses", "diagnosis"), ("hypotheses", "hypothesis"),
        ("oases", "oasis"), ("parentheses", "parenthesis"),
        ("theses", "thesis"), ("axes", "axis"),
        ("matrices", "matrix"), ("indices", "index"),
        ("appendices", "appendix"), ("vertices", "vertex"),
        ("wolves", "wolf"), ("halves", "half"), ("calves", "calf"),
        ("leaves", "leaf"), ("loaves", "loaf"), ("thieves", "thief"),
        ("selves", "self"), ("shelves", "shelf"),
        ("wives", "wife"), ("knives", "knife"), ("lives", "life"),
        ("potatoes", "potato"), ("tomatoes", "tomato"), ("heroes", "hero"),
        ("echoes", "echo"), ("vetoes", "veto"), ("torpedoes", "torpedo"),
        ("mosquitoes", "mosquito"), ("volcanoes", "volcano"),
        ("photos", "photo"), ("pianos", "piano"), ("halos", "halo"),
        ("pies", "pie"), ("ties", "tie"), ("movies", "movie"),
        ("cookies", "cookie"), ("selfies", "selfie"),
        ("buses", "bus"), ("quizzes", "quiz"),
        ("statuses", "status"), ("viruses", "virus"),
        ("cafes", "cafe"), ("safes", "safe"), ("giraffes", "giraffe"),
        ("strafes", "strafe"), ("turfs", "turf"), ("golfs", "golf"),
        ("solos", "solo"), ("cellos", "cello"), ("discos", "disco"),
        ("memos", "memo"), ("autos", "auto"), ("egos", "ego"),
        ("kilos", "kilo"), ("tempos", "tempo"), ("turbos", "turbo"),
        ("dynamos", "dynamo"), ("lassos", "lasso"), ("jumbos", "jumbo"),
        ("mementos", "memento"), ("logos", "logo"), ("embryos", "embryo"),
        ("ghettos", "ghetto"), ("concertos", "concerto"), ("sopranos", "soprano"),
        ("combos", "combo"), ("pros", "pro"),
        ("shoes", "shoe"), ("foes", "foe"), ("hoes", "hoe"),
        ("toes", "toe"),
        ("does", "do"), ("goes", "go"), ("noes", "no"), ("sos", "so"),
        ("dwarves", "dwarf"), ("hooves", "hoof"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural) == singular
