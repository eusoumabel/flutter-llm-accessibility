# Decisões

## ADR-R001 — O escopo do estudo é limitado a Semantics e Interaction

Status: Aceito

Contexto:
A especificação considera inicialmente outras categorias, mas o cronograma do projeto exige um benchmark inicial gerenciável.

Decisão:
O experimento principal focará em Semantics e Interaction, excluindo categorias mais amplas como contraste ou avaliação geral de UX.

Motivo:
Essas categorias são diretamente inferíveis a partir do código-fonte e são consistentes com o primeiro ciclo de pesquisa.

Data:
2026-09-30

## ADR-R002 — Tamanho e composição do dataset

Status: Aceito

Contexto:
O estudo é desenvolvido no âmbito de uma disciplina, sem número mínimo ou máximo de amostras imposto. A análise prevê resultados por categoria e por tipo de violação.

Decisão:
O dataset terá 6 amostras por subcategoria, totalizando 48 amostras e 80 variantes:

- 3 pares acessível/violação sintéticos;
- 1 par acessível/violação obtido por mutação de código real;
- 1 componente único de código real com violação pré-existente;
- 1 negativo difícil em formato de componente único.

Motivo:
A composição equilibra variantes positivas e negativas (40/40), cobre todas as subcategorias e mantém o custo experimental baixo (80 variantes × 2 prompts × 3 repetições × 2 modelos = 960 chamadas).

Consequências:
Com 5 variantes positivas por subcategoria, a análise por subcategoria é descritiva e sem poder estatístico. Essa limitação é registrada em ameaças à validade.

Data:
2026-10-18

## ADR-R003 — Limiar de tamanho de alvo interativo

Status: Aceito

Contexto:
As diretrizes de referência divergem: Material/Android 48 dp, iOS 44 pt, WCAG 2.5.5 (AAA) 44 px e WCAG 2.5.8 (AA) 24 px.

Decisão:
O limiar adotado é 48×48 dp. Variantes com violação de tamanho devem ter área interativa menor que 24×24 dp; variantes acessíveis devem ter área maior ou igual a 48×48 dp. Áreas entre 24 e 47 dp não compõem amostras.

Motivo:
48 dp é a diretriz verificada pelo próprio Flutter (`androidTapTargetGuideline`) e o mínimo padrão do Material. Restringir as violações a menos de 24 dp garante que elas violem todas as diretrizes de referência, tornando o ground truth incontestável.

Data:
2026-10-18

## ADR-R004 — Regras de desempate entre subcategorias

Status: Aceito

Contexto:
Algumas subcategorias se sobrepõem, especialmente SEM-03, SEM-05 e INT-03, o que tornaria o ground truth ambíguo.

Decisão:
A taxonomia é mantida, e as fronteiras são resolvidas por regras de desempate documentadas em [annotation_guidelines.md](annotation_guidelines.md).

Motivo:
Fundir subcategorias reduziria a granularidade da análise por tipo de violação.

Data:
2026-10-18

## ADR-R005 — Múltiplas violações por variante

Status: Aceito

Decisão:
Uma variante pode conter até 3 violações. Todas são listadas no ground truth, e o campo `subcategory` registra a violação principal. Amostras sintéticas e mutadas contêm uma única violação. Em código real, a violação principal é definida pela ordem de impacto documentada em [annotation_guidelines.md](annotation_guidelines.md).

Motivo:
Código real frequentemente contém mais de um problema; limitar a 3 e definir uma violação principal preserva a categorização da amostra. Manter as amostras sintéticas com uma única violação preserva o par mínimo.

Data:
2026-10-18

## ADR-R006 — Negativos difíceis

Status: Aceito

Decisão:
O dataset inclui negativos difíceis em formato de componente único, categorizados pela subcategoria que imitam, com `has_violation: false`.

Motivo:
Os negativos difíceis medem falsos positivos em casos plausíveis, além das variantes acessíveis dos pares.

Data:
2026-10-18

## ADR-R007 — Licenças aceitas para código externo

Status: Aceito

Contexto:
O repositório é distribuído sob licença MIT.

Decisão:
São aceitos apenas códigos sob MIT, BSD-2-Clause, BSD-3-Clause e Apache-2.0, preservando o aviso de copyright no `metadata.json`. Código sob GPL ou sem licença declarada é excluído.

Data:
2026-10-18

## ADR-R008 — Inventário de candidatos

Status: Aceito

Decisão:
Todo candidato de código real avaliado, incluído ou descartado, é registrado em `dataset/candidates.csv` com URL, commit, licença, decisão e motivo.

Motivo:
Garante rastreabilidade da triagem e permite reportar quantos candidatos foram avaliados e incluídos.

Data:
2026-10-18

## ADR-R009 — Versão de referência do Flutter

Status: Aceito

Contexto:
O comportamento semântico padrão dos widgets pode mudar entre versões do Flutter, o que afeta o ground truth.

Decisão:
A versão de referência é Flutter 3.41.8 (canal stable, Dart 3.11.5). O comportamento semântico padrão dos widgets é avaliado segundo essa versão.

Data:
2026-10-18

## ADR-R010 — Responsabilidade pelas amostras

Status: Aceito

Decisão:
Cada pesquisador é responsável por levantar e anotar uma parcela das amostras. Não há dupla anotação nem cálculo de concordância entre anotadores.

Consequências:
A ausência de dupla anotação é registrada como ameaça à validade interna.

Data:
2026-10-18

## ADR-R011 — Adaptação de código real

Status: Aceito

Contexto:
Componentes reais raramente são autocontidos: dependem de temas, strings de localização, gerenciadores de estado e pacotes do aplicativo de origem.

Decisão:
É permitida adaptação mínima documentada. O método `build` e todo o código relacionado à acessibilidade são preservados como no original. Apenas dependências externas (constantes de tema, strings de localização, gerenciadores de estado, pacotes de terceiros) são substituídas por literais, parâmetros ou equivalentes do Flutter padrão, e código não relacionado ao componente é removido. Cada alteração é registrada em `notes`.

Motivo:
Sem adaptação, poucos componentes reais poderiam ser incluídos e várias subcategorias ficariam sem cobertura.

Consequências:
As amostras de origem real deixam de ser cópias literais; a adaptação é registrada como ameaça à validade externa.

Data:
2026-10-18

## ADR-R012 — Contagem de violações por tipo

Status: Aceito

Decisão:
O limite de 3 violações por variante (ADR-R005) conta tipos distintos de violação, não ocorrências. Cada tipo recebe uma única entrada em `violations`, com `affected_lines` cobrindo todas as ocorrências daquele tipo.

Data:
2026-10-18

## ADR-R013 — Itens tocáveis sem papel de botão

Status: Aceito

Contexto:
`InkWell`, `InkResponse`, `GestureDetector` e `ListTile` com `onTap` expõem texto e ação de toque, mas não declaram papel de botão na versão de referência do Flutter (ADR-R009).

Decisão:
Itens de lista, cards e demais elementos tocáveis construídos com esses widgets, sem `button: true` (ou papel equivalente, como `link: true`), são classificados como SEM-03 (`missing_role`), inclusive quando apenas navegam ou abrem detalhes.

Consequências:
Muitos componentes reais passam a conter SEM-03, como violação principal ou secundária. Negativos difíceis não podem conter elementos tocáveis sem papel.

Data:
2026-10-18

## ADR-R014 — Preenchimento de lacunas de código real

Status: Aceito

Contexto:
Algumas células da composição planejada (ADR-R002) não têm candidato real adequado, por exemplo violações naturais de SEM-02 e INT-01 ou implementações acessíveis de INT-02.

Decisão:
Após uma busca adicional direcionada, as lacunas restantes são preenchidas assim:

- violação natural ausente: um par adicional por mutação de código real na mesma subcategoria;
- fonte acessível ausente para par por mutação: a variante acessível é construída pelos pesquisadores a partir de uma violação real, e a construção é documentada em `notes`;
- negativo difícil ausente: um componente real sem violação, ainda que semelhante à fonte de um par.

Data:
2026-10-18

## ADR-R015 — Tooltip externo não nomeia o controle

Status: Aceito

Contexto:
Na versão de referência do Flutter (ADR-R009), `Tooltip(message: ..., child: IconButton(...))` cria um nó semântico pai contendo apenas o tooltip e um nó filho com o papel de botão e a ação, sem nome. Já `IconButton(tooltip: ...)` atribui o tooltip ao próprio nó do botão. O `labeledTapTargetGuideline` do Flutter reprova o primeiro caso.

Decisão:
Um controle cujo nome acessível é fornecido apenas por um `Tooltip` externo, em nó distinto do nó que contém a ação, é classificado como SEM-01 (`missing_accessible_label`).

Consequências:
As amostras SEM_026 e SEM_027 foram reclassificadas como violações naturais de SEM-01; SEM_020 e INT_012 foram removidas do dataset, e as células correspondentes foram preenchidas com novos candidatos. Os IDs SEM_020 e INT_012 não são reutilizados.

Data:
2026-10-18

## ADR-R016 — Texto selecionável não é alvo interativo

Status: Aceito

Contexto:
`SelectableText` expõe a ação semântica de pressionar longamente para seleção de texto, e o Flutter verifica o tamanho desse alvo.

Decisão:
Texto selecionável não é considerado alvo interativo para INT-01 nem para a zona cinzenta da ADR-R003, pois a seleção de texto não é um controle.

Data:
2026-10-18

## ADR-R017 — Provedores e parâmetros dos modelos

Status: Aceito

Contexto:
O experimento passou a comparar Google Gemini e Anthropic Claude, substituindo a OpenAI. Os modelos atuais do Claude não aceitam `temperature` nem permitem desativar o raciocínio interno.

Decisão:
- Provedores: Gemini (`gemini-2.5-flash`) e Claude (`claude-opus-5-5`), executados na mesma rodada por meio de `LLM_PROVIDERS`.
- Gemini com `temperature` 0 e raciocínio no padrão do provedor.
- Claude sem `temperature` (amostragem padrão), com `effort` `low` e `max_tokens` 16000.
- Sem fallback automático para outro modelo em caso de recusa; recusas são registradas como resultado inválido.
- Modelos e parâmetros são definidos no `.env`, que prevalece sobre variáveis já exportadas no terminal, e registrados em `experiments/*/config.yaml` e em cada resposta bruta.

Motivo:
O Claude Opus 5.5 é o modelo atual recomendado; a ausência de temperatura é documentada e a variação resultante é medida pelas repetições. O fallback misturaria respostas de modelos diferentes na mesma condição experimental.

Consequências:
Os dois provedores não operam sob a mesma configuração de amostragem; a diferença é registrada como ameaça à validade.

Data:
2026-10-18

## ADR-R018 — Esquema de resposta comum

Status: Aceito

Contexto:
Os prompts pedem resposta em JSON sem definir um formato verificável, o que gera respostas malformadas e dificulta a normalização.

Decisão:
Os dois provedores recebem o mesmo JSON Schema (`prompts/response_schema.json`): um objeto com a lista `violations`, cujos itens têm `type` (texto livre), `affected_code`, `explanation` e `confidence` (`low`, `medium` ou `high`). O texto dos prompts não foi alterado.

Motivo:
O tipo em texto livre evita expor a taxonomia ao prompt P0 (zero-shot), preservando a comparação da RQ3. O valor categórico de confiança evita números fora do intervalo, pois o Claude não aplica restrições numéricas no esquema.

Consequências:
O casamento entre o tipo previsto e a subcategoria do ground truth exige um procedimento de mapeamento, ainda a ser definido. Até lá, as métricas consideram apenas a detecção de violação.

Data:
2026-10-18

## ADR-R019 — Versionamento das respostas brutas

Status: Aceito

Contexto:
As respostas brutas em `results/raw/` são a evidência original do experimento, mas estavam excluídas do Git pelo `.gitignore`.

Decisão:
`results/raw/` passa a ser versionado no Git, incluindo o registro de falhas `_errors.jsonl`. As respostas brutas não contêm chaves de API.

Motivo:
Garante rastreabilidade e reprodutibilidade da análise a partir da evidência original, que deve permanecer imutável.

Data:
2026-10-18
