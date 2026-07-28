import asyncio
from agent_demo.agents import (
    create_analysis_agent,
    create_verifier_agent,
)


QUESTION = (
    "What is the Pearson correlation between weekly_usage_hours and churned? "
    "Report the number of complete observations and explain whether this "
    "correlation proves causation."
)


async def main() -> None:
    """Run one statistical analysis Agent task."""
    analysis_agent = create_analysis_agent()
    verifier_agent = create_verifier_agent()

    print("Question:")
    print(QUESTION)

    analysis_response = await analysis_agent.run(QUESTION)

    print("\nAnalysis response:")
    print(analysis_response.text)

    verification_request = f"""
    Original question:
    {QUESTION}

    Analysis response:
    {analysis_response.text}

    Independently verify this response.
    """

    verification_response = await verifier_agent.run(verification_request)

    print("\nVerifier response:")
    print(verification_response.text)


if __name__ == "__main__":
    asyncio.run(main())