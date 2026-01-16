"""Agents module for storylord.

This module provides the agent abstraction layer for story generation.
Agents can be discovered via entry points from installed packages.
"""

from agents.protocols import Architect, Editor, Narrator
from agents.discovery import (
    discover_architects,
    discover_editors,
    discover_narrators,
    get_architect,
    get_editor,
    get_narrator,
    list_architects,
    list_editors,
    list_narrators,
)

# Import built-in agents from their respective modules
from agents.architect import DefaultArchitect
from agents.editor import DefaultEditor
from agents.narrative import DefaultNarrator

__all__ = [
    # Protocols
    "Architect",
    "Editor",
    "Narrator",
    # Discovery
    "discover_architects",
    "discover_editors",
    "discover_narrators",
    "get_architect",
    "get_editor",
    "get_narrator",
    "list_architects",
    "list_editors",
    "list_narrators",
    # Built-in implementations
    "DefaultArchitect",
    "DefaultEditor",
    "DefaultNarrator",
]
