# Changelog

## [Unreleased]

## [1.4.0] - 2025-07-11

### Added

- `compás` → `compases` irregular plural (was incorrectly handled by regex)
- 17 Spanish loanwords ending in `-r` with `-s` pluralization: `monitor`, `scanner`, `manager`, `browser`, `printer`, `computer`, `editor`, `visitor`, `sponsor`, `partner`, `provider`, `supplier`, `investor`, `founder`, `developer`, `sender`, `receiver`
- 9 Spanish words ending in `-é` as explicit irregulars: `café`, `té`, `bebé`, `puré`, `cliché`, `paté`, `rosé`, `bidé`, `frappé`
- 10 Spanish accent restoration mappings in `_EXTRA_SINGLES`: `caimanes`→`caimán`, `guardianes`→`guardián`, `sotanes`→`sotán`, `comodines`→`comodín`, `edenes`→`edén`, `limones`→`limón`, `melones`→`melón`, `dragones`→`dragón`, `campeones`→`campeón`
- 20 Spanish uncountables: medical/scientific (`parálisis`, `tuberculosis`, `psoriasis`, `elefantiasis`, `pediculosis`, `rabies`, `mumps`), biblical (`génesis`, `apocalipsis`), anatomical (`biceps`, `triceps`, `cuádriceps`, `forceps`), compound words (`lavacoches`, `sacamuelas`, `cortaplumas`, `abrelatas`, `parachoques`, `rompecorazones`, `sacaorchos`)
- 5 Spanish `-y` words: `ley`, `rey`, `buey`, `hoy`, `convoy`
- 4 non-tech loanwords: `sandwich`, `whisky`, `ponche`, `parche`

### Fixed

- Idempotency bug: `pluralize(pluralize("café", lang="es"), lang="es")` returned `"cafeses"` instead of `"cafés"`. The regex rule `-és$` → `-eses` was incorrectly matching already-plural forms like `cafés`, `tés`, `bebés`. Fixed by adding these words as explicit irregulars.

### Changed

- Spanish irregular plurals: 61 → 351
- Spanish extra singles: 34 → 80
- Spanish uncountables: 62 → 87
- Test suite: 2,799 → 2,817 tests
- Updated comparison table in README to include `pluralsingular` as competitor
- Updated roadmap to reflect actual release history

## [1.3.0] - 2025-07-11

### Added

- ~130 Latin/Greek classical irregular plurals (Fase 1): -um→-a, -a→-ata, -a→-ae, -en→-ina, -is→-ides, -itis→-itides, -on→-a, -ix/ex→-ices, Hebrew -im, Arabic -i, and other irregulars
- ~40 English uncountables (Fase 2): herd animals, fish, and other invariable nouns
- ~300 explicit inverse singularizations (Fase 3): -uses→-use, -eses→-esis, -oes→-oe, -xes→-xe, -zzes→-zz, -ois→-oi
- ~98 foreign -o words with -os pluralization (Fase 4): musical terms, food, animals, and general loanwords
- ~130 proper noun irregulars with case preservation (Fase 5): names ending in -ie/-y→-ies
- ~22 singular -s words with -es pluralization (Fase 6): acropolis, aegis, alias, cosmos, ethos, etc.
- ~52 suffix-based uncountables (Fase 7): demonyms in -ese, fish names, pox diseases
- `rhinoceros` to `_UNCOUNTABLE`
- `octopi`, `hippopotami`, `platypi` to `_IRREGULAR_SINGLES` for correct singularization of Latin plural forms

### Changed

- Roadmap Fase 8 (verbs/pronouns) evaluated and explicitly marked as out of scope

## [1.2.0] - 2025-07-11

### Changed

- `pluralize()` and `singularize()` now preserve leading and trailing whitespace around the input word
- English `-che` words handled as explicit irregulars instead of a regex rule, fixing singularization for words like `caches`, `niches`, `quiches`
- Expanded compound prefix detection for hyphenated words: `meta`, `post`, `re`, `pre`, `anti`, `pro`, `non`, `sub`, `co`, `ex`, `inter`, `intra`, `multi`, `semi`, `pseudo`, `proto`, `neo`

### Added

- 20+ new English `-che` irregulars (`ache`, `cliche`, `quiche`, `brioche`, `pastiche`, `douche`, `gouache`, `cloche`, `barouche`, `cartouche`, `caliche`, `huarache`, `seiche`, `troche`, `microfiche`, `attache`, `synecdoche`, etc.)
- 6 compound `-ache` words (`headache`, `earache`, `toothache`, `backache`, `heartache`, `stomachache`)
- 13 demonyms ending in `-ese` as uncountables (`japanese`, `chinese`, `vietnamese`, `burmese`, `lebanese`, `portuguese`, `javanese`, `sundanese`, `senegalese`, `congolese`, `sudanese`, `maltese`, `siamese`)
- `ref/ROADMAP-INFLECT.md` — roadmap to reach feature parity with `inflect` in English word coverage
- Comprehensive edge-case tests for whitespace preservation, `-che` singularization, and compound prefixes

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
