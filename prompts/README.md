# Prompts

Este diretório contém os prompts experimentais usados no pipeline de avaliação. Cada prompt é versionado como artefato científico e deve permanecer estável após a conclusão da fase piloto.

## Prompts incluídos

- P0: prompt zero-shot
- P1: prompt informado por diretrizes

## Princípio

Nenhum prompt deve incluir informações sobre o ground truth da amostra, metadados ocultos ou status da mutação. O modelo deve ver apenas o prompt e o código do componente, com identificadores neutros de caso quando necessário para o registro experimental.
