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
pnpm pack
dsh plugin --profile <name> add ./*.tgz
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`. Las claves y los parámetros de cada regla están en [README.md](README.md#configuration) (versión principal en inglés).

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
