# Changelog

## [Unreleased]

### Changed

- `LanguageRules` is now `frozen=True` — prevents accidental attribute reassignment while allowing in-place extension via the public API
- `register()` now raises `ValueError` if `code` is empty
- English pluralization rules expanded: `fe → ves`, `consonant+f → ves`, `consonant+o → oes` added as regex rules (previously handled only as irregulars)
- English singularization rules expanded: `ves → f`, `oes → o` added as regex rules
- `pyproject.toml`: added author email, `Bug Tracker` and `Changelog` URLs

### Added

- 25 new English irregular exceptions for the new regex rules (`cafe → cafes`, `solo → solos`, `turf → turfs`, `shoe → shoes`, etc.)
- Tests for `frozen=True` behavior, empty code validation, and all new regex rules

## [0.1.0] - 2025-07-10

### Added

- `pluralize()` and `singularize()` for English and Spanish
- `count` parameter for count-aware pluralization
- Case preservation (title case, all caps)
- Hyphenated word support (`mother-in-law` → `mothers-in-law`)
- Extensibility API: `add_irregular`, `add_plural`, `add_singular`, `add_uncountable`, `add_plural_rule`, `add_singular_rule`, `register_language`
- `supported_languages()` to list registered languages
- `LanguageRules` dataclass for custom language registration
- `py.typed` marker for PEP 561
- CI workflow (lint + type check + test on Python 3.10–3.13)
- Release workflow (trusted publishing to PyPI)
- 95% coverage requirement enforced in CI
