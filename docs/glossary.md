# Dicionário de termos

Este documento explica os principais termos usados no repositório e na pesquisa.

## Dataset e amostras

**Dataset**: conjunto organizado de amostras usado para avaliar os modelos. Neste projeto, contém componentes Flutter, metadados e ground truth.

**Sample / amostra**: unidade individual do dataset. Cada amostra possui um diretório em `dataset/samples/<ID>/`, arquivos de código e um `metadata.json`.

**Componente**: trecho ou widget Flutter analisado pelo benchmark. Pode ser representado por um único arquivo `component.dart` ou por um par de variantes.

**Variante**: versão específica do código de uma sample. As chaves usuais são `accessible`, `violation` e `component`.

**Sample pareada**: amostra com `accessible.dart` e `violation.dart`. É o formato recomendado para comparar uma implementação acessível com a mesma implementação contendo uma violação.

**Sample unitária**: amostra com um único arquivo, como `component.dart`, sem uma versão acessível equivalente. É válida para catalogação e classificação, mas não permite comparação pareada.

## Metadados e taxonomia

**Metadata / metadados**: informações estruturadas que descrevem uma sample, incluindo origem, categoria, arquivos, ground truth, referências, mutações e validação. A fonte canônica é `dataset/samples/*/metadata.json`.

**Schema**: contrato que define os campos, tipos e relações esperadas nos metadados. O schema é aplicado pelo `validate_dataset.py`.

**Taxonomia**: classificação controlada dos tipos de acessibilidade investigados. Está em `dataset/taxonomy.json` e organiza categorias, códigos, descrições e mutações possíveis.

**Categoria**: grupo amplo da taxonomia, atualmente `semantics` ou `interaction`.

**Subcategoria**: tipo específico de violação dentro de uma categoria, como `missing_accessible_label` ou `insufficient_target_size`.

**Código da violação**: identificador curto e estável da subcategoria, como `SEM-01` ou `INT-01`.

**Possible mutation / mutação possível**: transformação que pode ser aplicada a um componente para produzir ou representar uma violação de determinada subcategoria. É registrada na taxonomia em `possible_mutations`.

**Mutação aplicada**: transformação efetivamente usada em uma sample. É registrada no array `mutations` do metadata. Uma mesma sample pode possuir várias mutações, cada uma com `id`, `description` e `target_variants`.

**Proveniência**: registro da origem do código, incluindo repositório, URL, arquivo original, commit e licença.

## Ground truth e avaliação

**Ground truth**: classificação considerada correta para uma variante, definida antes da execução do modelo. Informa se existe violação e quais tipos estão presentes.

**Violação**: problema de acessibilidade identificado no código segundo a taxonomia e as diretrizes de anotação.

**`has_violation`**: campo booleano que indica se a variante contém uma violação.

**`violations`**: lista de violações associadas a uma variante. Deve ser vazia quando `has_violation` é `false`.

**Predição**: resposta produzida pelo modelo sobre a presença ou o tipo de violação.

**Match**: situação em que a predição corresponde ao ground truth.

**Falso positivo (`FP`)**: o modelo prevê uma violação que não existe no ground truth.

**Falso negativo (`FN`)**: o modelo não identifica uma violação que existe no ground truth.

**Verdadeiro positivo (`TP`)**: o modelo identifica corretamente uma violação.

**Verdadeiro negativo (`TN`)**: o modelo identifica corretamente a ausência de violação.

**Precision / precisão**: proporção de predições positivas que estão corretas. $precision = TP / (TP + FP)$.

**Recall / revocação**: proporção de violações reais que foram identificadas. $recall = TP / (TP + FN)$.

**F1**: média harmônica entre precisão e revocação. $F1 = 2 * precision * recall / (precision + recall)$.

## Prompts, modelos e execução

**Prompt**: instrução enviada ao modelo junto com o código da sample. Os prompts são versionados em `prompts/`.

**Zero-shot**: prompt sem exemplos resolvidos fornecidos ao modelo.

**Guideline-informed**: prompt que inclui orientações explícitas sobre acessibilidade.

**Few-shot**: prompt que inclui exemplos de entrada e saída antes do caso avaliado.

**LLM**: modelo de linguagem de grande escala usado para analisar o código.

**Provedor**: serviço que disponibiliza o modelo por API, como OpenAI ou Google Gemini.

**Modelo**: identificador específico usado no provedor, como `gpt-4o-mini` ou `gemini-2.5-flash`.

**Repetição**: execução do mesmo caso com a mesma configuração para medir consistência e variabilidade.

**Randomização**: embaralhamento da ordem dos casos antes da execução para reduzir efeitos de ordem.

**Temperatura**: parâmetro que controla a variabilidade da geração do modelo.

## Artefatos e resultados

**Artefato canônico**: arquivo derivado que representa uma visão padronizada dos dados, como `dataset/ground_truth.jsonl`. A fonte original continua sendo o metadata.

**JSONL**: formato em que cada linha é um objeto JSON independente. É usado no `ground_truth.jsonl`.

**CSV**: formato tabular usado em `dataset/dataset.csv` para inspeção e análise exploratória.

**Resposta bruta (`raw`)**: resposta original do provedor, junto com metadados como modelo, tokens, timestamp e latência. Deve permanecer imutável.

**Resultado normalizado (`normalized`)**: representação estruturada derivada das respostas brutas, preparada para cálculo e análise.

**Latência**: tempo entre o envio da requisição e o recebimento da resposta.

**Token**: unidade de texto contabilizada pelo provedor para entrada e saída do modelo.

## Status e controle metodológico

**Candidate**: sample criada, ainda sem revisão completa.

**Annotated**: ground truth preenchido.

**Review pending**: aguardando revisão.

**Validated**: revisão concluída e sample aprovada.

**Frozen**: sample, taxonomia, prompts e configuração bloqueados para um ciclo experimental.

**Reprodutibilidade**: capacidade de repetir o fluxo usando os mesmos dados, prompts, configuração e scripts e obter resultados comparáveis.

**Rastreabilidade**: capacidade de relacionar uma saída ao metadata, código, prompt, modelo, execução e configuração que a produziram.
