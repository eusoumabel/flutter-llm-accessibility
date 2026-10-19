# Protocolo do Dataset

## Como um componente entra no dataset

1. Encontrar um componente ou trecho Flutter candidato.
2. Verificar a proveniência e a licença da fonte (ver ADR-R007).
3. Registrar o candidato em `dataset/candidates.csv`, incluído ou descartado, com a decisão e o motivo (ver ADR-R008).
4. Registrar a origem, o repositório e os campos de metadados.
5. Classificar o componente com base na taxonomia e nas orientações de anotação.
6. Criar o arquivo de metadados em `dataset/samples/<ID>/metadata.json`, escolhendo um dos formatos suportados:
	- par acessível/violação, recomendado para comparação controlada;
	- componente único, quando não houver uma versão acessível equivalente.
7. Validar o metadado e o conjunto de arquivos associados.
8. Revisar a amostra para ambiguidades e completude.
9. Incluir a amostra no dataset somente após validação e revisão.

## Critérios de exclusão

Uma amostra pode ser excluída se:

- o status de licenciamento for incerto;
- a amostra depender de contexto externo que não esteja disponível;
- a questão não puder ser atribuída com confiança suficiente;
- a variante for demasiado ambígua para receber um rótulo estável de ground truth;
- a licença não for MIT, BSD-2-Clause, BSD-3-Clause ou Apache-2.0;
- uma variante contiver mais de 3 violações;
- uma área interativa estiver entre 24 e 47 dp (ver ADR-R003).

## Formatos de amostra

No formato pareado, o diretório contém `accessible.dart`, `violation.dart` e `metadata.json`. As duas variantes devem representar o mesmo componente e diferir, idealmente, apenas no aspecto de acessibilidade investigado.

No formato de componente único, o diretório contém um arquivo de código, como `component.dart`, e `metadata.json`. O arquivo deve ser declarado em `files.component`, e a chave correspondente em `ground_truth` deve ser `component`.

O formato pareado é preferível para experimentos comparativos. O formato único é apropriado para catalogação de componentes reais ou casos em que não seja possível reconstruir uma implementação acessível equivalente.

## Regras de proveniência

Todo código externo deve incluir nome do repositório, URL, caminho do arquivo original, referência de commit e detalhes da licença quando disponíveis. Preferir hashes de commit em vez de nomes de branch para garantir rastreabilidade.

## Licenças aceitas

São aceitos códigos sob MIT, BSD-2-Clause, BSD-3-Clause e Apache-2.0 (ADR-R007). O aviso de copyright original deve ser preservado em `source.license.copyright` no `metadata.json`. Código real pode receber adaptação mínima documentada para se tornar autocontido (ADR-R011). Código sob GPL ou sem licença declarada é excluído.

## Inventário de candidatos

Todo candidato de código real avaliado é registrado em `dataset/candidates.csv`, mesmo quando descartado (ADR-R008). As colunas são:

- `candidate_id`: identificador sequencial do candidato (`CAND_###`);
- `repository`, `url`, `file_path`, `commit`, `license`: proveniência;
- `widget_types`: widgets relevantes;
- `suspected_subcategory`: subcategoria provável segundo as diretrizes;
- `decision`: `included`, `excluded` ou `pending`;
- `reason`: motivo da decisão;
- `sample_id`: ID da sample gerada, quando incluído;
- `evaluated_at`: data da avaliação.

## Composição planejada

A composição por subcategoria está definida em ADR-R002: 3 pares sintéticos, 1 par por mutação de código real, 1 componente único real com violação e 1 negativo difícil.
