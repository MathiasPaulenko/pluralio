# Changelog

## [Unreleased]

## [1.5.3] - 2025-07-12

### Added

- 291 additional Portuguese irregular plurals (97 → 388): expanded `-ão` → `-ões` group with ~80 common words (`criação`, `emoção`, `região`, `questão`, `lição`, etc.), added `-ês` → `-eses` gentilicios (`freguês`, `português`, `japonês`, `inglês`, `francês`, `holandês`, `dinamarquês`, `chinês`, `norueguês`, `polonês`), added monosyllables (`som`, `flor`, `cor`, `mar`, `paz`, `luz`, `cruz`, `rapaz`, `arroz`), added `-el` → `-éis` (`anel`, `pincel`, `painel`, `pastel`, `coronel`), added `-ol` → `-óis` (`girassol`), added `-ães` group (`catalão`, `guardião`, `sotão`, `caimão`, `tecelão`), and ~130 tech/business loanwords (`framework`, `endpoint`, `callback`, `middleware`, `hash`, `bucket`, `pipeline`, `build`, `ticket`, `socket`, `fixture`, `mock`, `diff`, `commit`, `driver`, `buffer`, `proxy`, `header`, `footer`, `script`, `backlog`, `kanban`, `scrum`, `review`, `merge`, `branch`, `fork`, `push`, `pull`, `tag`, `log`, `bug`, `hack`, `patch`, `release`, `deploy`, `rollback`, `backup`, `snapshot`, `dashboard`, `plugin`, `addon`, `snippet`, `template`, `theme`, `skin`, `layout`, `form`, `input`, `output`, `flag`, `switch`, `toggle`, `hook`, `trigger`, `handler`, `listener`, `observer`, `wrapper`, `adapter`, `parser`, `lexer`, `compiler`, `debugger`, `profiler`, `linter`, `runner`, `worker`, `master`, `slave`, `leader`, `follower`, `node`, `host`, `peer`, `client`, `broker`, `shard`, `replica`, `pod`, `volume`, `image`, `registry`, `chart`, `graph`, `test`, `suite`, `case`, `stub`, `spy`, `coverage`, `report`, `alert`, `event`, `message`, `webhook`, `payload`, `request`, `response`, `session`, `cookie`, `query`, `cursor`, `field`, `schema`, `migration`, `seed`, `job`, `task`, `queue`, `stack`, `heap`, `pool`, `cache`, `stream`, `pipe`, `port`, `channel`, `signal`, `beacon`, `sensor`, `device`, `badge`, `card`, `menu`, `tab`, `icon`, `button`, `label`, `filter`, `sort`, `block`, `section`, `item`, `element`, `post`, `comment`, `user`, `account`, `profile`, `role`, `group`, `team`, `project`, `issue`, `plan`, `tier`, `quota`, `limit`, `invoice`, `payment`, `charge`, `refund`, `license`, `subscription`, `monitor`, `scanner`, `manager`, `browser`, `printer`, `computer`, `sender`, `receiver`, `editor`, `visitor`, `sponsor`, `partner`, `provider`, `supplier`, `investor`, `founder`, `developer`)
- 56 additional Portuguese extra singles (32 → 88): accent restoration for all new `-ões`, `-ães`, `-éis`, `-óis`, `-eses`, `-ãos`, and `-eis` plural forms

### Changed

- Moved 14 tech loanwords from uncountable to irregular plurals (`framework`, `pipeline`, `build`, `socket`, `commit`, `proxy`, `deploy`, `backup`, `switch`, `node`, `host`, `cookie`, `cache`, `post`) — these are pluralizable with `+s`, not invariable
- Portuguese uncountable count adjusted from 92 to 91

## [1.5.2] - 2025-07-12

### Changed

- Optimized `_split_whitespace`: fast path for words without surrounding whitespace (common case), skips 3 string operations
- Skip `.lower()` allocation for already-lowercase strings via `islower()` check
- Inlined `unicodedata.normalize` call to avoid redundant variable assignment
- Performance: ~30% faster across all languages (EN/ES/PT pluralize and singularize)

## [1.5.1] - 2025-07-12

### Added

- 62 additional Portuguese uncountables (30 → 92): `-x` invariables (`fax`, `complex`, `suplex`, etc.), anatomical `-ps` (`bíceps`, `tríceps`, `fórceps`), Greek/biblical `-is` (`oásis`, `gênesis`), `-s` invariables (`pires`, `ourives`, `cosmos`, `seis`), adverbs (`menos`, `jamais`), music genres (`blues`, `soul`, `funk`, `reggae`, `folk`, `metal`), sports (`rugby`, `skate`, `poker`, `darts`), and tech/foreign loanwords (`deploy`, `commit`, `cloud`, `kernel`, `streaming`, etc.)

### Changed

- Test suite: 3,116 → 3,188 tests
- 100% coverage maintained

## [1.5.0] - 2025-07-12

### Added

- Portuguese (`pt`) pluralization and singularization support
- Portuguese regex rules: `-ão`→`-ões`, `-m`→`-ns`, `-il`→`-is`, `-l`→`-is`, `-r`→`-res`, `-z`→`-zes`, `-x`→invariable, vowel→`+s`
- Portuguese singularization rules: `-ões`→`-ão`, `-ães`→`-ão`, `-zes`→`-z`, `-ns`→`-m`, consonant+`-is`→`-il`, `-is`→`-l`, double consonant+`-es`→strip `s`, `-tes`/`-des`/`-mes`/`-les`→strip `s`, `-res`→`-r`, default strip `s`
- 97 Portuguese irregular plurals covering `-ão`→`-ões`/`-ães`/`-ãos` splits, accent shifts (`-el`→`-éis`, `-ol`→`-óis`), `-il` paroxítona→`-eis`, and foreign loanwords
- 32 Portuguese extra singles for accent restoration (`papéis`→`papel`, `sóis`→`sol`, `méis`→`mel`, `fiéis`→`fiel`, etc.)
- 92 Portuguese uncountables including `-x` invariables (`tórax`, `látex`, `fax`, `complex`), anatomical `-ps` (`bíceps`, `tríceps`, `fórceps`), Greek/biblical `-is` (`oásis`, `gênesis`), `-s` invariables (`lápis`, `vírus`, `óculos`, `férias`, `pires`, `ourives`), pronouns (`nós`, `vós`), adverbs (`menos`, `jamais`), compound words, music genres (`blues`, `soul`, `funk`, `reggae`), sports (`rugby`, `skate`, `poker`), and foreign/tech loanwords (`software`, `deploy`, `commit`, `cloud`, `kernel`)
- Portuguese test suite: pluralization, singularization, and round-trip tests

### Fixed

- `cantil`→`cantiis` (should be `cantis`): added `il$`→`is` rule before `l$`→`is`
- `leis`→`lel`, `reis`→`rel`, `pais`→`pal`: added consonant+`is`→`il` rule and extra singles for vowel+`is` words
- `mel`→`meis` (should be `méis`), `fiel`→`fieis` (should be `fiéis`): added to irregulars
- `árvores`→`árvor` (should be `árvore`): added to extra singles
- `chaves`→`chav`, `chefes`→`chef`, `peixes`→`peix`: replaced overly aggressive consonant+`es` rule with specific `-res`→`-r` rule
- `grão`→`grões` (should be `grãos`), `são`→`sões` (should be `sãos`): added to irregulars
- `nós`→`nó`, `vós`→`vó`: added to uncountables

### Changed

- Test suite: 2,859 → 3,116 tests
- 100% coverage maintained across all modules

## [1.4.2] - 2025-07-12

### Changed

- Optimized `_match_case`: single-pass case detection instead of 3 passes, with fast path for all-lowercase words
- Skip `unicodedata.normalize` for ASCII-only strings (most English words)
- Eliminated redundant `.lower()` call in `_apply_rules` — caller passes pre-computed lowercase
- Simplified `_apply_rules` signature (removed unused `irregulars` and `rule_list` params)
- Streamlined `_split_whitespace` to avoid redundant string operations
- Performance: ~145K → ~285K ops/sec (~96% faster)

## [1.4.1] - 2025-07-12

### Added

- 19 English uncountable `-ics` disciplines: `politics`, `ethics`, `gymnastics`, `linguistics`, `athletics`, `civics`, `statistics`, `informatics`, `classics`, `mechanics`, `dynamics`, `genetics`, `obstetrics`, `pediatrics`, `psychiatrics`, `orthopaedics`, `academics`, `logistics`, `hysterics`
- 4 English uncountable games: `billiards`, `darts`, `checkers`, `craps`
- 5 Spanish compound uncountables: `quitamanchas`, `matasanos`, `guardabosques`, `guardacostas`
- Spanish invariable adjective `gris` to uncountables

### Fixed

- `annex` round-trip: `annexes` singularized to `annexe` (British) instead of `annex` (American English)
- `finesse` round-trip: `finesses` singularized to `finess` instead of `finesse`
- `bellyache` round-trip: `bellyaches` singularized to `bellyach` instead of `bellyache`
- `peine` round-trip: `peines` singularized to `pein` instead of `peine` (vowel+consonant+e pattern)
- `rol` round-trip: `roles` singularized to `role` (English loanword) instead of `rol` (Spanish singular)

### Changed

- Test suite: 2,817 → 2,859 tests
- Deep validation: 1,141 English words + 466 Spanish words, 0 failures

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
