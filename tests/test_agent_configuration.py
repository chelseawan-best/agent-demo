from agent_demo.agent_tools import (
    get_column_statistics,
    get_correlation,
    get_dataset_overview,
)
from agent_demo.agents import (
    create_analysis_agent,
    create_verifier_agent,
)


def test_agent_tools_have_expected_metadata() -> None:
    tools = [
        get_dataset_overview,
        get_column_statistics,
        get_correlation,
    ]

    assert [tool.name for tool in tools] == [
        "get_dataset_overview",
        "get_column_statistics",
        "get_correlation",
    ]

    for tool in tools:
        assert tool.description


def test_agents_can_be_created_without_api_call(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")

    analysis_agent = create_analysis_agent()
    verifier_agent = create_verifier_agent()

    assert analysis_agent.name == "StatisticalAnalysisAgent"
    assert verifier_agent.name == "StatisticalVerifierAgent"
