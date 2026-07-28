# Statistical Agent Demo

A small Microsoft Agent Framework project for answering statistical questions about a synthetic subscription dataset. An analysis agent selects deterministic Python tools, and a verifier agent independently checks the response.

## How It Works

```text
Question -> Analysis Agent -> Python Tool -> Answer -> Verifier Agent
```

- The LLM selects the calculation and explains the result.
- pandas performs the numerical computation.
- A second agent re-runs tools and returns `PASS` or `REVISE`.
- Offline evaluation checks the statistical ground truth without an API.

## Project Structure

```text
agent-demo/
|-- data/sample.csv
|-- evaluation/
|   |-- tasks.json
|   `-- evaluate.py
|-- src/agent_demo/
|   |-- tools.py          # Statistical functions
|   |-- agent_tools.py    # Microsoft Agent Framework tool wrappers
|   |-- prompts.py        # Agent instructions
|   |-- agents.py         # Analysis and verifier agent factories
|   `-- run_demo.py       # End-to-end demo
|-- tests/
|-- .env.example
`-- pyproject.toml
```

## Setup

Requirements: Python 3.11+, [`uv`](https://docs.astral.sh/uv/), and an OpenAI API key for live runs.

```bash
git clone https://github.com/chelseawan-best/agent-demo.git
cd agent-demo
uv sync --group dev
```

For live execution, create `.env` locally:

```dotenv
OPENAI_API_KEY=your_official_openai_api_key
OPENAI_MODEL=gpt-5.6-terra
```

Do not commit `.env`.

## Run

Run the tests:

```bash
uv run pytest -v
```

Run the offline evaluation without an API key:

```bash
PYTHONPATH=src uv run python evaluation/evaluate.py --mode offline
```

Run one live Analysis -> Verifier task:

```bash
PYTHONPATH=src uv run python -m agent_demo.run_demo
```

Run all evaluation tasks through both agents:

```bash
PYTHONPATH=src uv run python evaluation/evaluate.py --mode online
```

Online results are written to `evaluation/results.json`.

## Current Status

- 7 tests pass.
- 3/3 offline evaluation tasks pass.
- Live execution is implemented but has not yet been measured with an official API key.

## Limitations

- The dataset is synthetic and contains 12 rows.
- Pearson correlation does not establish causation.
- The verifier is also model-based and may make mistakes.
- This project demonstrates agent orchestration and evaluation; it does not train or fine-tune a model.

## References

- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)
- [Stanford CS336](https://cs336.stanford.edu/)
- [Stanford CS329A](https://cs329a.stanford.edu/)
