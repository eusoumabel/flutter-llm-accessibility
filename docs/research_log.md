# Diário de Pesquisa

## 2026-09-30

### Atividade
Estrutura inicial do repositório criada com base na especificação da pesquisa.
Criar os scripts de validação e gerar os artefatos canônicos do dataset a partir dos metadados iniciais.


### Decisão
O projeto será organizado como infraestrutura de dataset e experimentos, e não como um aplicativo Flutter convencional.

### Problema
A especificação exige separação estrita entre o ground truth e qualquer entrada visível ao modelo.

### Próximo passo

## 2026-10-18

### Atividade
Análise da documentação e planejamento da população do dataset. Conclusão das diretrizes de anotação para as 8 subcategorias e registro das decisões ADR-R002 a ADR-R010.

### Decisão
- Composição de 48 amostras (6 por subcategoria) e 80 variantes (ADR-R002).
- Limiar de tamanho de alvo de 48 dp, com violações abaixo de 24 dp (ADR-R003).
- Regras de desempate entre subcategorias, até 3 violações por variante com violação principal, negativos difíceis, licenças aceitas e inventário de candidatos (ADR-R004 a ADR-R008).
- Cada pesquisador é responsável por uma parcela das amostras, sem dupla anotação (ADR-R010).

### Problema
- A variante `violation` de `INT_001` difere da variante acessível em mais de um aspecto (tamanho, rótulo e papel), enquanto o ground truth registra apenas INT-01. A amostra será refeita com alteração apenas do tamanho.
- A proveniência de `SEM_001` e `INT_001` está incompleta (URL, arquivo e commit nulos).

### Próximo passo
Definir a versão de referência do Flutter (ADR-R009), corrigir as amostras existentes e iniciar a construção das amostras por subcategoria.

## 2026-10-18 (população com código real)

### Atividade
Triagem de código real em 12 repositórios clonados e em arquivos obtidos pela busca de código do GitHub, com 66 candidatos registrados em `dataset/candidates.csv`. Criação de 28 amostras de origem real (SEM_016 a SEM_033 e INT_010 a INT_019), verificadas com `flutter analyze` e pela árvore semântica do Flutter 3.41.8. Correção das amostras sintéticas SEM_001 e INT_001.

### Decisão
- Adaptação mínima documentada de código real (ADR-R011) e contagem de violações por tipo (ADR-R012).
- Itens tocáveis sem papel de botão são SEM-03 (ADR-R013).
- Preenchimento de lacunas por pares adicionais ou variantes acessíveis construídas (ADR-R014).
- Tooltip externo não nomeia o controle (ADR-R015) e texto selecionável não é alvo interativo (ADR-R016).

### Problema
- A verificação da árvore semântica mostrou que `Tooltip(child: IconButton(...))` deixa o nó do botão sem nome; SEM_026 e SEM_027 foram reclassificadas como SEM-01, e SEM_020 e INT_012 foram removidas do dataset (seus IDs não são reutilizados).
- Não foram encontradas violações naturais de SEM-04 após busca direcionada; a célula foi preenchida com o par adicional SEM_032 (ADR-R014).
- A composição final difere da planejada na ADR-R002: SEM-01 tem 3 violações naturais e SEM-04 tem 2 pares por mutação e nenhuma violação natural. O dataset tem 50 amostras e 83 variantes (42 com violação e 41 sem).

### Próximo passo
Revisão manual concluída: as 50 amostras estão com status `validated`.

## 2026-10-18 (configuração dos provedores)

### Atividade
Substituição da OpenAI pelo Anthropic Claude no runner, adoção de um esquema de resposta comum aos dois provedores e correção da normalização e do cálculo de métricas.

### Decisão
- Gemini `gemini-2.5-flash` (temperatura 0) e Claude `claude-opus-5-5` (effort `low`, sem temperatura, sem fallback), executados na mesma rodada (ADR-R017).
- Esquema de resposta comum com tipo em texto livre e confiança categórica (ADR-R018).

### Problema
- `calculate_metrics.py` procurava as predições por uma chave que não correspondia ao `case_id` gravado, contando todas as variantes como sem violação prevista; `normalize_results.py` sobrescrevia resultados de modelos e repetições diferentes. Ambos foram corrigidos.
- Variáveis já exportadas no terminal prevaleciam silenciosamente sobre o `.env`; o carregamento foi invertido.
- Resultados simulados da estrutura inicial (`results/normalized/CASE_0001` a `CASE_0004` e os brutos correspondentes) foram removidos.
- As respostas brutas passaram a ser versionadas (ADR-R019).

### Próximo passo
Configurar as chaves, executar o piloto e definir o procedimento de mapeamento dos tipos previstos para a taxonomia.

## 2026-11-10 (rodada 2)

### Atividade
Preparação da rodada 2 a partir da análise das respostas da rodada 1 (antigo piloto).

### Decisão
- O estudo passa a ser organizado em rodadas, executadas uma vez cada; o piloto passa a ser a rodada 1 (ADR-R020).
- Grau de gravidade por subcategoria, derivado da ordem de impacto da anotação (ADR-R021, proposto).
- Prompts v2: campo `severity`, resposta em português do Brasil, apenas a violação mais grave nos dois prompts e P1 com as subcategorias (ADR-R022).

### Problema
- No P0, a violação mais grave é escolhida sem a escala da taxonomia e pode divergir da violação principal do ground truth.

### Próximo passo
Revisar os graus de gravidade e executar a rodada 2.

## 2026-11-22 (análise entre rodadas)

### Atividade
Ferramentas para comparar rodadas: `map_types.py`, `compare_rounds.py` e `build_round_comparison.py`. `build_pilot_review.py` passou a receber `--round`. Diretório vazio `results/normalized/final/` removido.

### Decisão
- A revisão cega dos falsos positivos da rodada 1 não será feita; a análise passa a comparar as rodadas com uma bateria fixa de medidas e uma planilha aberta (ADR-R023, proposto).
- Tipos previstos associados à taxonomia de forma semiautomática.

### Problema
- Na rodada 1, 303 tipos distintos: 183 associados automaticamente, 26 com mais de uma subcategoria, 11 genéricos, 51 fora do escopo e 32 sem correspondência, que aguardam classificação manual.

### Próximo passo
Revisar os graus de gravidade (ADR-R021), executar a rodada 2 e completar o mapeamento manual das duas rodadas.

## 2026-11-22 (rodada 2 e linha de base)

### Atividade
- ADR-R021 (gravidades) e ADR-R023 (comparação entre rodadas) aceitas; execução da rodada 2.
- Linha de base com ferramentas tradicionais (ADR-R024, proposto): Flutter 3.41.8 instalado via fvm, projeto `baselines/flutter_static/` e script `run_static_baseline.py`.
- `compare_rounds.py` passou a listar os candidatos à revisão do ground truth (`analysis/tables/ground_truth_review_candidates.csv`); na rodada 1 são as 9 variantes corretas acusadas pelas quatro configurações.

### Decisão
- A linha de base usa a versão de referência do Flutter, e não a versão instalada na máquina (3.47.9).

### Problema
- A cota da API do Gemini se esgotou durante a rodada 2 (erro 429); as chamadas que falharam ficaram em `results/raw/round_02/_errors.jsonl` e serão refeitas depois da recarga de créditos.
- Linha de base: `flutter analyze` não detecta nenhuma violação; os widget tests detectam 15 das 42 variantes com violação (revocação 0,36, precisão 0,83), concentradas em SEM-01, INT-01 e SEM-05, e acusam 3 variantes corretas, duas delas por tratar texto selecionável como alvo de toque (o oposto da ADR-R016).

### Próximo passo
Recarregar a cota do Gemini, completar a rodada 2 e gerar a comparação entre as rodadas.

## 2026-11-22 (rodada 2 concluída)

### Atividade
Após a recarga da cota do Gemini, as chamadas que faltavam foram refeitas; a rodada 2 tem as 332 respostas com status `ok`. Comparação entre as rodadas gerada em `analysis/tables/` e planilha em `analysis/round_comparison/comparacao_round_01_round_02.xlsx`.

### Problema
- As medidas de violação principal e categoria do P0 ainda dependem do mapeamento manual (103 itens sem subcategoria definida nas duas rodadas); as do P1 da rodada 2 estão totalmente mapeadas.
- 13 variantes corretas são candidatas à revisão do ground truth; SEM_021 e SEM_028 foram acusadas pelas quatro configurações nas duas rodadas.

### Próximo passo
Completar o mapeamento manual, revisar os candidatos do ground truth e decidir a rodada 3 e a repetição de estabilidade.
