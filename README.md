# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Projeto do MBA de Inteligência Artificial — Engenharia de Prompts em Escala.

O objetivo é pegar um prompt de baixa qualidade publicado no LangSmith Prompt Hub, otimizá-lo com técnicas avançadas de Prompt Engineering e validar a qualidade através de métricas automáticas. O critério de aprovação é atingir **0.8 (80%) em todas as 5 métricas de avaliação**.

A tarefa do prompt é converter relatos de bugs em user stories no formato ágil ("Como um... eu quero... para que...").

---

## Tecnologias

- **Python 3.9+**
- **LangChain** — orquestração de LLMs e templates de prompts
- **LangSmith** — gerenciamento de prompts, rastreamento e avaliação
- **OpenAI GPT-4o / Google Gemini 2.5 Flash** — modelos de linguagem

---

## Pré-requisitos

- Python 3.9 ou superior instalado
- Conta no [LangSmith](https://smith.langchain.com/) (gratuita)
- Chave de API da [OpenAI](https://platform.openai.com/api-keys) **ou** [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini é gratuito)

---

## Como Executar

### 1. Clonar o repositório e criar o ambiente virtual

```bash
git clone <url-do-seu-repositorio>
cd mba-ia-pull-evaluation-prompt

# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

Abra o `.env` e preencha:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_chave_aqui
LANGSMITH_PROJECT=nome_do_seu_projeto
USERNAME_LANGSMITH_HUB=seu_usuario_langsmith

# Escolha um provedor: "openai" ou "google"
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash

# Preencha somente o provedor que for usar
OPENAI_API_KEY=sua_chave_openai
GOOGLE_API_KEY=sua_chave_google
```

> **Dica:** O Gemini tem tier gratuito (15 req/min, 1500 req/dia) — ideal para o desafio sem custos.

### 3. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

Isso baixa o prompt de baixa qualidade `leonanluppi/bug_to_user_story_v1` do LangSmith e salva em `prompts/bug_to_user_story_v1.yml`.

### 4. Otimizar o prompt

Edite o arquivo `prompts/bug_to_user_story_v2.yml` com sua versão otimizada (veja a seção [Técnicas Aplicadas](#técnicas-aplicadas)).

### 5. Fazer push do prompt otimizado

```bash
python src/push_prompts.py
```

Publica o prompt otimizado no LangSmith como `{seu_username}/bug_to_user_story_v2`.

### 6. Executar a avaliação

```bash
python src/evaluate.py
```

Avalia o prompt contra os 15 exemplos do dataset e exibe o resultado das 5 métricas.

### 7. Rodar os testes de validação

```bash
pytest tests/test_prompts.py
```

---

## Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt/
├── .env.example                    # Template das variáveis de ambiente
├── .env                            # Suas credenciais (não versionar!)
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml    # Prompt original de baixa qualidade
│   └── bug_to_user_story_v2.yml    # Prompt otimizado (criado por você)
│
├── datasets/
│   └── bug_to_user_story.jsonl     # 15 exemplos para avaliação
│
├── src/
│   ├── pull_prompts.py             # Faz pull do prompt do LangSmith
│   ├── push_prompts.py             # Faz push do prompt otimizado
│   ├── evaluate.py                 # Executa avaliação completa
│   ├── metrics.py                  # 5 métricas de avaliação
│   └── utils.py                    # Funções auxiliares
│
└── tests/
    └── test_prompts.py             # Testes de validação do prompt
```

---

## Técnicas Aplicadas

> **Preencha esta seção com as técnicas que você escolheu ao criar o `bug_to_user_story_v2.yml`.**

### Few-Shot Learning (obrigatório)

<!-- Descreva como você aplicou Few-Shot Learning -->
<!-- Quantos exemplos incluiu? Por que escolheu esses exemplos específicos? -->

**Exemplo:**
> Incluí 3 exemplos de entrada/saída cobrindo bugs de baixa, média e alta complexidade. O modelo passou a estruturar as user stories consistentemente após ver os exemplos.

### [Nome da Técnica Adicional]

<!-- Escolha uma: Chain of Thought, Tree of Thought, Skeleton of Thought, ReAct, Role Prompting -->
<!-- Explique por que escolheu e como aplicou -->

**Exemplo:**
> Apliquei **Role Prompting** definindo a persona de Product Manager Sênior. Isso melhorou a qualidade da escrita e o entendimento do contexto de negócio dos bugs.

---

## Resultados Finais

> **Preencha esta seção após executar a avaliação com todas as métricas >= 0.8.**

### Comparativo v1 vs v2

| Métrica      | Prompt v1 (ruim) | Prompt v2 (otimizado) | Aprovado? |
|--------------|------------------|-----------------------|-----------|
| Helpfulness  | ~0.45            | ?                     | ?         |
| Correctness  | ~0.52            | ?                     | ?         |
| F1-Score     | ~0.48            | ?                     | ?         |
| Clarity      | ~0.50            | ?                     | ?         |
| Precision    | ~0.46            | ?                     | ?         |

### Saída do avaliador

```
# Cole aqui o output do terminal após rodar python src/evaluate.py
```

### Dashboard LangSmith

<!-- Adicione o link público do seu projeto no LangSmith -->
**Link:** [Ver no LangSmith](https://smith.langchain.com/)

<!-- Adicione screenshots das avaliações aqui -->

---

## Métricas de Avaliação

As 5 métricas são calculadas automaticamente por `src/metrics.py` usando um LLM como juiz:

| Métrica         | Tipo    | O que avalia                                      | Mínimo |
|-----------------|---------|---------------------------------------------------|--------|
| **F1-Score**    | Base    | Equilíbrio entre precisão e abrangência           | 0.8    |
| **Clarity**     | Base    | Clareza, organização e linguagem sem ambiguidade  | 0.8    |
| **Precision**   | Base    | Ausência de alucinações e foco no bug reportado   | 0.8    |
| **Helpfulness** | Derivada| Média de Clarity + Precision                      | 0.8    |
| **Correctness** | Derivada| Média de F1-Score + Precision                     | 0.8    |

Todas as 5 métricas devem ser >= 0.8 para aprovação.

---

## Dataset de Avaliação

O arquivo `datasets/bug_to_user_story.jsonl` contém 15 exemplos de bugs:

- 5 bugs simples (ex: botão quebrado, validação de formulário)
- 7 bugs de complexidade média (ex: integração com webhook, paginação mobile)
- 3 bugs complexos (ex: inconsistência de checkout, conflitos de sincronização mobile)
