"""Portuguese edge cases for pluralization and singularization."""
from __future__ import annotations

import unicodedata

import pytest

from pluralio import is_plural, is_singular, pluralize, singularize


class TestPtCasePreservation:
    """Portuguese case preservation for irregulars and regex words."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("Coração", "Corações"),
        ("CORAÇÃO", "CORAÇÕES"),
        ("Papel", "Papéis"),
        ("PAPEL", "PAPÉIS"),
        ("Cão", "Cães"),
        ("CÃO", "CÃES"),
        ("Cidadão", "Cidadãos"),
        ("CIDADÃO", "CIDADÃOS"),
        ("Framework", "Frameworks"),
        ("FRAMEWORK", "FRAMEWORKS"),
        ("Bem", "Bens"),
        ("BEM", "BENS"),
    ])
    def test_pt_title_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="pt") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("Corações", "Coração"),
        ("CORAÇÕES", "CORAÇÃO"),
        ("Papéis", "Papel"),
        ("PAPÉIS", "PAPEL"),
        ("Cães", "Cão"),
        ("CÃES", "CÃO"),
        ("Cidadãos", "Cidadão"),
        ("CIDADÃOS", "CIDADÃO"),
    ])
    def test_pt_title_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="pt") == expected



class TestPtMixedCase:
    """Portuguese mixed case preservation."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhone", "iPhones"),
    ])
    def test_pt_mixed_case_pluralize(self, word: str, expected: str) -> None:
        assert pluralize(word, lang="pt") == expected

    @pytest.mark.parametrize(("word", "expected"), [
        ("iPhones", "iPhone"),
    ])
    def test_pt_mixed_case_singularize(self, word: str, expected: str) -> None:
        assert singularize(word, lang="pt") == expected



class TestPtHyphenatedWords:
    """Portuguese hyphenated word pluralization."""

    @pytest.mark.parametrize(("singular", "plural"), [
        ("café-bar", "cafés-bar"),
        ("coração-de-leão", "corações-de-leão"),
        ("papel-moeda", "papéis-moeda"),
    ])
    def test_pt_hyphenated_pluralize(self, singular: str, plural: str) -> None:
        assert pluralize(singular, lang="pt") == plural

    @pytest.mark.parametrize(("singular", "plural"), [
        ("café-bar", "cafés-bar"),
        ("coração-de-leão", "corações-de-leão"),
        ("papel-moeda", "papéis-moeda"),
    ])
    def test_pt_hyphenated_singularize(self, singular: str, plural: str) -> None:
        assert singularize(plural, lang="pt") == singular

    def test_pt_hyphenated_roundtrip(self) -> None:
        for word in ["café-bar", "coração-de-leão", "papel-moeda"]:
            assert singularize(pluralize(word, lang="pt"), lang="pt") == word

    def test_pt_verb_noun_compound_pluralize(self) -> None:
        for singular, plural in [
            ("quebra-cabeça", "quebra-cabeças"),
            ("guarda-chuva", "guarda-chuvas"),
            ("guarda-roupa", "guarda-roupas"),
            ("beija-flor", "beija-flores"),
            ("passa-tempo", "passa-tempos"),
            ("arranha-céu", "arranha-céus"),
            ("limpa-pára-brisa", "limpa-pára-brisas"),
            ("corta-caminho", "corta-caminhos"),
        ]:
            assert pluralize(singular, lang="pt") == plural

    def test_pt_verb_noun_compound_singularize(self) -> None:
        for singular, plural in [
            ("quebra-cabeça", "quebra-cabeças"),
            ("guarda-chuva", "guarda-chuvas"),
            ("guarda-roupa", "guarda-roupas"),
            ("beija-flor", "beija-flores"),
            ("passa-tempo", "passa-tempos"),
            ("arranha-céu", "arranha-céus"),
        ]:
            assert singularize(plural, lang="pt") == singular

    def test_pt_verb_noun_compound_roundtrip(self) -> None:
        for word in ["quebra-cabeça", "guarda-chuva", "guarda-roupa",
                      "beija-flor", "passa-tempo", "arranha-céu"]:
            assert singularize(pluralize(word, lang="pt"), lang="pt") == word

    def test_pt_leading_hyphen_pluralize(self) -> None:
        assert pluralize("-casa", lang="pt") == "-casas"

    def test_pt_leading_hyphen_singularize(self) -> None:
        assert singularize("-casas", lang="pt") == "-casa"

    def test_pt_hyphen_only(self) -> None:
        assert pluralize("-", lang="pt") == "-"
        assert singularize("-", lang="pt") == "-"

    def test_pt_double_hyphen(self) -> None:
        assert pluralize("--", lang="pt") == "--"
        assert singularize("--", lang="pt") == "--"



class TestPtIdempotency:
    """Portuguese pluralize of already-plural words should return unchanged."""

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "feijões", "limões", "leões",
        "botões", "estações", "nações", "relações", "funções",
        "criações", "emoções", "regiões", "questões", "lições",
        "intenções", "atenções", "conclusões", "decisões",
        "cães", "alemães", "capitães", "charlatães", "pães",
        "irmãos", "mãos", "chãos", "cristãos", "cidadãos", "órgãos",
        "papéis", "níveis", "anéis", "pincéis", "painéis", "pastéis",
        "sóis", "faróis", "anzóis", "caracóis", "lençóis",
        "gases", "países", "deuses", "portugueses", "japoneses",
        "ingleses", "franceses", "chineses",
        "meses", "leis", "reis", "pais",
        "frameworks", "endpoints", "callbacks", "middlewares",
        "hashes", "urls", "widgets", "buckets", "pipelines",
        "builds", "tickets", "sockets", "fixtures", "mocks", "diffs",
        "commits", "drivers", "buffers", "proxies", "headers",
        "branches", "forks", "pushes", "pulls", "tags",
        "logs", "bugs", "patches", "releases", "deploys",
        "backups", "snapshots", "dashboards", "plugins", "addons",
        "templates", "themes", "layouts", "forms", "inputs", "outputs",
        "flags", "switches", "toggles", "hooks", "triggers",
        "handlers", "listeners", "observers", "wrappers", "adapters",
        "parsers", "compilers", "debuggers", "runners", "workers",
        "nodes", "hosts", "peers", "clients", "brokers",
        "pods", "volumes", "images", "registries", "charts", "graphs",
        "tests", "suites", "cases", "stubs", "spies",
        "alerts", "events", "messages", "webhooks", "payloads",
        "requests", "responses", "sessions", "cookies",
        "queries", "cursors", "fields", "schemas", "migrations",
        "jobs", "tasks", "queues", "stacks", "heaps", "pools", "caches",
        "streams", "pipes", "ports", "channels", "signals", "beacons",
        "sensors", "devices", "badges", "cards", "menus", "tabs", "icons",
        "buttons", "labels", "filters", "sorts", "blocks", "sections",
        "items", "elements", "posts", "comments",
        "users", "accounts", "profiles", "roles", "groups", "teams",
        "projects", "issues", "plans", "tiers", "quotas", "limits",
        "invoices", "payments", "charges", "refunds",
        "licenses", "subscriptions", "monitors", "scanners",
        "managers", "browsers", "printers", "computers",
        "senders", "receivers", "editors", "visitors",
        "sponsors", "partners", "providers", "suppliers",
        "investors", "founders", "developers",
    ])
    def test_pt_pluralize_already_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word



class TestPtRoundTrip:
    """Portuguese pluralize → singularize round-trip identity."""

    @pytest.mark.parametrize("word", [
        "casa", "livro", "gato", "coração", "canção", "balão",
        "feijão", "limão", "leão", "botão", "estação", "nação",
        "cão", "alemão", "capitão", "charlatão", "pão",
        "irmão", "mão", "chão", "cidadão", "órgão",
        "papel", "nível", "mel", "fiel", "anel", "pincel",
        "sol", "farol", "anzol", "caracol", "lençol",
        "barril", "funil", "fuzil",
        "projétil", "fóssil", "míssil", "fácil", "réptil",
        "gás", "país", "deus", "português", "japonês",
        "inglês", "francês", "holandês", "chinês",
        "mês", "lei", "rei", "pai",
        "bem", "som", "flor", "cor", "mar", "paz", "luz",
        "framework", "endpoint", "callback", "middleware",
        "hash", "url", "widget", "bucket", "pipeline",
        "build", "ticket", "socket", "fixture", "mock", "diff",
        "commit", "driver", "buffer", "proxy", "header",
        "branch", "fork", "push", "pull", "tag",
        "log", "bug", "patch", "release", "deploy",
        "backup", "snapshot", "dashboard", "plugin", "addon",
        "template", "theme", "layout", "form", "input", "output",
        "flag", "switch", "toggle", "hook", "trigger",
        "handler", "listener", "observer", "wrapper", "adapter",
        "parser", "compiler", "debugger", "runner", "worker",
        "node", "host", "peer", "client", "broker",
        "pod", "volume", "image", "registry", "chart", "graph",
        "test", "suite", "case", "stub", "spy",
        "alert", "event", "message", "webhook", "payload",
        "request", "response", "session", "cookie",
        "query", "cursor", "field", "schema", "migration",
        "job", "task", "queue", "stack", "heap", "pool", "cache",
        "stream", "pipe", "port", "channel", "signal", "beacon",
        "sensor", "device", "badge", "card", "menu", "tab", "icon",
        "button", "label", "filter", "sort", "block", "section",
        "item", "element", "post", "comment",
        "user", "account", "profile", "role", "group", "team",
        "project", "issue", "plan", "tier", "quota", "limit",
        "invoice", "payment", "charge", "refund",
        "license", "subscription", "monitor", "scanner",
        "manager", "browser", "printer", "computer",
        "sender", "receiver", "editor", "visitor",
        "sponsor", "partner", "provider", "supplier",
        "investor", "founder", "developer",
    ])
    def test_pt_roundtrip(self, word: str) -> None:
        plural = pluralize(word, lang="pt")
        assert singularize(plural, lang="pt") == word



class TestPtUnicodeNormalization:
    """Portuguese NFD input should produce same result as NFC."""

    @pytest.mark.parametrize("word", [
        "coração", "canção", "balão", "leão", "estação",
        "cão", "alemão", "capitão", "pão",
        "papel", "nível", "mel", "fiel",
        "sol", "farol", "anzol", "lençol",
        "gás", "país", "português", "japonês",
        "mês", "árvore",
    ])
    def test_pt_nfd_pluralize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = pluralize(word, lang="pt")
        nfd_result = pluralize(nfd, lang="pt")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "leões", "estações",
        "cães", "alemães", "capitães", "pães",
        "papéis", "níveis", "fiéis",
        "sóis", "faróis", "anzóis", "lençóis",
        "gases", "países", "portugueses", "japoneses",
        "meses", "árvores",
    ])
    def test_pt_nfd_singularize_matches_nfc(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        nfc_result = singularize(word, lang="pt")
        nfd_result = singularize(nfd, lang="pt")
        assert unicodedata.normalize("NFC", nfd_result) == nfc_result

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "gás", "português",
    ])
    def test_pt_nfd_is_singular(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_singular(nfd, lang="pt") == is_singular(word, lang="pt")

    @pytest.mark.parametrize("word", [
        "corações", "papéis", "cães", "gases", "portugueses",
    ])
    def test_pt_nfd_is_plural(self, word: str) -> None:
        nfd = unicodedata.normalize("NFD", word)
        assert is_plural(nfd, lang="pt") == is_plural(word, lang="pt")



class TestPtIsSingularIsPlural:
    """Portuguese is_singular / is_plural checks."""

    @pytest.mark.parametrize("word", [
        "coração", "canção", "balão", "leão", "estação",
        "cão", "alemão", "capitão", "pão",
        "papel", "nível", "mel", "fiel",
        "sol", "farol", "anzol", "lençol",
        "gás", "país", "português", "japonês",
        "mês", "lei", "rei", "pai",
        "bem", "som", "flor", "cor", "mar", "paz", "luz",
        "framework", "endpoint", "callback", "middleware",
        "casa", "livro", "gato", "nome", "filme",
    ])
    def test_pt_singular_words(self, word: str) -> None:
        assert is_singular(word, lang="pt") is True
        assert is_plural(word, lang="pt") is False

    @pytest.mark.parametrize("word", [
        "corações", "canções", "balões", "leões", "estações",
        "cães", "alemães", "capitães", "pães",
        "papéis", "níveis", "fiéis",
        "sóis", "faróis", "anzóis", "lençóis",
        "gases", "países", "portugueses", "japoneses",
        "meses", "leis", "reis", "pais",
        "bens", "sons", "flores", "cores", "mares", "pazes", "luzes",
        "frameworks", "endpoints", "callbacks", "middlewares",
        "casas", "livros", "gatos", "nomes", "filmes",
    ])
    def test_pt_plural_words(self, word: str) -> None:
        assert is_plural(word, lang="pt") is True
        assert is_singular(word, lang="pt") is False

    @pytest.mark.parametrize("word", [
        "tórax", "látex", "lápis", "vírus", "óculos",
        "nós", "vós", "blues", "funk",
    ])
    def test_pt_uncountable_both(self, word: str) -> None:
        assert is_singular(word, lang="pt") is True
        assert is_plural(word, lang="pt") is True



class TestPtCountAware:
    """Portuguese count-aware pluralization."""

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_one_returns_singular(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=1) == word

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_zero_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=0) == pluralize(word, lang="pt")

    @pytest.mark.parametrize("word", [
        "coração", "papel", "cão", "irmão", "gás",
        "framework", "casa", "livro",
    ])
    def test_pt_count_two_returns_plural(self, word: str) -> None:
        assert pluralize(word, lang="pt", count=2) == pluralize(word, lang="pt")



class TestPtWhitespace:
    """Portuguese whitespace preservation."""

    def test_pt_preserves_whitespace_pluralize(self) -> None:
        assert pluralize("  coração  ", lang="pt") == "  corações  "

    def test_pt_preserves_whitespace_singularize(self) -> None:
        assert singularize("  corações  ", lang="pt") == "  coração  "

    def test_pt_whitespace_only_returns_as_is(self) -> None:
        assert pluralize("   ", lang="pt") == "   "
        assert singularize("   ", lang="pt") == "   "

    def test_pt_count_one_preserves_whitespace(self) -> None:
        assert pluralize("  coração  ", lang="pt", count=1) == "  coração  "



class TestPtSingleLetterAndEdge:
    """Portuguese single letters and boundary cases."""

    def test_pt_single_letter_a(self) -> None:
        assert pluralize("a", lang="pt") == "as"
        assert singularize("as", lang="pt") == "a"

    def test_pt_single_letter_a_uppercase(self) -> None:
        assert pluralize("A", lang="pt") == "AS"
        assert singularize("AS", lang="pt") == "A"

    def test_pt_empty_string(self) -> None:
        assert pluralize("", lang="pt") == ""
        assert singularize("", lang="pt") == ""

    def test_pt_whitespace_only(self) -> None:
        assert pluralize("   ", lang="pt") == "   "
        assert singularize("   ", lang="pt") == "   "



class TestPtUncountableConsistency:
    """Portuguese uncountable words should be unchanged in both directions."""

    @pytest.mark.parametrize("word", [
        "tórax", "látex", "clímax", "sintaxe", "fax",
        "bíceps", "tríceps", "fórceps",
        "oásis", "gênesis",
        "lápis", "atlas", "vírus", "ônibus", "óculos",
        "férias", "núpcias", "cócegas", "afazeres",
        "três", "mais", "cais", "dois",
        "pires", "ourives", "cosmos", "seis",
        "menos", "jamais",
        "nós", "vós",
        "blues", "soul", "funk", "reggae", "folk", "metal",
        "software", "hardware", "web", "blog", "chat",
        "spam", "jazz", "rock", "punk", "flash",
        "marketing", "design", "streaming", "podcast",
        "feed", "shell", "kernel", "cloud",
        "backend", "frontend", "runtime", "workflow",
        "sandbox", "thread", "hub", "ping", "byte",
        "rugby", "skate", "poker", "darts",
        "hacker", "nerd", "geek",
        "download", "upload", "screenshot", "fallback",
    ])
    def test_pt_uncountable_unchanged(self, word: str) -> None:
        assert pluralize(word, lang="pt") == word
        assert singularize(word, lang="pt") == word


# ---------------------------------------------------------------------------
# Spanish edge cases
# ---------------------------------------------------------------------------



