<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-export-ctl-check-hero-en-light.webp" width="100%" alt="dsh-export-ctl-check: the left column carries the plugin name, two value lines and the note that 8 rules close the register loop and no control list is held; the right side is one item's scoreboard — eight cells, one per rule, each with the rule id, the field it reads and the value it observed (controlled empty → hit; licenseNo condition not met → skipped; licenseAt filled → pass; endUse/endUser filled → pass; destination filled → pass; licenseNo unique → pass; category civil-military with values unconfigured → skipped; itemName clean → pass), followed by the single EC-001 warn finding and the two skips EC-002 and EC-007">
</picture>

# dsh-export-ctl-check

**Check an export-control item register line by line — which row, which column, what is missing. Differences only, no verdict.**

An offline checker for customs-compliance and export-control teams: it reads one item register (an exporter header plus one row per item) and checks that register's own completeness and closure against a versioned rule pack. No network, no model call, no change to the original material.

[Install](#three-step-setup) · [Configuration](#configuration) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibility)
[![npm](https://img.shields.io/npm/v/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-export-ctl-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibility)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-export-ctl-check?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-export-ctl-check?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-export-ctl-check/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-export-ctl-check)

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
```

</div>

<sub>Community plugin, not affiliated with DeepSeek. Canonical repository: <https://github.com/PerryLink/dsh-export-ctl-check> (Gitee is a mirror).</sub>

## What it is

`dsh-export-ctl-check` reads one export-control item register — the exporter header plus one row per item — and cross-checks that register's own completeness and closure rather than judging the items: whether each item states in the controlled column whether it is controlled, whether an item marked as controlled carries an export licence number, whether a recorded licence number is accompanied by an issue date, whether the end use or the end user is recorded, whether the destination is recorded, whether a licence number repeats inside the same register, whether the control category comes from the institution's own vocabulary, and whether a template placeholder (an empty bracket pair, `XXX`, `TBD` or a fill-me marker) still survives in the item-name column.

It lists only differences that can be pointed to inside the material, and gives the row, the column, what is missing and what to fill in. It does not decide whether an item is controlled, whether a licence is required, or whether an export complies. Hand it the material in chat — installation is one command, and the findings are meant to be read directly. 33 tests (`npx vitest run`) cover paired fixtures for the 8 rules, and `samples/quickstart` runs one real check offline.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-export-ctl-check-flow-v5-light.svg" width="100%" alt="dsh-export-ctl-check structure: two inputs on the left — the register (JSON/YAML: four optional header scalars, rows[], 13 canonical column aliases, requireAnyOf) and the rule pack (8 rules, 6 check kinds, validated at load for document / number / clause / excerpt / kind / source) — plus the boundary the pack will not cross (no control list held); in the middle eight gates are stacked in one ladder, the first three forming the conditional chain controlled → licenseNo → licenseAt, each gate leaving through exactly one exit, with the quickstart state in the right column; on the right the two exits and one report — issues[] (one warn: controlled empty on row 1, with expected, fix and the locator row/column) and skipped[] (EC-002, EC-007 with their reasons) — resolving into error 0 / warn 1 / info 0, issues 1, markdown and reportJson">
</picture>

## Three-step setup

1. **Install** (pick one channel):

   ```sh
   # git channel (latest main)
   dsh plugin --profile web add github:PerryLink/dsh-export-ctl-check
   # npm channel (published releases)
   dsh plugin --profile web add dsh-export-ctl-check
   # tarball channel: pnpm pack in this repo, then
   dsh plugin --profile web add ./dsh-export-ctl-check-<version>.tgz
   ```

   No runtime dependencies; `lib/index.mjs` and `rules/` are the shipped artifacts.

2. **Minimal config** (the defaults work; the rule pack ships with the package):

   ```yaml
   - insert:
       - id: dsh-export-ctl-check
         name: dsh-export-ctl-check
   ```

3. **Verify it mounts**:

   ```sh
   dsh --profile web --dump-config | grep 'dsh-export-ctl-check'
   node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   export_ctl_check: 1 issue(s) — error 0, warn 1, info 0
   skipped: 2
   ```

**Uninstall**: `dsh plugin --profile web remove dsh-export-ctl-check` (or remove the row from the profile patch).

> The plugin makes no network calls and writes no material files; every check happens locally. The sample lives in `samples/quickstart/input/`, the expected output in `samples/quickstart/expected/result.json`. You can also search for the Customs Compliance Suite in WorkBuddy / Coze (this check is one part of it; availability is as listed in that marketplace).

## Core capabilities

`export_ctl_check` has a single tool surface: read the material, run the rule pack, return one report. Capabilities, by what you can get out of it:

- **Eight rules in one pass** — `EC-001` through `EC-008` cover the controlled declaration, the licence number, the issue date, end use and end user, the destination, repeated licence numbers, the control category and the item-name placeholder. Each rule checks presence, not correctness.
- **Pinned to row and column** — every finding carries `locator` (`row` + `field`), `found`, `expected` and `fix`, so you can go straight back to that cell of the register.
- **Skips must explain themselves** — checks that cannot run land in `skipped` with a reason; an empty issue list is not the same as a pass, and an unconfigured rule or a missing column is never silently read as success.
- **Rules are data** — the rule pack `rules/export-ctl-check.yaml` is separate from the code; swapping the file switches the rule-set version without touching TypeScript. The loader validates `document` / `number` / `clause` / `excerpt` / `kind` / `source` for every rule.
- **No fabricated citations** — an excerpt must be a verbatim quotation; when the basis is only a principle, `kind` is `derived-from-principle` and severity is capped at `warn`, while an institutional threshold is capped at `info`.
- **Fully offline** — no network request, no model call, no write to the register; the tool returns a text report (`markdown`) and a structured report (`reportJson`).

### Rule table

| Rule | What it checks | Severity | Basis kind |
|---|---|---|---|
| `EC-001` | each item states whether it is controlled | `warn` | derived from principle |
| `EC-002` | a controlled item carries a licence number | `warn` | direct |
| `EC-003` | a recorded licence carries an issue date | `warn` | derived from principle |
| `EC-004` | end use or end user is recorded | `warn` | direct |
| `EC-005` | a destination is recorded | `warn` | direct |
| `EC-006` | licence numbers do not repeat in the register | `warn` | derived from principle |
| `EC-007` | the control category comes from your vocabulary | `info` | derived from principle |
| `EC-008` | the item name holds no unreplaced placeholder | `warn` | direct |

### Examples

This is the plugin's real output on its own `EC-001` fixture, not an illustration.

**Tool** `export_ctl_check`

**Input**

~~~json
{"rows":[{"物项名称":"某型高性能传感器","是否受控":""}]}
~~~

**Output**

~~~json
{
  "id": "dsh-export-ctl-check.EC-001.de09b5a6",
  "ruleId": "EC-001",
  "severity": "warn",
  "locator": {
    "field": "controlled",
    "row": 1
  },
  "found": "第 1 行「controlled」为空",
  "expected": "「controlled」应填写",
  "fix": "补填是否受控；本条只核对是否声明，不判断该判断是否正确"
}
~~~

*Observed from `tests/fixtures/EC-001/EC-001-unsafe.json (cases.json expects EC-001 count 1); run via lib/index.mjs rules/export-ctl-check.yaml`*

### What you ask, what it answers

| You ask | What it answers |
|---|---|
| An item is marked as controlled but has no licence number. Is that reported? | Yes, `EC-002` reports the gap: when a row's controlled value is one the rule is configured to treat as controlled, it requires an export licence number. The rule checks only that the number is filled in; it does not judge whether the licence is genuine, still valid, or covers that item and that destination. If your register writes some other word for controlled, add it to the rule's condition values, or the row counts as not controlled and the rule stays silent — this plugin holds no control list to decide the question for you. |
| An item states whether it is controlled but leaves end use and end user empty. Does anything catch that? | Yes, `EC-004` reports the row: it asks for at least one of those two columns to be filled. One of the two is enough, and the rule does not judge whether the stated use or user is true or whether the case is one the law prohibits or restricts. |
| A licence number is written down but the issue-date column is blank. Is that a finding? | `EC-003` requires it. The condition is the licence number: a row without one is not asked for a date at all. The rule does not check the licence's validity period, and it does not weigh the issue date against the export date — it establishes that a date is there, not that it comes first. |
| One and the same licence number appears on several rows. What does the check say? | `EC-006` reports the number as repeated across the register. It cannot tell a single licence covering several items — a normal way to keep the register — from a number copied by mistake, so a hit needs a person to confirm it; the rule does not renumber anything, and it does not say how many rows may share one licence. If your register is deliberately written one-licence-many-items, give the rows of that licence a serial number, or switch the rule off. |
| A row has no destination at all. | `EC-005` reports it, because every item has to carry a destination. It checks that the column is filled, not that the destination is permitted: whether a country or region is embargoed or restricted is read from lists the competent authority publishes, and this plugin holds no country list of its own. |
| The item-name column still reads a bracketed sample value or `XXX` — defect or real name? | `EC-008` reports the row when the name contains one of the terms the rule looks for: bracketed placeholders, `XXX`, `xxx`, `TBD`, `todo`, or a fill-me marker. That term list follows your own template and can be adjusted. The rule looks for those terms in that one column only; it never judges whether the name itself is factually correct. |

## Configuration

Every tunable lives in the Schemastery schema in `src/config.ts`, so it can be changed from `cordis.yml` without touching code; per-rule thresholds live in the rule pack under `rules/`.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

<details>
<summary>Rule-level parameters (in the rule pack, not here)</summary>

- `EC-002` `conditionValues` — which values of the controlled column mark an item as controlled. The shipped defaults are:

```text
是 · Y · yes · true · 受控 · √
```

  If your register writes something else, add it to this list; otherwise the row counts as uncontrolled and the rule stays silent.
- `EC-007` `values` — your institution's control-category values, for example `[nuclear, missile, biological, chemical, dual-use]`. Empty means "not configured", and the rule reports itself in `skipped`; the plugin hard-codes no taxonomy.
- `EC-008` `terms` — the placeholder terms. The shipped defaults are:

```text
【 】 {{ }} XXX xxx 待填 待补充 TBD todo 示例
```

</details>

Example override in your profile patch:

```yaml
- insert:
    - id: dsh-export-ctl-check
      name: dsh-export-ctl-check
      config:
        onlyRules: [EC-001, EC-002, EC-003]
        skipNotes: institution rules, 2026 edition
```

## Material format

The tool accepts JSON or YAML. Its input is either `file` (an absolute path to the material) or `material` (inline text) — exactly one. Excel can be converted to JSON/YAML first, in chat if the platform supports it.

```yaml
exporter: 某某进出口有限公司
contractNo: SC-2026-018
listVersion: 2026 年版
rows:
  - { 序号: '1', 物项名称: 某型高性能传感器, 商品编号: '9031809090',
      管制类别: 军民两用, 最终用途: 用于工业自动化产线的位移测量,
      最终用户: 某某工业自动化有限公司, 最终目的地: 德国,
      许可证号: EX2026-0018, 许可日期: 2026-02-25, 是否受控: 是 }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own column names are kept, so a finding names the column it read. Fields are optional at the read layer and validated by the check engine, so a partial export produces "missing item" findings instead of a crash.

## Standards it follows

| Document | Number | Cited by rules |
|---|---|---|
| Export Control Law of the People's Republic of China | Adopted 17 October 2020 at the 22nd session of the 13th NPC Standing Committee, promulgated by Presidential Order No. 58, effective 1 December 2020 | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| Export Control Law of the People's Republic of China | Current version not verified in this pass | EC-007 |

**Boundary:** this plugin checks an **export-control item register** for the closed loop a register can be held to — that each item states whether it is controlled, that a controlled item carries a licence number, that a licence carries an issue date, that the end use or end user is recorded, that a destination is recorded, that licence numbers do not repeat, that the control category comes from your vocabulary, and that no placeholder survives. It does **not** decide whether an item is controlled, whether a licence is required, or whether an export would breach the rules.

### Rule pack

Rule data lives in `rules/export-ctl-check.yaml`. Its header explains that the plugin holds no control list and does no list lookup, so it cannot detect an undeclared controlled item. The load-time guard still requires a document, clause, excerpt and source per rule, and still forbids a principle-derived or locally configured check from being `error`.

> ### ⚠️ Read this before trusting a citation in the report
>
> **`excerpt` status is per rule, not uniform.** Some rules quote the clause verbatim (`kind: direct`), some are derived from the principle of the cited articles (`kind: derived-from-principle`, capped at `warn`), and some use thresholds your institution configures (`kind: institutional-configuration`, capped at `info`). The pack never paraphrases a quotation: when the text was not obtained, the `excerpt` field says so and the reasoning lives in `note`; a test asserts that no rule claims a quotation it does not have. **For any rule still marked as not obtained, replace the `excerpt` with the real clause and raise `kind` to `direct` once the text is in hand.**
>
> The conclusion is the reviewer's: this plugin lists differences it can point to in the material and does not decide facts or compliance.

## FAQ

<details>
<summary>Is the material uploaded or processed over the network?</summary>

No. The plugin only reads what you hand it through `file` or `material`, parses it locally and runs the rules locally: no network requests, no telemetry, no model calls. The result exists only in the tool return value and the DSH host's own session log; the package keeps no second copy.

</details>

<details>
<summary>I believe an item should be controlled but nothing was reported. Is that a miss?</summary>

It is the plugin's most important boundary, not a miss: it holds no control list and does not map a commodity code or a technical parameter onto a list entry, so it cannot find an item that should have been declared controlled and was not. Whether an item is controlled is the exporter's own determination against the published list. What the plugin does guarantee is that checks it cannot run land in `skipped` rather than passing silently.

</details>

<details>
<summary>Does it fight other plugins over command names, events or slots?</summary>

No. It declares only the `tools` dependency and registers one `export_ctl_check` tool; it registers no command, no client slot, no `webServer` prefix, provides no service key and mutates no globals. The point-by-point argument is in "Interoperability".

</details>

<details>
<summary>How big is the performance overhead?</summary>

Local parsing plus rule matching — no network, no model call. The default tool timeout budget is `120000` ms. 33 tests (`npx vitest run`) cover paired fixtures for all 8 rules, and `samples/quickstart` can be re-run offline.

</details>

<details>
<summary>Can the rule pack be replaced?</summary>

Yes. `rulesFile` can point at any rule-pack file (relative to the package root or absolute); rules are data, and the loader validates the citation fields and the severity caps. Swapping the file switches the rule-set version without touching TypeScript.

</details>

## Security boundaries

- **Read-only material.** The plugin reads through `file` or `material`, never writes back and never changes the original; the only write is the session log the DSH host keeps, and the package adds no second copy.
- **No network, no model call.** No network requests, no telemetry, no model calls; every check happens locally.
- **No adjudicating wording.** The report lists literal differences between the material and the cited clauses; it does not judge compliance, liability or factual truth. The conclusion is the reviewer's.
- **Failure is not silent.** The rule pack is validated on load; checks that cannot run land in `skipped` with a reason, and an empty issue list is never read as "nothing is wrong".
- **No fabricated citations.** An excerpt must be a verbatim quotation; when the text cannot be obtained the pack says so and caps the severity.
- **Registration is an effect.** Tool registration returns a disposer, so stop or hot-reload unregisters the tool and leaves no dangling listener.

## Known limitations

- **No control list inside.** The controlled column is the register's own declaration; the plugin checks only the closure after that declaration and cannot find an undeclared controlled item. This is the plugin's most important capability boundary.
- **It does not judge the licence itself.** `EC-002` and `EC-003` check that the number and the issue date are filled in; they do not verify authenticity, validity period, or coverage of that item and destination, and they do not compare the issue date with the export date.
- **It does not judge end use or end user truthfulness.** `EC-004` only requires at least one of the two columns to be filled; it does not judge whether the stated use or user is true or prohibited.
- **It does not judge whether a destination is restricted.** `EC-005` only checks that the destination column is filled; no country or region list is built in.
- **A repeated licence number is a lead, not a conclusion.** One licence covering several items is a normal way to keep a register, so a `EC-006` hit needs human confirmation; the plugin does not renumber and does not cap how many rows one licence may cover.
- **`EC-007` needs your vocabulary.** `values` ships empty, so the rule reports itself in `skipped` until configured; how control categories are split depends on the list version, and the plugin hard-codes no taxonomy.
- **Citation status is per rule.** Some rules still mark their `excerpt` as not obtained, keep `kind: derived-from-principle` and stay capped at `warn`; once the text is in hand, replace the excerpt and raise the kind to `direct`.
- **The full rule set is still 8 rules.** It covers register-level completeness and closure, not a substantive review of the item, the licence or the transaction.

## Interoperability

The plugin registers one tool and occupies no other plugin's surface:

- **Only the `tools` dependency.** `inject = ['tools']`; with no tools service it registers nothing.
- **Only `export_ctl_check`.** No command, no client slot, no `webServer` prefix, so it does not contend for those seats.
- **No service key, no global mutation.** It patches no prototype, writes no `process.env` and replaces no global fetch.
- **The bundle patch only inserts its own row.** `cordis.patch.yml` adds the plugin row and never overrides a built-in row's `config`.
- **The shared kit is copied in.** `src/shared/` is a shared kit copied into the package, not a runtime dependency on another plugin.
- **Tool registration is an effect.** `apply()` returns a disposer, so stop or hot-reload unregisters cleanly.

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-rc.2`. `engines.dsh` is declared as `>=0.2.1-0 <0.3.0` and is enforced by the host since 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native` and `ptc`; for a whole directory use `ptc` so the schema cost is paid once |

## Troubleshooting

- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if your runtime sits outside it, grant an explicit exemption: `dsh plugin --profile <name> allow-version dsh-export-ctl-check@0.1.0 --dsh-version <runtime> --accept-risk`.
- **I believe an item is controlled but nothing is reported.** The plugin holds no control list; confirm against the published list yourself — see "Known limitations".
- **`EC-002` fires on an item I am sure is uncontrolled.** Its controlled column says it is controlled; correct the column or record the licence — the plugin reads the declaration, not the goods.
- **`EC-006` fires on one licence across several items.** Give the rows of that licence a serial number, or disable the rule.
- **`EC-005` does not know which destinations are restricted.** It checks only that a destination is recorded; the country list is deliberately not built in.
- **A rule did not run.** Read the `skipped` array; it names the rule id and the reason.
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer range that predates the 0.2 line; the runtime enforces peer compatibility at install time. This is a known upstream issue in `dsh-plugin-dev`.
- **The times look shifted.** All arithmetic is wall-clock string arithmetic on the provided values; no time-zone conversion is performed.

## Ecosystem & quality

- [Gitee mirror](https://gitee.com/perrylink/dsh-export-ctl-check) (sync mirror; GitHub is canonical)
- [dshfind plugin page](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check) (installs and ranking)
- [OpenSSF Scorecard report](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check) (driven by [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listed)
- [Choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) (the selection index for the 62 checkers and general plugins)

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

The plugin is data-only: `src/model.ts` declares the table shape, the shared kit in `src/shared/` supplies the reader and the check engine, and the rule pack declares every check. The last command copies the shared kit from `../_shared` into `src/shared/`; re-run it after every shared-kit change. README images are generated programmatically by [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow: a light/dark hero WebP pair and a light/dark structure SVG pair) and are safe to re-run.

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `export`, `ctl`

## Family & thanks

This project is part of the DeepSeek Harness plugin family from [PerryLink](https://github.com/PerryLink) (all Apache-2.0). If it is useful, **a star helps the next person find it** — nothing is gated behind it.

- [@PerryLink](https://github.com/PerryLink) — creator and maintainer: the rule pack, the check engine, the paired fixtures and the five-language docs.

<details>
<summary>Expand all plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 FROZEN — see the repo README |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 FROZEN — see the repo README |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** |  |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** |  |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRED (repo archived) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRED (repo archived) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** |  |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRED (repo archived) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 FROZEN — see the repo README |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 FROZEN — see the repo README |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 FROZEN — see the repo README |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 FROZEN — see the repo README |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 FROZEN — see the repo README |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRED (repo archived) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRED (repo archived) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRED (repo archived) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-export-ctl-check contributors

<p align="center"><sub>Apache-2.0 · Community plugin, not affiliated with DeepSeek.</sub></p>
