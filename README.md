# dsh-export-ctl-check

**Boundary:** this plugin checks an **出口管制物项台账** for the closed loop a register can be held to — that
each item states whether it is controlled, that a controlled item carries a licence number, that a licence
carries an issue date, that the end use or end user is recorded, that a destination is recorded, that licence
numbers do not repeat, that the control category comes from your vocabulary, and that no placeholder survives.
It does **not** decide whether an item is controlled, whether a licence is required, or whether an export would
breach the rules.

> ### ⚠️ What this plugin deliberately cannot do
>
> **It does not contain the control list, and it does not try to map a commodity code or a technical parameter
> onto a list entry.** Because of that it **cannot find the most serious defect of all: an item that should
> have been declared controlled and was not.** Whether an item is controlled is the exporter's own
> determination under the law, and confirming it means checking the published list. This limit is stated in
> the pack's header, in each rule's note, and in the troubleshooting section below — it is the single most
> important thing to know about this plugin.
>
> The 是否受控 column is therefore the register's own declaration. Everything here checks what happens *after*
> that declaration: is a licence recorded, is it dated, is the destination and end use stated, does the
> register hold together. **It never checks whether the declaration was right.**
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The
> regime lives in 《中华人民共和国出口管制法》, the dual-use export licensing measures, and the published
> control list. The verification pass could not retrieve verbatim clause text, so the pack states the gap in
> the `excerpt` field itself and keeps every rule at `warn` or `info`. **When the texts are in hand, replace
> each `excerpt` with the real clause and raise `kind` to `direct`.**

## Compatibility

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a shipment's item list use `ptc` |

## What it does

Registers the `export_ctl_check` tool. It reads one item register — the exporter header plus one row per item —
applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `EC-001` | each item states whether it is controlled | warn | principle |
| `EC-002` | a controlled item carries a licence number | warn | principle |
| `EC-003` | a recorded licence carries an issue date | warn | principle |
| `EC-004` | the end use or end user is recorded | warn | principle |
| `EC-005` | a destination is recorded | warn | principle |
| `EC-006` | licence numbers do not repeat | warn | principle |
| `EC-007` | the control category comes from your vocabulary (off by default) | info | local |
| `EC-008` | the item name holds no unreplaced placeholder | warn | principle |

## Install

```sh
pnpm pack
dsh plugin --profile <name> add ./dsh-export-ctl-check-0.1.0.tgz
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `EC-002` `conditionValues` — the values in your 是否受控 column that mark an item as controlled, by default
  `[是, Y, yes, true, 受控, √]`.
- `EC-007` `values` — your control categories, e.g. `[核, 导弹, 生物, 化学, 军民两用]`. Empty means no check;
  the plugin ships no list of its own.
- `EC-008` `terms` — the placeholders to look for.

## Material format

The tool accepts JSON or YAML:

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

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own
column names are kept, so a finding names the column it read.

## Rule sources

Rule data lives in `rules/export-ctl-check.yaml`. Its header explains that the plugin holds no control list and
does no list lookup, so it cannot detect an undeclared controlled item. The load-time guard still requires a
document, clause, excerpt and source per rule, and still forbids a principle-derived or locally configured
check from being `error`.

## Troubleshooting

- **It did not flag an item I believe is controlled.** By design: it has no control list and never maps an
  item to one. Confirm against the published list yourself; this plugin cannot do it for you.
- **`EC-002` fires on an item I am sure is uncontrolled.** Its 是否受控 column says it is controlled. Either
  correct the column or record the licence — the plugin reads the declaration, not the goods.
- **`EC-006` fires on one licence across several items.** A single licence covering several items is normal;
  distinguish the rows, or disable the rule if your register is written that way.
- **`EC-005` does not know which destinations are restricted.** It checks only that a destination is recorded.
  No country list is built in, deliberately.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-export-ctl-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-export-ctl-check   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-export-ctl-check contributors.
