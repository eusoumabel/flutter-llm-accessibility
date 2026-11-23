# Protocolo de Análise

## Regra de matching

O benchmark deve tratar uma predição do modelo como match quando o tipo de violação previsto corresponde à categoria de violação do ground truth dentro da mesma variante da amostra.

Possíveis resultados:

- MATCH: a violação foi identificada corretamente.
- PARTIAL_MATCH: a predição identifica parte da questão relevante, mas não a categoria completa do ground truth.
- NO_MATCH: a predição não se alinha com o ground truth.

## Métricas

- precision = VP / (VP + FP)
- recall = VP / (VP + FN)
- F1 = 2 * precision * recall / (precision + recall)

## Comparação entre rodadas

Cada rodada é avaliada com a mesma bateria de medidas (ADR-R023), por modelo e prompt, com `scripts/compare_rounds.py`:

| Medida | Definição |
| --- | --- |
| Conformidade | Respostas válidas, itens por resposta e proporção de respostas com no máximo um item |
| Detecção binária (RQ1) | VP, FP, VN, FN, precisão, revocação, F1 e proporção de código correto acusado, FP / (FP + VN) |
| Violação principal (RQ1) | Entre as detecções, proporção em que a subcategoria principal do ground truth (`subcategory` dos metadados, ADR-R005) está entre os tipos previstos (qualquer posição) e é o primeiro tipo previsto |
| Categoria | Entre as detecções, proporção com algum tipo previsto na categoria do ground truth |
| Ruído | Itens em variantes sem violação, itens fora do escopo, genéricos e ainda sem mapeamento |
| Gravidade | Distribuição da gravidade prevista e, quando o tipo corresponde a uma única subcategoria, concordância com a gravidade da taxonomia (ADR-R021) |
| Custo | Tokens e latência média por resposta |

A RQ2 é reportada como a diferença P1 − P0 de cada medida dentro da rodada. O tipo previsto é associado à taxonomia por `scripts/map_types.py` e revisado manualmente em `analysis/type_mapping/type_mapping.csv`. Itens fora do escopo não contam como erro de subcategoria.

A leitura qualitativa usa a planilha gerada por `scripts/build_round_comparison.py`, com a resposta de cada modelo e prompt em cada rodada e o resultado de cada variante.

## Agregação

O estudo deve reportar resultados por:

- todas as amostras;
- modelo;
- prompt;
- categoria (Semantics vs Interaction);
- tipo de violação quando a quantidade de amostras for suficiente;
- tipo de origem.

## Tratamento de resultados inválidos

Timeouts de resposta, JSON inválido, recusas do provedor e predições malformadas devem ser registrados explicitamente e avaliados segundo um protocolo documentado antes da interpretação final.

Na implementação atual, o runner grava o status de cada resposta (`ok`, `refusal`, `max_tokens`, `invalid_json`) e `calculate_metrics.py` exclui as respostas não válidas da matriz de confusão, reportando-as na contagem `invalid` de cada grupo. Falhas da API são registradas em `results/raw/<ciclo>/_errors.jsonl` e refeitas em nova execução, de modo que não entram nas métricas.
