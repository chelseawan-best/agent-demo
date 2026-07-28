import os

from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

from agent_demo.agent_tools import (
    get_column_statistics,
    get_correlation,
    get_dataset_overview,
)
from agent_demo.prompts import ANALYSIS_AGENT_INSTRUCTIONS


DEFAULT_MODEL = "gpt-5.6-terra"


def create_analysis_agent():
    """Create the tool-using statistical analysis agent."""
    load_dotenv()

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    client = OpenAIChatClient(model=model)

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
