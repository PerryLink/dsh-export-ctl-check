<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-export-ctl-check-hero-en-light.webp" width="100%" alt="dsh-export-ctl-check: la columna izquierda lleva el nombre del plugin, dos líneas de valor y la nota de que 8 reglas cierran el bucle del registro y no se mantiene ninguna lista de control; a la derecha está el marcador de un artículo — ocho celdas, una por regla, cada una con su id, el campo que lee y el valor observado (controlled vacío → acierto; licenseNo con la condición sin cumplir → omitida; licenseAt rellena → pasa; endUse/endUser rellenos → pasa; destination rellena → pasa; licenseNo sin duplicados → pasa; category civil-military con valores sin configurar → omitida; itemName limpio → pasa), con el único hallazgo warn de EC-001 y las dos omisiones EC-002 y EC-007 debajo">
</picture>

# dsh-export-ctl-check

**Revisa un registro de artículos sujetos a control de exportación línea por línea — qué fila, qué columna, qué falta. Solo diferencias, sin veredicto.**

Un verificador sin conexión para equipos de cumplimiento aduanero y control de exportaciones: lee un registro de artículos (cabecera del exportador más una fila por artículo) y comprueba la completitud y el cierre de ese propio registro con un paquete de reglas versionado. Sin red, sin llamadas al modelo y sin modificar el material original.

[Instalación](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-export-ctl-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

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

<sub>Plugin comunitario, sin relación con DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-export-ctl-check> (Gitee es un espejo).</sub>

## Qué es

`dsh-export-ctl-check` lee un registro de artículos sujetos a control de exportación —la cabecera del exportador más una fila por artículo— y comprueba la completitud y el cierre de ese propio registro, no un juicio sobre los artículos: si cada artículo indica en la columna de control si está sujeto a control, si un artículo marcado como controlado lleva un número de licencia de exportación, si un número de licencia anotado va acompañado de su fecha de expedición, si consta el uso final o el usuario final, si consta el destino final, si un número de licencia se repite dentro del mismo registro, si la categoría de control es uno de los valores de la propia institución, y si en la columna del nombre del artículo sobrevive algún marcador de plantilla.

Solo enumera las diferencias que pueden señalarse dentro del material y, para cada una, da la fila, la columna, lo que falta y lo que hay que completar; no decide si un artículo está sujeto a control, si necesita licencia ni si una exportación cumple la normativa. Basta con entregarle el material en el chat: la instalación es un solo comando y los hallazgos se leen directamente. 33 pruebas (`npx vitest run`) cubren los pares de fixtures de las 8 reglas, y `samples/quickstart` ejecuta una verificación real sin conexión.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-export-ctl-check-flow-v5-light.svg" width="100%" alt="dsh-export-ctl-check, estructura: a la izquierda dos entradas — el registro (JSON/YAML: cuatro campos de cabecera opcionales, rows[], 13 columnas canónicas con alias, requireAnyOf) y el paquete de reglas (8 reglas, 6 tipos de comprobación, validado al cargar) — más el límite que no cruza (no mantiene lista de control); en el centro ocho puertas en una escalera, las tres primeras forman la cadena condicional controlled → licenseNo → licenseAt y cada puerta sale por una sola salida; a la derecha las dos salidas y un informe — issues[] (un warn: controlled vacío en la fila 1, con expected, fix y el locator fila/columna) y skipped[] (EC-002 y EC-007 con su motivo) — que dan error 0 / warn 1 / info 0, issues 1, markdown y reportJson">
</picture>

## Instalación en tres pasos

1. **Instalar** (elige un canal):

   ```sh
   # canal git (última main)
   dsh plugin --profile web add github:PerryLink/dsh-export-ctl-check
   # canal npm (versiones publicadas)
   dsh plugin --profile web add dsh-export-ctl-check
   # canal tarball: tras pnpm pack en este repositorio
   dsh plugin --profile web add ./dsh-export-ctl-check-<version>.tgz
   ```

   Sin dependencias de ejecución; `lib/index.mjs` y `rules/` son los artefactos publicados.

2. **Configuración mínima** (los valores por defecto ya sirven; el paquete de reglas viaja con el paquete):

   ```yaml
   - insert:
       - id: dsh-export-ctl-check
         name: dsh-export-ctl-check
   ```

3. **Comprobar que se ha montado**:

   ```sh
   dsh --profile web --dump-config | grep 'dsh-export-ctl-check'
   node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   export_ctl_check: 1 issue(s) — error 0, warn 1, info 0
   skipped: 2
   ```

**Desinstalar**: `dsh plugin --profile web remove dsh-export-ctl-check` (o borre la fila del patch del perfil).

> El plugin no hace peticiones de red y no escribe archivos de material; toda la verificación ocurre en local. El ejemplo está en `samples/quickstart/input/` y la salida esperada en `samples/quickstart/expected/result.json`. También puede buscar el paquete de cumplimiento aduanero en WorkBuddy / Coze (esta verificación es una de sus partes; la disponibilidad es la que figure en esa tienda).

## Capacidades principales

`export_ctl_check` tiene una sola superficie de herramienta: leer el material, ejecutar el paquete de reglas y devolver un informe. Capacidades, según lo que se obtiene:

- **Ocho reglas de una pasada** — `EC-001` a `EC-008` cubren la declaración de control, el número de licencia, la fecha de expedición, el uso final y el usuario final, el destino, los números de licencia repetidos, la categoría de control y el marcador en el nombre del artículo. Cada regla comprueba que algo esté relleno, no que sea correcto.
- **Localizado por fila y columna** — cada hallazgo lleva `locator` (`row` + `field`), `found`, `expected` y `fix`, de modo que se puede volver directamente a esa celda del registro.
- **Las omisiones deben explicarse** — las comprobaciones que no pueden ejecutarse van a `skipped` con su motivo; una lista de problemas vacía no equivale a un aprobado, y una regla sin configurar o una columna ausente nunca se leen como éxito en silencio.
- **Las reglas son datos** — el paquete de reglas `rules/export-ctl-check.yaml` está separado del código; sustituir el archivo cambia la versión del conjunto de reglas sin tocar TypeScript. El cargador valida `document` / `number` / `clause` / `excerpt` / `kind` / `source` en cada regla.
- **Sin citas inventadas** — el extracto debe ser una cita literal; cuando la base es solo un principio, `kind` es `derived-from-principle` y la gravedad queda limitada a `warn`; un umbral institucional queda limitado a `info`.
- **Totalmente sin conexión** — sin peticiones de red, sin llamadas al modelo y sin escribir en el registro; la herramienta devuelve un informe de texto (`markdown`) y un informe estructurado (`reportJson`).

### Tabla de reglas

| Regla | Qué comprueba | Gravedad | Tipo de base |
|---|---|---|---|
| `EC-001` | cada artículo indica si está sujeto a control | `warn` | derivada de principio |
| `EC-002` | un artículo controlado lleva número de licencia | `warn` | directa |
| `EC-003` | una licencia anotada lleva fecha de expedición | `warn` | derivada de principio |
| `EC-004` | consta el uso final o el usuario final | `warn` | directa |
| `EC-005` | consta un destino | `warn` | directa |
| `EC-006` | los números de licencia no se repiten en el registro | `warn` | derivada de principio |
| `EC-007` | la categoría de control sale de su vocabulario | `info` | derivada de principio |
| `EC-008` | el nombre del artículo no conserva marcadores sin sustituir | `warn` | directa |

### Ejemplos

Esta es la salida real del plugin sobre su propio fixture `EC-001`, no una ilustración.

**Herramienta** `export_ctl_check`

**Entrada**

~~~json
{"rows":[{"物项名称":"某型高性能传感器","是否受控":""}]}
~~~

**Salida**

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

*Obtenido de `tests/fixtures/EC-001/EC-001-unsafe.json (cases.json expects EC-001 count 1); run via lib/index.mjs rules/export-ctl-check.yaml`*

### Lo que usted pregunta, lo que responde

| Usted pregunta | Qué responde |
|---|---|
| Un artículo está marcado como controlado pero no tiene número de licencia. ¿Se informa? | Sí, `EC-002` informa de esa laguna: cuando el valor de control de una fila es uno de los que la regla trata como controlado, exige un número de licencia de exportación. La regla solo comprueba que el número esté anotado; no juzga si la licencia es auténtica, si sigue vigente o si cubre ese artículo y ese destino. Si su registro escribe otra palabra para «controlado», agréguela a los valores de condición de la regla; de lo contrario la fila cuenta como no controlada y la regla calla: este plugin no contiene lista de control alguna que decida por usted. |
| Un artículo indica si está controlado, pero deja vacíos el uso final y el usuario final. ¿Se detecta? | Sí, `EC-004` informa de la fila: pide que al menos una de esas dos columnas esté completa. Con una basta, y la regla no juzga si el uso o el usuario declarados son ciertos ni si el caso es uno de los que la ley prohíbe o restringe. |
| Hay número de licencia, pero la columna de la fecha de expedición está vacía. ¿Es un hallazgo? | `EC-003` la exige. La condición es el número de licencia: a una fila sin número no se le pide fecha alguna. La regla no comprueba el período de validez de la licencia ni contrasta la fecha de expedición con la de exportación: establece que la fecha está, no que sea anterior. |
| Un mismo número de licencia aparece en varias filas. ¿Qué dice la comprobación? | `EC-006` informa del número como repetido dentro del registro. No distingue una licencia que cubre varios artículos —forma normal de llevar el registro— de un número copiado por error, así que un hallazgo necesita confirmación humana; la regla no renumera nada ni fija cuántas filas pueden compartir una licencia. Si su registro se lleva deliberadamente a razón de una licencia por varios artículos, numere las filas de esa licencia o desactive la regla. |
| Una fila no tiene destino final. | `EC-005` la informa, porque todo artículo debe llevar destino. Comprueba que la columna esté completa, no que el destino esté permitido: si un país o región está embargado o restringido se lee en las listas que publica la autoridad competente, y este plugin no contiene ninguna lista de países. |
| La columna del nombre del artículo todavía dice un valor de ejemplo entre corchetes o `XXX`. ¿Es un defecto o un nombre real? | `EC-008` informa de la fila cuando el nombre contiene uno de los términos que la regla busca: marcadores entre corchetes, `XXX`, `xxx`, `TBD`, `todo` o una marca de «rellenar». Esa lista de términos sigue su propia plantilla y puede ajustarse. La regla busca esos términos solo en esa columna: nunca juzga si el nombre es fácticamente correcto. |

## Configuración

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

<details>
<summary>Parámetros por regla (en el paquete de reglas, no aquí)</summary>

- `EC-002` `conditionValues` — qué valores de la columna de control marcan un artículo como controlado. Los valores de fábrica son:

```text
是 · Y · yes · true · 受控 · √
```

  Si su registro usa otra forma, añádala a esta lista; de lo contrario la fila cuenta como no controlada y la regla calla.
- `EC-007` `values` — las categorías de control de su institución, por ejemplo `[nuclear, misiles, biológico, químico, doble uso]`. Vacío significa «sin configurar» y la regla se declara en `skipped`; el plugin no codifica ninguna taxonomía.
- `EC-008` `terms` — los términos de plantilla que se buscan. Los de fábrica son:

```text
【 】 {{ }} XXX xxx 待填 待补充 TBD todo 示例
```

</details>

Ejemplo de sobrescritura en el patch del perfil:

```yaml
- insert:
    - id: dsh-export-ctl-check
      name: dsh-export-ctl-check
      config:
        onlyRules: [EC-001, EC-002, EC-003]
        skipNotes: normas internas, edición 2026
```

## Formato del material

La herramienta acepta JSON o YAML. La entrada es `file` (ruta absoluta al material) o `material` (texto en línea): exactamente una de las dos. Excel puede convertirse antes a JSON/YAML, también en el chat si la plataforma lo permite.

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

Los nombres de columna se comparan sin distinguir mayúsculas y sin contar espacios, guiones bajos ni guiones; se conservan los nombres propios del registro, de modo que cada hallazgo nombra la columna que leyó. Los campos son opcionales en la capa de lectura y los valida el motor, así que una exportación parcial produce hallazgos de «falta» en lugar de un fallo.

## Normas que sigue

| Documento | Número | Reglas que lo citan |
|---|---|---|
| Ley de Control de Exportaciones de la República Popular China | Aprobada el 17 de octubre de 2020 en la 22.ª sesión del Comité Permanente de la XIII Asamblea Popular Nacional, promulgada por la Orden Presidencial n.º 58, en vigor desde el 1 de diciembre de 2020 | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| Ley de Control de Exportaciones de la República Popular China | Versión vigente no verificada en esta pasada | EC-007 |

**Límite:** este plugin comprueba un **registro de artículos sujetos a control de exportación** en el bucle cerrado que un registro puede exigirse — que cada artículo indique si está controlado, que un artículo controlado lleve número de licencia, que una licencia lleve fecha de expedición, que conste el uso final o el usuario final, que conste un destino, que los números de licencia no se repitan, que la categoría de control salga de su vocabulario y que no sobreviva ningún marcador. **No** decide si un artículo está controlado, si se necesita licencia ni si una exportación infringiría la normativa.

### Paquete de reglas

Los datos de las reglas están en `rules/export-ctl-check.yaml`. Su cabecera explica que el plugin no contiene lista de control ni hace búsquedas en listas, por lo que no puede detectar un artículo controlado no declarado. El cargador sigue exigiendo documento, cláusula, extracto y fuente por regla, y sigue prohibiendo que una comprobación derivada de principio o configurada localmente sea `error`.

> ### ⚠️ Lea esto antes de fiarse de una cita del informe
>
> **El estado de `excerpt` es por regla, no uniforme.** Algunas reglas citan la cláusula literalmente (`kind: direct`), otras se derivan del principio de los artículos citados (`kind: derived-from-principle`, tope `warn`) y otras usan umbrales que configura su institución (`kind: institutional-configuration`, tope `info`). El paquete nunca parafrasea una cita: cuando el texto no se obtuvo, el campo `excerpt` lo dice y el razonamiento vive en `note`; una prueba asegura que ninguna regla afirma una cita que no tiene. **Para toda regla aún marcada como no obtenida, sustituya el `excerpt` por la cláusula real y eleve `kind` a `direct` cuando tenga el texto.**
>
> La conclusión es del revisor: este plugin enumera diferencias que puede señalar en el material y no decide hechos ni cumplimiento.

## FAQ

<details>
<summary>¿Se sube el material o se procesa por la red?</summary>

No. El plugin solo lee lo que usted le entrega mediante `file` o `material`, lo analiza en local y ejecuta las reglas en local: sin peticiones de red, sin telemetría, sin llamadas al modelo. El resultado solo existe en el valor de retorno de la herramienta y en el registro de sesión del propio host DSH; el paquete no guarda una segunda copia.

</details>

<details>
<summary>Creo que un artículo debería estar controlado y no se informó. ¿Es un fallo?</summary>

Es el límite más importante del plugin, no un fallo: no contiene lista de control ni asigna un código de mercancía o un parámetro técnico a una entrada de lista, así que no puede encontrar un artículo que debería haberse declarado controlado y no se declaró. Determinar si un artículo está controlado corresponde al exportador frente a la lista publicada. Lo que el plugin sí garantiza es que las comprobaciones que no puede ejecutar van a `skipped` y no pasan en silencio.

</details>

<details>
<summary>¿Compite con otros plugins por nombres de comando, eventos o slots?</summary>

No. Declara solo la dependencia `tools` y registra una única herramienta `export_ctl_check`; no registra comandos, ni slots de cliente, ni prefijos `webServer`, no ofrece service keys y no modifica objetos globales. El argumento punto por punto está en «Interoperabilidad».

</details>

<details>
<summary>¿Cuánto cuesta en rendimiento?</summary>

Análisis local más coincidencia de reglas: sin red y sin llamadas al modelo. El presupuesto de tiempo de espera por defecto es `120000` ms. 33 pruebas (`npx vitest run`) cubren los pares de fixtures de las 8 reglas, y `samples/quickstart` puede repetirse sin conexión.

</details>

<details>
<summary>¿Se puede sustituir el paquete de reglas?</summary>

Sí. `rulesFile` puede apuntar a cualquier archivo de reglas (relativo a la raíz del paquete o absoluto); las reglas son datos y el cargador valida los campos de cita y los topes de gravedad. Sustituir el archivo cambia la versión del conjunto de reglas sin tocar TypeScript.

</details>

## Límites de seguridad

- **Material de solo lectura.** El plugin lee mediante `file` o `material`, nunca escribe de vuelta ni modifica el original; la única escritura es el registro de sesión que guarda el host DSH, y el paquete no añade una segunda copia.
- **Sin red y sin llamadas al modelo.** Sin peticiones de red, sin telemetría y sin llamadas al modelo; toda la verificación ocurre en local.
- **Sin lenguaje que adjudique.** El informe enumera diferencias literales entre el material y las cláusulas citadas; no juzga cumplimiento, responsabilidad ni verdad de los hechos. La conclusión es del revisor.
- **El fallo no es silencioso.** El paquete de reglas se valida al cargar; las comprobaciones que no pueden ejecutarse van a `skipped` con su motivo, y una lista de problemas vacía nunca se lee como «no hay nada mal».
- **Sin citas inventadas.** El extracto debe ser una cita literal; cuando el texto no puede obtenerse, el paquete lo dice y limita la gravedad.
- **El registro es un effect.** El registro de la herramienta devuelve un disposer, así que detener o recargar en caliente la desregistra y no deja escuchas colgadas.

## Limitaciones conocidas

- **No hay lista de control dentro.** La columna de control es la declaración del propio registro; el plugin solo comprueba el cierre posterior a esa declaración y no puede encontrar un artículo controlado no declarado. Es el límite de capacidad más importante del plugin.
- **No juzga la licencia en sí.** `EC-002` y `EC-003` comprueban que el número y la fecha de expedición estén rellenos; no verifican autenticidad, período de validez ni cobertura de ese artículo y ese destino, y no comparan la fecha de expedición con la de exportación.
- **No juzga la veracidad del uso final ni del usuario final.** `EC-004` solo exige que al menos una de las dos columnas esté rellena; no juzga si lo declarado es cierto o si está prohibido.
- **No juzga si un destino está restringido.** `EC-005` solo comprueba que la columna de destino esté rellena; no hay lista de países ni regiones incorporada.
- **Un número de licencia repetido es una pista, no una conclusión.** Una licencia que cubre varios artículos es una forma normal de llevar el registro, así que un hallazgo de `EC-006` necesita confirmación humana; el plugin no renumera ni fija cuántas filas puede cubrir una licencia.
- **`EC-007` necesita su vocabulario.** `values` viene vacío, así que la regla se declara en `skipped` hasta configurarse; cómo se dividen las categorías de control depende de la versión de la lista y el plugin no codifica ninguna taxonomía.
- **El estado de las citas es por regla.** Algunas reglas aún marcan su `excerpt` como no obtenido, mantienen `kind: derived-from-principle` y quedan topadas en `warn`; cuando tenga el texto, sustituya el extracto y eleve el tipo a `direct`.
- **El conjunto completo sigue siendo de 8 reglas.** Cubre la completitud y el cierre a nivel de registro, no una revisión sustantiva del artículo, la licencia o la operación.

## Interoperabilidad

El plugin registra una herramienta y no ocupa la superficie de otros plugins:

- **Solo la dependencia `tools`.** `inject = ['tools']`; sin servicio de herramientas no registra nada.
- **Solo `export_ctl_check`.** Sin comandos, sin slots de cliente y sin prefijo `webServer`, por lo que no compite por esos puestos.
- **Sin service keys y sin mutación global.** No parchea prototipos, no escribe `process.env` y no sustituye el fetch global.
- **El patch del bundle solo inserta su propia fila.** `cordis.patch.yml` añade la fila del plugin y nunca sobrescribe el `config` de una fila integrada.
- **El kit compartido se copia dentro.** `src/shared/` es un kit compartido copiado en el paquete, no una dependencia de ejecución de otro plugin.
- **El registro de la herramienta es un effect.** `apply()` devuelve un disposer, así que detener o recargar en caliente desregistra limpiamente.

## Compatibilidad

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` se declara como `>=0.2.1-0 <0.3.0` y el host lo aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native` y `ptc`; para un directorio completo use `ptc` y pague el coste de esquema una sola vez |

## Solución de problemas

- **El plugin se instala pero la herramienta no aparece.** Compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` incorrecto hace que el cargador omita la entrada en silencio.
- **`dsh plugin add` rechaza el paquete por incompatibilidad.** El rango de peers cubre `0.1.x` y `0.2.x`; si su runtime queda fuera, conceda una exención explícita: `dsh plugin --profile <name> allow-version dsh-export-ctl-check@0.1.0 --dsh-version <runtime> --accept-risk`.
- **Creo que un artículo está controlado y no se informa.** El plugin no contiene lista de control; confírmelo usted frente a la lista publicada — véase «Limitaciones conocidas».
- **`EC-002` salta en un artículo que sé que no está controlado.** Su columna de control dice que sí lo está; corrija la columna o anote la licencia — el plugin lee la declaración, no la mercancía.
- **`EC-006` salta con una licencia en varios artículos.** Numere las filas de esa licencia o desactive la regla.
- **`EC-005` no sabe qué destinos están restringidos.** Solo comprueba que conste un destino; la lista de países no se incorpora a propósito.
- **Una regla no se ejecutó.** Lea el arreglo `skipped`; indica el id de la regla y el motivo.
- **`check` informa `manifest-peers` como fallo.** El verificador estático compara con un rango de peers codificado que es anterior a la línea 0.2; el runtime aplica la compatibilidad al instalar. Es un problema conocido de `dsh-plugin-dev`.
- **Las horas parecen desplazadas.** Toda la aritmética es de hora de pared sobre las cadenas entregadas; no se hace conversión de zona horaria.

## Ecosistema y calidad

- [Espejo en Gitee](https://gitee.com/perrylink/dsh-export-ctl-check) (espejo sincronizado; GitHub es el canónico)
- [Página en dshfind](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check) (instalaciones y ranking)
- [Informe OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (publicado)
- [Elegir un verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice de selección de los 62 verificadores y plugins generales)

## Desarrollo

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, la suite compartida de tablas más fixtures emparejados
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

El plugin es de datos: `src/model.ts` declara la forma de la tabla, el kit compartido de `src/shared/` aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación. El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio del kit compartido. Las imágenes del README se generan mediante [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow: par de WebP hero claro/oscuro y par de SVG de estructura claro/oscuro) y se pueden volver a ejecutar.

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `export`, `ctl`

## Familia y agradecimientos

Este proyecto forma parte de la familia de plugins de DeepSeek Harness de [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Si le resulta útil, **una estrella ayuda a que la siguiente persona lo encuentre** — nada queda bloqueado por ello.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: el paquete de reglas, el motor de comprobación, los fixtures emparejados y la documentación en cinco idiomas.

<details>
<summary>Expandir todos los plugins</summary>

| Plugin | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRADO (repo archivado) |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRADO (repo archivado) |

</details>

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-export-ctl-check contributors

<p align="center"><sub>Apache-2.0 · Plugin comunitario, sin relación con DeepSeek.</sub></p>
