"""
Test that import order doesn't matter with lazy initialization.
This test imports agents.first BEFORE config to verify the fix.
"""
import sys
from pathlib import Path

# Add src to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_import_agents_before_config():
    """Test that importing agents.first before config doesn't cause errors."""
    # Import agents.first BEFORE config (would have failed before lazy initialization)
    from agents.first import get_agent

    # Now import config
    from config import settings

    # Verify that we can get the agent without errors
    agent = get_agent()
    assert agent is not None

    # Verify the agent is callable and has the invoke method
    assert hasattr(agent, "invoke")


def test_agent_invocation_with_reversed_imports():
    """Test that the agent actually works when imported before config."""
    # Import in reverse order again to ensure no side effects from previous test
    from agents.first import get_agent
    from config import settings

    # Test that the agent can actually be invoked successfully
    result = get_agent().invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )

    # Verify we got a valid result
    assert result is not None
    assert "messages" in result
    assert len(result["messages"]) > 0
