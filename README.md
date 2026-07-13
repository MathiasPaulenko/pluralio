<div align="center">

# pluralio

**Pluralization and singularization for Python**

English · Spanish · Portuguese · French · Italian · Esperanto · Zero dependencies · Type-safe · Extensible

[![PyPI version](https://img.shields.io/pypi/v/pluralio.svg?style=flat-square)](https://pypi.org/project/pluralio/)
[![Python versions](https://img.shields.io/pypi/pyversions/pluralio.svg?style=flat-square)](https://pypi.org/project/pluralio/)
[![CI](https://github.com/MathiasPaulenko/pluralio/actions/workflows/ci.yml/badge.svg?style=flat-square)](https://github.com/MathiasPaulenko/pluralio/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen?style=flat-square)](https://github.com/MathiasPaulenko/pluralio)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg?style=flat-square)](https://github.com/astral-sh/ruff)
[![Type checker: mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg?style=flat-square)](https://github.com/python/mypy)
[![Downloads](https://img.shields.io/pypi/dm/pluralio.svg?style=flat-square)](https://pypi.org/project/pluralio/)
[![Docs](https://img.shields.io/badge/docs-sphinx-blue.svg?style=flat-square)](https://mathiaspaulenko.github.io/pluralio/)

</div>

---

## Features

- **Zero dependencies** — pure Python standard library, nothing else to install
- **Type-safe** — full type hints, `py.typed` marker included (PEP 561)
- **97% test coverage** — 7,066 tests, every line is verified
- **Extensible at runtime** — add irregulars, rules, uncountables, or entire languages without touching source code
- **Case preservation** — `"Library"` → `"Libraries"`, `"BOX"` → `"BOXES"`
- **Count-aware** — `pluralize("item", count=1)` → `"item"`
- **Hyphenated words** — `"mother-in-law"` → `"mothers-in-law"`
- **Python 3.10+** — tested on 3.10, 3.11, 3.12, 3.13, and 3.14

## Table of contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [API reference](#api-reference)
- [Extending rules](#extending-rules)
  - [Add an irregular word](#add-an-irregular-word)
  - [Add only plural or singular direction](#add-only-plural-or-singular-direction)
  - [Add an uncountable / invariable word](#add-an-uncountable--invariable-word)
  - [Add a regex rule](#add-a-regex-rule)
  - [Register a new language](#register-a-new-language)
- [Comparison](#comparison)
- [Performance](#performance)
- [Supported languages](#supported-languages)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Installation

```bash
pip install pluralio
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add pluralio
```

## Quick start

```python
import pluralio

# ── English (default) ──────────────────────────────────────────
pluralio.pluralize("cat")              # "cats"
pluralio.pluralize("box")              # "boxes"
pluralio.pluralize("child")            # "children"
pluralio.pluralize("city")             # "cities"
pluralio.singularize("cities")         # "city"
pluralio.singularize("mice")           # "mouse"
pluralio.singularize("children")       # "child"

# ── Spanish ────────────────────────────────────────────────────
pluralio.pluralize("gato", lang="es")         # "gatos"
pluralio.pluralize("lápiz", lang="es")        # "lápices"
pluralio.pluralize("examen", lang="es")       # "exámenes"
pluralio.singularize("lápices", lang="es")    # "lápiz"
pluralio.singularize("alemanes", lang="es")   # "alemán"

# ── Portuguese ────────────────────────────────────────────────
pluralio.pluralize("casa", lang="pt")         # "casas"
pluralio.pluralize("coração", lang="pt")      # "corações"
pluralio.pluralize("papel", lang="pt")        # "papéis"
pluralio.pluralize("flor", lang="pt")         # "flores"
pluralio.singularize("corações", lang="pt")   # "coração"
pluralio.singularize("papéis", lang="pt")     # "papel"

# ── French ────────────────────────────────────────────────────
pluralio.pluralize("chat", lang="fr")         # "chats"
pluralio.pluralize("cheval", lang="fr")       # "chevaux"
pluralio.pluralize("bateau", lang="fr")       # "bateaux"
pluralio.pluralize("travail", lang="fr")      # "travaux"
pluralio.pluralize("bijou", lang="fr")        # "bijoux"
pluralio.singularize("chevaux", lang="fr")    # "cheval"
pluralio.singularize("travaux", lang="fr")    # "travail"

# ── Count-aware ────────────────────────────────────────────────
pluralio.pluralize("item", count=1)    # "item"  (singular)
pluralio.pluralize("item", count=0)    # "items" (plural)
pluralio.pluralize("item", count=5)    # "items" (plural)

# ── Case preservation ─────────────────────────────────────────
pluralio.pluralize("Library")          # "Libraries"
pluralio.pluralize("LIBRARY")          # "LIBRARIES"
pluralio.singularize("Libraries")      # "Library"

# ── Hyphenated words ──────────────────────────────────────────
pluralio.pluralize("mother-in-law")    # "mothers-in-law"
pluralio.singularize("mothers-in-law") # "mother-in-law"

# ── Italian ────────────────────────────────────────────────────
pluralio.pluralize("gatto", lang="it")         # "gatti"
pluralio.pluralize("amico", lang="it")         # "amici"
pluralio.pluralize("libro", lang="it")         # "libri"
pluralio.singularize("amici", lang="it")       # "amico"
pluralio.singularize("libri", lang="it")       # "libro"

# ── List supported languages ──────────────────────────────────
pluralio.supported_languages()         # ["en", "es", "fr", "it", "pt"]

# ── Inspect word form ─────────────────────────────────────────
pluralio.is_plural("cats")             # True
pluralio.is_singular("cat")           # True
pluralio.is_plural("sheep")            # True   (uncountable — valid as both)
pluralio.is_singular("sheep")          # True   (uncountable — valid as both)
```

## How it works

Every word goes through a **three-step priority chain**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Input word (stripped)                     │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
              ┌─────────────────────────┐
              │  1. Uncountable check   │  ← highest priority
              │     word in set?        │
              └────────────┬────────────┘
                           │ no
                           ▼
              ┌─────────────────────────┐
              │  2. Irregular lookup    │
              │     word in dict?       │
              └────────────┬────────────┘
                           │ no
                           ▼
              ┌─────────────────────────┐
              │  3. Regex rules         │  ← first match wins
              │     (ordered list)      │
              └────────────┬────────────┘
                           │ no match
                           ▼
              ┌─────────────────────────┐
              │  Return word unchanged  │
              └─────────────────────────┘
```

- **Uncountable** words (e.g. `"sheep"`, `"information"`) are returned as-is.
- **Irregular** words (e.g. `"man"` → `"men"`) are looked up in a dictionary.
- **Regex rules** are applied in order — the first matching pattern wins.
- The **casing** of the input is always preserved in the output.

## API reference

### Core functions

| Function | Description |
| --- | --- |
| `pluralize(word, lang="en", count=None)` | Convert a word to its plural form. |
| `singularize(word, lang="en")` | Convert a word to its singular form. |
| `is_plural(word, lang="en")` | Check if a word is in plural form. |
| `is_singular(word, lang="en")` | Check if a word is in singular form. |
| `supported_languages()` | Return a sorted list of registered language codes. |

### Extensibility functions

| Function | Description |
| --- | --- |
| `add_irregular(singular, plural, lang="en")` | Add an irregular pair (both directions). |
| `add_plural(singular, plural, lang="en")` | Add only the singular → plural direction. |
| `add_singular(plural, singular, lang="en")` | Add only the plural → singular direction. |
| `add_uncountable(word, lang="en")` | Mark a word as invariable. |
| `add_plural_rule(pattern, replacement, lang="en")` | Insert a pluralization regex rule (top priority). |
| `add_singular_rule(pattern, replacement, lang="en")` | Insert a singularization regex rule (top priority). |
| `register_language(lang, *, plural_rules=..., ...)` | Register a completely new language. |

### Low-level registry

| Function | Description |
| --- | --- |
| `LanguageRules` | Dataclass holding all rules for a language. |
| `register(rules)` | Register a `LanguageRules` instance. |
| `get_rules(lang)` | Retrieve rules for a language (raises `ValueError` if not found). |

## Extending rules

pluralio is designed to be extended at runtime — no need to modify the source code.

### Add an irregular word

Registers both pluralize and singularize directions:

```python
pluralio.add_irregular("person", "people")

pluralio.pluralize("person")      # "people"
pluralio.singularize("people")    # "person"
```

### Add only plural or singular direction

When you need just one direction (e.g. Spanish accent restoration):

```python
# Only pluralize direction
pluralio.add_plural("joven", "jóvenes", lang="es")
pluralio.pluralize("joven", lang="es")    # "jóvenes"

# Only singularize direction (accent restoration)
pluralio.add_singular("alemanes", "alemán", lang="es")
pluralio.singularize("alemanes", lang="es")  # "alemán"
```

### Add an uncountable / invariable word

```python
pluralio.add_uncountable("data")

pluralio.pluralize("data")      # "data"
pluralio.singularize("data")    # "data"
```

### Add a regex rule

Custom rules are inserted at the **top** of the rule list (highest priority — first match wins):

```python
pluralio.add_plural_rule(r"us$", "i")
pluralio.pluralize("cactus")    # "cacti"

pluralio.add_singular_rule(r"i$", "us")
pluralio.singularize("cacti")   # "cactus"
```

### Register a new language

```python
pluralio.register_language(
    "fr",
    plural_rules=[(r"$", "s")],
    singular_rules=[(r"s$", "")],
    irregular_plurals={"cheval": "chevaux"},
    uncountable={"information"},
)

pluralio.pluralize("chat", lang="fr")        # "chats"
pluralio.pluralize("cheval", lang="fr")      # "chevaux"
pluralio.singularize("chevaux", lang="fr")   # "cheval"
pluralio.pluralize("information", lang="fr") # "information"
```

## Comparison

How does pluralio compare to other Python inflection libraries?

| Feature | pluralio | [inflect] | [pluralsingular] | [pluralizer] |
| --- | --- | --- | --- | --- |
| Spanish pluralization | ✅ 100% | ❌ 39% | ⚠️ 74% | ❌ 40% |
| Spanish singularization | ✅ 100% | ❌ 29% | ⚠️ 87% | ❌ N/A |
| Portuguese pluralization | ✅ 100% | ❌ | ❌ | ❌ |
| French pluralization | ✅ 100% | ❌ | ❌ | ❌ |
| Italian pluralization | ✅ 100% | ❌ | ❌ | ❌ |
| Esperanto pluralization | ✅ 100% | ❌ | ❌ | ❌ |
| Singularize | ✅ | ✅ | ✅ | ❌ |
| Count-aware (`count=1`) | ✅ | ✅ | ❌ | ❌ |
| Case preservation | ✅ | ❌ | ❌ | ✅ |
| Hyphenated words | ✅ | ❌ | ❌ | ❌ |
| Unicode normalization (NFC/NFD) | ✅ | ❌ | ❌ | ❌ |
| Idempotency (ES) | ✅ | ❌ | ❌ | ❌ |
| Uncountables (ES) | ✅ ~87 | ❌ | ❌ | ❌ |
| Accent restoration (ES) | ✅ | ❌ | ⚠️ Partial | ❌ |
| Runtime extensibility | ✅ | ❌ | ❌ | ✅ |
| Add custom languages | ✅ | ❌ | ✅ | ❌ |
| Zero dependencies | ✅ | ❌ | ✅ | ✅ |
| Type hints (`py.typed`) | ✅ | ✅ | ❌ | ❌ |
| Sphinx documentation | ✅ | ❌ | ❌ | ❌ |
| Python 3.10+ | ✅ | ✅ | ✅ | ✅ |
| Test coverage | 100% | ~95% | ~60% | ~70% |

[inflect]: https://github.com/jazzband/inflect
[pluralsingular]: https://pypi.org/project/pluralsingular/
[pluralizer]: https://github.com/audreyfeldroy/inflection

## Performance

pluralio is fast — no regex compilation at call time, `lru_cache` on regex application, and `islower()` short-circuit for the common case:

```
pluralize:    ~1.8 µs/call
singularize:  ~1.8 µs/call
```

Benchmark: 100,000 calls across 13 mixed-language words (English, Spanish, Portuguese, French, Italian) on Python 3.14.

## Supported languages

| Language | Code | Regex rules | Irregulars | Uncountables | Status |
| --- | --- | --- | --- | --- | --- |
| English | `en` | 7 + 22 | 684 | 219 | ✅ Complete |
| Spanish | `es` | 9 + 8 | 352 + 81 extra singles | 92 | ✅ Complete |
| Portuguese | `pt` | 8 + 13 | 388 + 88 extra singles | 88 | ✅ Complete |
| French | `fr` | 6 + 4 | 104 + 27 extra singles | 81 | ✅ Complete |
| Italian | `it` | 19 + 12 | 239 + 0 extra singles | 144 | ✅ Complete |
| Esperanto | `eo` | 2 + 2 | 0 | 33 | ✅ Complete |

## Roadmap

| Version | Goal | Status |
| --- | --- | --- |
| `1.0.0` | English + Spanish, core engine, extensibility API | ✅ Released |
| `1.5.0` | Portuguese (`pt`) | ✅ Released |
| `1.6.0` | French (`fr`) | ✅ Released |
| `1.7.0` | Italian (`it`) | ✅ Released |
| `2.0.0` | Rules restructured into `pluralio/rules/` subpackage, performance optimization | ✅ Released |
| `2.1.0` | Esperanto (`eo`) — trivial `-j` plural | ✅ Released |
| `2.2.0` | Catalan (`ca`) — Romance, natural fit | 🔜 Planned |
| `3.0.0` | German (`de`) — umlauts + multiple plural patterns | 🔜 Planned |

## Contributing

Contributions are welcome! Whether it's a bug report, a new language, or a feature suggestion — please read our guides first:

- 📖 [Contributing Guide](CONTRIBUTING.md) — development setup, coding standards, PR process
- 🤝 [Code of Conduct](CODE_OF_CONDUCT.md) — community expectations
- 🐛 [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)

### Quick start for contributors

```bash
git clone https://github.com/MathiasPaulenko/pluralio.git
cd pluralio
pip install -e ".[dev]"

# Run checks
ruff check pluralio/ tests/
mypy pluralio/ tests/
pytest
```

## Security

If you discover a security vulnerability, please see our [Security Policy](SECURITY.md) for responsible disclosure instructions. **Do not open a public issue.**

## License

[MIT](LICENSE) — Copyright (c) 2025 Mathias Paulenko
