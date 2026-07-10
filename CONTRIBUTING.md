# Contributing to pluralio

Thanks for your interest in contributing! This document covers everything you need to get started.

## Development setup

### Prerequisites

- Python 3.10+
- [pip](https://pip.pypa.io/)

### Install in development mode

```bash
git clone https://github.com/MathiasPaulenko/pluralio.git
cd pluralio
pip install -e ".[dev]"
```

### Verify your environment

```bash
ruff check pluralio/ tests/
mypy pluralio/
pytest
```

All three must pass before submitting a PR.

## Project structure

```text
pluralio/
├── pluralio/
│   ├── __init__.py        # Public API + extensibility functions
│   ├── core.py            # pluralize(), singularize(), _match_case(), hyphens
│   ├── registry.py        # LanguageRules dataclass, register(), get_rules()
│   ├── rules_en.py        # English rules (irregulars, regex, uncountables)
│   ├── rules_es.py        # Spanish rules (irregulars, regex, uncountables)
│   └── py.typed           # PEP 561 marker
├── tests/
│   ├── conftest.py
│   ├── test_registry.py
│   ├── test_core.py
│   ├── test_en_plurals.py
│   ├── test_en_singles.py
│   ├── test_es_plurals.py
│   ├── test_es_singles.py
│   ├── test_edge_cases.py
│   ├── test_round_trip.py
│   └── test_registry_isolation.py
├── ref/                   # Design docs, rules reference, development plan
├── .github/workflows/     # CI + release workflows
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── README.md
```

## Coding standards

- **Style**: PEP 8, enforced by `ruff` (line-length = 100)
- **Typing**: Strict mypy, type hints required on all public functions
- **Tests**: 95% coverage minimum, enforced in CI (`--cov-fail-under=95`)
- **Dependencies**: Zero runtime dependencies (stdlib only)
- **Python**: Code must work on Python 3.10, 3.11, 3.12, and 3.13

## Adding a new language

1. Create `pluralio/rules_xx.py` with a `LanguageRules` dataclass
2. Call `register(_RULES)` at module level
3. Import the module in `pluralio/__init__.py`
4. Add tests in `tests/test_xx_plurals.py` and `tests/test_xx_singles.py`
5. Add round-trip tests in `tests/test_round_trip.py`
6. Update `README.md` languages table
7. Update `CHANGELOG.md`

No changes needed to `core.py` or `registry.py`.

## Adding irregulars or rules to an existing language

Edit the corresponding `rules_xx.py` file and add tests in the appropriate test file.

## Pull request process

1. Fork the repo and create a branch from `main`
2. Write tests for your changes
3. Ensure all checks pass:

   ```bash
   ruff check pluralio/ tests/
   mypy pluralio/
   pytest
   ```

4. Update `CHANGELOG.md` with a description of your changes
5. Open a pull request using the [PR template](.github/pull_request_template.md)
6. Wait for CI to pass — all checks must be green

## Commit messages

Use clear, descriptive commit messages. Suggested format:

```text
<type>: <short description>

<optional longer description>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

Examples:

```text
feat: add Portuguese pluralization rules
fix: correct singularize for words ending in -ces
docs: update README with count parameter example
test: add round-trip tests for Spanish irregulars
```

## Reporting bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) when opening an issue. Include:

- Python version
- OS
- Minimal reproduction code
- Expected vs actual output

## Suggesting features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md) when opening an issue. Describe:

- The use case
- The proposed API
- Any alternatives you've considered

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
