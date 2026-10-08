# dsh-export-ctl-check — 出口管制物项台账与许可证闭环核对

`dsh-export-ctl-check` 读取一份出口管制物项台账——出口经营者表头加每条物项一行——核对这份台账自身的齐备与闭环，而不对物项本身作出判断：每条物项是否在「是否受控」栏写明是否受控、标为受控的物项是否填写了出口许可证号、填了许可证号的是否写明了发证日期、最终用途或最终用户是否至少填写了一项、最终目的地是否填写、许可证号是否在同一份台账内重复、管制类别是否取用本机构自己的管制类别取值、物项名称栏是否残留【】、XXX、待填、TBD、示例之类未替换的占位符。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 物项标为受控却没填许可证号，会被报出吗？ | 会，`EC-002` 报出这个缺口：某一行的「是否受控」取值属于本条配置为受控的那些值（出厂为 `是`、`Y`、`yes`、`true`、`受控`、`√`）时，它就要求填写出口许可证号。本条只核对证号栏是否填写，不判断该许可证是否真实、是否仍在有效期内、是否覆盖该物项与该目的地。台账若用别的写法表示受控，请把该写法加入本条的判定取值，否则该行会被当作非受控而不报——本插件不持有管制清单，无从替你判断。 |
| 物项已标明是否受控，但最终用途与最终用户两栏都空着，会被发现吗？ | 会，`EC-004` 报出该行：它要求这两栏至少填写一项。填了一项即算通过，本条也不判断所填用途与用户是否真实、是否属于法律禁止或限制的情形。 |
| 许可证号填了，发证日期栏却空着，算问题吗？ | `EC-003` 要求填写。条件是许可证号本身：没有证号的行不会被要求填日期。本条不核对许可证的有效期，也不拿发证日期与出口日期作比较——它只确认日期填了，不判断日期是否在前。 |
| 同一个许可证号出现在好几行上，会怎么说？ | `EC-006` 按重复报出该证号。它分不清「一份许可证覆盖多个物项」（台账常见写法）与「抄错了号」，所以命中需要人工确认；本条不会替你改号，也不给出同一个许可证号最多能出现在几行。若本机构台账本就是「一证多物项」，请为同一许可证的各行加上序号区分，或停用本条。 |
| 某行的最终目的地栏是空的。 | `EC-005` 报出该行，因为每条物项都要填写目的地。它只核对这一栏是否填写，不判断该目的地是否被允许：某国家或地区是否属于禁运或受限制，要看主管部门公布的名单，本插件不内置任何国家名单。 |
| 物项名称栏还写着 `【示例】` 或 `XXX`，算缺陷还是算真实名称？ | 名称里出现本条要找的词时，`EC-008` 报出该行——这些词是 `【`、`】`、`{{`、`}}`、`XXX`、`xxx`、`待填`、`待补充`、`TBD`、`todo`、`示例`。这份词表跟随本机构自己的模板，可以调整。本条只看这一栏里有没有这些词，不判断名称本身填得对不对。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《中华人民共和国出口管制法》 | 2020 年 10 月 17 日第十三届全国人大常委会第二十二次会议通过，主席令第五十八号公布，自 2020 年 12 月 1 日起施行 | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| 《中华人民共和国出口管制法》 | 现行版本本次未核实 | EC-007 |

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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-export-ctl-check contributors.
