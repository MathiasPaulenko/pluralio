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
        ("criação", "criações"), ("emoção", "emoções"), ("região", "regiões"),
        ("temporão", "temporões"), ("verão", "verões"),
        ("questão", "questões"), ("lição", "lições"),
        ("exceção", "exceções"), ("reunião", "reuniões"), ("operação", "operações"),
        ("intenção", "intenções"), ("atenção", "atenções"), ("conclusão", "conclusões"),
        ("decisão", "decisões"), ("profissão", "profissões"), ("expressão", "expressões"),
        ("pressão", "pressões"), ("sessão", "sessões"), ("missão", "missões"),
        ("paixão", "paixões"), ("tradição", "tradições"), ("eleição", "eleições"),
        ("seleção", "seleções"), ("coleção", "coleções"), ("direção", "direções"),
        ("correção", "correções"), ("reflexão", "reflexões"), ("inclusão", "inclusões"),
        ("exclusão", "exclusões"), ("produção", "produções"), ("redução", "reduções"),
        ("indução", "induções"), ("dedução", "deduções"), ("introdução", "introduções"),
        ("construção", "construções"), ("destruição", "destruições"),
        ("explicação", "explicações"), ("aplicação", "aplicações"),
        ("indicação", "indicações"), ("observação", "observações"),
        ("informação", "informações"), ("transformação", "transformações"),
        ("formação", "formações"), ("organização", "organizações"),
        ("civilização", "civilizações"), ("realização", "realizações"),
        ("imaginação", "imaginações"), ("preocupação", "preocupações"),
        ("combinação", "combinações"), ("preparação", "preparações"),
        ("comparação", "comparações"), ("inscrição", "inscrições"),
        ("descrição", "descrições"), ("prescrição", "prescrições"),
        ("transmissão", "transmissões"), ("permissão", "permissões"),
        ("submissão", "submissões"), ("emissão", "emissões"),
        ("omissão", "omissões"), ("intromissão", "intromissões"),
        ("compressão", "compressões"), ("impressão", "impressões"),
        ("progressão", "progressões"), ("regressão", "regressões"),
        ("agressão", "agressões"), ("concessão", "concessões"),
        ("sucessão", "sucessões"), ("intercessão", "intercessões"),
        ("procissão", "procissões"),
        ("invenção", "invenções"), ("conexão", "conexões"),
        ("ligação", "ligações"), ("prevenção", "prevenções"),
        ("convicção", "convicções"), ("sanção", "sanções"),
        ("fração", "frações"), ("porção", "porções"),
        ("sensação", "sensações"), ("tentação", "tentações"),
        ("citação", "citações"), ("afirmação", "afirmações"),
        ("negação", "negações"), ("confirmação", "confirmações"),
        ("rejeição", "rejeições"), ("injeção", "injeções"),
        ("ejeção", "ejeções"), ("objeção", "objeções"),
        ("projeção", "projeções"), ("seção", "seções"),
        ("tração", "trações"), ("contração", "contrações"),
        ("extração", "extrações"), ("atração", "atrações"),
        ("distração", "distrações"), ("reação", "reações"),
        ("interação", "interações"), ("transação", "transações"),
        ("intuição", "intuições"), ("ambição", "ambições"),
        ("exibição", "exibições"), ("proibição", "proibições"),
        ("contribuição", "contribuições"), ("distribuição", "distribuições"),
        ("atribuição", "atribuições"), ("retribuição", "retribuições"),
        ("substituição", "substituições"), ("instituição", "instituições"),
        ("constituição", "constituições"), ("restituição", "restituições"),
        ("execução", "execuções"), ("perseguição", "perseguições"),
        ("obstrução", "obstruções"), ("alucinação", "alucinações"),
        ("animação", "animações"), ("anexação", "anexações"),
        ("supressão", "supressões"),
        # -ão → -ães
        ("cão", "cães"), ("alemão", "alemães"), ("capitão", "capitães"),
        ("charlatão", "charlatães"), ("sacristão", "sacristães"),
        ("escrivão", "escrivães"), ("pão", "pães"),
        ("catalão", "catalães"), ("guardião", "guardiães"), ("sotão", "sotães"),
        ("caimão", "caimães"), ("tecelão", "tecelães"),
        # -ão → -ãos
        ("irmão", "irmãos"), ("mão", "mãos"), ("chão", "chãos"),
        ("cristão", "cristãos"), ("cidadão", "cidadãos"), ("órgão", "órgãos"),
        ("grão", "grãos"), ("são", "sãos"),
        # Accent ADDS in plural (-el → -éis)
        ("papel", "papéis"), ("nível", "níveis"), ("fóssil", "fósseis"),
        ("fácil", "fáceis"), ("réptil", "répteis"), ("míssil", "mísseis"),
        ("anel", "anéis"), ("pincel", "pincéis"), ("painel", "painéis"),
        ("pastel", "pastéis"), ("mel", "méis"), ("fiel", "fiéis"),
        ("coronel", "coronéis"),
        # Accent ADDS in plural (-ol → -óis)
        ("sol", "sóis"), ("farol", "faróis"), ("anzol", "anzóis"),
        ("caracol", "caracóis"), ("lençol", "lençóis"),
        ("girassol", "girassóis"),
        # -il (paroxítona) → -eis
        ("projétil", "projéteis"),
        # -il (oxítona) → -is
        ("barril", "barris"), ("funil", "funis"), ("fuzil", "fuzis"),
        # -s → -ses (accented singulars)
        ("gás", "gases"), ("país", "países"), ("deus", "deuses"),
        ("freguês", "fregueses"), ("português", "portugueses"),
        ("japonês", "japoneses"), ("inglês", "ingleses"),
        ("francês", "franceses"), ("holandês", "holandeses"),
        ("dinamarquês", "dinamarqueses"), ("chinês", "chineses"),
        ("norueguês", "noruegueses"), ("polonês", "poloneses"),
        # Monosyllables / special
        ("bem", "bens"), ("som", "sons"), ("flor", "flores"),
        ("cor", "cores"), ("mar", "mares"), ("paz", "pazes"),
        ("luz", "luzes"), ("cruz", "cruzes"), ("rapaz", "rapazes"),
        ("arroz", "arrozes"),
        # Foreign loanwords (+s, not +es)
        ("club", "clubs"), ("chip", "chips"), ("bit", "bits"),
        ("email", "emails"), ("link", "links"), ("banner", "banners"),
        ("server", "servers"), ("router", "routers"), ("token", "tokens"),
        ("docker", "dockers"), ("container", "containers"),
        # Tech/business loanwords
        ("framework", "frameworks"), ("endpoint", "endpoints"),
        ("callback", "callbacks"), ("middleware", "middlewares"),
        ("hash", "hashes"), ("url", "urls"), ("widget", "widgets"),
        ("bucket", "buckets"), ("pipeline", "pipelines"),
        ("build", "builds"), ("ticket", "tickets"), ("socket", "sockets"),
        ("fixture", "fixtures"), ("mock", "mocks"), ("diff", "diffs"),
        ("commit", "commits"), ("driver", "drivers"), ("buffer", "buffers"),
        ("proxy", "proxies"), ("header", "headers"), ("footer", "footers"),
        ("script", "scripts"), ("backlog", "backlogs"), ("kanban", "kanbans"),
        ("scrum", "scrums"), ("review", "reviews"),
        ("merge", "merges"), ("branch", "branches"), ("fork", "forks"),
        ("push", "pushes"), ("pull", "pulls"), ("tag", "tags"),
        ("log", "logs"), ("bug", "bugs"), ("hack", "hacks"),
        ("patch", "patches"), ("release", "releases"), ("deploy", "deploys"),
        ("rollback", "rollbacks"), ("backup", "backups"),
        ("snapshot", "snapshots"), ("dashboard", "dashboards"),
        ("plugin", "plugins"), ("addon", "addons"), ("snippet", "snippets"),
        ("template", "templates"), ("theme", "themes"), ("skin", "skins"),
        ("layout", "layouts"), ("form", "forms"), ("input", "inputs"),
        ("output", "outputs"), ("flag", "flags"), ("switch", "switches"),
        ("toggle", "toggles"), ("hook", "hooks"), ("trigger", "triggers"),
        ("handler", "handlers"), ("listener", "listeners"),
        ("observer", "observers"), ("wrapper", "wrappers"),
        ("adapter", "adapters"), ("parser", "parsers"), ("lexer", "lexers"),
        ("compiler", "compilers"), ("debugger", "debuggers"),
        ("profiler", "profilers"), ("linter", "linters"),
        ("runner", "runners"), ("worker", "workers"),
        ("master", "masters"), ("slave", "slaves"),
        ("leader", "leaders"), ("follower", "followers"),
        ("node", "nodes"), ("host", "hosts"), ("peer", "peers"),
        ("client", "clients"), ("broker", "brokers"),
        ("shard", "shards"), ("replica", "replicas"),
        ("pod", "pods"), ("volume", "volumes"),
        ("image", "images"), ("registry", "registries"),
        ("chart", "charts"), ("graph", "graphs"),
        ("test", "tests"), ("suite", "suites"), ("case", "cases"),
        ("stub", "stubs"), ("spy", "spies"),
        ("coverage", "coverages"), ("report", "reports"),
        ("alert", "alerts"), ("event", "events"), ("message", "messages"),
        ("webhook", "webhooks"), ("payload", "payloads"),
        ("request", "requests"), ("response", "responses"),
        ("session", "sessions"), ("cookie", "cookies"),
        ("query", "queries"), ("cursor", "cursors"),
        ("field", "fields"), ("schema", "schemas"),
        ("migration", "migrations"), ("seed", "seeds"),
        ("job", "jobs"), ("task", "tasks"),
        ("queue", "queues"), ("stack", "stacks"), ("heap", "heaps"),
        ("pool", "pools"), ("cache", "caches"),
        ("stream", "streams"), ("pipe", "pipes"),
        ("port", "ports"), ("channel", "channels"),
        ("signal", "signals"), ("beacon", "beacons"),
        ("sensor", "sensors"), ("device", "devices"),
        ("badge", "badges"), ("card", "cards"),
        ("menu", "menus"), ("tab", "tabs"), ("icon", "icons"),
        ("button", "buttons"), ("label", "labels"),
        ("filter", "filters"), ("sort", "sorts"),
        ("block", "blocks"), ("section", "sections"),
        ("item", "items"), ("element", "elements"),
        ("post", "posts"), ("comment", "comments"),
        ("user", "users"), ("account", "accounts"),
        ("profile", "profiles"), ("role", "roles"),
        ("group", "groups"), ("team", "teams"),
        ("project", "projects"), ("issue", "issues"),
        ("plan", "plans"), ("tier", "tiers"),
        ("quota", "quotas"), ("limit", "limits"),
        ("invoice", "invoices"), ("payment", "payments"),
        ("charge", "charges"), ("refund", "refunds"),
        ("license", "licenses"), ("subscription", "subscriptions"),
        ("monitor", "monitors"), ("scanner", "scanners"),
        ("manager", "managers"), ("browser", "browsers"),
        ("printer", "printers"), ("computer", "computers"),
        ("sender", "senders"), ("receiver", "receivers"),
        ("editor", "editors"), ("visitor", "visitors"),
        ("sponsor", "sponsors"), ("partner", "partners"),
        ("provider", "providers"), ("supplier", "suppliers"),
        ("investor", "investors"), ("founder", "founders"),
        ("developer", "developers"),
        # Back-filled from extra singles
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
        # Music genres (invariable)
        "blues", "soul", "funk", "reggae", "folk", "metal",
        # Foreign loanwords (invariable)
        "software", "hardware", "web", "blog", "chat",
        "spam", "jazz", "rock", "punk", "flash",
        "marketing", "design", "streaming", "podcast",
        "feed", "shell",
        "kernel", "cloud", "backend", "frontend",
        "runtime", "workflow",
        "sandbox", "thread",
        "hub", "ping", "byte",
        # Sports/games (invariable)
        "rugby", "skate", "poker", "darts",
        # Culture (invariable)
        "hacker", "nerd", "geek",
        # Tech actions (invariable)
        "download", "upload", "screenshot", "fallback",
    ])
    def test_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word
