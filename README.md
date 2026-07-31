# Statistical Agent Demo

A statistical analysis agent built with Microsoft Agent Framework and an
OpenAI-compatible API. The project uses deterministic pandas tools for
calculation, a separate verifier model for review, and a final revision pass.

## Workflow

```text
Question -> Analysis Agent -> Python Tools -> Verifier -> Revision Agent -> Final Answer
```

- The analysis agent selects tools and explains their results.
- Python tools read the dataset and perform the calculations.
- The verifier independently checks numerical claims and interpretation.
- The revision agent reconciles the analysis with independently verified evidence
  and produces the final answer.

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

Requirements: Python 3.11+, [`uv`](https://docs.astral.sh/uv/), and an
OpenRouter API key.

```bash
git clone https://github.com/chelseawan-best/agent-demo.git
cd agent-demo
uv sync --group dev
cp .env.example .env
```

Add the API key to `.env`:

```dotenv
LLM_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
ANALYSIS_MODEL=openai/gpt-4.1-mini
VERIFIER_MODEL=google/gemini-2.5-flash
```

The local `.env` file is ignored by Git.

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

Online evaluation results are written to `evaluation/results.json`.

## Limitations

- The dataset is synthetic and contains 12 rows.
- Correlation does not establish causation.
- Model-based verification can still make mistakes.
- The project demonstrates agent orchestration, not model training or fine-tuning.

## References

- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)
- [Stanford CS336](https://cs336.stanford.edu/)
- [Stanford CS329A](https://cs329a.stanford.edu/)
