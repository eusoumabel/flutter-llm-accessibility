# Changelog

Todas as alterações relevantes da infraestrutura do dataset e dos experimentos devem ser documentadas aqui.

## [Unreleased]

- Estrutura inicial do projeto com base na especificação da pesquisa.
- Taxonomia inicial adicionada para violações de acessibilidade em semântica e interação.
- Exemplos iniciais de metadados de amostra adicionados para ambas as categorias.
- Templates de prompt para P0 e P1 adicionados.
- Scripts de validação e geração de artefatos criados.
- Diretrizes de anotação completas para as 8 subcategorias, com regras de desempate, limiar de tamanho de alvo, múltiplas violações e negativos difíceis.
- Decisões ADR-R002 a ADR-R010 registradas.
- Inventário de candidatos `dataset/candidates.csv` adicionado.
- 22 amostras sintéticas (SEM_002 a SEM_015 e INT_002 a INT_009) e 28 amostras de código real (SEM_016 a SEM_033 e INT_010 a INT_019) adicionadas; SEM_001 e INT_001 corrigidas.
- Decisões ADR-R011 a ADR-R016 registradas.
- Colunas `wcag` e `flutter_guideline` passam a ser preenchidas em `dataset.csv`.
- Provedor OpenAI substituído por Anthropic Claude; runner executa Gemini e Claude na mesma rodada, com esquema de resposta comum (`prompts/response_schema.json`), modo `--dry-run`, retomada de execuções e registro de status por chamada (ADR-R017, ADR-R018).
- Respostas brutas em `results/raw/` passam a ser versionadas (ADR-R019); resultados simulados da estrutura inicial removidos.
- Correção do vínculo entre predições e ground truth em `calculate_metrics.py` e da sobrescrita de resultados em `normalize_results.py`.

## [v1.0] - TBD

- 