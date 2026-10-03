# Como adicionar uma nova sample

Este documento descreve o processo completo para adicionar uma nova amostra ao dataset de acessibilidade Flutter.

Uma sample é composta por:

- um diretório próprio em `dataset/samples/<ID>/`;
- um ou mais arquivos de código Flutter/Dart;
- um arquivo `metadata.yaml` com a fonte de verdade da amostra;
- ground truth explícito para cada variante do código.

O arquivo `metadata.yaml` é a fonte canônica. Os arquivos `dataset/ground_truth.jsonl` e `dataset/dataset.csv` são derivados e devem ser regenerados pelos scripts.

## 1. Antes de criar a sample

Verifique se o caso atende aos critérios do estudo:

- o problema é observável a partir do código-fonte disponível;
- a categoria pertence à taxonomia atual;
- a violação pode ser descrita com precisão e confiança;
- o código não depende de contexto externo que não esteja incluído;
- a origem e a licença do código podem ser documentadas;
- existe uma distinção clara entre a variante acessível e a variante com violação, quando o desenho do caso usar duas variantes.

Não adicione uma amostra quando o comportamento depender de informações ausentes, quando a licença for incerta ou quando o ground truth for ambíguo.

## 2. Escolher o ID e criar o diretório

Os IDs seguem o formato:

- `SEM_###` para amostras da categoria `semantics`;
- `INT_###` para amostras da categoria `interaction`.

O número deve ser único no diretório `dataset/samples/`. Consulte os diretórios existentes antes de escolher o próximo número.

Exemplo:

```bash
mkdir -p dataset/samples/SEM_002
```

O ID usado no nome do diretório deve ser exatamente o mesmo valor informado no campo `id` do `metadata.yaml`.

## 3. Escolher o formato da amostra

O repositório suporta dois formatos. A escolha depende do objetivo da amostra.

### Formato recomendado: par acessível/violação

Use este formato quando for possível representar o mesmo componente em duas versões comparáveis:

- `accessible.dart`: implementação acessível de referência;
- `violation.dart`: a mesma implementação com uma violação intencional.

Esse é o formato preferido para o benchmark porque permite comparar duas variantes mantendo o comportamento visual e funcional tão próximo quanto possível.

```text
dataset/samples/SEM_002/
├── accessible.dart
├── violation.dart
└── metadata.yaml
```

O `metadata.yaml` correspondente é:

```yaml
files:
  accessible: accessible.dart
  violation: violation.dart

ground_truth:
  accessible:
    has_violation: false
    violations: []
  violation:
    has_violation: true
    violations:
      - id: SEM-01
        type: missing_accessible_label
```

### Formato alternativo: componente único

Use este formato quando não existir uma implementação acessível equivalente, por exemplo, ao catalogar um componente real que só pode ser classificado na forma encontrada:

```text
dataset/samples/SEM_003/
├── component.dart
└── metadata.yaml
```

O `metadata.yaml` deve apontar para o arquivo único e usar uma chave correspondente no `ground_truth`:

```yaml
files:
  component: component.dart

ground_truth:
  component:
    has_violation: true
    violations:
      - id: SEM-01
        type: missing_accessible_label
        description: >
          Descrição objetiva da violação observável no código.
        affected_lines:
          start: 10
          end: 15
        confidence: confirmed
```

O formato único é válido para validação e análise. Ele não oferece, porém, a comparação pareada entre uma implementação acessível e uma implementação com violação.

### Regras comuns aos dois formatos

Regras para os arquivos de código:

- os nomes declarados em `files` devem corresponder aos arquivos existentes no diretório;
- cada chave em `ground_truth` deve corresponder a uma chave de arquivo ou à chave `component`;
- os arquivos devem ser pequenos e autocontidos sempre que possível;
- mantenha o contexto necessário para que um modelo consiga analisar o caso;
- não inclua o ground truth, o código da taxonomia ou rótulos explícitos nos arquivos enviados ao modelo;
- no formato pareado, preserve a mesma funcionalidade visual e de negócio entre as variantes, alterando somente o aspecto relacionado à acessibilidade;
- use linhas estáveis para que `affected_lines` continue apontando para o trecho correto.

## 4. Preencher o `metadata.yaml`

Use este modelo como ponto de partida:

```yaml
schema_version: "1.0"
id: SEM_002
title: "Título curto e descritivo"
category: semantics
subcategory: missing_accessible_label
status: candidate

source:
  type: mutation
  repository:
    name: nome-do-repositorio
    url: https://github.com/organizacao/repositorio
  original_file: caminho/para/o/arquivo.dart
  commit: hash-do-commit
  license:
    name: BSD-3-Clause
    verified: true

component:
  framework: flutter
  language: dart
  widget_types:
    - IconButton
  description: >
    Descrição neutra do componente e do contexto necessário para analisá-lo.

files:
  accessible: accessible.dart
  violation: violation.dart

ground_truth:
  accessible:
    has_violation: false
    violations: []
  violation:
    has_violation: true
    violations:
      - id: SEM-01
        type: missing_accessible_label
        description: >
          Descrição objetiva da violação observável no código.
        affected_lines:
          start: 10
          end: 15
        confidence: confirmed

references:
  flutter:
    - type: documentation
      reference: "Nome ou URL da diretriz/documentação Flutter"
  wcag:
    - criterion: "4.1.2"
      description: "Name, Role, Value"

mutation:
  applied: true
  type: remove_semantics
  description: >
    Descrição da transformação aplicada para produzir a variante com violação.

validation:
  automated:
    performed: false
    tool: null
    result: null
  manual:
    performed: false
    reviewers: []
  status: pending

notes: null
created_at: "2026-09-30"
updated_at: "2026-09-30"
```

### Campos obrigatórios

O validador exige os seguintes campos no nível principal:

- `schema_version`;
- `id`;
- `title`;
- `category`;
- `subcategory`;
- `status`;
- `source`;
- `component`;
- `files`;
- `ground_truth`;
- `references`;
- `mutation`;
- `validation`;
- `created_at`;
- `updated_at`.

### Categoria e subcategoria

Os valores de `category` e `subcategory` devem existir em `dataset/taxonomy.yaml`.

A taxonomia atual contém:

- `semantics`: `missing_accessible_label`, `incorrect_accessible_label`, `missing_role`, `missing_state`, `inaccessible_custom_control`;
- `interaction`: `insufficient_target_size`, `inaccessible_custom_gesture`, `interaction_not_exposed`.

Se a violação for de um tipo ainda inexistente, primeiro altere `dataset/taxonomy.yaml` com:

- o novo nome da subcategoria;
- o código correspondente, como `SEM-06` ou `INT-04`;
- uma descrição objetiva e não ambígua.

Depois atualize as diretrizes em `docs/annotation_guidelines.md` e revise a documentação metodológica antes de criar amostras usando a nova categoria.

### Status da amostra

Use o status conforme o estágio de revisão:

- `candidate`: amostra criada, ainda não revisada;
- `annotated`: ground truth preenchido;
- `review_pending`: aguardando revisão;
- `validated`: revisão concluída e amostra aprovada;
- `excluded`: amostra rejeitada, mantida para rastreabilidade;
- `frozen`: amostra bloqueada para um ciclo experimental.

Uma amostra só deve ser incluída em um experimento congelado depois de passar por revisão e validação.

### Ground truth

Para cada variante listada em `ground_truth`:

- `has_violation: false` exige `violations: []`;
- `has_violation: true` exige pelo menos uma entrada em `violations`;
- `id` deve corresponder ao código da taxonomia;
- `type` deve corresponder à subcategoria;
- `description` deve explicar o problema visível no código;
- `affected_lines` deve apontar para o trecho relevante;
- `confidence` deve registrar o grau de certeza da anotação, preferencialmente `confirmed` quando o caso estiver validado.

O ground truth nunca deve ser inserido no prompt ou nos arquivos de código destinados ao modelo.

### Proveniência

Preencha `source` com o máximo de rastreabilidade possível:

- tipo de origem, como `mutation`, `external` ou `synthetic`;
- nome e URL do repositório;
- caminho original do arquivo;
- hash do commit, quando aplicável;
- nome da licença;
- confirmação de que a licença foi verificada.

Para código externo, prefira um hash de commit em vez de uma branch mutável.

### Mutação

Quando a amostra for criada a partir de uma implementação acessível, registre:

- `applied: true`;
- o tipo da mutação, como `remove_semantics` ou `reduce_target_size`;
- uma descrição da mudança e do comportamento que foi preservado.

A mutação deve ser mínima: altere o aspecto de acessibilidade necessário sem introduzir mudanças não relacionadas.

## 5. Revisar manualmente a amostra

Antes de validar, confira:

- no formato pareado, o código acessível realmente representa o comportamento esperado;
- no formato pareado, o código com violação contém a falha descrita;
- no formato único, o componente contém evidência suficiente para sustentar o ground truth;
- no formato pareado, a diferença entre as variantes é compreensível e limitada à acessibilidade;
- a categoria e a subcategoria estão corretas;
- o código da violação está correto;
- as linhas afetadas estão atualizadas;
- a referência Flutter/WCAG é pertinente;
- o status de licença foi verificado;
- nenhum rótulo de ground truth aparece no código ou no prompt;
- a amostra não depende de contexto omitido.

Atualize `validation.manual.performed`, `validation.manual.reviewers` e `validation.status` após a revisão. Quando a revisão terminar, altere também o `status` principal para `validated`.

## 6. Executar a validação

Na raiz do repositório, execute:

```bash
python3 scripts/validate_dataset.py
```

O script verifica, entre outros pontos:

- presença dos campos obrigatórios;
- formato e duplicidade dos IDs;
- existência da categoria e subcategoria na taxonomia;
- existência dos arquivos referenciados;
- consistência entre `has_violation` e `violations`;
- presença de ground truth para as variantes.

Corrija todos os erros antes de continuar.

## 7. Regenerar os artefatos derivados

Depois que a validação passar, regenere os arquivos derivados:

```bash
python3 scripts/generate_ground_truth.py
python3 scripts/generate_dataset_csv.py
```

Esses comandos atualizam:

- `dataset/ground_truth.jsonl`, usado como ground truth canônico tabular para o pipeline;
- `dataset/dataset.csv`, usado para inspeção e análise exploratória.

Não edite esses arquivos manualmente. Se houver um erro, corrija o `metadata.yaml` e gere os artefatos novamente.

## 8. Verificar o impacto experimental

Se a amostra fizer parte do ciclo experimental atual:

1. confirme que `experiments/final/config.yaml` usa os prompts e o número de repetições desejados;
2. verifique se o dataset está congelado antes da execução final;
3. execute o experimento somente depois de revisar a amostra;
4. mantenha as respostas brutas em `results/raw/`;
5. normalize os resultados com `python3 scripts/normalize_results.py`;
6. calcule as métricas com `python3 scripts/calculate_metrics.py`.

Adicionar uma amostra não exige alterar `config.yaml` quando o experimento já coleta automaticamente todas as amostras sob `dataset/samples/`. Só altere a configuração quando a mudança for metodologicamente planejada, como incluir outro prompt, mudar repetições ou criar uma nova versão experimental.

## 9. Checklist final

- [ ] ID único e compatível com a categoria.
- [ ] Diretório criado em `dataset/samples/<ID>/`.
- [ ] Arquivos de código adicionados e referenciados corretamente.
- [ ] `metadata.yaml` preenchido com todos os campos obrigatórios.
- [ ] Categoria, subcategoria e código conferidos em `dataset/taxonomy.yaml`.
- [ ] Ground truth revisado e consistente.
- [ ] Proveniência e licença registradas.
- [ ] Linhas afetadas atualizadas.
- [ ] Revisão manual concluída.
- [ ] `python3 scripts/validate_dataset.py` executado com sucesso.
- [ ] `ground_truth.jsonl` e `dataset.csv` regenerados.
- [ ] Alterações revisadas antes de qualquer execução experimental.
