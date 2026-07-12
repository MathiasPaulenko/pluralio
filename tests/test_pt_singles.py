from __future__ import annotations

import pytest

from pluralio import singularize


class TestPortugueseSingularRules:
    def test_oes_to_ao(self) -> None:
        for plural, singular in [("corações", "coração"), ("balões", "balão")]:
            assert singularize(plural, lang="pt") == singular

    def test_aes_to_ao(self) -> None:
        for plural, singular in [("cães", "cão"), ("pães", "pão")]:
            assert singularize(plural, lang="pt") == singular

    def test_zes_to_z(self) -> None:
        for plural, singular in [("luzes", "luz"), ("rapazes", "rapaz")]:
            assert singularize(plural, lang="pt") == singular

    def test_ns_to_m(self) -> None:
        for plural, singular in [("homens", "homem"), ("jardins", "jardim")]:
            assert singularize(plural, lang="pt") == singular

    def test_is_to_l(self) -> None:
        for plural, singular in [("animais", "animal"), ("azuis", "azul")]:
            assert singularize(plural, lang="pt") == singular

    def test_is_to_il(self) -> None:
        for plural, singular in [("barris", "barril"), ("funis", "funil"), ("cantis", "cantil")]:
            assert singularize(plural, lang="pt") == singular

    def test_vowel_is_strip(self) -> None:
        for plural, singular in [("leis", "lei"), ("reis", "rei"), ("pais", "pai")]:
            assert singularize(plural, lang="pt") == singular

    def test_es_strip(self) -> None:
        for plural, singular in [("flores", "flor"), ("motores", "motor")]:
            assert singularize(plural, lang="pt") == singular

    def test_consonant_e_singular(self) -> None:
        for plural, singular in [("nomes", "nome"), ("filmes", "filme"), ("noites", "noite"),
                                 ("sedes", "sede"), ("redes", "rede"), ("paredes", "parede"),
                                 ("cobres", "cobre"), ("pobres", "pobre"), ("peles", "pele"),
                                 ("vales", "vale"), ("artes", "arte"), ("mortes", "morte"),
                                 ("partes", "parte"), ("elefantes", "elefante"),
                                 ("dificuldades", "dificuldade")]:
            assert singularize(plural, lang="pt") == singular

    def test_s_strip(self) -> None:
        for plural, singular in [("casas", "casa"), ("livros", "livro"),
                                 ("chaves", "chave"), ("chefes", "chefe"), ("peixes", "peixe")]:
            assert singularize(plural, lang="pt") == singular


class TestPortugueseIrregularSingles:
    @pytest.mark.parametrize("plural,singular", [
        # -ões → -ão
        ("corações", "coração"), ("canções", "canção"), ("balões", "balão"),
        ("feijões", "feijão"), ("limões", "limão"), ("leões", "leão"),
        ("botões", "botão"), ("feições", "feição"), ("travões", "travão"),
        ("estações", "estação"), ("nações", "nação"), ("opiniões", "opinião"),
        ("relações", "relação"), ("funções", "função"), ("instruções", "instrução"),
        # -ães → -ão
        ("cães", "cão"), ("alemães", "alemão"), ("capitães", "capitão"),
        ("charlatães", "charlatão"), ("sacristães", "sacristão"),
        ("escrivães", "escrivão"), ("pães", "pão"),
        # -ãos → -ão
        ("irmãos", "irmão"), ("mãos", "mão"), ("chãos", "chão"),
        ("cristãos", "cristão"), ("cidadãos", "cidadão"), ("órgãos", "órgão"),
        ("grãos", "grão"), ("sãos", "são"),
        # -éis → -el
        ("papéis", "papel"), ("níveis", "nível"),
        ("méis", "mel"), ("fiéis", "fiel"),
        ("fósseis", "fóssil"), ("fáceis", "fácil"),
        ("répteis", "réptil"), ("mísseis", "míssil"),
        # -óis → -ol
        ("sóis", "sol"), ("faróis", "farol"), ("anzóis", "anzol"),
        ("caracóis", "caracol"), ("lençóis", "lençol"),
        # -is → -il
        ("barris", "barril"), ("funis", "funil"), ("fuzis", "fuzil"),
        # -eis → -il
        ("projéteis", "projétil"),
        # Special
        ("bens", "bem"),
        # Loanwords
        ("clubs", "club"), ("chips", "chip"), ("bits", "bit"),
        ("emails", "email"), ("links", "link"), ("banners", "banner"),
        ("servers", "server"), ("routers", "router"), ("tokens", "token"),
        ("dockers", "docker"), ("containers", "container"),
        # -s → -ses (accented singulars)
        ("gases", "gás"), ("países", "país"), ("deuses", "deus"),
        # Extra singles (accent restoration)
        ("portugueses", "português"), ("japoneses", "japonês"),
        ("meses", "mês"),
        ("leis", "lei"), ("reis", "rei"), ("pais", "pai"),
        ("árvores", "árvore"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="pt") == singular
