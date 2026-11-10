# Prompts

Este diretório contém os prompts experimentais usados no pipeline de avaliação. Cada versão é um artefato científico e não é alterada depois de usada numa rodada; mudanças entram numa nova versão (ADR-R020).

## Versões

| Versão | Rodadas | Mudanças |
| --- | --- | --- |
| v1 | round_01 | P0 zero-shot e P1 guiado por diretrizes; esquema com `type`, `affected_code`, `explanation` e `confidence` (ADR-R018) |
| v2 | round_02 | Campo `severity` no esquema; resposta em português do Brasil; apenas a violação mais grave nos dois prompts; P1 com as subcategorias e a gravidade de cada uma (ADR-R021, ADR-R022) |

Cada versão contém `P0_zero_shot.md`, `P1_guidelines.md` e `response_schema.json`. O arquivo de configuração da rodada indica quais arquivos usar.

## Princípio

Nenhum prompt deve incluir informações sobre o ground truth da amostra, metadados ocultos ou status da mutação. O modelo deve ver apenas o prompt e o código do componente.

O P0 não contém a taxonomia, para preservar a condição zero-shot. O P1 contém as diretrizes, que correspondem às subcategorias da taxonomia.
