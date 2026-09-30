# Diretrizes de Anotação

## missing_accessible_label

### Definição
Um componente significativo ou interativo não fornece informação acessível suficiente para que um leitor de tela ou tecnologia assistiva descreva sua finalidade.

### Incluir
- botões de ícone customizados sem rótulo semântico;
- controles significativos sem nome ou finalidade acessíveis;
- widgets customizados usados como alvos de interação sem descrição acessível.

### Excluir
- widgets padrão que já expõem rótulo ou semântica automaticamente;
- conteúdo puramente decorativo;
- casos em que o contexto necessário não está disponível na amostra.

### Caso-limite
Se o rótulo for fornecido fora do trecho visível, o anotador deve marcar o caso como ambíguo e resolvê-lo ou excluí-lo antes do congelamento final do dataset.

## insufficient_target_size

### Definição
Um alvo interativo é pequeno demais para ser operado com conforto e confiabilidade.

### Incluir
- áreas customizadas de `GestureDetector` menores que um tamanho acessível razoável;
- zonas de interação muito pequenas sem alternativa de acesso.

### Excluir
- casos em que a interação não é verdadeiramente direcionada ao usuário;
- elementos decorativos não interativos.

## Regra geral

Se a questão não puder ser inferida com confiança a partir do código-fonte disponível, a amostra não deve ser tratada como violação sem justificativa explícita e documentada.
