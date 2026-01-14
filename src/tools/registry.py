"""Runtime tool registry for agents.

This module provides the ToolRegistry class that agents use to access
and execute tools during story generation.
"""

import structlog
from typing import Any

from tools.discovery import discover_tools
from tools.protocols import Tool

log = structlog.get_logger(__name__)


class ToolRegistry:
    """Runtime registry of tools available to an agent.

    The registry loads and instantiates tools by name, providing a unified
    interface for agents to discover tool schemas and execute tools.
    """

    def __init__(self, tool_names: list[str] | None = None):
        """Initialize the registry with the specified tools.

        Args:
            tool_names: List of tool names to load. If None, no tools are loaded.
        """
        self._tools: dict[str, Tool] = {}

        if tool_names:
            available = discover_tools()
            for name in tool_names:
                if name in available:
                    self._tools[name] = available[name]()
                    log.debug("tool_loaded", tool=name)
                else:
                    log.warning("tool_not_found", tool=name)

    def get(self, name: str) -> Tool:
        """Get a tool by name.

        Args:
            name: The name of the tool.

        Returns:
            The tool instance.

        Raises:
            KeyError: If the tool is not in the registry.
        """
        return self._tools[name]

    def list_tools(self) -> list[dict]:
        """Return tool schemas for LLM function calling.

        Returns:
            A list of tool schema dictionaries suitable for LLM binding.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.get_schema(),
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, **params: Any) -> Any:
        """Execute a tool by name.

        Args:
            name: The name of the tool to execute.
            **params: The parameters to pass to the tool.

        Returns:
            The result of the tool execution.

        Raises:
            KeyError: If the tool is not in the registry.
        """
        log.info("tool_executing", tool=name, params=params)
        result = self._tools[name].execute(**params)
        log.info("tool_executed", tool=name)
        return result

    def __len__(self) -> int:
        """Return the number of tools in the registry."""
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """Check if a tool is in the registry."""
        return name in self._tools
