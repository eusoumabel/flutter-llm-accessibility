# Comparação entre rodadas

| Rodada | Modelo | Prompt | Itens/resp. | Revocação | Precisão | F1 | FP em código correto | Principal (qualquer) | Principal (1º) | Categoria | Fora do escopo | Sem mapear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| round_01 | claude-opus-5-5 | P0 | 2.22 | 0.98 | 0.60 | 0.74 | 0.66 | 0.81 | 0.78 | 1.00 | 56 | 22 |
| round_01 | claude-opus-5-5 | P1 | 1.48 | 0.98 | 0.69 | 0.81 | 0.44 | 0.83 | 0.71 | 0.93 | 2 | 22 |
| round_01 | gemini-2.5-flash | P0 | 0.99 | 0.91 | 0.64 | 0.75 | 0.51 | 0.45 | 0.45 | 0.76 | 18 | 13 |
| round_01 | gemini-2.5-flash | P1 | 1.19 | 0.91 | 0.61 | 0.73 | 0.58 | 0.26 | 0.21 | 1.00 | 1 | 4 |
| round_02 | claude-opus-5-5 | P0 | 0.73 | 0.95 | 0.66 | 0.78 | 0.51 | 0.70 | 0.70 | 0.85 | 13 | 14 |
| round_02 | claude-opus-5-5 | P1 | 0.49 | 0.93 | 0.95 | 0.94 | 0.05 | 0.92 | 0.92 | 0.95 | 0 | 0 |
| round_02 | gemini-2.5-flash | P0 | 0.87 | 0.98 | 0.57 | 0.72 | 0.76 | 0.49 | 0.49 | 0.61 | 11 | 28 |
| round_02 | gemini-2.5-flash | P1 | 0.70 | 0.93 | 0.67 | 0.78 | 0.46 | 0.67 | 0.67 | 0.92 | 0 | 0 |

## RQ2: diferença P1 − P0 dentro de cada rodada

| Rodada | Modelo | Revocação | Precisão | FP em código correto | Principal (1º) |
| --- | --- | --- | --- | --- | --- |
| round_01 | claude-opus-5-5 | +0.00 | +0.09 | -0.22 | -0.07 |
| round_01 | gemini-2.5-flash | +0.00 | -0.03 | +0.07 | -0.24 |
| round_02 | claude-opus-5-5 | -0.02 | +0.29 | -0.46 | +0.22 |
| round_02 | gemini-2.5-flash | -0.05 | +0.10 | -0.29 | +0.18 |

103 itens ainda sem subcategoria definida em `analysis/type_mapping/type_mapping.csv`; as colunas de violação principal e categoria são provisórias até a revisão manual.
