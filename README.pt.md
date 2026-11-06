<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-export-ctl-check-hero-en-light.webp" width="100%" alt="dsh-export-ctl-check: a coluna esquerda traz o nome do plugin, duas linhas de valor e a nota de que 8 regras fecham o ciclo do registo e nenhuma lista de controlo é mantida; à direita está o marcador de um item — oito células, uma por regra, cada uma com o seu id, o campo que lê e o valor observado (controlled vazio → acerto; licenseNo com a condição não cumprida → ignorada; licenseAt preenchida → passa; endUse/endUser preenchidos → passa; destination preenchida → passa; licenseNo sem duplicados → passa; category civil-military com valores por configurar → ignorada; itemName limpo → passa), com o único achado warn de EC-001 e as duas omissões EC-002 e EC-007 por baixo">
</picture>

# dsh-export-ctl-check

**Confere um registro de itens sujeitos a controle de exportação linha a linha — qual linha, qual coluna, o que falta. Só diferenças, sem veredito.**

Um verificador offline para equipes de conformidade aduaneira e controle de exportações: lê um registro de itens (cabeçalho do exportador mais uma linha por item) e confere a completude e o fechamento desse próprio registro com um pacote de regras versionado. Sem rede, sem chamada ao modelo e sem alterar o material original.

[Instalação](#instalação-em-três-passos) · [Configuração](#configuração) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidade)
[![npm](https://img.shields.io/npm/v/dsh-export-ctl-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-export-ctl-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-export-ctl-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-export-ctl-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidade)

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

<sub>Plugin da comunidade, sem vínculo com a DeepSeek. Repositório canônico: <https://github.com/PerryLink/dsh-export-ctl-check> (o Gitee é um espelho).</sub>

## O que é

`dsh-export-ctl-check` lê um registro de itens sujeitos a controle de exportação — o cabeçalho do exportador mais uma linha por item — e confere a completude e o fechamento desse próprio registro, não um julgamento sobre os itens: se cada item declara na coluna de controle se está sujeito a controle, se um item marcado como controlado traz um número de licença de exportação, se um número de licença registrado vem acompanhado da data de emissão, se consta o uso final ou o usuário final, se consta o destino final, se um número de licença se repete dentro do mesmo registro, se a categoria de controle vem do vocabulário da própria instituição e se na coluna do nome do item sobrevive algum marcador de modelo.

Ele lista apenas as diferenças que podem ser apontadas dentro do material e, para cada uma, informa a linha, a coluna, o que falta e o que preencher; não decide se um item está sujeito a controle, se precisa de licença nem se uma exportação cumpre a norma. Basta entregar o material no chat: a instalação é um único comando e os achados são para ler diretamente. 33 testes (`npx vitest run`) cobrem os pares de fixtures das 8 regras, e `samples/quickstart` executa uma verificação real offline.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-export-ctl-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-export-ctl-check-flow-v5-light.svg" width="100%" alt="dsh-export-ctl-check, estrutura: à esquerda duas entradas — o registo (JSON/YAML: quatro campos de cabeçalho opcionais, rows[], 13 colunas canónicas com alias, requireAnyOf) e o pacote de regras (8 regras, 6 tipos de verificação, validado ao carregar) — mais o limite que não cruza (não mantém lista de controlo); ao centro oito portas numa escada, as três primeiras formam a cadeia condicional controlled → licenseNo → licenseAt e cada porta sai por uma única saída; à direita as duas saídas e um relatório — issues[] (um warn: controlled vazio na linha 1, com expected, fix e o locator linha/coluna) e skipped[] (EC-002 e EC-007 com o seu motivo) — que dão error 0 / warn 1 / info 0, issues 1, markdown e reportJson">
</picture>

## Instalação em três passos

1. **Instalar** (escolha um canal):

   ```sh
   # canal git (main mais recente)
   dsh plugin --profile web add github:PerryLink/dsh-export-ctl-check
   # canal npm (versões publicadas)
   dsh plugin --profile web add dsh-export-ctl-check
   # canal tarball: após pnpm pack neste repositório
   dsh plugin --profile web add ./dsh-export-ctl-check-<version>.tgz
   ```

   Sem dependências de execução; `lib/index.mjs` e `rules/` são os artefatos publicados.

2. **Configuração mínima** (os padrões já funcionam; o pacote de regras viaja com o pacote):

   ```yaml
   - insert:
       - id: dsh-export-ctl-check
         name: dsh-export-ctl-check
   ```

3. **Verificar que foi montado**:

   ```sh
   dsh --profile web --dump-config | grep 'dsh-export-ctl-check'
   node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   export_ctl_check: 1 issue(s) — error 0, warn 1, info 0
   skipped: 2
   ```

**Desinstalar**: `dsh plugin --profile web remove dsh-export-ctl-check` (ou remova a linha do patch do perfil).

> O plugin não faz requisições de rede e não grava arquivos de material; toda a verificação acontece localmente. O exemplo está em `samples/quickstart/input/` e a saída esperada em `samples/quickstart/expected/result.json`. Também é possível procurar o pacote de conformidade aduaneira no WorkBuddy / Coze (esta verificação é uma de suas partes; a disponibilidade é a que constar naquela loja).

## Capacidades principais

`export_ctl_check` tem uma única superfície de ferramenta: ler o material, executar o pacote de regras e devolver um relatório. Capacidades, pelo que se obtém:

- **Oito regras em uma passada** — `EC-001` a `EC-008` cobrem a declaração de controle, o número de licença, a data de emissão, o uso final e o usuário final, o destino, números de licença repetidos, a categoria de controle e o marcador no nome do item. Cada regra confere se algo está preenchido, não se está correto.
- **Localizado por linha e coluna** — cada achado traz `locator` (`row` + `field`), `found`, `expected` e `fix`, de modo que se pode voltar direto àquela célula do registro.
- **Omissões precisam se explicar** — verificações que não podem rodar vão para `skipped` com o motivo; uma lista de problemas vazia não equivale a aprovação, e uma regra sem configuração ou uma coluna ausente nunca são lidas como sucesso em silêncio.
- **Regras são dados** — o pacote de regras `rules/export-ctl-check.yaml` é separado do código; trocar o arquivo muda a versão do conjunto de regras sem tocar em TypeScript. O carregador valida `document` / `number` / `clause` / `excerpt` / `kind` / `source` em cada regra.
- **Sem citações inventadas** — o trecho deve ser uma citação literal; quando a base é apenas um princípio, `kind` é `derived-from-principle` e a gravidade fica limitada a `warn`; um limite institucional fica limitado a `info`.
- **Totalmente offline** — sem requisições de rede, sem chamada ao modelo e sem gravar no registro; a ferramenta devolve um relatório de texto (`markdown`) e um relatório estruturado (`reportJson`).

### Tabela de regras

| Regra | O que confere | Gravidade | Tipo de base |
|---|---|---|---|
| `EC-001` | cada item declara se está sujeito a controle | `warn` | derivada de princípio |
| `EC-002` | um item controlado traz número de licença | `warn` | direta |
| `EC-003` | uma licença registrada traz data de emissão | `warn` | derivada de princípio |
| `EC-004` | consta o uso final ou o usuário final | `warn` | direta |
| `EC-005` | consta um destino | `warn` | direta |
| `EC-006` | os números de licença não se repetem no registro | `warn` | derivada de princípio |
| `EC-007` | a categoria de controle vem do seu vocabulário | `info` | derivada de princípio |
| `EC-008` | o nome do item não conserva marcadores não substituídos | `warn` | direta |

### Exemplos

Esta é a saída real do plugin sobre o próprio fixture `EC-001`, não uma ilustração.

**Ferramenta** `export_ctl_check`

**Entrada**

~~~json
{"rows":[{"物项名称":"某型高性能传感器","是否受控":""}]}
~~~

**Saída**

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

*Obtido de `tests/fixtures/EC-001/EC-001-unsafe.json (cases.json expects EC-001 count 1); run via lib/index.mjs rules/export-ctl-check.yaml`*

### O que você pergunta, o que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Um item está marcado como controlado mas não tem número de licença. Isso é relatado? | Sim, `EC-002` relata essa lacuna: quando o valor de controle de uma linha é um dos que a regra trata como controlado, ela exige um número de licença de exportação. A regra confere apenas se o número está preenchido; não julga se a licença é autêntica, se continua válida ou se cobre aquele item e aquele destino. Se o seu registro usa outra palavra para controlado, acrescente-a aos valores de condição da regra; caso contrário a linha conta como não controlada e a regra fica silenciosa — este plugin não contém lista de controle alguma que decida por você. |
| Um item declara se está controlado, mas deixa o uso final e o usuário final vazios. Isso é detectado? | Sim, `EC-004` relata a linha: pede que pelo menos uma dessas duas colunas esteja preenchida. Uma basta, e a regra não julga se o uso ou o usuário declarados são verdadeiros nem se o caso é um dos que a lei proíbe ou restringe. |
| Há número de licença, mas a coluna da data de emissão está vazia. É um achado? | `EC-003` exige a data. A condição é o número de licença: uma linha sem número não é cobrada por data alguma. A regra não confere o período de validade da licença nem compara a data de emissão com a de exportação: estabelece que a data está lá, não que venha antes. |
| Um mesmo número de licença aparece em várias linhas. O que a verificação diz? | `EC-006` relata o número como repetido dentro do registro. Não distingue uma licença que cobre vários itens — forma normal de manter o registro — de um número copiado por engano, então um achado precisa de confirmação humana; a regra não renumera nada nem fixa quantas linhas podem compartilhar uma licença. Se o seu registro é deliberadamente de uma licença para vários itens, numere as linhas dessa licença ou desative a regra. |
| Uma linha não tem destino final. | `EC-005` a relata, porque todo item precisa trazer destino. Confere que a coluna esteja preenchida, não que o destino seja permitido: se um país ou região está embargado ou restrito lê-se nas listas publicadas pela autoridade competente, e este plugin não contém lista de países alguma. |
| A coluna do nome do item ainda diz um valor de exemplo entre colchetes ou `XXX`. É defeito ou nome real? | `EC-008` relata a linha quando o nome contém um dos termos que a regra procura: marcadores entre colchetes, `XXX`, `xxx`, `TBD`, `todo` ou uma marca de «preencher». Essa lista de termos segue o seu próprio modelo e pode ser ajustada. A regra procura esses termos apenas nessa coluna: nunca julga se o nome é factualmente correto. |

## Configuração

Todos os parâmetros ajustáveis vivem no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem tocar no código; os limites por regra ficam no pacote de regras em `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/export-ctl-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras que deixam de rodar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Rodar apenas estas regras; vazio roda todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de timeout cooperativo da ferramenta |

<details>
<summary>Parâmetros por regra (no pacote de regras, não aqui)</summary>

- `EC-002` `conditionValues` — quais valores da coluna de controle marcam um item como controlado. Os padrões de fábrica são:

```text
是 · Y · yes · true · 受控 · √
```

  Se o seu registro usa outra forma, acrescente-a a esta lista; caso contrário a linha conta como não controlada e a regra fica silenciosa.
- `EC-007` `values` — as categorias de controle da sua instituição, por exemplo `[nuclear, míssil, biológico, químico, uso duplo]`. Vazio significa «não configurado» e a regra se declara em `skipped`; o plugin não codifica taxonomia alguma.
- `EC-008` `terms` — os termos de modelo procurados. Os padrões de fábrica são:

```text
【 】 {{ }} XXX xxx 待填 待补充 TBD todo 示例
```

</details>

Exemplo de sobrescrita no patch do perfil:

```yaml
- insert:
    - id: dsh-export-ctl-check
      name: dsh-export-ctl-check
      config:
        onlyRules: [EC-001, EC-002, EC-003]
        skipNotes: normas internas, edição 2026
```

## Formato do material

A ferramenta aceita JSON ou YAML. A entrada é `file` (caminho absoluto para o material) ou `material` (texto em linha): exatamente uma das duas. O Excel pode ser convertido antes para JSON/YAML, inclusive no chat se a plataforma permitir.

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

Os nomes de coluna são comparados sem diferenciar maiúsculas e ignorando espaços, sublinhados e hífens; os nomes próprios do registro são preservados, de modo que cada achado nomeia a coluna que leu. Os campos são opcionais na camada de leitura e validados pelo motor, então uma exportação parcial gera achados de «falta» em vez de falha.

## Normas seguidas

| Documento | Número | Regras que o citam |
|---|---|---|
| Lei de Controle de Exportações da República Popular da China | Aprovada em 17 de outubro de 2020 na 22.ª sessão do Comitê Permanente da 13.ª Assembleia Popular Nacional, promulgada pela Ordem Presidencial n.º 58, em vigor desde 1 de dezembro de 2020 | EC-001, EC-002, EC-003, EC-004, EC-005, EC-006, EC-008 |
| Lei de Controle de Exportações da República Popular da China | Versão vigente não verificada nesta passagem | EC-007 |

**Limite:** este plugin confere um **registro de itens sujeitos a controle de exportação** no ciclo fechado que se pode exigir de um registro — que cada item declare se está controlado, que um item controlado traga número de licença, que uma licença traga data de emissão, que conste o uso final ou o usuário final, que conste um destino, que os números de licença não se repitam, que a categoria de controle venha do seu vocabulário e que não sobreviva marcador algum. **Não** decide se um item está controlado, se é necessária licença nem se uma exportação infringiria a norma.

### Pacote de regras

Os dados das regras ficam em `rules/export-ctl-check.yaml`. O cabeçalho explica que o plugin não contém lista de controle nem faz consulta a listas, portanto não consegue detectar um item controlado não declarado. O carregador continua exigindo documento, cláusula, trecho e fonte por regra, e continua proibindo que uma verificação derivada de princípio ou configurada localmente seja `error`.

> ### ⚠️ Leia isto antes de confiar em uma citação do relatório
>
> **O estado de `excerpt` é por regra, não uniforme.** Algumas regras citam a cláusula literalmente (`kind: direct`), outras derivam do princípio dos artigos citados (`kind: derived-from-principle`, teto `warn`) e outras usam limites que a sua instituição configura (`kind: institutional-configuration`, teto `info`). O pacote nunca parafraseia uma citação: quando o texto não foi obtido, o campo `excerpt` diz isso e o raciocínio fica em `note`; um teste garante que nenhuma regra afirma uma citação que não tem. **Para toda regra ainda marcada como não obtida, substitua o `excerpt` pela cláusula real e eleve `kind` para `direct` quando tiver o texto.**
>
> A conclusão é do revisor: este plugin lista diferenças que consegue apontar no material e não decide fatos nem conformidade.

## FAQ

<details>
<summary>O material é enviado ou processado pela rede?</summary>

Não. O plugin só lê o que você entrega por `file` ou `material`, analisa localmente e roda as regras localmente: sem requisições de rede, sem telemetria, sem chamadas ao modelo. O resultado existe apenas no valor de retorno da ferramenta e no log de sessão do próprio host DSH; o pacote não guarda uma segunda cópia.

</details>

<details>
<summary>Acho que um item deveria ser controlado e nada foi relatado. É uma falha?</summary>

É o limite mais importante do plugin, não uma falha: ele não contém lista de controle nem mapeia um código de mercadoria ou parâmetro técnico para uma entrada de lista, então não consegue encontrar um item que deveria ter sido declarado controlado e não foi. Determinar se um item está controlado cabe ao exportador diante da lista publicada. O que o plugin garante é que verificações que não pode executar vão para `skipped` em vez de passar em silêncio.

</details>

<details>
<summary>Ele briga com outros plugins por nomes de comando, eventos ou slots?</summary>

Não. Declara apenas a dependência `tools` e registra uma única ferramenta `export_ctl_check`; não registra comando, slot de cliente, prefixo `webServer`, não oferece service key e não altera objetos globais. O argumento ponto a ponto está em «Interoperabilidade».

</details>

<details>
<summary>Qual é o custo de desempenho?</summary>

Análise local mais correspondência de regras: sem rede, sem chamada ao modelo. O orçamento de timeout padrão é `120000` ms. 33 testes (`npx vitest run`) cobrem os pares de fixtures das 8 regras, e `samples/quickstart` pode ser repetido offline.

</details>

<details>
<summary>O pacote de regras pode ser substituído?</summary>

Sim. `rulesFile` pode apontar para qualquer arquivo de regras (relativo à raiz do pacote ou absoluto); regras são dados e o carregador valida os campos de citação e os tetos de gravidade. Trocar o arquivo muda a versão do conjunto de regras sem tocar em TypeScript.

</details>

## Limites de segurança

- **Material somente leitura.** O plugin lê por `file` ou `material`, nunca grava de volta nem altera o original; a única escrita é o log de sessão que o host DSH mantém, e o pacote não acrescenta uma segunda cópia.
- **Sem rede e sem chamada ao modelo.** Sem requisições de rede, sem telemetria e sem chamadas ao modelo; toda a verificação acontece localmente.
- **Sem linguagem que adjudique.** O relatório lista diferenças literais entre o material e as cláusulas citadas; não julga conformidade, responsabilidade nem verdade dos fatos. A conclusão é do revisor.
- **Falha não é silenciosa.** O pacote de regras é validado ao carregar; verificações que não podem rodar vão para `skipped` com o motivo, e uma lista de problemas vazia nunca é lida como «não há nada errado».
- **Sem citações inventadas.** O trecho deve ser uma citação literal; quando o texto não pode ser obtido, o pacote diz isso e limita a gravidade.
- **Registro é um effect.** O registro da ferramenta devolve um disposer, então parar ou recarregar a quente a desregistra e não deixa escutas penduradas.

## Limitações conhecidas

- **Não há lista de controle dentro.** A coluna de controle é a declaração do próprio registro; o plugin só confere o fechamento depois dessa declaração e não consegue encontrar um item controlado não declarado. É o limite de capacidade mais importante do plugin.
- **Não julga a licença em si.** `EC-002` e `EC-003` conferem que o número e a data de emissão estão preenchidos; não verificam autenticidade, período de validade nem cobertura daquele item e daquele destino, e não comparam a data de emissão com a de exportação.
- **Não julga a veracidade do uso final nem do usuário final.** `EC-004` só exige que pelo menos uma das duas colunas esteja preenchida; não julga se o declarado é verdadeiro ou se é proibido.
- **Não julga se um destino é restrito.** `EC-005` só confere que a coluna de destino está preenchida; não há lista de países ou regiões embutida.
- **Número de licença repetido é pista, não conclusão.** Uma licença cobrindo vários itens é forma normal de manter o registro, então um achado de `EC-006` precisa de confirmação humana; o plugin não renumera nem fixa quantas linhas uma licença pode cobrir.
- **`EC-007` precisa do seu vocabulário.** `values` vem vazio, então a regra se declara em `skipped` até ser configurada; como as categorias de controle são divididas depende da versão da lista e o plugin não codifica taxonomia alguma.
- **O estado das citações é por regra.** Algumas regras ainda marcam seu `excerpt` como não obtido, mantêm `kind: derived-from-principle` e ficam limitadas a `warn`; quando tiver o texto, substitua o trecho e eleve o tipo para `direct`.
- **O conjunto completo continua com 8 regras.** Cobre completude e fechamento no nível do registro, não uma revisão substantiva do item, da licença ou da operação.

## Interoperabilidade

O plugin registra uma ferramenta e não ocupa a superfície de outros plugins:

- **Só a dependência `tools`.** `inject = ['tools']`; sem serviço de ferramentas ele não registra nada.
- **Só `export_ctl_check`.** Sem comandos, sem slots de cliente e sem prefixo `webServer`, portanto não disputa essas vagas.
- **Sem service keys e sem mutação global.** Não faz patch de protótipos, não escreve `process.env` e não substitui o fetch global.
- **O patch do bundle só insere a própria linha.** `cordis.patch.yml` acrescenta a linha do plugin e nunca sobrescreve o `config` de uma linha embutida.
- **O kit compartilhado é copiado para dentro.** `src/shared/` é um kit compartilhado copiado no pacote, não uma dependência de execução de outro plugin.
- **O registro da ferramenta é um effect.** `apply()` devolve um disposer, então parar ou recarregar a quente desregistra limpo.

## Compatibilidade

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-rc.2`. `engines.dsh` é declarado como `>=0.2.1-0 <0.3.0` e o host o aplica desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native` e `ptc`; para um diretório inteiro use `ptc` e pague o custo de esquema uma única vez |

## Solução de problemas

- **O plugin instala mas a ferramenta não aparece.** Confira que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou; um `main` errado faz o carregador pular a entrada em silêncio.
- **`dsh plugin add` recusa o pacote por incompatibilidade.** A faixa de peers cobre `0.1.x` e `0.2.x`; se o seu runtime ficar fora dela, conceda uma isenção explícita: `dsh plugin --profile <name> allow-version dsh-export-ctl-check@0.1.0 --dsh-version <runtime> --accept-risk`.
- **Acho que um item é controlado e nada é relatado.** O plugin não contém lista de controle; confirme você mesmo diante da lista publicada — veja «Limitações conhecidas».
- **`EC-002` dispara em um item que sei não ser controlado.** A coluna de controle dele diz que é controlado; corrija a coluna ou registre a licença — o plugin lê a declaração, não a mercadoria.
- **`EC-006` dispara com uma licença em vários itens.** Numere as linhas dessa licença ou desative a regra.
- **`EC-005` não sabe quais destinos são restritos.** Só confere se consta um destino; a lista de países não é embutida de propósito.
- **Uma regra não rodou.** Leia o arranjo `skipped`; ele indica o id da regra e o motivo.
- **`check` informa `manifest-peers` como falha.** O verificador estático compara com uma faixa de peers codificada anterior à linha 0.2; o runtime aplica a compatibilidade na instalação. É um problema conhecido do `dsh-plugin-dev`.
- **Os horários parecem deslocados.** Toda a aritmética é de relógio de parede sobre as strings fornecidas; não há conversão de fuso horário.

## Ecossistema e qualidade

- [Espelho no Gitee](https://gitee.com/perrylink/dsh-export-ctl-check) (espelho sincronizado; o GitHub é o canônico)
- [Página no dshfind](https://dshfind.com/plugins/PerryLink/dsh-export-ctl-check) (instalações e ranking)
- [Relatório OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-export-ctl-check) (movido por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (listado)
- [Escolher um verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice de seleção dos 62 verificadores e plugins gerais)

## Desenvolvimento

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, a suíte compartilhada de tabelas mais fixtures emparelhados
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes
node ../scripts/sync-shared.mjs dsh-export-ctl-check
```

O plugin é de dados: `src/model.ts` declara a forma da tabela, o kit compartilhado de `src/shared/` fornece o leitor e o motor de verificação, e o pacote de regras declara cada verificação. O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o de novo após cada mudança no kit compartilhado. As imagens do README são geradas por [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow: par de WebP hero claro/escuro e par de SVG de estrutura claro/escuro) e podem ser executadas de novo.

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `export`, `ctl`

## Família e agradecimentos

Este projeto faz parte da família de plugins de DeepSeek Harness da [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Se ele for útil, **uma estrela ajuda a próxima pessoa a encontrá-lo** — nada fica bloqueado por isso.

- [@PerryLink](https://github.com/PerryLink) — criador e mantenedor: o pacote de regras, o motor de verificação, os fixtures emparelhados e a documentação em cinco idiomas.

<details>
<summary>Expandir todos os plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver o README do repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 APOSENTADO (repo arquivado) |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 APOSENTADO (repo arquivado) |

</details>

## Licença

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-export-ctl-check contributors

<p align="center"><sub>Apache-2.0 · Plugin da comunidade, sem vínculo com a DeepSeek.</sub></p>
