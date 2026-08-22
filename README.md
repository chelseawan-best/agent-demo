# Travel Planner Agent

This branch is the minimal starting point for a single-agent travel planner.

## Current flow

```text
user request -> LLM agent -> flight/hotel/activity tools -> travel plan
```

The three tools currently return deterministic demo data. They are intentionally
small so they can later be replaced by real API adapters without changing the
agent interface.

## Run

Set `OPENAI_API_KEY` (or the Azure variables described in `utils/models.py`),
then run:

```bash
langgraph dev
```

The graph is registered in `langgraph.json`.

## Deliberately not included yet

This first version does not include bookings, multi-agent delegation, skills,
file-system tools, memory, databases, or external travel APIs. Those will be
added as separate feature branches after the single-agent loop is understood.

## Reference

The `reference` branch contains the original MIT-licensed workshop. This branch
is a smaller reimplementation, not a production booking system.
