# Resultados

Este diretório armazena os resultados dos experimentos em duas etapas distintas:

- raw/: respostas brutas da API e metadados da requisição
- normalized/: saídas estruturadas prontas para análise

Os dados brutos devem permanecer imutáveis após a recepção do provedor do modelo e são versionados no Git como evidência (ADR-R019). A camada normalizada é gerada a partir desses arquivos brutos e pode ser transformada sem alterar a evidência original.

Estrutura das respostas brutas:

```text
raw/<pilot|final>/<modelo>/<prompt>/<sample_id>_<variante>/run_<n>.json
raw/<pilot|final>/_errors.jsonl
```

O arquivo `_errors.jsonl` registra falhas da API (limite de requisições, indisponibilidade, rede); essas chamadas são refeitas na execução seguinte. As respostas brutas não contêm chaves de API.
