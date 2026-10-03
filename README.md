# Dataset de Pesquisa sobre Acessibilidade com LLM em Flutter

Este repositório fornece a infraestrutura de pesquisa para avaliar de forma reproduzível se modelos de linguagem conseguem detectar violações de acessibilidade em componentes Flutter a partir do código-fonte.

## O que é este projeto

Este não é um aplicativo Flutter convencional. É um repositório científico de dataset e experimentos projetado para suportar:

- versionamento do dataset;
- metadados como fonte de verdade;
- gestão da taxonomia de acessibilidade;
- versionamento de prompts para benchmarking;
- armazenamento de resultados brutos e normalizados;
- cálculo de métricas e análise de resultados;
- documentação metodológica e registro da pesquisa.

## Perguntas principais da pesquisa

- RQ1: Com que precisão LLMs identificam problemas de acessibilidade em componentes Flutter?
- RQ2: O desempenho varia entre categorias de acessibilidade, como semântica e interação?
- RQ3: Prompts guiados por diretrizes melhoram a detecção quando comparados a zero-shot?

## Estrutura do repositório

- dataset/: taxonomia, metadados, ground truth gerado e arquivos de amostras
- prompts/: artefatos de prompt para zero-shot, guideline-informed e estratégia opcional few-shot
- experiments/: definições de configuração para piloto e experimento final
- results/: respostas brutas da API e saídas normalizadas
- analysis/: tabelas, gráficos e notebooks de análise
- scripts/: automação para validação, exportação e execução dos experimentos
- docs/: metodologia, critérios de anotação e documentação do processo de pesquisa

## Documentação

### Metodologia e decisões

- [Índice da documentação](docs/README.md)
- [Metodologia](docs/methodology.md)
- [Protocolo do dataset](docs/dataset_protocol.md)
- [Diretrizes de anotação](docs/annotation_guidelines.md)
- [Protocolo do experimento](docs/experiment_protocol.md)
- [Protocolo de análise](docs/analysis_protocol.md)
- [Ameaças à validade](docs/threats_to_validity.md)
- [Decisões de pesquisa](docs/decisions.md)
- [Diário de pesquisa](docs/research_log.md)
- [Guia de execução](docs/execution_guide.md)
- [Dicionário de termos](docs/glossary.md)

### Operação do repositório

- [Como adicionar uma nova sample](docs/adding_samples.md)
- [Documentação do dataset](dataset/README.md)
- [Documentação dos prompts](prompts/README.md)
- [Documentação dos experimentos](experiments/README.md)
- [Documentação dos resultados](results/README.md)
- [Documentação dos scripts](scripts/README.md)

## Modelo de reprodutibilidade

A verdade canônica de cada amostra está em `dataset/samples/*/metadata.json`, e a taxonomia está em `dataset/taxonomy.json`. Cada subcategoria também registra suas `possible_mutations`, enquanto cada sample registra as mutações aplicadas em `mutations`. Arquivos derivados como `dataset/ground_truth.jsonl` e `dataset/dataset.csv` são gerados automaticamente e devem ser atualizados pelos scripts em `scripts/`, em vez de editados manualmente.

## Configuração do provedor real

Este projeto está conectado aos provedores OpenAI e Google Gemini. Selecione o provedor com `LLM_PROVIDER`:

- `openai`: usa `OPENAI_API_KEY` e `OPENAI_MODEL`;
- `gemini`: usa `GEMINI_API_KEY` e `GEMINI_MODEL`.

Para executar um experimento real:

1. copie o arquivo `.env.example` para `.env`;
2. defina a chave correspondente ao provedor selecionado;
3. opcionalmente ajuste o modelo e a temperatura;
4. execute `python3 scripts/run_experiment.py`.

Exemplo:

```bash
cp .env.example .env
python3 -m pip install -r requirements.txt
python3 scripts/run_experiment.py
```

## Status

Este repositório foi estruturado como infraestrutura de pesquisa. Ele inclui a estrutura necessária, a taxonomia inicial, amostras iniciais, templates de prompts e scripts de automação para começar a coleta de dados e a experimentação piloto.
