from langchain.agents import create_agent
from tools import get_weather


_agent = None


def get_agent():
    """Get or create the agent instance (lazy initialization)."""
    global _agent
    if _agent is None:
        _agent = create_agent(
            model="anthropic:claude-sonnet-4-5-20250929",
            tools=[get_weather],
            system_prompt="You are a helpful assistant",
        )
    return _agent
