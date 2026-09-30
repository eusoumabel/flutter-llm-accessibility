# Protocolo do Dataset

## Como um componente entra no dataset

1. Encontrar um componente ou trecho Flutter candidato.
2. Verificar a proveniência e a licença da fonte.
3. Registrar a origem, o repositório e os campos de metadados.
4. Classificar o componente com base na taxonomia e nas orientações de anotação.
5. Criar o arquivo de metadados em `dataset/samples/<ID>/metadata.yaml`.
6. Validar o metadado e o conjunto de arquivos associados.
7. Revisar a amostra para ambiguidades e completude.
8. Incluir a amostra no dataset somente após validação e revisão.

## Critérios de exclusão

Uma amostra pode ser excluída se:

- o status de licenciamento for incerto;
- a amostra depender de contexto externo que não esteja disponível;
- a questão não puder ser atribuída com confiança suficiente;
- a variante for demasiado ambígua para receber um rótulo estável de ground truth.

## Regras de proveniência

Todo código externo deve incluir nome do repositório, URL, caminho do arquivo original, referência de commit e detalhes da licença quando disponíveis. Preferir hashes de commit em vez de nomes de branch para garantir rastreabilidade.
