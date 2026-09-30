# Scripts

Este diretório contém a automação necessária para validar, gerar e avaliar o dataset de pesquisa e os resultados dos experimentos.

## Scripts incluídos

- validate_dataset.py: garante que os metadados e IDs permaneçam consistentes com a taxonomia e as regras do repositório.
- generate_ground_truth.py: constrói o artefato canônico `dataset/ground_truth.jsonl` a partir dos metadados.
- generate_dataset_csv.py: constrói o artefato exploratório `dataset/dataset.csv` a partir dos metadados.
- run_experiment.py: prepara a ordem aleatória das amostras e executa os fluxos de prompt/modelo.
- normalize_results.py: mapeia respostas brutas da API para registros normalizados de avaliação.
- calculate_metrics.py: calcula matrizes de confusão e métricas agregadas.
