from agent_demo.agent_tools import (
    get_column_statistics,
    get_correlation,
    get_dataset_overview,
)
from agent_demo.agents import (
    create_analysis_agent,
    create_revision_agent,
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
    monkeypatch.setenv("LLM_API_KEY", "offline-test-key")
    monkeypatch.setenv("LLM_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("ANALYSIS_MODEL", "provider/analysis-model")
    monkeypatch.setenv("VERIFIER_MODEL", "provider/verifier-model")

    analysis_agent = create_analysis_agent()
    verifier_agent = create_verifier_agent()
    revision_agent = create_revision_agent()

    assert analysis_agent.name == "StatisticalAnalysisAgent"
    assert verifier_agent.name == "StatisticalVerifierAgent"
    assert revision_agent.name == "StatisticalRevisionAgent"
    assert analysis_agent.client.model == "provider/analysis-model"
    assert verifier_agent.client.model == "provider/verifier-model"
    assert revision_agent.client.model == "provider/analysis-model"
    assert analysis_agent.client.base_url == "https://example.test/v1"
    assert verifier_agent.client.base_url == "https://example.test/v1"
