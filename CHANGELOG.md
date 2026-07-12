# Changelog

## [Unreleased]

## [2.0.0] - 2025-07-13

### Breaking

- Language rule modules moved from `pluralio/rules_en.py` to `pluralio/rules/en.py` (same for `es`, `fr`, `it`, `pt`). Use `import pluralio` as before — the public API is unchanged. If you imported rule modules directly (e.g. `from pluralio import rules_en`), update to `from pluralio.rules import en`.

### Changed

- `pluralio/rules/` is now a subpackage with its own `__init__.py` that triggers registration of all built-in languages
- `_match_case` optimized with `islower()` short-circuit (~5% faster on lowercase inputs)

## [1.8.3] - 2025-07-13

### Fixed

- `_match_case` now guards against empty strings, preventing `IndexError` on edge-case inputs
- `is_singular` now uses `pluralize(x) != x` instead of `singularize(x) == x`, fixing inconsistency with `is_plural`

### Added

- `__all__` exports in `core.py` and `registry.py` for explicit public API surface
- `snapshot()` and `restore()` functions in `registry.py` for test-safe registry isolation
- `mypy` type checking now covers `tests/` directory in CI
- `ruff` lint rules expanded: `B` (bugbear), `C4` (comprehensions), `SIM` (simplifications), `PT` (pytest style)
- `.hypothesis/` added to `.gitignore`

### Changed

- Extracted `_transform()` in `core.py` to deduplicate `pluralize`/`singularize` logic
- `conftest.py` now uses public `snapshot`/`restore` API instead of accessing private `_REGISTRY`
- `test_edge_cases.py` (2948 lines) split into 6 per-language files: `test_cross_edge_cases.py`, `test_en_edge_cases.py`, `test_es_edge_cases.py`, `test_pt_edge_cases.py`, `test_fr_edge_cases.py`, `test_it_edge_cases.py`
- `__version__` fallback reads from `pyproject.toml` when package metadata is unavailable
- Module docstring documents side-effect import requirement for language registration
- `LanguageRules` docstring improved with `.. warning::` block about intentional container mutability

## [1.8.2] - 2025-07-13

### Fixed

- Italian `-tà` abstract nouns (`verità`, `felicità`, `libertà`) now invariable via new `à$` plural rule
- Italian `-ese` nationality words (`inglese`, `francese`, `giapponese`, `cinese`, `portoghese`, `olandese`, `svedese`, `norvegese`, `finlandese`, `danese`) now round-trip correctly via new `esi$ → ese` singular rule
- Italian round-trip for 27 common `-e` words: `piede`, `fine`, `margine`, `bottone`, `gigante`, `santone`, `difensore`, `attaccante`, `esemplare`, `necessario`, `sufficiente`, `importante`, `evidente`, `intelligente`, `potente`, `urgente`, `simile`, `facile`, `difficile`, `utile`, `inutile`, `possibile`, `impossibile`, `probabile`, `improbabile`, `portatile`, `turbine`
- `sangue`, `peggio`, `week-end` added to uncountables
- Months (`gennaio`–`dicembre`), seasons (`primavera`, `estate`, `autunno`, `inverno`), and numbers (`due`, `tre`, `cinque`, `sei`, `sette`, `nove`, `dieci`, `mille`) added to uncountables

### Added

- New plural rule: `à$` → invariable (for abstract nouns ending in `-tà`)
- New singular rule: `esi$ → ese` (for nationality words)
- 27 new Italian irregular plurals for common `-e` words
- 27 new Italian uncountables (months, seasons, numbers, invariable nouns)

### Changed

- Italian irregulars expanded: 239 (was 212)
- Italian uncountables expanded: 144 (was 117)
- Italian plural rules: 19 (was 18)
- Italian singular rules: 12 (was 11)

## [1.8.1] - 2025-07-13

### Fixed

- Italian round-trip for `bicchiere`, `giornale`, `mare`, `padre`, `madre`, `re` (masculine `-e` words that singularized to `-o` instead of `-e`)
- Italian round-trip for `zio` → `zii` (was singularizing to `zo`)
- `società` added to uncountables (invariable noun, was being pluralized incorrectly)

### Added

- 13 new Italian irregular plurals: `bicchiere`, `giornale`, `mare`, `padre`, `madre`, `re`, `zio`, `zia`, `fratello`, `nonno`, `nonna`, `cugino`, `cugina`

### Changed

- Italian irregulars expanded: 212 (was 199)
- Italian uncountables expanded: 117 (was 116)

## [1.8.0] - 2025-07-13

### Added

- 54 new Italian irregular plurals: Greek-origin masculine `-a` (`schema`, `dogma`, `emblema`, `idioma`, `fantasma`), profession nouns in `-ista` (`artista`, `autista`, `giornalista`, `linguista`, `turista`, `astronauta`), masculine `-e` nouns (`fiume`, `ponte`, `cliente`, `residente`, `presidente`, `generale`, `animale`, `fossile`, `fucile`, `cortile`), adjectives in `-are` (`volgare`, `regolare`, `singolare`, `particolare`), feminine `-a` nouns (`borsa`, `coppia`, `porta`, `torta`, `tazza`, `sala`, `ruota`, `penna`, `palla`, `tela`, `sorella`, `frusta`), body part irregulars (`braccio → braccia`, `lenzuolo → lenzuola`, `ciglio → ciglia`), `-cio` words (`laccio`, `straccio`, `sacrificio`, `abbraccio`), `-go` piana (`obbligo → obblighi`), and feminine `-e` nouns (`torre`, `corte`, `sorte`, `morte`, `canzone`)
- 60 new Italian uncountables: tech loanwords (`streaming`, `download`, `upload`, `hashtag`, `follower`, `like`, `share`, `tweet`, `link`, `click`, `login`, `logout`, `reset`, `backup`, `input`, `output`, `format`, `record`, `report`, `budget`), media terms (`show`, `preview`, `trailer`, `remake`, `sequel`, `break`, `flop`, `sketch`, `spot`), sports (`tennis`, `golf`, `hockey`, `rugby`, `match`, `round`, `ring`, `volley`, `sprint`, `set`), accented invariables (`città`, `virtù`, `tè`, `perché`, `cioè`, `sé`), days of the week (`lunedì`–`domenica`), and misc (`shock`, `stop`, `start`, `loop`, `cross`, `short`, `staff`)

### Changed

- Italian irregulars expanded: 199 (was 145)
- Italian uncountables expanded: 116 (was 56)

## [1.7.2] - 2025-07-13

### Fixed

- Italian masculine `-e` words (`cuore`, `studente`, `dente`, `nome`, `sole`, `colore`, `valore`, `dottore`, `signore`, `attore`, `professore`, `imperatore`, `scultore`, `pittore`, `scrittore`) now round-trip correctly
- Italian feminine `-zione`/`-sione` words (`nazione`, `stazione`, `lezione`, `funzione`, etc.) now round-trip correctly via `-ioni → -ione` singular rule
- Italian masculine `-tore` words now singularize correctly via `-tori → -tore` regex rule
- Italian feminine `-cia`/`-gia` words after consonant (`pioggia → piogge`, `roccia → rocce`, `fascia → fasce`, `ascia → asce`) now pluralize correctly via consonant-aware regex
- Italian feminine `-cia`/`-gia` words after vowel (`valigia → valigie`, `camicia → camicie`) now pluralize correctly via vowel-aware regex
- Italian `-ie` feminine words (`superficie → superfici`, `effigie → effigi`) now pluralize correctly via `-ie → -i` regex rule
- Italian Greek-origin masculine `-a` words (`problema → problemi`, `sistema → sistemi`, `clima → climi`, `dramma → drammi`, `programma → programmi`, etc.) now pluralize correctly as irregulars
- Italian masculine `-io` words (`studio → studi`, `esercizio → esercizi`) now round-trip correctly as irregulars
- Italian feminine `-a` plurals (`sedie`, `chiavi`, `isole`, `stelle`, `barche`, etc.) now idempotent as irregulars
- `is_singular`/`is_plural` now correct for masculine `-e` words (`cuore`, `studente`, etc.)
- Removed 19 loanwords from `_IRREGULAR_PLURALS` (already in `_UNCOUNTABLE`, no duplication needed)

### Changed

- Italian regex rules expanded: 18 plural rules (was 15), 11 singular rules (was 8)
- Italian irregulars expanded: 145 (was 121)

## [1.7.1] - 2025-07-13

### Fixed

- Italian feminine `-e` singulars (`notte`, `mente`, `fronte`, `sede`, `parte`, `classe`, `noce`, `fede`, `pace`, `croce`, `gente`, `nave`, `valle`, `parete`, `radice`) now round-trip correctly
- Italian masculine `-io`/`-cio`/`-gio` words (`bacio`, `spazio`, `ufficio`, `socio`, `cambio`, `esempio`, `principio`, `stadio`, `negozio`, `formaggio`, `viaggio`, `raggio`, `coraggio`, `passaggio`, `messaggio`) now round-trip correctly
- Italian feminine `-a` plurals (`case`, `scuole`, `banane`, `gatte`, `paste`, `piante`, `famiglie`, `squadre`, `feste`, `donne`, `ragazze`, `macchine`, `piazze`, `pizze`, `bambine`) now idempotent
- `voce` moved from uncountable to irregular plurals (`voce → voci`)
- `noir` added to uncountable for `film-noir` compound
- Removed 18 redundant `_EXTRA_SINGLES` (all auto-generated from inverse mapping)
- `is_singular`/`is_plural` now correct for feminine `-e` words

## [1.7.0] - 2025-07-13

### Added

- Italian (`it`) language support with 15 plural rules and 8 singular rules
- 121 irregular plurals covering sdrucciola `-co → -ci` (amico → amici), sdrucciola `-go → -gi` (asparago → asparagi), piana `-go → -ghi` explicit mappings (lago → laghi), completely irregular words (uomo → uomini, dio → dei, uovo → uova), foreign loanwords (film, bar, computer), common `-e`/`-io` words for round-trip correctness (cane → cani, vizio → vizi), feminine `-e` singulars (notte → notti, mente → menti), masculine `-io`/`-cio`/`-gio` words (bacio → baci, formaggio → formaggi, viaggio → viaggi), and feminine `-a` words for plural idempotency (casa → case, scuola → scuole)
- 56 uncountable/invariable words including foreign loanwords, Greek-origin forms in `-i` (analisi, crisi), pluralia tantum (occhiali, forbici), truncated forms (foto, auto), accented-vowel words (caffè), and invariable loanwords (noir)
- Italian test suite: `test_it_plurals.py`, `test_it_singles.py`, and Italian edge cases in `test_edge_cases.py`

## [1.6.2] - 2025-07-13

### Added

- 9 pluralia tantum words: `ciseaux`, `lunettes`, `jumelles`, `pincettes`, `arrérages`, `ambages`, `fraîtures`, `mœurs`, `condoléances`, `frais`, `gens`
- 2 `-ou → -oux` irregulars: `gnou → gnoux`, `bayou → bayoux`
- 4 `-al → -als` exceptions: `étal → étals`, `val → vals`, `gal → gals`, `recal → recals`
- `cour → cours` irregular mapping for round-trip correctness
- 7 accentless variant mappings: `generaux → general`, `hopitaux → hopital`, `metaux → metal`, `signaux → signal`, `regaux → regal`, `recitaux → recital`, `voeux → voeu`
- `aux → au` extra single for compound singularization (`pots-aux-feux → pot-au-feu`)
- French hyphenated compound pluralization: all noun segments are now pluralized/singularized (e.g. `café-théâtre → cafés-théâtres`, `chou-fleur → choux-fleurs`, `pot-au-feu → pots-aux-feux`)

### Changed

- French hyphenated compound handling in `core.py`: pluralizes/singularizes all noun segments, skipping function words (`de`, `en`, `et`, etc.) and fixed parts (`vie`, `ciel`)
- Removed `cours` from uncountable (now handled via `cour → cours` irregular)
- Updated supported languages table with accurate rule counts (104 irregulars, 27 extra singles, 81 uncountables)

## [1.6.1] - 2025-07-13

### Fixed

- `bleu`, `pneu`, `émeu` now pluralize to `bleus`, `pneus`, `émeus` instead of `bleux`, `pneux`, `émeux` (were incorrectly caught by `eu$ → eux` regex; added as irregulars with `+s`)
- `tuyau`, `noyau`, `boyau`, `sarrau` now pluralize to `tuyaux`, `noyaux`, `boyaux`, `sarraux` instead of `tuyaus`, `noyaus`, etc. (added `au$ → aux` regex rule and irregular mappings)
- `tuyaux`, `noyaux`, `boyaux`, `sarraux` now singularize back to `tuyau`, `noyau`, `boyau`, `sarrau` instead of `tuyal`, `noyal`, etc. (added to `_EXTRA_SINGLES`)
- `bail` now pluralizes to `baux` instead of `bails` (was missing from `-ail → -aux` irregulars)
- `endroit` removed from uncountable — now correctly pluralizes to `endroits`
- `paris` removed from uncountable — now correctly singularizes to `pari`
- `fils` added to uncountable (pluralia tantum) — no longer singularizes to `fil`
- `ideaux`, `émaux` (accentless variants) now singularize to `ideal`, `email` via `_EXTRA_SINGLES`

### Added

- `au$ → aux` pluralization regex rule (between `eau$` and `eu$`)
- Accentless variant mappings for `ideaux → ideal` and `emaux → email`
- Tests for all new irregulars and fixed cases

## [1.6.0] - 2025-07-13

### Added

- French (`fr`) language support: 5 regex rules (`-al → -aux`, `-eau → -eaux`, `-eu → -eux`, `-s/-x/-z → invariable`, default `+s`), 90 irregular plurals (`cheval → chevaux`, `travail → travaux`, `bijou → bijoux`, `œil → yeux`, `monsieur → messieurs`, etc.), 20 extra singles for singularization restoration (`travaux → travail`, `yeux → œil`, etc.), 60 uncountable/invariable words (`information`, `temps`, `riz`, `croix`, `nez`, etc.)
- French edge case tests: case preservation (title, all caps), mixed case, hyphenated words, idempotency, round-trip (50+ words), count-aware pluralization, whitespace preservation, single letters, uncountable consistency (70+ words), `is_singular`/`is_plural` checks

### Changed

- Updated `pyproject.toml` description to include French (`EN/ES/PT/FR`)
- Added `french` to keywords in `pyproject.toml`
- Updated README to reflect French language support

## [1.5.5] - 2025-07-12

### Fixed

- `dinamarqueses` now singularizes to `dinamarqués` (was `dinamarques` — missing accent restoration in `_EXTRA_SINGLES`)
- `fraces` now singularizes to `frac` (was `fraz` — incorrectly caught by `ces$` → `z` singularization rule; added `frac` → `fraces` to irregular plurals)

### Added

- 452 Spanish edge case tests: case preservation (title, all caps), mixed case, hyphenated words (noun+noun, leading/double hyphen), idempotency (45+ already-plural words), round-trip (45+ words), count-aware pluralization, whitespace preservation, single letters, uncountable consistency (70+ words), `is_singular`/`is_plural` checks
- 150 English edge case tests: count-aware pluralization (18 words × 3 counts), mixed case, single letters, uncountable consistency (40+ words), `is_singular`/`is_plural` checks, hyphenated compound round-trip (13 compounds)

## [1.5.4] - 2025-07-12

### Fixed

- Portuguese verb+noun hyphenated compounds now pluralize the last segment (noun) instead of the first (verb): `quebra-cabeça` → `quebra-cabeças` (was `quebras-cabeça`), `guarda-chuva` → `guarda-chuvas`, `beija-flor` → `beija-flores`, `arranha-céu` → `arranha-céus`, `passa-tempo` → `passa-tempos`, `guarda-roupa` → `guarda-roupas`
- Added 28 Portuguese verb prefixes to `_LAST_SEGMENT_PLURAL_FIRST_WORDS`: `quebra`, `guarda`, `arranha`, `limpa`, `mata`, `saca`, `abre`, `corta`, `lança`, `trava`, `cata`, `chupa`, `espanta`, `passa`, `pisa`, `salta`, `adivinha`, `roí`, `cai`, `sobe`, `desce`, `para`, `pára`, `bota`, `tira`, `pega`, `leva`, `traz`, `beija`

### Changed

- Moved 3 Portuguese compound words from uncountable to pluralizable: `guarda-chuva`, `beija-flor`, `passa-tempo` — these are verb+noun compounds that pluralize the noun, not invariable words
- Portuguese uncountable count adjusted from 91 to 88

### Added

- 725 Portuguese edge case tests: case preservation (title, all caps, mixed), hyphenated words (noun+noun, verb+noun), idempotency (140+ already-plural words), round-trip (140+ words), NFD normalization, `is_plural`/`is_singular` checks, count-aware pluralization, whitespace preservation, single letters, uncountable consistency

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
