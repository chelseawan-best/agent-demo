import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

from agent_demo.agents import (
    create_analysis_agent,
    create_verifier_agent,
)
from agent_demo.tools import (
    calculate_correlation,
    dataset_overview,
    describe_numeric_column,
)


PROJECT_ROOT = Path(__file__).parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample.csv"
TASKS_PATH = PROJECT_ROOT / "evaluation" / "tasks.json"
RESULTS_PATH = PROJECT_ROOT / "evaluation" / "results.json"


def load_tasks() -> list[dict[str, Any]]:
    """Load evaluation task definitions."""
    with TASKS_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def run_expected_tool(task: dict[str, Any]) -> dict:
    """Run the deterministic Python tool specified by one task."""
    tool_name = task["expected_tool"]
    arguments = task["tool_arguments"]

    if tool_name == "get_dataset_overview":
        return dataset_overview(DATA_PATH)
    if tool_name == "get_column_statistics":
        return describe_numeric_column(DATA_PATH, **arguments)
    if tool_name == "get_correlation":
        return calculate_correlation(DATA_PATH, **arguments)

    raise ValueError(f"Unknown expected tool: {tool_name}")


def matches_expected(actual: Any, expected: Any) -> bool:
    """Check whether actual data contains the expected subset."""
    if isinstance(expected, dict):
        return all(
            key in actual and matches_expected(actual[key], value)
            for key, value in expected.items()
        )

    if isinstance(expected, float):
        return abs(float(actual) - expected) <= 1e-8

    return actual == expected


def run_offline() -> None:
    """Validate deterministic statistical ground truth without an API."""
    tasks = load_tasks()
    passed = 0

    for task in tasks:
        actual = run_expected_tool(task)
        success = matches_expected(actual, task["expected"])
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {task['id']}")

        if success:
            passed += 1
        else:
            print("  expected:", task["expected"])
            print("  actual:", actual)

    print(f"\n{passed}/{len(tasks)} offline checks passed")

    if passed != len(tasks):
        raise SystemExit(1)


async def run_online() -> None:
    """Run Analysis and Verifier agents and save their responses."""
    tasks = load_tasks()
    analysis_agent = create_analysis_agent()
    verifier_agent = create_verifier_agent()
    results = []

    for task in tasks:
        started = time.perf_counter()
        analysis = await analysis_agent.run(task["question"])

        verification_request = f"""
Original question:
{task["question"]}

Analysis response:
{analysis.text}

Independently verify this response.
"""
        verification = await verifier_agent.run(verification_request)
        latency_seconds = time.perf_counter() - started

        results.append(
            {
                "id": task["id"],
                "question": task["question"],
                "analysis_response": analysis.text,
                "verifier_response": verification.text,
                "latency_seconds": latency_seconds,
            }
        )
        print(f"[COMPLETED] {task['id']}")

    RESULTS_PATH.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )
    print(f"\nResults written to {RESULTS_PATH}")


def main() -> None:
    """Select offline or online evaluation mode."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["offline", "online"],
        default="offline",
    )
    arguments = parser.parse_args()

    if arguments.mode == "offline":
        run_offline()
    else:
        asyncio.run(run_online())


if __name__ == "__main__":
    main()