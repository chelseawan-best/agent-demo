import os

from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from agent_demo.agent_tools import (
    get_column_statistics,
    get_correlation,
    get_dataset_overview,
)
from agent_demo.prompts import (
    ANALYSIS_AGENT_INSTRUCTIONS,
    REVISION_AGENT_INSTRUCTIONS,
    VERIFIER_AGENT_INSTRUCTIONS,
)


DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_ANALYSIS_MODEL = "openai/gpt-4.1-mini"
DEFAULT_VERIFIER_MODEL = "google/gemini-2.5-flash"


def create_model_client(model_env_name: str, default_model: str):
    """Create an OpenAI-compatible client from provider-neutral settings."""
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY is not set. Add it to your local .env file.")

    return OpenAIChatCompletionClient(
        model=os.getenv(model_env_name, default_model),
        api_key=api_key,
        base_url=os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL),
    )


def create_analysis_agent():
    """Create the tool-using statistical analysis agent."""
    client = create_model_client("ANALYSIS_MODEL", DEFAULT_ANALYSIS_MODEL)

    agent = client.as_agent(
        name="StatisticalAnalysisAgent",
        description="Analyzes the synthetic subscription dataset with verified Python tools.",
        instructions=ANALYSIS_AGENT_INSTRUCTIONS,
        tools=[
            get_dataset_overview,
            get_column_statistics,
            get_correlation,
        ],
    )

    return agent


def create_verifier_agent():
    """Create a verifier that can use a model different from the analyst."""
    client = create_model_client("VERIFIER_MODEL", DEFAULT_VERIFIER_MODEL)

    agent = client.as_agent(
        name="StatisticalVerifierAgent",
        description="Independently verifies statistical claims with Python tools.",
        instructions=VERIFIER_AGENT_INSTRUCTIONS,
        tools=[
            get_dataset_overview,
            get_column_statistics,
            get_correlation,
        ],
    )

    return agent


def create_revision_agent():
    """Create a final editor that reconciles analysis and verified evidence."""
    client = create_model_client("ANALYSIS_MODEL", DEFAULT_ANALYSIS_MODEL)

    return client.as_agent(
        name="StatisticalRevisionAgent",
        description="Produces the final analysis after checking verifier feedback.",
        instructions=REVISION_AGENT_INSTRUCTIONS,
    )
