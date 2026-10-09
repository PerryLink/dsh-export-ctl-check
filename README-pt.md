# dsh-export-ctl-check — Registo de artigos sujeitos a controlo de exportação e verificação do fecho das licenças

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-export-ctl-check` lê um registo de artigos sujeitos a controlo de exportação —o cabeçalho do exportador mais uma linha por artigo— e verifica a completude e o fecho desse próprio registo, não um juízo sobre os artigos: se cada artigo indica na coluna 是否受控 se está sujeito a controlo, se um artigo marcado como controlado traz um 出口许可证号, se um número de licença registado vem acompanhado da data de emissão, se consta o uso final ou o utilizador final, se consta o destino final, se um número de licença se repete dentro do mesmo registo, se a categoria de controlo é um dos valores de 管制类别 da própria instituição, e se na coluna do nome do artigo sobrevive algum marcador como 【】, XXX, 待填, TBD ou 示例.

## Como é a saída

![Terminal demo of dsh-export-ctl-check: real output over its EC-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-export-ctl-check/main/docs/assets/dsh-export-ctl-check-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `EC-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Um artigo marcado como controlado sem número de licença é reportado? | `EC-002` reporta essa lacuna: numa linha cujo valor de 是否受控 seja um dos que a regra trata como controlado —de fábrica `是`, `Y`, `yes`, `true`, `受控`, `√`— exige um 出口许可证号. Verifica apenas que o número está preenchido; não julga se a licença é autêntica, se continua válida ou se abrange esse artigo e esse destino. Se o seu registo escreve outra palavra para «controlado», acrescente-a aos valores de condição da regra; caso contrário a linha conta como não controlada e a regra fica em silêncio — este plugin não contém qualquer lista de controlo que decida por você. |
| Um artigo indica se está controlado, mas deixa vazias as colunas 最终用途 e 最终用户. Isso é detetado? | `EC-004` reporta a linha: pede que pelo menos uma dessas duas colunas esteja preenchida. Basta uma, e a regra não julga se o uso ou o utilizador declarados são verdadeiros nem se o caso é um dos que a lei proíbe ou restringe. |
| Há número de licença, mas a coluna da data de emissão está vazia. É um achado? | `EC-003` exige-a. A condição é o número de licença: a uma linha sem número não se pede data nenhuma. A regra não verifica o período de validade da licença nem confronta a data de emissão com a de exportação: estabelece que a data existe, não que seja anterior. |
| O mesmo número de licença aparece em várias linhas. O que diz a verificação? | `EC-006` reporta o número como repetido dentro do registo. Não distingue uma licença que abrange vários artigos —forma normal de manter o registo— de um número copiado por engano, pelo que um resultado precisa de confirmação humana; a regra não renumera nada nem fixa quantas linhas podem partilhar uma licença. Se o seu registo é deliberadamente escrito como uma licença para vários artigos, numere as linhas dessa licença ou desative a regra. |
| Uma linha não tem 最终目的地. | `EC-005` reporta-a, porque todo o artigo tem de trazer destino. Verifica que a coluna está preenchida, não que o destino seja permitido: se um país ou região está embargado ou restringido lê-se nas listas que a autoridade competente publica, e este plugin não contém nenhuma lista de países. |
| A coluna do nome do artigo ainda diz `【示例】` ou `XXX`. É tratado como defeito ou como nome real? | `EC-008` reporta a linha quando o nome contém um dos termos que a regra procura: `【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo` ou `示例`. Essa lista de termos segue o seu próprio modelo e pode ser ajustada. A regra procura esses termos apenas nessa coluna: nunca julga se o nome está factualmente correto. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-export-ctl-check
dsh --profile <name> --dump-config | grep 'dsh-export-ctl-check'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-export-ctl-check contributors.
