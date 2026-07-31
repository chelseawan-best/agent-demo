import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

from agent_demo.agents import (
    create_analysis_agent,
    create_revision_agent,
    create_verifier_agent,
)
from agent_demo.agent_tools import clear_tool_calls, get_tool_calls
from agent_demo.evaluation import used_expected_tool
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


def validate_ground_truth() -> None:
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

    print(f"\n{passed}/{len(tasks)} ground-truth checks passed")

    if passed != len(tasks):
        raise SystemExit(1)


async def run_online() -> None:
    """Run Analysis and Verifier agents and save their responses."""
    tasks = load_tasks()
    analysis_agent = create_analysis_agent()
    verifier_agent = create_verifier_agent()
    revision_agent = create_revision_agent()
    results = []

    for task in tasks:
        started = time.perf_counter()

        clear_tool_calls()
        analysis = await analysis_agent.run(task["question"])
        analysis_tool_calls = get_tool_calls()

        clear_tool_calls()
        verification_request = f"""
Original question:
{task["question"]}

Analysis response:
{analysis.text}

Independently verify this response.
"""
        verification = await verifier_agent.run(verification_request)
        verifier_tool_calls = get_tool_calls()

        revision_request = f"""
Original question:
{task["question"]}

Initial analysis:
{analysis.text}

Verifier feedback:
{verification.text}

Produce the final revised analysis.
"""
        revision = await revision_agent.run(revision_request)
        latency_seconds = time.perf_counter() - started

        results.append(
            {
                "id": task["id"],
                "question": task["question"],
                "analysis_response": analysis.text,
                "analysis_tool_calls": analysis_tool_calls,
                "analysis_used_expected_tool": used_expected_tool(
                    analysis_tool_calls, task
                ),
                "verifier_response": verification.text,
                "verifier_tool_calls": verifier_tool_calls,
                "final_analysis_response": revision.text,
                "ground_truth": task["expected"],
                "expected_tool": task["expected_tool"],
                "expected_tool_arguments": task["tool_arguments"],
                "latency_seconds": latency_seconds,
            }
        )
        analysis_status = (
            "PASS" if used_expected_tool(analysis_tool_calls, task) else "FAIL"
        )
        print(
            f"[COMPLETED] {task['id']} "
            f"analysis_tool={analysis_status}"
        )

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
        choices=["ground-truth", "online", "offline"],
        default="ground-truth",
        help="Use 'ground-truth' without an API or 'online' for the three-agent workflow.",
    )
    arguments = parser.parse_args()

    if arguments.mode in {"ground-truth", "offline"}:
        validate_ground_truth()
    else:
        asyncio.run(run_online())


if __name__ == "__main__":
    main()
