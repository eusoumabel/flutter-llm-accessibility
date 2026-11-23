# Revisão cega dos falsos positivos do piloto

Este guia explica como dois revisores classificam, de forma independente, os **falsos positivos** do experimento piloto `EXP_PILOT_001`. Um falso positivo é uma resposta que apontou alguma violação numa variante que, pelo gabarito, não tem violação.

A revisão tem três objetivos:

1. encontrar erros no gabarito antes do experimento final;
2. entender por que os modelos apontam problemas em código correto;
3. produzir dados para a seção de resultados do piloto, incluindo a concordância entre os revisores.

Os falsos negativos (10 respostas) e os verdadeiros positivos não fazem parte desta revisão. Veja a seção [Limitações](#limitações).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `revisao_pilot.xlsx` | Os itens a revisar. É enviado ao Google Drive. |
| `apps_script/Code.gs` e `apps_script/Classificador.html` | O classificador, instalado na planilha do Google. |
| `chave_respostas_pilot.csv` | Liga cada letra (A a D) ao modelo e ao prompt. **Não envie ao Drive e não abra antes de os dois revisores terminarem.** |
| `../../scripts/build_pilot_review.py` | Gera a planilha e a chave de uma rodada a partir de `results/raw/<rodada>/` (`--round round_01`). Os arquivos `*_pilot` acima foram gerados antes da renomeação para rodadas (ADR-R020). |

O script usa uma semente fixa (`--seed 20261023`), então as letras são sempre as mesmas. Rodar o script de novo recria a planilha local, mas **não afeta** a cópia no Google, onde fica o trabalho dos revisores.

## O que está na planilha

- **34 variantes** sem violação que receberam pelo menos um alerta.
- **90 respostas** com alerta, entre as 4 respostas de cada variante (2 modelos × 2 prompts).
- **171 alertas**, que são os itens a classificar. Uma resposta pode ter mais de um alerta, e cada um é julgado separadamente.

| Aba | Para que serve |
|---|---|
| Como usar | Resumo das classes. |
| Resumo por variante | Uma linha por variante, com quantas respostas e quantos alertas ela teve. |
| Codigo | Código numerado, gabarito, as outras variantes da mesma amostra e a nota da anotação. |
| Falsos positivos | Um alerta por linha: resposta, tipo, trecho citado, explicação e confiança. |
| Revisão – *nome* | Criada pelo classificador no primeiro acesso de cada revisor. É onde ficam as classificações dele. |

As quatro primeiras abas são a **fonte** dos itens e não devem ser alteradas.

---

## Antes de começar

### Passo 0. Fixar as regras

Para que a revisão não seja ajustada aos resultados, as regras precisam estar decididas **antes** de olhar as respostas. Proposta para a ADR-R020:

| Classe | Significado | Consequência |
|---|---|---|
| **FP-GT** | O problema existe e está na taxonomia: o gabarito errou | A amostra é corrigida no dataset v0.2, antes do experimento final. O piloto não é refeito. |
| **FP-FORA** | Problema real, mas fora do escopo SEM/INT | Continua contando como FP na métrica principal. Uma métrica secundária exclui esses casos. |
| **FP-SUG** | Só uma recomendação de boa prática | Erro do modelo; conta normalmente. |
| **FP-FALSO** | O que o modelo afirma é falso | Erro do modelo; conta normalmente. |

A ADR também deve registrar:

- **Independência:** cada revisor classifica sozinho e não abre a aba do outro até os dois terminarem;
- **Consenso:** as divergências são resolvidas em discussão, e a classe de consenso é a que vale (passo 5);
- **Escopo:** só os falsos positivos são revisados (veja [Limitações](#limitações)).

### Passo 1. Preparar a planilha no Google (uma pessoa faz, uma vez)

1. No Google Drive, clique em **Novo → Upload de arquivo** e envie `revisao_pilot.xlsx`. Não envie a chave.
2. Abra o arquivo e clique em **Arquivo → Salvar como Planilhas Google**. Use essa cópia daqui em diante.
3. Na cópia, clique em **Extensões → Apps Script**.
4. No editor, apague o conteúdo de `Código.gs` e cole o de `apps_script/Code.gs`.
5. Clique no **+** ao lado de "Arquivos", escolha **HTML** e dê o nome `Classificador`, exatamente assim, sem `.html`. Apague o conteúdo e cole o de `apps_script/Classificador.html`.
6. Clique em **Salvar** (ícone de disquete) e volte para a planilha.
7. Clique em **Compartilhar**, adicione o e-mail do colega como **Editor** e envie.

### Passo 2. Abrir o classificador (cada revisor)

1. Abra uma janela com **apenas a sua conta Google** logada, por exemplo uma janela anônima ou um perfil próprio do Chrome. Com mais de uma conta logada, o Google pode responder `PERMISSION_DENIED`.
2. Abra a planilha e **recarregue a página**. Aparece o menu **Revisão do piloto**.
3. Clique em **Revisão do piloto → Abrir classificador**. Na primeira vez, o Google pede autorização:
   - escolha a sua conta;
   - em "O Google não verificou este app", clique em **Avançado → Acessar (não seguro)**. O aviso aparece porque o script não foi publicado;
   - clique em **Permitir**.

No primeiro acesso, o classificador cria a sua aba, **"Revisão – seu nome"**, e mostra no topo *"Revisando como …"*. Você vê **só as suas respostas**.

#### Opcional: abrir como app da Web

Para usar o classificador numa aba própria do navegador, com um link:

1. Copie o ID da planilha, que é o trecho da URL entre `/d/` e `/edit`.
2. No início do `Code.gs`, preencha `const PLANILHA_ID = '...';` e salve.
3. Clique em **Implantar → Nova implantação → App da Web** e configure:
   - **Executar como:** Usuário que acessa o app da Web;
   - **Quem pode acessar:** Qualquer pessoa com Conta do Google. Na prática, só consegue usar quem também tem acesso à planilha.
4. Clique em **Implantar** e envie o link `/exec` ao colega.

Quando o código mudar, crie uma versão nova: **Implantar → Gerenciar implantações → lápis → Versão: Nova versão → Implantar**. Sem isso, o link continua rodando o código antigo.

---

## Revisão

### Passo 3. Classificar cada alerta

O classificador mostra **um alerta por vez**:

- **No topo:**
  - o caminho, por exemplo *Variante 1 de 34 › INT_004 · accessible › Resposta A (alerta 1 de 3)*;
  - as respostas A a D, com um círculo por alerta. Verde é salvo, laranja é alterado e não salvo, e o contorno marca o item atual;
  - a barra de progresso e a lista **Ir para**. As variantes vêm ordenadas com as de mais erros primeiro.
- **O caso:** "O gabarito diz" (verde) e "O modelo diz" (laranja), lado a lado. No lado verde também aparece a outra versão da amostra, para comparar.
- **Sua decisão:** as perguntas, uma de cada vez. A última resposta define a classe.
- **Código da variante:** fica embaixo. O trecho citado pelo modelo aparece em amarelo.

As perguntas seguem esta ordem:

```text
1. O que o modelo afirma é verdade neste código?
   (O trecho existe? O widget se comporta como ele diz?)
   ├── Não ───────────────────────────────────────────> FP-FALSO
   ├── Não sei ──> marca "DÚVIDA:" na justificativa; confira (passo 3.1) e siga
   └── Sim
       2. É uma barreira real para quem usa leitor de tela
          ou tem dificuldade motora? Ou é só "poderia melhorar"?
          ├── Só sugestão ("considere…", "seria melhor…") ──> FP-SUG
          └── Barreira real
              3. Essa barreira se encaixa em alguma subcategoria SEM-01 a INT-03?
                 (a lista de subcategorias abre sozinha nesta pergunta)
                 ├── Não ──> FP-FORA (ex.: contraste, foco, idioma, tamanho visual do ícone)
                 └── Sim ──> FP-GT → escolha qual subcategoria faltou no gabarito
```

Depois de chegar à classe, preencha:

| Campo | Pergunta que responde | Exemplo |
|---|---|---|
| **Classe** | Por que o modelo errou? | `FP-GT` |
| **Subcategoria** (só em FP-GT) | Qual problema da taxonomia faltou no gabarito? | `SEM-04` |
| **Evidência** | Em que você se baseou? | `Árvore semântica` |
| **Justificativa** | Onde está o problema e qual critério você aplicou? | "Linha 12: o switch customizado não expõe ligado/desligado; a árvore não tem `isToggled`." |

Clique em **Salvar e ir para o próximo** (ou `⌘/Ctrl + Enter`). Depois do último alerta de uma variante, a tela vai direto para a próxima variante pendente. Tudo o que foi salvo fica na sua aba, e ao reabrir o classificador você continua de onde parou. O que **não foi salvo** se perde ao fechar a tela, e o contador do topo avisa quando há alterações pendentes.

Exemplos:

| Situação | Classe | Subcategoria | Evidência | Justificativa |
|---|---|---|---|---|
| O modelo diz que falta o estado "selecionado" e, de fato, falta | FP-GT | SEM-04 | Leitura do código | "Linhas 10-14: o chip muda de cor ao selecionar, mas não expõe `selected` na semântica." |
| O modelo diz que o ícone de 16 px é pequeno, mas a área de toque tem 48 dp | FP-FORA | *(vazio)* | Diretriz/ADR | "Linha 23: o tamanho visual é questão de baixa visão; o alvo segue o padrão de 48 dp (ADR-R003)." |
| O modelo sugere "considere adicionar um hint" | FP-SUG | *(vazio)* | Leitura do código | "Linha 8: o rótulo já descreve a ação; o hint seria só um complemento." |
| O modelo diz que o botão não tem rótulo, mas o `tooltip` do próprio `IconButton` o nomeia | FP-FALSO | *(vazio)* | Árvore semântica | "Linha 24: o tooltip vira o rótulo do botão; a árvore mostra o label no mesmo nó." |

Cuidados:

- **Use os mesmos critérios da anotação.** Valem as diretrizes de anotação e as ADRs, principalmente R003 (limiar de alvo), R004 (desempate), R013, R015 e R016 (casos-limite).
- **Julgue pelo conteúdo, não pela origem.** Às vezes dá para adivinhar o modelo pelo estilo da resposta. Por exemplo, no P1 o Gemini copia o título da seção do prompt no campo do tipo. Não tente adivinhar.
- **Dúvidas:** se não conseguir decidir, comece a justificativa com `DÚVIDA:` e siga com a melhor hipótese.
- **Não mexa no dataset durante a revisão.** As correções são aplicadas depois do consenso.

#### Subcategorias da taxonomia

| Código | Nome | Descrição |
|---|---|---|
| SEM-01 | Rótulo acessível ausente | Componente interativo ou informativo não expõe um rótulo suficiente para o leitor de tela. |
| SEM-02 | Rótulo acessível incorreto | Existe rótulo, mas ele não comunica corretamente o propósito do componente. |
| SEM-03 | Papel semântico ausente | Componente customizado não expõe o papel adequado (botão, link, checkbox…). |
| SEM-04 | Estado não exposto | Estado relevante (selecionado, marcado, expandido, habilitado) não é exposto pela semântica. |
| SEM-05 | Controle customizado inacessível | Controle interativo customizado não fornece informação semântica equivalente à de um controle nativo. |
| INT-01 | Alvo de toque insuficiente | Área interativa menor que o limiar adotado (ADR-R003). |
| INT-02 | Gesto customizado sem alternativa | Gesto customizado (toque duplo, pressionar longo, arrastar, pinçar) sem equivalente acessível. |
| INT-03 | Interação não exposta | O comportamento interativo não chega aos mecanismos de acessibilidade (ex.: ação de toque ausente na árvore semântica). |

As descrições são traduções de `dataset/taxonomy.json`. Os critérios detalhados estão em `docs/annotation_guidelines.md` e nas ADRs.

#### 3.1 Como conferir o comportamento real no Flutter

Quando a dúvida for sobre o que o Flutter expõe ao leitor de tela, faça o mesmo teste usado na criação do dataset. Num projeto Flutter temporário (Flutter 3.41.8, ADR-R009), crie `test/dump_test.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('semantics', (tester) async {
    final handle = tester.ensureSemantics();
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(body: Center(child: /* cole o componente aqui */)),
    ));
    debugDumpSemanticsTree();
    await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
    handle.dispose();
  });
}
```

Rode `flutter test test/dump_test.dart`. Na árvore impressa, confira:

- se o nó interativo tem `label`;
- quais `flags` ele tem (`isButton`, `isChecked`, `isSelected`…);
- quais `actions` ele expõe (`tap`, `longPress`…);
- se o rótulo e a ação estão no **mesmo nó**.

As linhas `meetsGuideline` falham quando o alvo é menor que 48×48 ou quando um alvo tocável não tem rótulo. Se preferir, me diga a variante que eu rodo o teste.

---

## Depois da revisão

### Passo 4. Exportar

Quando **os dois** tiverem terminado, clique em **Arquivo → Fazer download → Microsoft Excel (.xlsx)** e salve por cima de `analysis/pilot_review/revisao_pilot.xlsx`. O arquivo baixado tem as abas dos dois revisores.

### Passo 5. Concordância e consenso

Com o arquivo exportado, eu:

1. calculo a concordância entre os revisores (kappa de Cohen sobre as 4 classes) e listo os alertas em que vocês divergiram, inclusive na subcategoria dos FP-GT;
2. preparo a lista de divergências, com as justificativas dos dois lado a lado.

Vocês discutem **só as divergências** e registram a classe de consenso, com justificativa. Em seguida, decidem o que fazer com cada variante, a partir das classes de consenso:

- **corrigir o gabarito**, se pelo menos um alerta for FP-GT;
- **revisar o critério de anotação**, se sobrar uma dúvida que a discussão não resolveu;
- **manter o gabarito**, nos outros casos.

Para cada correção, escrevam juntos a ação. Por exemplo: "Acrescentar SEM-04 nas linhas 10-18 da variante accessible". As dúvidas que sobrarem são boas para levar ao orientador.

### Passo 6. Abrir a chave e consolidar

Só agora abra `chave_respostas_pilot.csv`. Com ela, eu:

- conto as classes de consenso por modelo e por prompt (por exemplo: quantos FP-FALSO o Claude teve no P0);
- monto as tabelas para a dissertação, com o kappa como medida de confiabilidade;
- listo as correções do dataset, para vocês aprovarem uma a uma.

### Passo 7. Aplicar as correções (dataset v0.2)

Para cada correção aprovada:

1. editar `dataset/samples/<ID>/metadata.json` e, se for o caso, o `.dart`;
2. anotar o motivo em `notes` e atualizar `updated_at`;
3. rodar `python3 scripts/validate_dataset.py`;
4. regenerar `ground_truth.jsonl` e `dataset.csv`;
5. registrar no `docs/research_log.md` e no `CHANGELOG.md`, citando a ADR-R020.

O piloto não é refeito. As métricas do piloto podem ser recalculadas com o gabarito corrigido, apenas como informação.

---

## Limitações

- **Falsos negativos não revisados.** As 10 respostas vazias em variantes com violação, em 5 variantes, não passam por revisão. Um eventual erro do gabarito nesses casos não é detectado.
- **Verdadeiros positivos não revisados.** Hoje, um TP só significa que o modelo apontou *alguma* violação numa variante que tem violação. Ele pode ter apontado um problema diferente do anotado e acertado por coincidência. Por isso, a revocação do piloto está superestimada até que a regra de comparação da ADR-R018 seja definida.
- **Independência por combinação.** Como editores da planilha, os revisores conseguem abrir a aba um do outro. A independência depende do combinado do passo 0.

Essas limitações devem constar em `docs/threats_to_validity.md`.
