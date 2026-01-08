from config import settings
from agents.first import get_agent

print(
    get_agent().invoke(
        {
            "messages": [
                {"role": "user", "content": "hey bud, what is the weather in sf"}
            ]
        }
    )
)
