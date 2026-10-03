# Guia de execução

Este documento descreve como preparar, validar e executar o pipeline de pesquisa.

## Pré-requisitos

- Python 3.13 ou compatível;
- dependências instaladas a partir de `requirements.txt`;
- uma chave válida do provedor escolhido para executar chamadas reais;
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

Para usar OpenAI ou Gemini, crie o arquivo local de ambiente:

```bash
cp .env.example .env
```

Edite `.env` e escolha um provedor:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sua-chave
OPENAI_MODEL=gpt-4o-mini
```

ou:

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=sua-chave
GEMINI_MODEL=gemini-2.5-flash
```

O arquivo `.env` não deve ser versionado.

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
- versão ou identificador do modelo;
- temperatura;
- armazenamento de respostas brutas.

O runner atual usa as variáveis do `.env` para selecionar o provedor, modelo e temperatura. O arquivo de configuração documenta o desenho do experimento e deve ser congelado antes da execução final.

## 6. Executar o experimento

Execute:

```bash
python3 scripts/run_experiment.py
```

O script:

1. lê `experiments/final/config.yaml`;
2. descobre todas as samples em `dataset/samples/*/metadata.json`;
3. carrega o código de cada variante;
4. embaralha a ordem das samples;
5. combina samples, prompts e repetições;
6. chama OpenAI ou Gemini conforme `LLM_PROVIDER`;
7. grava a resposta bruta, uso de tokens, modelo, timestamp e latência.

As respostas são gravadas em:

```text
results/raw/final/<modelo>/<prompt>/<case_id>/run_<n>.json
```

O ground truth não é enviado ao provedor. Ele permanece separado no dataset e é usado somente na avaliação.

Uma execução real exige uma chave válida e pode gerar custos no provedor. Sem chave, o script deve encerrar com uma mensagem de configuração ausente.

## 7. Normalizar as respostas

Depois que a execução terminar:

```bash
python3 scripts/normalize_results.py
```

O script lê os JSON em `results/raw/` e produz registros menores em `results/normalized/`, contendo a predição de violação e os tipos previstos pelo modelo.

As respostas em `results/raw/` são evidência original e devem permanecer imutáveis. A normalização pode ser refeita quando o formato analítico mudar.

## 8. Calcular as métricas

Execute:

```bash
python3 scripts/calculate_metrics.py
```

O script combina `dataset/ground_truth.jsonl` com os resultados normalizados e calcula:

- verdadeiros positivos (`tp`);
- falsos positivos (`fp`);
- verdadeiros negativos (`tn`);
- falsos negativos (`fn`);
- precisão (`precision`);
- revocação (`recall`);
- F1 (`f1`).

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
python3 scripts/run_experiment.py
python3 scripts/normalize_results.py
python3 scripts/calculate_metrics.py
```

## Quando adicionar ou modificar uma sample

Depois de criar ou alterar `dataset/samples/<ID>/metadata.json`:

1. execute `validate_dataset.py`;
2. regenere `ground_truth.jsonl`;
3. regenere `dataset.csv`;
4. revise o diff dos artefatos derivados;
5. só então execute o benchmark.

Consulte [Como adicionar uma nova sample](adding_samples.md) para o procedimento detalhado.
