# Ameaças à Validade

## Validade de construto

O dataset pode não representar completamente todas as falhas reais de acessibilidade em Flutter. O estudo se concentra intencionalmente em problemas visíveis no código-fonte em Semantics e Interaction, o que pode sub-representar preocupações mais amplas de acessibilidade.

## Validade interna

A formulação dos prompts, o aleatoriedade do modelo e a ambiguidade de anotação podem afetar os resultados. Versionamento consistente de prompts e execuções repetidas são necessários para reduzir esses efeitos.

## Validade externa

O benchmark usa componentes isolados, não aplicações completas. Isso limita a generalização direta para aplicações reais de produção em Flutter.

## Validade de conclusão

Tamanho pequeno do dataset, mutações sintéticas e cobertura limitada de modelos podem afetar a força estatística das conclusões. Os resultados devem ser interpretados como evidência para condições benchmarkadas, e não como afirmações universais.

## Anotação

Cada amostra é anotada por um único pesquisador, sem dupla anotação nem medida de concordância entre anotadores (ADR-R010). As diretrizes de anotação e as regras de desempate reduzem, mas não eliminam, o risco de viés de anotação.

## Tamanho por subcategoria

Cada subcategoria possui 5 variantes positivas (ADR-R002), o que limita a análise por tipo de violação a resultados descritivos.

## Adaptação de código real

As amostras de origem real foram adaptadas para se tornarem autocontidas (ADR-R011). Embora o código de acessibilidade seja preservado, a remoção de dependências pode simplificar o contexto em relação ao aplicativo original.

## Definição de INT-03

INT-03 é anotado a partir da árvore semântica: a ação não é exposta como ação semântica. Leitores de tela como TalkBack e VoiceOver podem simular um toque no centro do elemento focado quando não há ação semântica, de modo que alguns casos de INT-03 podem ser operáveis com leitor de tela, embora continuem inacessíveis para Switch Access, Voice Access e navegação por teclado. Esse comportamento não foi verificado em dispositivo.

## Configuração dos provedores

O Gemini é executado com temperatura 0, enquanto o Claude Opus 5.5 não aceita temperatura e usa a amostragem padrão (ADR-R017). Os dois modelos usam raciocínio interno com configurações próprias de cada provedor. As diferenças de desempenho entre provedores podem refletir, em parte, essas condições de geração.

## Mapeamento dos tipos previstos

O tipo de violação previsto é texto livre (ADR-R018). Enquanto o procedimento de mapeamento para a taxonomia não for definido e validado, as métricas refletem apenas a detecção da presença de violação.
