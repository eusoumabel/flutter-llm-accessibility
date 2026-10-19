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
