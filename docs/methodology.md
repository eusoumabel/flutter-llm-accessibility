# Metodologia

## Problema de pesquisa

Este estudo examina se modelos de linguagem conseguem detectar violações de acessibilidade em componentes Flutter analisando apenas o código-fonte.

## Perguntas de pesquisa

- RQ1: Com que precisão LLMs identificam problemas de acessibilidade em componentes Flutter?
- RQ2: O desempenho de detecção varia entre categorias de acessibilidade, como semântica e interação?
- RQ3: A orientação explícita no prompt melhora o desempenho de detecção em comparação com zero-shot?

## Hipóteses

- H1: LLMs podem identificar uma parcela significativa das violações de acessibilidade presentes em componentes Flutter.
- H2: A capacidade de detecção varia de acordo com a categoria da violação.
- H3: Prompts com diretrizes explícitas de acessibilidade produzem desempenho diferente de prompts zero-shot.

## Desenho experimental

O benchmark usa um conjunto controlado de variantes de código Flutter representando implementações acessíveis ou versões com violações intencionais. As amostras são agrupadas por categoria, com preferência por pares acessível/violação quando possível.

A unidade principal de análise é:

- variante da amostra;
- modelo;
- prompt;
- execução.

Cada configuração é executada múltiplas vezes para avaliar consistência e variabilidade.

## Estrutura do dataset e dos prompts

O repositório separa:

- metadados de pesquisa e taxonomia;
- definições de prompt;
- respostas brutas do modelo;
- saídas normalizadas;
- resultados de avaliação.

Essa separação preserva a distinção entre ground truth e entrada visível ao modelo, o que é essencial para uma avaliação válida.

## Análise planejada

A análise final inclui:

- métricas gerais de acurácia;
- comparação entre modelos;
- comparação entre prompts;
- análise por categoria para semântica e interação;
- categorização de erros para falsos positivos e falsos negativos;
- medição de consistência entre execuções repetidas.

## Integridade da pesquisa

O estudo seguirá os princípios definidos na especificação do projeto: reprodutibilidade, rastreabilidade, ground truth explícito, armazenamento isolado de dados e resultados, e separação estrita entre entrada do modelo e rótulos do benchmark.
