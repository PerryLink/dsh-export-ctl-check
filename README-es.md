# dsh-export-ctl-check — Registro de artículos sujetos a control de exportación y verificación del cierre de licencias

`dsh-export-ctl-check` lee un registro de artículos sujetos a control de exportación —la cabecera del exportador más una fila por artículo— y verifica la completitud y el cierre de ese propio registro, no un juicio sobre los artículos: si cada artículo indica en la columna 是否受控 si está sujeto a control, si un artículo marcado como controlado lleva un 出口许可证号, si un número de licencia anotado va acompañado de su fecha de expedición, si consta el uso final o el usuario final, si consta el destino final, si un número de licencia se repite dentro del mismo registro, si la categoría de control es uno de los valores de 管制类别 de la propia institución, y si en la columna del nombre del artículo sobrevive algún marcador como 【】, XXX, 待填, TBD o 示例.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| ¿Se informa si un artículo marcado como controlado no tiene número de licencia? | `EC-002` informa de esa laguna: en una fila cuyo valor de 是否受控 sea uno de los que la regla trata como controlado —de fábrica `是`, `Y`, `yes`, `true`, `受控`, `√`— exige un 出口许可证号. Solo comprueba que el número esté anotado; no juzga si la licencia es auténtica, si sigue vigente o si cubre ese artículo y ese destino. Si su registro escribe otra palabra para «controlado», agréguela a los valores de condición de la regla; de lo contrario la fila cuenta como no controlada y la regla calla: este plugin no contiene lista de control alguna que decida por usted. |
| Un artículo indica si está controlado, pero deja vacías las columnas 最终用途 y 最终用户. ¿Se detecta? | `EC-004` informa de la fila: pide que al menos una de esas dos columnas esté completa. Con una basta, y la regla no juzga si el uso o el usuario declarados son ciertos ni si el caso es uno de los que la ley prohíbe o restringe. |
| Hay número de licencia, pero la columna de la fecha de expedición está vacía. ¿Es un hallazgo? | `EC-003` la exige. La condición es el número de licencia: a una fila sin número no se le pide fecha alguna. La regla no comprueba el período de validez de la licencia ni contrasta la fecha de expedición con la de exportación: establece que la fecha está, no que sea anterior. |
| Un mismo número de licencia aparece en varias filas. ¿Qué dice la comprobación? | `EC-006` informa del número como repetido dentro del registro. No distingue una licencia que cubre varios artículos —forma normal de llevar el registro— de un número copiado por error, así que un hallazgo necesita confirmación humana; la regla no renumera nada ni fija cuántas filas pueden compartir una licencia. Si su registro se lleva deliberadamente a razón de una licencia por varios artículos, numere las filas de esa licencia o desactive la regla. |
| Una fila no tiene 最终目的地. | `EC-005` la informa, porque todo artículo debe llevar destino. Comprueba que la columna esté completa, no que el destino esté permitido: si un país o región está embargado o restringido se lee en las listas que publica la autoridad competente, y este plugin no contiene ninguna lista de países. |
| La columna del nombre del artículo todavía dice `【示例】` o `XXX`. ¿Se trata como defecto o como nombre real? | `EC-008` informa de la fila cuando el nombre contiene uno de los términos que la regla busca: `【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo` o `示例`. Esa lista de términos sigue su propia plantilla y puede ajustarse. La regla busca esos términos solo en esa columna: nunca juzga si el nombre es fácticamente correcto. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-export-ctl-check contributors.
