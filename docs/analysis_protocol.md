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
