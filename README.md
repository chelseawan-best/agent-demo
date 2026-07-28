# Statistical Agent Demo

A compact research prototype for studying reliable, tool-using LLM agents. The project uses Microsoft Agent Framework to coordinate a statistical analysis agent, deterministic Python tools, and an independent verifier agent over a synthetic subscription dataset.

The repository is designed to separate three questions that are often mixed together:

1. **Are the statistical calculations correct?** Deterministic Python functions and offline ground truth answer this.
2. **Can an LLM select and use the right tool?** The analysis agent handles tool selection and response generation.
3. **Can a second agent detect unsupported claims?** The verifier independently checks numbers and statistical interpretation.

## Current Status

- 7 offline tests pass.
- 3/3 deterministic evaluation tasks pass.
- Analysis and verifier agents can be constructed without making an API call.
- The live Analysis -> Verifier workflow is implemented.
- Live model behavior, latency, token usage, and verifier impact still require a valid OpenAI API credential.

No live results are claimed in this repository yet.

## Architecture

```text
User question
    |
    v
StatisticalAnalysisAgent
    |  plans and selects a tool
    v
Microsoft Agent Framework tool layer
    |
    v
Deterministic pandas functions
    |
    v
Evidence-grounded analysis response
    |
    v
StatisticalVerifierAgent
    |  independently re-runs tools
    v
PASS or REVISE + corrected answer
```

## End-to-End Workflow

1. The user asks a question about the synthetic subscription dataset.
2. `StatisticalAnalysisAgent` receives the question, its instructions, and three available tool schemas.
3. The model chooses the smallest useful tool set.
4. Microsoft Agent Framework executes the selected Python tools locally.
5. The tool outputs are returned to the model as evidence.
6. The analysis agent produces a result, evidence summary, and statistical limitation.
7. `StatisticalVerifierAgent` receives the original question and analysis response.
8. The verifier independently calls the same tools to check numerical and interpretive claims.
9. The verifier returns `PASS` or `REVISE`, verified evidence, identified problems, and a correction when needed.

## Design Principles

### Deterministic computation, probabilistic orchestration

The LLM decides **what to calculate**; Python decides **the numerical result**. This avoids asking a language model to perform arithmetic that pandas can execute exactly.

### Separation of concerns

- `tools.py` contains provider-independent statistical logic.
- `agent_tools.py` adapts those functions to Microsoft Agent Framework.
- `agents.py` configures model-backed roles.
- `prompts.py` stores behavioral contracts.
- `evaluation/` keeps benchmark definitions and runners outside production code.

The statistical layer can therefore be reused with another orchestration framework without rewriting the calculations.

### Least-privilege tools

The model is not allowed to provide arbitrary file paths. Agent-facing wrappers operate only on `data/sample.csv`, reducing accidental access to secrets or unrelated files.

### Independent verification

The verifier does not approve an answer because it sounds plausible. It has access to the same deterministic tools and is instructed to verify every numerical claim independently.

### Evaluation before optimization

The repository establishes deterministic ground truth before measuring model behavior. Prompt changes, additional agents, memory, or training methods should be introduced only after a reproducible failure is observed.

## Strengths

- **Auditable:** statistical functions, tool wrappers, prompts, and evaluation tasks are separate and inspectable.
- **Reproducible:** `uv.lock` pins the Python environment.
- **Provider-safe:** API credentials stay in a local `.env` file and are never committed.
- **Testable without an API:** local correctness and agent construction are covered offline.
- **Research-oriented:** the verifier and evaluation harness expose accuracy, failure, and cost questions instead of presenting only a product demo.
- **Extensible:** additional datasets, tools, models, and agent roles can be added without changing the core architecture.

## Project Structure

```text
agent-demo/
|-- data/
|   `-- sample.csv                  # Synthetic subscription dataset
|-- evaluation/
|   |-- tasks.json                 # Questions, expected tools, and ground truth
|   `-- evaluate.py                # Offline and online evaluation modes
|-- src/agent_demo/
|   |-- __init__.py
|   |-- tools.py                   # Deterministic pandas functions
|   |-- agent_tools.py             # Microsoft @tool wrappers
|   |-- prompts.py                 # Analysis and verifier instructions
|   |-- agents.py                  # Agent factories and model client
|   `-- run_demo.py                # One-question Analysis -> Verifier workflow
|-- tests/
|   |-- test_tools.py
|   `-- test_agent_configuration.py
|-- .env.example
|-- pyproject.toml
`-- uv.lock
```

## Core Functions

| Function | Location | Responsibility |
|---|---|---|
| `load_dataset` | `tools.py` | Validate and load a non-empty CSV file. |
| `dataset_overview` | `tools.py` | Return shape, columns, and missing-value counts. |
| `describe_numeric_column` | `tools.py` | Return count, missingness, center, spread, and range. |
| `calculate_correlation` | `tools.py` | Compute Pearson correlation from complete observation pairs. |
| `get_dataset_overview` | `agent_tools.py` | Expose overview metadata as a read-only framework tool. |
| `get_column_statistics` | `agent_tools.py` | Expose descriptive statistics with a typed column argument. |
| `get_correlation` | `agent_tools.py` | Expose correlation with two typed column arguments. |
| `create_analysis_agent` | `agents.py` | Bind the model, analysis instructions, and tools. |
| `create_verifier_agent` | `agents.py` | Bind the model, verifier instructions, and independent tools. |
| `run_offline` | `evaluation/evaluate.py` | Validate deterministic results without an API. |
| `run_online` | `evaluation/evaluate.py` | Run both agents, capture responses, and measure latency. |

## Setup

### Prerequisites

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/)
- An OpenAI API key only for live execution

### Install

```bash
git clone https://github.com/chelseawan-best/agent-demo.git
cd agent-demo
uv sync --group dev
```

The project uses a `src/` layout. Prefix direct module commands with `PYTHONPATH=src` in this environment.

## Offline Validation

Offline commands do not call an LLM and do not require an API key.

Run all tests:

```bash
uv run pytest -v
```

Run deterministic evaluation tasks:

```bash
PYTHONPATH=src uv run python evaluation/evaluate.py --mode offline
```

Expected summary:

```text
7 passed
3/3 offline checks passed
```

## Live Demo

Create a local `.env` file from the example:

```dotenv
OPENAI_API_KEY=your_official_openai_api_key
OPENAI_MODEL=gpt-5.6-terra
```

Do not commit `.env`.

Run one Analysis -> Verifier task first:

```bash
PYTHONPATH=src uv run python -m agent_demo.run_demo
```

The demo asks for the correlation between `weekly_usage_hours` and `churned`, the complete observation count, and a causality caveat.

## Evaluation Modes

### Offline

```bash
PYTHONPATH=src uv run python evaluation/evaluate.py --mode offline
```

This mode routes each benchmark task directly to its deterministic Python function and checks the result against a nested expected subset. It validates the dataset, calculations, and benchmark definitions, but not LLM behavior.

### Online

```bash
PYTHONPATH=src uv run python evaluation/evaluate.py --mode online
```

This mode runs every task through the analysis agent and verifier agent, records the two responses, measures total latency, and writes `evaluation/results.json`.

Online mode may make multiple model requests per task because tool calling commonly requires one request to choose a tool and another to interpret its result. Run the single-task demo before the full evaluation.

## Evaluation Questions

The initial benchmark covers:

1. Dataset dimensions and missingness.
2. Descriptive statistics for `monthly_price`.
3. Pearson correlation between usage and churn, including complete-case count and causal interpretation.

Future online evaluation should add structured scoring for:

- correct tool selection;
- numerical accuracy;
- unsupported causal claims;
- verifier false positives and false negatives;
- latency, token usage, and API cost;
- single-agent versus verifier-assisted performance.

## Limitations

- The dataset is synthetic and contains only 12 rows.
- Pearson correlation is descriptive and does not establish causation.
- The verifier is model-based and can fail independently.
- Current online evaluation stores free-form responses rather than automatically scoring them.
- No live model results are included because an official API run has not yet been completed.
- The demo does not train or fine-tune an agent; it studies framework-level orchestration and verification.

## Learning and Research Basis

The implementation is grounded in the following materials:

- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners): tool use, planning, metacognition, and Microsoft Agent Framework patterns.
- [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/): language-model foundations, inference, evaluation, and alignment context.
- [Stanford CS329A: Self-Improving AI Agents](https://cs329a.stanford.edu/): multi-step reasoning, tool use, agent workflows, and agentic evaluation.

The concrete statistical domain, least-privilege file boundary, deterministic ground-truth harness, and Analysis -> Verifier experiment are project-specific design decisions.

## Next Research Steps

1. Run the online benchmark with an official API key.
2. Capture tool-call traces, token usage, latency, and cost.
3. Add a direct-LLM baseline and a tool-agent-only baseline.
4. Compare both baselines with the verifier-assisted workflow.
5. Build a failure taxonomy for planning, argument selection, calculation use, and interpretation.
6. Test whether verifier benefits justify the additional model calls.

## Security

- Keep credentials in `.env` only.
- Never commit, log, or screenshot API keys.
- Use read-only tools whenever possible.
- Require approval for any future tool that writes files, sends messages, makes purchases, or changes external state.

## License

This educational prototype currently does not include a license file. Add an explicit license before redistributing or accepting external contributions.
