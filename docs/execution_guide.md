# Guia de execução

Este documento descreve como preparar, validar e executar o pipeline de pesquisa.

## Pré-requisitos

- Python 3.13 ou compatível;
- dependências instaladas a partir de `requirements.txt`;
- chaves válidas dos provedores listados em `LLM_PROVIDERS` para executar chamadas reais;
- o repositório aberto na raiz do projeto.

Instale as dependências com:

```bash
python3 -m pip install -r requirements.txt
```

O projeto usa JSON para os metadados das samples e para a taxonomia. A configuração do experimento em `experiments/` permanece em YAML e, por isso, `PyYAML` continua listado nas dependências.

## Visão geral do fluxo

```text
metadata.json + taxonomy.json
              |
              v
    validate_dataset.py
              |
              +--> generate_ground_truth.py --> dataset/ground_truth.jsonl
              |
              +--> generate_dataset_csv.py --> dataset/dataset.csv
              |
              v
       run_experiment.py
              |
              v
       results/raw/<ciclo>/
              |
              v
       normalize_results.py
              |
              v
       results/normalized/
              |
              v
       calculate_metrics.py
```

A ordem recomendada é validar primeiro, gerar os artefatos derivados depois e só então executar o provedor externo.

## 1. Preparar o ambiente

Na raiz do repositório:

```bash
cd ../flutter-llm-accessibility
python3 -m pip install -r requirements.txt
```

Crie o arquivo local de ambiente:

```bash
cp .env.example .env
```

Edite `.env` e preencha as chaves:

```dotenv
LLM_PROVIDERS=gemini,claude

GEMINI_API_KEY=sua-chave
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0

ANTHROPIC_API_KEY=sua-chave
CLAUDE_MODEL=claude-opus-5-5
CLAUDE_EFFORT=low
CLAUDE_MAX_TOKENS=16000
```

Para executar apenas um provedor, use por exemplo `LLM_PROVIDERS=gemini`. O Claude Opus 5.5 não aceita `temperature`; a profundidade do raciocínio é controlada por `CLAUDE_EFFORT` (ADR-R017).

Os valores do `.env` prevalecem sobre variáveis de mesmo nome já exportadas no terminal, e o script avisa quando isso ocorre. O arquivo `.env` não deve ser versionado.

## 2. Validar o dataset

Execute:

```bash
python3 scripts/validate_dataset.py
```

O script lê `dataset/taxonomy.json` e todos os arquivos `dataset/samples/*/metadata.json`. Ele verifica:

- campos obrigatórios;
- formato e duplicidade dos IDs;
- categoria e subcategoria existentes;
- arquivos declarados em `files`;
- correspondência entre `files` e `ground_truth`;
- consistência entre `has_violation` e `violations`;
- códigos e tipos de violação;
- mutações declaradas em `taxonomy.json`;
- variantes afetadas por cada mutação.

Não continue para a execução experimental se essa etapa falhar.

## 3. Gerar o ground truth canônico

Execute:

```bash
python3 scripts/generate_ground_truth.py
```

Entrada:

- `dataset/samples/*/metadata.json`.

Saída:

- `dataset/ground_truth.jsonl`.

Cada linha representa uma variante de uma sample, incluindo `sample_id`, `variant`, categoria, indicação de violação e tipos de violação. Esse arquivo é derivado e não deve ser editado manualmente.

## 4. Gerar o CSV exploratório

Execute:

```bash
python3 scripts/generate_dataset_csv.py
```

Entrada:

- `dataset/samples/*/metadata.json`.

Saída:

- `dataset/dataset.csv`.

O CSV contém uma linha por variante e inclui os IDs das mutações aplicadas na coluna `mutation_ids`. Ele serve para inspeção e análise exploratória, não substituindo os metadados canônicos.

## 5. Conferir a configuração do experimento

A configuração atual fica em:

```text
experiments/final/config.yaml
```

Antes de uma execução, confira:

- `experiment.id`;
- `dataset_version`;
- prompts listados em `prompts`;
- número de `repetitions`;
- identificadores dos modelos e parâmetros registrados em `models`;
- armazenamento de respostas brutas.

O runner usa as variáveis do `.env` para selecionar provedores, modelos e parâmetros, e grava em cada resposta bruta os parâmetros efetivamente usados. O arquivo de configuração documenta o desenho do experimento, deve refletir os valores do `.env` e deve ser congelado antes da execução final.

## 6. Executar o experimento

Confira primeiro as chamadas planejadas, sem contatar os provedores:

```bash
python3 scripts/run_experiment.py --experiment pilot --dry-run
```

Depois execute o piloto e, após revisá-lo, o experimento final:

```bash
python3 scripts/run_experiment.py --experiment pilot
python3 scripts/run_experiment.py --experiment final
```

O script:

1. lê `experiments/<pilot|final>/config.yaml`;
2. descobre todas as samples em `dataset/samples/*/metadata.json`;
3. combina provedores, variantes, prompts e repetições e embaralha a ordem das chamadas;
4. ignora chamadas cuja resposta bruta já existe, o que permite retomar uma execução interrompida;
5. envia o prompt com o código da variante e o esquema `prompts/response_schema.json`;
6. grava a resposta bruta com provedor, modelo, parâmetros, status, motivo de parada, uso de tokens, timestamp e latência.

As respostas são gravadas em:

```text
results/raw/<pilot|final>/<modelo>/<prompt>/<sample_id>_<variante>/run_<n>.json
```

O campo `status` registra `ok`, `refusal` (recusa do provedor), `max_tokens` (resposta truncada) ou `invalid_json`; esses resultados são respostas do modelo e ficam gravados. Falhas da API (limite de requisições, indisponibilidade, rede) não interrompem a execução: são registradas em `results/raw/<pilot|final>/_errors.jsonl` e a chamada é refeita na próxima execução do script. Não há fallback automático para outro modelo (ADR-R017).

O ground truth não é enviado ao provedor. Ele permanece separado no dataset e é usado somente na avaliação.

Uma execução real exige chaves válidas e gera custos nos provedores. Sem chave, o script encerra com uma mensagem de configuração ausente.

## 7. Normalizar as respostas

Depois que a execução terminar:

```bash
python3 scripts/normalize_results.py
```

O script lê os JSON em `results/raw/` e produz, no mesmo caminho relativo em `results/normalized/`, registros menores com amostra, variante, status, validade, a predição de violação e os tipos previstos pelo modelo (texto livre, ADR-R018).

As respostas em `results/raw/` são evidência original e devem permanecer imutáveis. A normalização pode ser refeita quando o formato analítico mudar.

## 8. Calcular as métricas

Execute:

```bash
python3 scripts/calculate_metrics.py --experiment final
```

O script combina `dataset/ground_truth.jsonl` com os resultados normalizados, por amostra e variante, e calcula por modelo e prompt, e por modelo, prompt e categoria:

- verdadeiros positivos (`tp`);
- falsos positivos (`fp`);
- verdadeiros negativos (`tn`);
- falsos negativos (`fn`);
- precisão (`precision`);
- revocação (`recall`);
- F1 (`f1`);
- resultados inválidos (`invalid`), excluídos da matriz de confusão.

O relatório é gravado em `analysis/metrics/metrics_<pilot|final>.json`. Nesta versão, a métrica considera apenas a detecção de violação (variante com ou sem violação); o casamento do tipo previsto com a subcategoria ainda depende de um procedimento de mapeamento a definir (ADR-R018).

Interprete os números somente depois de verificar se todas as respostas esperadas foram normalizadas e se resultados inválidos foram registrados.

## Execução completa

Para executar o fluxo completo sem chamada externa durante a preparação:

```bash
python3 scripts/validate_dataset.py
python3 scripts/generate_ground_truth.py
python3 scripts/generate_dataset_csv.py
```

Para executar também o experimento real e a análise:

```bash
python3 scripts/run_experiment.py --experiment final
python3 scripts/normalize_results.py
python3 scripts/calculate_metrics.py --experiment final
```

## Quando adicionar ou modificar uma sample

Depois de criar ou alterar `dataset/samples/<ID>/metadata.json`:

1. execute `validate_dataset.py`;
2. regenere `ground_truth.jsonl`;
3. regenere `dataset.csv`;
4. revise o diff dos artefatos derivados;
5. só então execute o benchmark.

Consulte [Como adicionar uma nova sample](adding_samples.md) para o procedimento detalhado.
