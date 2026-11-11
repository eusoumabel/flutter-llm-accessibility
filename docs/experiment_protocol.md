# Protocolo do Experimento

## Checklist

- [ ] O dataset está congelado para a rodada atual
- [ ] A taxonomia está congelada e documentada
- [ ] Os prompts da rodada estão numa versão própria em `prompts/vN/`
- [ ] Os identificadores dos modelos são registrados exatamente como informados pelo provedor
- [ ] A configuração do experimento foi armazenada em `experiments/`
- [ ] O acesso à API foi verificado
- [ ] A rodada anterior foi analisada e as mudanças desta rodada estão registradas em ADR
- [ ] A randomização está pronta para execução
- [ ] As respostas brutas estão habilitadas
- [ ] A geração de saídas normalizadas está habilitada
- [ ] O ground truth permanece oculto do caminho de entrada do modelo

## Fluxo operacional

1. Validar o dataset.
2. Gerar o arquivo canônico de ground truth.
3. Selecionar as variantes de prompt.
4. Embaralhar os casos experimentais.
5. Executar o pipeline de modelo/provedor.
6. Armazenar respostas brutas.
7. Normalizar as predições.
8. Calcular as métricas de avaliação.
9. Escrever o relatório de análise.

Os comandos e as dependências entre os scripts estão detalhados no [Guia de execução](execution_guide.md). A configuração de cada rodada permanece em `experiments/round_NN/config.yaml`; metadata e taxonomia usam JSON.
