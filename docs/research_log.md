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
