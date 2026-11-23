# Scripts

Este diretório contém a automação necessária para validar, gerar e avaliar o dataset de pesquisa e os resultados dos experimentos.

## Scripts incluídos

- validate_dataset.py: garante que os metadados e IDs permaneçam consistentes com a taxonomia e as regras do repositório.
- generate_ground_truth.py: constrói o artefato canônico `dataset/ground_truth.jsonl` a partir dos metadados JSON.
- generate_dataset_csv.py: constrói o artefato exploratório `dataset/dataset.csv` a partir dos metadados JSON e lista as mutações aplicadas.
- run_experiment.py: prepara a ordem aleatória das amostras e executa os fluxos de prompt/modelo.
- normalize_results.py: mapeia respostas brutas da API para registros normalizados de avaliação.
- calculate_metrics.py: calcula matrizes de confusão e métricas agregadas.
- map_types.py: associa os tipos previstos de uma rodada à taxonomia e mantém o mapeamento revisado em `analysis/type_mapping/type_mapping.csv` (ADR-R023).
- compare_rounds.py: calcula a mesma bateria de medidas para várias rodadas e o resultado de cada variante em cada rodada.
- build_round_comparison.py: gera a planilha aberta, lado a lado, com as respostas de cada rodada.
- run_static_baseline.py: executa a linha de base com `flutter analyze` e as diretrizes de acessibilidade do `flutter_test` (ADR-R024).
- build_pilot_review.py: gera a planilha da revisão cega dos falsos positivos de uma rodada.

A ordem recomendada e os comandos completos estão em [Guia de execução](../docs/execution_guide.md).
