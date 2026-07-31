# Statistical Agent Demo

A statistical analysis workflow built with Microsoft Agent Framework. Language
models decide how to use deterministic pandas tools; Python performs the
calculations.

## Workflow

```text
Question
  -> Analysis Agent + Python tools
  -> Verifier Agent + Python tools
  -> Revision Agent
  -> Final answer
```

### 1. Analysis

Input: the user's statistical question.

The Analysis Agent selects the minimum required tool, supplies its arguments,
and explains the returned evidence. It must report relevant missing data and
must not present correlation as causation.

Available tools:

- `get_dataset_overview`: rows, columns, and missing-value counts.
- `get_column_statistics`: descriptive statistics for one numeric column.
- `get_correlation`: Pearson correlation and complete-pair count.

### 2. Verification

Input: the original question and initial analysis.

The Verifier Agent uses a separately configured model and independently calls
the Python tools. It checks numerical claims, completeness, missing data,
sample-size limitations, and unsupported causal conclusions. It returns
`PASS` or `REVISE` with verified evidence.

### 3. Revision

Input: the original question, initial analysis, and verifier feedback.

The Revision Agent reconciles the two preceding results and produces the final
answer. It does not calculate the statistics again because the Verifier already
performed the independent tool check.

## Evaluation

`evaluation/tasks.json` defines questions, expected tools, arguments, and
deterministic ground truth.

- `ground-truth` mode calls Python directly to validate the reference answers.
- `online` mode runs the complete agent workflow, records actual tool calls and
  arguments, checks Analysis tool selection, and saves all stage outputs and
  latency to `evaluation/results.json`.

## Project Structure

```text
agent-demo/
|-- data/sample.csv
|-- evaluation/
|   |-- evaluate.py
|   `-- tasks.json
|-- src/agent_demo/
|   |-- agent_tools.py
|   |-- agents.py
|   |-- evaluation.py
|   |-- prompts.py
|   |-- run_demo.py
|   `-- tools.py
|-- tests/
|-- .env.example
`-- pyproject.toml
```

## Setup

Requirements: Python 3.11+, [`uv`](https://docs.astral.sh/uv/), an API key,
and an OpenAI-compatible model provider.

```bash
git clone https://github.com/chelseawan-best/agent-demo.git
cd agent-demo
uv sync --group dev
cp .env.example .env
```

Configure `.env`. The base URL and model identifiers depend on the provider.

OpenRouter example:

```dotenv
LLM_API_KEY=your_key
LLM_BASE_URL=https://openrouter.ai/api/v1
ANALYSIS_MODEL=openai/gpt-4.1-mini
VERIFIER_MODEL=google/gemini-2.5-flash
```

Official OpenAI example:

```dotenv
LLM_API_KEY=your_key
LLM_BASE_URL=
ANALYSIS_MODEL=gpt-4.1-mini
VERIFIER_MODEL=gpt-4.1-mini
```

For a meaningful independent review, configure different Analysis and Verifier
models when the provider offers them. The local `.env` file is ignored by Git.

## Run

```bash
# Unit tests
uv run pytest -v

# Validate deterministic ground truth without an API call
PYTHONPATH=src uv run python evaluation/evaluate.py --mode ground-truth

# Run one end-to-end task
PYTHONPATH=src uv run python -m agent_demo.run_demo

# Run all online evaluation tasks
PYTHONPATH=src uv run python evaluation/evaluate.py --mode online
```

## Relationship to the Microsoft Course

This project applies ideas from Microsoft AI Agents for Beginners; it is not an
official course sample.

Covered course topics:

- Microsoft Agent Framework agent construction.
- Function-tool definition and model-directed tool use.
- Sequential multi-agent orchestration.
- Prompt-based verification and basic trustworthy-agent checks.

Extensions implemented in this project:

- Domain-specific deterministic pandas tools.
- Separate Analysis, Verifier, and Revision roles.
- Different model configuration for independent verification.
- Ground-truth tasks, tool-call traces, argument checks, and unit tests.
- Explicit missing-data, small-sample, and correlation-versus-causation checks.

Not implemented:

- RAG, long-term memory, autonomous planning, or metacognitive loops.
- MCP/A2A protocols, browser/computer tools, or human approval gates.
- Microsoft Foundry hosted agents or scalable deployment.
- Authentication, rate-limit handling, retries, production observability,
  token/cost tracking, and security hardening.
- Automated scoring of all natural-language claims or a research-scale benchmark.

## Limitations

- The synthetic dataset contains only 12 rows.
- Model-based verification can still make mistakes.
- Current tasks demonstrate correct orchestration, but do not yet measure whether
  verification and revision outperform a single-agent baseline.
- The project demonstrates agent engineering, not model training or fine-tuning.

## References

- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)
- [Microsoft Agent Framework tools](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-tools/)
- [Stanford CS336](https://cs336.stanford.edu/)
- [Stanford CS329A](https://cs329a.stanford.edu/)
