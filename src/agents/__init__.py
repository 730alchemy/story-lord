"""Agents module for storylord.

This module provides the agent abstraction layer for story generation.
Agents can be discovered via entry points from installed packages.
"""

from agents.protocols import Architect, Narrator
from agents.discovery import (
    discover_architects,
    discover_narrators,
    get_architect,
    get_narrator,
    list_architects,
    list_narrators,
)

# Backward compatibility - import built-in agents
from agents.builtins import DefaultArchitect, DefaultNarrator

__all__ = [
    # Protocols
    "Architect",
    "Narrator",
    # Discovery
    "discover_architects",
    "discover_narrators",
    "get_architect",
    "get_narrator",
    "list_architects",
    "list_narrators",
    # Built-in implementations
    "DefaultArchitect",
    "DefaultNarrator",
]
