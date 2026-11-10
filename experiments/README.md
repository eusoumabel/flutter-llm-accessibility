# Experimentos

Este diretório armazena a configuração de cada rodada do benchmark de acessibilidade com LLM (ADR-R020).

## Estrutura

- round_01/: rodada 1, executada como piloto (prompts v1, taxonomia 1.0)
- round_02/: rodada 2 (prompts v2, taxonomia 1.1 com gravidade)

Cada `config.yaml` registra o dataset, a taxonomia, os arquivos de prompt, o esquema de resposta, o número de repetições e os modelos usados na rodada.

## Garantias

- Os arquivos de prompt são versionados em `prompts/vN/`, e cada rodada aponta para a versão que usou.
- As versões do dataset e da taxonomia são registradas.
- As respostas brutas são armazenadas separadamente das previsões normalizadas.
- A configuração da rodada é persistida antes do início da execução e não é alterada depois dela.
