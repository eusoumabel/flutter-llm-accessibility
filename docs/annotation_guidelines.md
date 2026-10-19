# Diretrizes de Anotação

Este documento define os critérios para classificar cada variante de código segundo a taxonomia em `dataset/taxonomy.json`. As decisões que fundamentam estas regras estão registradas em [decisions.md](decisions.md).

## Princípios gerais

- Só é violação o que pode ser inferido com confiança a partir do código-fonte disponível na amostra.
- Considere a semântica fornecida automaticamente pelos widgets padrão do Flutter antes de marcar uma violação.
- Em caso de dúvida sobre o comportamento semântico padrão de um widget, verifique-o na versão de referência do Flutter antes de anotar (ver ADR-R009).
- Se a questão não puder ser inferida com confiança, a amostra não deve ser tratada como violação sem justificativa explícita e documentada; prefira excluí-la.

## Limiar de tamanho de alvo

Ver ADR-R003.

- Limiar adotado: 48×48 dp (diretriz `androidTapTargetGuideline` do Flutter e mínimo padrão do Material via `MaterialTapTargetSize.padded`).
- Variantes com violação de tamanho devem ter área interativa **menor que 24×24 dp**, de forma a violar todas as diretrizes de referência (Material 48 dp, iOS 44 pt, WCAG 2.5.5 e WCAG 2.5.8).
- Variantes acessíveis devem ter área interativa **maior ou igual a 48×48 dp**.
- Áreas entre 24 e 47 dp são zona cinzenta e não devem compor amostras.
- O tamanho deve ser determinável a partir do próprio código da amostra (por exemplo, `SizedBox`, `ConstrainedBox`, `padding` explícito ou padrão conhecido do widget).

## SEM-01 — missing_accessible_label

### Definição
Um componente significativo ou interativo não fornece informação acessível suficiente para que um leitor de tela ou tecnologia assistiva descreva sua finalidade.

### Incluir
- `IconButton` sem `tooltip` e sem `Semantics` com `label`;
- `Icon` ou `Image` significativos sem `semanticLabel`;
- controles cujo rótulo é uma string vazia ou indisponível;
- controles cujo nome é fornecido apenas por um `Tooltip` externo, em nó semântico distinto do nó que contém a ação (por exemplo, `Tooltip(message: ..., child: IconButton(...))`) (ADR-R015);
- widgets usados como alvo de interação cujo conteúdo visual não fornece texto (somente ícone, imagem ou desenho).

### Excluir
- widgets padrão que já expõem rótulo automaticamente (por exemplo, `ElevatedButton` com filho `Text`);
- conteúdo puramente decorativo, inclusive quando marcado com `excludeFromSemantics` ou `ExcludeSemantics` de forma intencional;
- casos em que o contexto necessário não está disponível na amostra.

### Caso-limite
Se o rótulo for fornecido fora do trecho visível, o anotador deve marcar o caso como ambíguo e resolvê-lo ou excluí-lo antes do congelamento final do dataset.

## SEM-02 — incorrect_accessible_label

### Definição
Existe um rótulo acessível, mas ele não comunica corretamente a finalidade do componente.

### Incluir
- rótulo que descreve a aparência e não a ação (por exemplo, `"coração"` para um botão de favoritar);
- rótulo que contradiz a ação executada (por exemplo, `"Salvar"` em um botão que exclui);
- rótulo genérico que não distingue o controle (por exemplo, `"botão"`, `"ícone"`, `"clique aqui"`);
- rótulo que não acompanha a mudança de estado quando a ação muda (por exemplo, sempre `"Adicionar favorito"`, mesmo quando a ação é remover).

### Excluir
- rótulo ausente ou vazio (classificar como SEM-01);
- diferenças de estilo de redação sem impacto na compreensão da finalidade.

## SEM-03 — missing_role

### Definição
Um componente com nome acessível e ação exposta não comunica seu papel semântico.

### Incluir
- `Semantics` com `label` e `onTap`, ou `GestureDetector`/`InkWell` com filho `Text`, atuando como botão, sem `button: true`;
- texto que funciona como título de seção sem `header: true`;
- texto que navega como link sem `link: true`;
- imagem significativa exposta sem `image: true`, quando o papel não é inferido automaticamente;
- itens de lista, cards e demais elementos tocáveis construídos com `InkWell`, `InkResponse`, `GestureDetector` ou `ListTile` com `onTap`, sem `button: true` ou papel equivalente, mesmo quando apenas navegam ou abrem detalhes (ADR-R013).

### Excluir
- widgets padrão que já expõem o papel (`ElevatedButton`, `TextButton`, `IconButton`, `Checkbox`, `Switch` etc.);
- componentes que não possuem nome acessível (avaliar SEM-01 ou SEM-05).

## SEM-04 — missing_state

### Definição
Um componente com nome e papel acessíveis não expõe, ou não atualiza, um estado relevante.

### Incluir
- controle de alternância customizado sem `toggled` ou `checked`;
- abas ou itens selecionáveis sem `selected`;
- seções expansíveis sem `expanded`;
- controle desabilitado visualmente sem `enabled: false` ou equivalente;
- estado declarado com valor fixo que não acompanha o estado real do componente.

### Excluir
- widgets padrão que já expõem o estado (`Checkbox`, `Switch`, `Radio`, `ExpansionTile` etc.);
- componentes sem estado relevante;
- componentes sem nome ou sem papel (avaliar SEM-01, SEM-03 ou SEM-05).

## SEM-05 — inaccessible_custom_control

### Definição
Um controle customizado, construído a partir de primitivas sem semântica própria, não fornece informação semântica equivalente à de um controle padrão.

### Incluir
- controle construído com `GestureDetector`, `Listener`, `CustomPaint`, `Container` ou similares sem nenhuma semântica;
- controle customizado ao qual faltam **duas ou mais** das informações: nome, papel e estado/valor.

### Excluir
- controles customizados aos quais falta apenas uma dessas informações (classificar como SEM-01, SEM-03 ou SEM-04);
- controles cuja informação semântica existe, mas cuja ação não pode ser acionada (avaliar INT-03).

## INT-01 — insufficient_target_size

### Definição
Um alvo interativo é pequeno demais para ser operado com conforto e confiabilidade, segundo o limiar adotado neste documento.

### Incluir
- área de `GestureDetector`, `InkWell` ou equivalente menor que 24×24 dp;
- `IconButton` ou botão padrão com restrições que removem o tamanho mínimo (por exemplo, `constraints` reduzidas, `padding: EdgeInsets.zero` combinado com `materialTapTargetSize: MaterialTapTargetSize.shrinkWrap`), resultando em área menor que 24×24 dp.

### Excluir
- casos em que a interação não é verdadeiramente direcionada ao usuário;
- elementos decorativos não interativos;
- áreas entre 24 e 47 dp (zona cinzenta, não usar em amostras);
- texto selecionável (`SelectableText`), cuja ação de pressionar longamente serve à seleção de texto e não constitui controle (ADR-R016);
- casos em que o tamanho efetivo depende de contexto ausente da amostra.

### Observação
INT-01 é independente das demais subcategorias e pode coexistir com elas na mesma variante.

## INT-02 — inaccessible_custom_gesture

### Definição
Uma ação só pode ser executada por meio de um gesto complexo e não há alternativa acessível equivalente.

### Incluir
- ação disponível apenas por arrastar, deslizar, pressionar longamente, toque duplo ou gestos com vários dedos, sem botão alternativo nem `CustomSemanticsAction`;
- gestos implementados com `Listener` ou com `excludeFromSemantics: true`, sem outro meio de execução.

### Excluir
- ações acionadas por toque simples (avaliar INT-03);
- gestos que o Flutter mapeia automaticamente para ações semânticas equivalentes na versão de referência;
- gestos com alternativa acessível presente na amostra.

## INT-03 — interaction_not_exposed

### Definição
O componente é anunciado pela tecnologia assistiva, mas a sua ação simples (toque) não pode ser descoberta ou acionada por ela.

### Incluir
- elemento tocável envolvido por `ExcludeSemantics` ou `Semantics(excludeSemantics: true)` sem reexpor a ação;
- `Semantics` com `label` sobre um alvo cujo toque é tratado apenas por `Listener` ou por um mecanismo que não registra ação semântica;
- `excludeFromSemantics: true` em um detector de toque que é o único meio de executar a ação.

### Excluir
- elementos sem nenhuma semântica (avaliar SEM-05);
- ações que exigem gesto complexo (avaliar INT-02).

## Regras de desempate

Ver ADR-R004. Aplique a cada elemento interativo, na ordem:

| Situação no código | Subcategoria |
|---|---|
| Controle customizado sem semântica, ou sem 2 ou mais entre nome, papel e estado | SEM-05 (substitui SEM-01, SEM-03 e SEM-04 nesse elemento) |
| Sem nome acessível, ou nome vazio | SEM-01 |
| Nome presente, mas enganoso ou que não descreve a finalidade | SEM-02 |
| Nome e ação presentes, papel ausente | SEM-03 |
| Nome e papel presentes, estado relevante ausente | SEM-04 |
| Ação exige gesto complexo sem alternativa | INT-02 |
| Anunciado, mas a ação simples não pode ser acionada pela tecnologia assistiva | INT-03 |
| Área interativa abaixo do limiar | INT-01 (independente) |

Desempates específicos:

- SEM-05 × INT-03: sem semântica nenhuma, SEM-05; com semântica parcial, mas ação oculta, INT-03.
- INT-02 × INT-03: gesto complexo, INT-02; toque simples não exposto, INT-03.
- Uma mesma falha em um mesmo elemento recebe uma única subcategoria.

## Múltiplas violações e violação principal

Ver ADR-R005.

- Uma variante pode ter no máximo 3 tipos distintos de violação (ADR-R012); cada tipo tem uma única entrada, com `affected_lines` cobrindo todas as ocorrências.
- Todas as violações são listadas em `ground_truth.<variante>.violations`, cada uma com suas linhas afetadas.
- O campo `subcategory` da sample registra a violação principal.
- Em amostras sintéticas e mutadas, a variante com violação contém uma única violação, introduzida pela mutação; essa é a violação principal.
- Em código real com mais de uma violação, a principal é a de maior impacto, segundo a ordem:
  1. impede a operação: SEM-05, INT-03, INT-02;
  2. impede a compreensão: SEM-01, SEM-02;
  3. informação incompleta: SEM-03, SEM-04;
  4. dificulta a operação: INT-01.
- Em caso de empate no mesmo nível, a principal é a que aparece primeiro no código; o critério usado deve ser registrado em `notes`.

## Negativos difíceis

Ver ADR-R006.

- Um negativo difícil é um componente sem violação que se assemelha a um caso de violação.
- É catalogado no formato de componente único, com `has_violation: false` e `violations: []`.
- Os campos `category` e `subcategory` registram a subcategoria que o negativo imita.
- Exemplo: `IconButton` com `tooltip` é o negativo de SEM-01.
- O campo `notes` deve explicar por que o componente não constitui violação.
