import asyncio

from agent_demo.agents import create_analysis_agent


QUESTION = (
    "What is the Pearson correlation between weekly_usage_hours and churned? "
    "Report the number of complete observations and explain whether this "
    "correlation proves causation."
)


async def main() -> None:
    """Run one statistical analysis Agent task."""
    agent = create_analysis_agent()

    print("Question:")
    print(QUESTION)

    response = await agent.run(QUESTION)

    print("\nAgent response:")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())