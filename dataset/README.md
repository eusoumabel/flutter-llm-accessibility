# Dataset

Este diretório armazena o dataset de pesquisa e seus metadados de fonte de verdade. As amostras são organizadas em diretórios sob `dataset/samples/`, cada uma com um identificador único e imutável e um arquivo de metadados descrevendo proveniência, taxonomia e ground truth.

## Fluxo

```
metadata.json
     |
     +--> ground_truth.jsonl
     +--> dataset.csv
```

Os arquivos de metadados são a fonte de verdade e não devem ser editados manualmente após a geração dos artefatos de validação.

## Formatos de sample

O dataset aceita dois formatos de amostra:

### Par acessível/violação

É o formato recomendado para comparar:

```text
dataset/samples/SEM_002/
├── accessible.dart
├── violation.dart
└── metadata.json
```

`accessible.dart` contém a implementação de referência e `violation.dart` contém a mesma implementação com a falha de acessibilidade documentada. Use esse formato quando quiser medir a diferença entre uma versão correta e uma versão com violação. O arquivo de metadados é `metadata.json`.

### Componente único

Também é permitido catalogar uma amostra sem uma versão acessível equivalente:

```text
dataset/samples/SEM_003/
├── component.dart
└── metadata.json
```

Nesse caso, o `metadata.json` deve declarar `files.component` e usar `component` como chave em `ground_truth`. O formato é válido, mas não permite a comparação pareada entre versões.

As referências entre `files` e `ground_truth` devem ser consistentes em qualquer formato. Consulte [Como adicionar uma nova sample](../docs/adding_samples.md) para o procedimento completo e os templates.

A taxonomia completa, incluindo as mutações possíveis por subcategoria, está em `dataset/taxonomy.json`. As mutações efetivamente aplicadas a cada sample são registradas no array `mutations` do `metadata.json`.

## Status atual

O scaffold inicial do projeto contém exemplos iniciais validados para uma amostra de semântica e outra de interação. Eles foram criados para demonstrar a estrutura requerida e o esquema esperado de metadados.
