# Experimentos

Este diretório armazena as definições de configuração e execução do piloto e dos testes finais do benchmark de acessibilidade com LLM.

## Estrutura

- pilot/: avaliação leve para validar todo o pipeline, os prompts e as premissas de metadados
- final/: configuração congelada para o experimento definitivo

## Garantias

- Os arquivos de prompt são versionados.
- As versões do dataset são registradas.
- As respostas brutas são armazenadas separadamente das previsões normalizadas.
- A configuração do experimento é persistida antes do início da execução.
