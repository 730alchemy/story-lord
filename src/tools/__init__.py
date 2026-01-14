"""Tools module for storylord.

This module provides the tool abstraction layer that allows agents to use
external tools during story generation.
"""

from tools.protocols import Tool
from tools.registry import ToolRegistry
from tools.discovery import discover_tools, get_tool, list_tools

__all__ = [
    "Tool",
    "ToolRegistry",
    "discover_tools",
    "get_tool",
    "list_tools",
]
