/**
 * dsh-export-ctl-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'export_ctl_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  itemNo: ['序号', '项号', '编号', 'itemNo'],
  itemName: ['物项名称', '货物名称', '技术名称', 'itemName'],
  hsCode: ['商品编号', 'HS编码', '海关商品编号', 'hsCode'],
  controlCode: ['管制编码', '管制清单编码', 'ECCN', 'controlCode'],
  controlList: ['管制清单', '适用清单', '清单名称', 'controlList'],
  category: ['管制类别', '类别', '管控类型', 'category'],
  endUse: ['最终用途', '用途', '最终用户用途', 'endUse'],
  endUser: ['最终用户', '收货人', '进口商', 'endUser'],
  destination: ['最终目的地', '目的国', '运抵国', 'destination'],
  licenseNo: ['许可证号', '出口许可证编号', '许可文件号', 'licenseNo'],
  licenseAt: ['许可日期', '发证日期', 'licenseAt'],
  controlled: ['是否受控', '受控', '是否管制', 'controlled'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'controls', '管制项'],
  columns: COLUMNS,
  header: {
  exporter: ['exporter', '出口经营者', '出口商'],
  contractNo: ['contractNo', '合同号', '合同编号'],
  checkedAt: ['checkedAt', '核对日期'],
  listVersion: ['listVersion', '清单版本', '管制清单版本'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '物项名称',
  'itemName',
  '管制编码',
  'controlCode',
  '是否受控',
  'controlled',
  '最终用途',
  'endUse',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
