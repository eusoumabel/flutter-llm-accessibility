# Dataset

Este diretório armazena o dataset de pesquisa e seus metadados de fonte de verdade. As amostras são organizadas em diretórios sob `dataset/samples/`, cada uma com um identificador único e imutável e um arquivo de metadados descrevendo proveniência, taxonomia e ground truth.

## Fluxo

```
metadata.yaml
     |
     +--> ground_truth.jsonl
     +--> dataset.csv
```

Os arquivos de metadados são a fonte de verdade e não devem ser editados manualmente após a geração dos artefatos de validação.

## Status atual

O scaffold inicial do projeto contém exemplos iniciais validados para uma amostra de semântica e outra de interação. Eles foram criados para demonstrar a estrutura requerida e o esquema esperado de metadados.
