from typing import Any


def used_expected_tool(tool_calls: list[dict], task: dict[str, Any]) -> bool:
    """Check whether an agent called the expected tool with expected arguments."""
    return any(
        call["name"] == task["expected_tool"]
        and call["arguments"] == task["tool_arguments"]
        for call in tool_calls
    )
