from __future__ import annotations

import pytest

from pluralio import pluralize


class TestPortuguesePluralRules:
    def test_vowel_plus_s(self) -> None:
        for singular, plural in [("casa", "casas"), ("livro", "livros"), ("gato", "gatos")]:
            assert pluralize(singular, lang="pt") == plural

    def test_ao_to_oes(self) -> None:
        for singular, plural in [("coração", "corações"), ("canção", "canções"),
                                 ("balão", "balões")]:
            assert pluralize(singular, lang="pt") == plural

    def test_m_to_ns(self) -> None:
        for singular, plural in [("homem", "homens"), ("jardim", "jardins")]:
            assert pluralize(singular, lang="pt") == plural

    def test_l_to_is(self) -> None:
        for singular, plural in [("animal", "animais"), ("azul", "azuis")]:
            assert pluralize(singular, lang="pt") == plural

    def test_il_to_is(self) -> None:
        for singular, plural in [("barril", "barris"), ("funil", "funis"), ("cantil", "cantis")]:
            assert pluralize(singular, lang="pt") == plural

    def test_r_to_es(self) -> None:
        for singular, plural in [("flor", "flores"), ("motor", "motores")]:
            assert pluralize(singular, lang="pt") == plural

    def test_z_to_zes(self) -> None:
        for singular, plural in [("luz", "luzes"), ("rapaz", "rapazes")]:
            assert pluralize(singular, lang="pt") == plural

    def test_x_invariable(self) -> None:
        for word in ["tórax", "lápis"]:
            assert pluralize(word, lang="pt") == word

    def test_consonant_e_plural(self) -> None:
        for singular, plural in [("nome", "nomes"), ("filme", "filmes"), ("noite", "noites"),
                                 ("chave", "chaves"), ("chefe", "chefes"), ("peixe", "peixes")]:
            assert pluralize(singular, lang="pt") == plural

    def test_already_plural_unchanged(self) -> None:
        for word in ["casas", "livros", "nomes", "filmes"]:
            assert pluralize(word, lang="pt") == word


class TestPortugueseIrregularPlurals:
    @pytest.mark.parametrize("singular,plural", [
        # -ão → -ões
        ("coração", "corações"), ("canção", "canções"), ("balão", "balões"),
        ("feijão", "feijões"), ("limão", "limões"), ("leão", "leões"),
        ("botão", "botões"), ("feição", "feições"), ("travão", "travões"),
        ("estação", "estações"), ("nação", "nações"), ("opinião", "opiniões"),
        ("relação", "relações"), ("função", "funções"), ("instrução", "instruções"),
        # -ão → -ães
        ("cão", "cães"), ("alemão", "alemães"), ("capitão", "capitães"),
        ("charlatão", "charlatães"), ("sacristão", "sacristães"),
        ("escrivão", "escrivães"), ("pão", "pães"),
        # -ão → -ãos
        ("irmão", "irmãos"), ("mão", "mãos"), ("chão", "chãos"),
        ("cristão", "cristãos"), ("cidadão", "cidadãos"), ("órgão", "órgãos"),
        ("grão", "grãos"), ("são", "sãos"),
        # Accent ADDS in plural (-el → -éis)
        ("papel", "papéis"), ("nível", "níveis"), ("fóssil", "fósseis"),
        ("fácil", "fáceis"), ("réptil", "répteis"), ("míssil", "mísseis"),
        # Accent ADDS in plural (-ol → -óis)
        ("sol", "sóis"), ("farol", "faróis"), ("anzol", "anzóis"),
        ("caracol", "caracóis"), ("lençol", "lençóis"),
        # -il (oxítona) → -is
        ("barril", "barris"), ("funil", "funis"), ("fuzil", "fuzis"),
        # -el → -éis (accent)
        ("mel", "méis"), ("fiel", "fiéis"),
        # -il (paroxítona) → -eis
        ("projétil", "projéteis"),
        # Monosyllables / special
        ("bem", "bens"),
        # Foreign loanwords (+s, not +es)
        ("club", "clubs"), ("chip", "chips"), ("bit", "bits"),
        ("email", "emails"), ("link", "links"), ("banner", "banners"),
        ("server", "servers"), ("router", "routers"), ("token", "tokens"),
        ("docker", "dockers"), ("container", "containers"),
        # -s → -ses (accented singulars)
        ("gás", "gases"), ("país", "países"), ("deus", "deuses"),
        # Back-filled from extra singles
        ("português", "portugueses"), ("japonês", "japoneses"),
        ("mês", "meses"),
    ])
    def test_irregular_plural(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="pt") == plural


class TestPortugueseUncountable:
    @pytest.mark.parametrize("word", [
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
    ])
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word
