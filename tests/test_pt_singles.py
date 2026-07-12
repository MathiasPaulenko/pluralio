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
        ("criações", "criação"), ("emoções", "emoção"), ("regiões", "região"),
        ("temporões", "temporão"), ("verões", "verão"),
        ("questões", "questão"), ("lições", "lição"),
        ("exceções", "exceção"), ("reuniões", "reunião"),
        ("operações", "operação"),
        ("intenções", "intenção"), ("atenções", "atenção"),
        ("conclusões", "conclusão"),
        ("decisões", "decisão"), ("profissões", "profissão"),
        ("expressões", "expressão"),
        ("pressões", "pressão"), ("sessões", "sessão"),
        ("missões", "missão"),
        ("paixões", "paixão"), ("tradições", "tradição"),
        ("eleições", "eleição"),
        ("seleções", "seleção"), ("coleções", "coleção"),
        ("direções", "direção"),
        ("correções", "correção"), ("reflexões", "reflexão"),
        ("inclusões", "inclusão"),
        ("exclusões", "exclusão"), ("produções", "produção"),
        ("reduções", "redução"),
        ("induções", "indução"), ("deduções", "dedução"),
        ("introduções", "introdução"),
        ("construções", "construção"), ("destruições", "destruição"),
        ("explicações", "explicação"), ("aplicações", "aplicação"),
        ("indicações", "indicação"), ("observações", "observação"),
        ("informações", "informação"),
        ("transformações", "transformação"), ("formações", "formação"),
        ("organizações", "organização"), ("civilizações", "civilização"),
        ("realizações", "realização"), ("imaginações", "imaginação"),
        ("preocupações", "preocupação"), ("combinações", "combinação"),
        ("preparações", "preparação"), ("comparações", "comparação"),
        ("inscrições", "inscrição"), ("descrições", "descrição"),
        ("prescrições", "prescrição"),
        ("transmissões", "transmissão"), ("permissões", "permissão"),
        ("submissões", "submissão"),
        ("emissões", "emissão"), ("omissões", "omissão"),
        ("intromissões", "intromissão"),
        ("compressões", "compressão"), ("impressões", "impressão"),
        ("progressões", "progressão"), ("regressões", "regressão"),
        ("agressões", "agressão"), ("concessões", "concessão"),
        ("sucessões", "sucessão"), ("intercessões", "intercessão"),
        ("procissões", "procissão"),
        ("invenções", "invenção"), ("conexões", "conexão"),
        ("ligações", "ligação"), ("prevenções", "prevenção"),
        ("convicções", "convicção"), ("sanções", "sanção"),
        ("frações", "fração"), ("porções", "porção"),
        ("sensações", "sensação"), ("tentações", "tentação"),
        ("citações", "citação"), ("afirmações", "afirmação"),
        ("negações", "negação"), ("confirmações", "confirmação"),
        ("rejeições", "rejeição"), ("injeções", "injeção"),
        ("ejeções", "ejeção"), ("objeções", "objeção"),
        ("projeções", "projeção"), ("seções", "seção"),
        ("trações", "tração"), ("contrações", "contração"),
        ("extrações", "extração"), ("atrações", "atração"),
        ("distrações", "distração"), ("reações", "reação"),
        ("interações", "interação"), ("transações", "transação"),
        ("intuições", "intuição"), ("ambições", "ambição"),
        ("exibições", "exibição"), ("proibições", "proibição"),
        ("contribuições", "contribuição"),
        ("distribuições", "distribuição"),
        ("atribuições", "atribuição"),
        ("retribuições", "retribuição"),
        ("substituições", "substituição"),
        ("instituições", "instituição"),
        ("constituições", "constituição"),
        ("restituições", "restituição"),
        ("execuções", "execução"), ("perseguições", "perseguição"),
        ("obstruções", "obstrução"),
        ("alucinações", "alucinação"), ("animações", "animação"),
        ("anexações", "anexação"), ("supressões", "supressão"),
        # -ães → -ão
        ("cães", "cão"), ("alemães", "alemão"), ("capitães", "capitão"),
        ("charlatães", "charlatão"), ("sacristães", "sacristão"),
        ("escrivães", "escrivão"), ("pães", "pão"),
        ("catalães", "catalão"), ("guardiães", "guardião"),
        ("sotães", "sotão"), ("caimães", "caimão"),
        ("tecelães", "tecelão"),
        # -ãos → -ão
        ("irmãos", "irmão"), ("mãos", "mão"), ("chãos", "chão"),
        ("cristãos", "cristão"), ("cidadãos", "cidadão"),
        ("órgãos", "órgão"), ("grãos", "grão"), ("sãos", "são"),
        # -éis → -el
        ("papéis", "papel"), ("níveis", "nível"),
        ("méis", "mel"), ("fiéis", "fiel"),
        ("anéis", "anel"), ("pincéis", "pincel"),
        ("painéis", "painel"), ("pastéis", "pastel"),
        ("coronéis", "coronel"),
        # -óis → -ol
        ("sóis", "sol"), ("faróis", "farol"), ("anzóis", "anzol"),
        ("caracóis", "caracol"), ("lençóis", "lençol"),
        ("girassóis", "girassol"),
        # -is → -il
        ("barris", "barril"), ("funis", "funil"), ("fuzis", "fuzil"),
        # -eis → -il
        ("projéteis", "projétil"),
        ("fósseis", "fóssil"), ("mísseis", "míssil"),
        ("fáceis", "fácil"), ("répteis", "réptil"),
        # Special
        ("bens", "bem"), ("sons", "som"), ("flores", "flor"),
        ("cores", "cor"), ("mares", "mar"), ("pazes", "paz"),
        ("luzes", "luz"), ("cruzes", "cruz"), ("rapazes", "rapaz"),
        ("arrozes", "arroz"),
        # Loanwords
        ("clubs", "club"), ("chips", "chip"), ("bits", "bit"),
        ("emails", "email"), ("links", "link"), ("banners", "banner"),
        ("servers", "server"), ("routers", "router"), ("tokens", "token"),
        ("dockers", "docker"), ("containers", "container"),
        # Tech/business loanwords
        ("frameworks", "framework"), ("endpoints", "endpoint"),
        ("callbacks", "callback"), ("middlewares", "middleware"),
        ("hashes", "hash"), ("urls", "url"), ("widgets", "widget"),
        ("buckets", "bucket"), ("pipelines", "pipeline"),
        ("builds", "build"), ("tickets", "ticket"), ("sockets", "socket"),
        ("fixtures", "fixture"), ("mocks", "mock"), ("diffs", "diff"),
        ("commits", "commit"), ("drivers", "driver"), ("buffers", "buffer"),
        ("proxies", "proxy"), ("headers", "header"), ("footers", "footer"),
        ("scripts", "script"), ("backlogs", "backlog"), ("kanbans", "kanban"),
        ("scrums", "scrum"), ("reviews", "review"),
        ("merges", "merge"), ("branches", "branch"), ("forks", "fork"),
        ("pushes", "push"), ("pulls", "pull"), ("tags", "tag"),
        ("logs", "log"), ("bugs", "bug"), ("hacks", "hack"),
        ("patches", "patch"), ("releases", "release"), ("deploys", "deploy"),
        ("rollbacks", "rollback"), ("backups", "backup"),
        ("snapshots", "snapshot"), ("dashboards", "dashboard"),
        ("plugins", "plugin"), ("addons", "addon"), ("snippets", "snippet"),
        ("templates", "template"), ("themes", "theme"), ("skins", "skin"),
        ("layouts", "layout"), ("forms", "form"), ("inputs", "input"),
        ("outputs", "output"), ("flags", "flag"), ("switches", "switch"),
        ("toggles", "toggle"), ("hooks", "hook"), ("triggers", "trigger"),
        ("handlers", "handler"), ("listeners", "listener"),
        ("observers", "observer"), ("wrappers", "wrapper"),
        ("adapters", "adapter"), ("parsers", "parser"), ("lexers", "lexer"),
        ("compilers", "compiler"), ("debuggers", "debugger"),
        ("profilers", "profiler"), ("linters", "linter"),
        ("runners", "runner"), ("workers", "worker"),
        ("masters", "master"), ("slaves", "slave"),
        ("leaders", "leader"), ("followers", "follower"),
        ("nodes", "node"), ("hosts", "host"), ("peers", "peer"),
        ("clients", "client"), ("brokers", "broker"),
        ("shards", "shard"), ("replicas", "replica"),
        ("pods", "pod"), ("volumes", "volume"),
        ("images", "image"), ("registries", "registry"),
        ("charts", "chart"), ("graphs", "graph"),
        ("tests", "test"), ("suites", "suite"), ("cases", "case"),
        ("stubs", "stub"), ("spies", "spy"),
        ("coverages", "coverage"), ("reports", "report"),
        ("alerts", "alert"), ("events", "event"), ("messages", "message"),
        ("webhooks", "webhook"), ("payloads", "payload"),
        ("requests", "request"), ("responses", "response"),
        ("sessions", "session"), ("cookies", "cookie"),
        ("queries", "query"), ("cursors", "cursor"),
        ("fields", "field"), ("schemas", "schema"),
        ("migrations", "migration"), ("seeds", "seed"),
        ("jobs", "job"), ("tasks", "task"),
        ("queues", "queue"), ("stacks", "stack"), ("heaps", "heap"),
        ("pools", "pool"), ("caches", "cache"),
        ("streams", "stream"), ("pipes", "pipe"),
        ("ports", "port"), ("channels", "channel"),
        ("signals", "signal"), ("beacons", "beacon"),
        ("sensors", "sensor"), ("devices", "device"),
        ("badges", "badge"), ("cards", "card"),
        ("menus", "menu"), ("tabs", "tab"), ("icons", "icon"),
        ("buttons", "button"), ("labels", "label"),
        ("filters", "filter"), ("sorts", "sort"),
        ("blocks", "block"), ("sections", "section"),
        ("items", "item"), ("elements", "element"),
        ("posts", "post"), ("comments", "comment"),
        ("users", "user"), ("accounts", "account"),
        ("profiles", "profile"), ("roles", "role"),
        ("groups", "group"), ("teams", "team"),
        ("projects", "project"), ("issues", "issue"),
        ("plans", "plan"), ("tiers", "tier"),
        ("quotas", "quota"), ("limits", "limit"),
        ("invoices", "invoice"), ("payments", "payment"),
        ("charges", "charge"), ("refunds", "refund"),
        ("licenses", "license"), ("subscriptions", "subscription"),
        ("monitors", "monitor"), ("scanners", "scanner"),
        ("managers", "manager"), ("browsers", "browser"),
        ("printers", "printer"), ("computers", "computer"),
        ("senders", "sender"), ("receivers", "receiver"),
        ("editors", "editor"), ("visitors", "visitor"),
        ("sponsors", "sponsor"), ("partners", "partner"),
        ("providers", "provider"), ("suppliers", "supplier"),
        ("investors", "investor"), ("founders", "founder"),
        ("developers", "developer"),
        # -s → -ses (accented singulars)
        ("gases", "gás"), ("países", "país"), ("deuses", "deus"),
        ("fregueses", "freguês"), ("ingleses", "inglês"),
        ("franceses", "francês"), ("holandeses", "holandês"),
        ("dinamarqueses", "dinamarquês"), ("chineses", "chinês"),
        ("noruegueses", "norueguês"), ("poloneses", "polonês"),
        # Extra singles (accent restoration)
        ("portugueses", "português"), ("japoneses", "japonês"),
        ("meses", "mês"),
        ("leis", "lei"), ("reis", "rei"), ("pais", "pai"),
        ("árvores", "árvore"),
    ])
    def test_irregular_single(self, plural: str, singular: str) -> None:
        assert singularize(plural, lang="pt") == singular
