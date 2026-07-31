from agent_demo.evaluation import used_expected_tool


def test_used_expected_tool_checks_name_and_arguments() -> None:
    task = {
        "expected_tool": "get_correlation",
        "tool_arguments": {
            "column_x": "weekly_usage_hours",
            "column_y": "churned",
        },
    }
    tool_calls = [
        {"name": "get_dataset_overview", "arguments": {}},
        {
            "name": "get_correlation",
            "arguments": {
                "column_x": "weekly_usage_hours",
                "column_y": "churned",
            },
        },
    ]

    assert used_expected_tool(tool_calls, task)


def test_used_expected_tool_rejects_wrong_arguments() -> None:
    task = {
        "expected_tool": "get_column_statistics",
        "tool_arguments": {"column": "monthly_price"},
    }
    tool_calls = [
        {
            "name": "get_column_statistics",
            "arguments": {"column": "weekly_usage_hours"},
        }
    ]

    assert not used_expected_tool(tool_calls, task)
