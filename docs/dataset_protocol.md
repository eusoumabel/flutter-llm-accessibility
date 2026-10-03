# Protocolo do Dataset

## Como um componente entra no dataset

1. Encontrar um componente ou trecho Flutter candidato.
2. Verificar a proveniência e a licença da fonte.
3. Registrar a origem, o repositório e os campos de metadados.
4. Classificar o componente com base na taxonomia e nas orientações de anotação.
5. Criar o arquivo de metadados em `dataset/samples/<ID>/metadata.yaml`, escolhendo um dos formatos suportados:
	- par acessível/violação, recomendado para comparação controlada;
	- componente único, quando não houver uma versão acessível equivalente.
6. Validar o metadado e o conjunto de arquivos associados.
7. Revisar a amostra para ambiguidades e completude.
8. Incluir a amostra no dataset somente após validação e revisão.

## Critérios de exclusão

Uma amostra pode ser excluída se:

- o status de licenciamento for incerto;
- a amostra depender de contexto externo que não esteja disponível;
- a questão não puder ser atribuída com confiança suficiente;
- a variante for demasiado ambígua para receber um rótulo estável de ground truth.

## Formatos de amostra

No formato pareado, o diretório contém `accessible.dart`, `violation.dart` e `metadata.yaml`. As duas variantes devem representar o mesmo componente e diferir, idealmente, apenas no aspecto de acessibilidade investigado.

No formato de componente único, o diretório contém um arquivo de código, como `component.dart`, e `metadata.yaml`. O arquivo deve ser declarado em `files.component`, e a chave correspondente em `ground_truth` deve ser `component`.

O formato pareado é preferível para experimentos comparativos. O formato único é apropriado para catalogação de componentes reais ou casos em que não seja possível reconstruir uma implementação acessível equivalente.

## Regras de proveniência

Todo código externo deve incluir nome do repositório, URL, caminho do arquivo original, referência de commit e detalhes da licença quando disponíveis. Preferir hashes de commit em vez de nomes de branch para garantir rastreabilidade.
