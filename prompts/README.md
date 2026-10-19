# Prompts

Este diretório contém os prompts experimentais usados no pipeline de avaliação. Cada prompt é versionado como artefato científico e deve permanecer estável após a conclusão da fase piloto.

## Prompts incluídos

- P0: prompt zero-shot
- P1: prompt informado por diretrizes

## Princípio

Nenhum prompt deve incluir informações sobre o ground truth da amostra, metadados ocultos ou status da mutação. O modelo deve ver apenas o prompt e o código do componente, com identificadores neutros de caso quando necessário para o registro experimental.

## Esquema de resposta

Todos os prompts são enviados com o mesmo JSON Schema, definido em `response_schema.json` (ADR-R018). O esquema exige a lista `violations`, cujos itens têm `type` (texto livre), `affected_code`, `explanation` e `confidence` (`low`, `medium` ou `high`). O esquema não contém a taxonomia, para não alterar a condição zero-shot do P0.
