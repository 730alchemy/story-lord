from langchain.agents import create_agent
from config import settings
from tools import get_weather


agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(result)
