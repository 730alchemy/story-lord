"""Agents module for storylord.

This module provides the agent abstraction layer for story generation.
Agents can be discovered via entry points from installed packages.
"""

from agents.protocols import Architect, Editor, Narrator
from agents.discovery import (
    discover_architects,
    discover_character_agent_types,
    discover_editors,
    discover_narrators,
    get_architect,
    get_character_agent_type,
    get_editor,
    get_narrator,
    list_architects,
    list_character_agent_types,
    list_editors,
    list_narrators,
)

# Import built-in agents from their respective modules
from agents.architect import DefaultArchitect
from agents.editor import DefaultEditor
from agents.narrative import DefaultNarrator

# Import character agent components
from agents.character import (
    AnswerInput,
    CharacterAgent,
    CharacterAgentType,
    CharacterRegistry,
    CharacterResponse,
    ChooseInput,
    SpeakInput,
    ThinkInput,
)
from agents.character.character_default import (
    DefaultCharacterAgent,
    DefaultCharacterAgentType,
)
from agents.character.character_mbti import MBTICharacterAgent, MBTICharacterAgentType

__all__ = [
    # Protocols
    "Architect",
    "Editor",
    "Narrator",
    # Discovery
    "discover_architects",
    "discover_character_agent_types",
    "discover_editors",
    "discover_narrators",
    "get_architect",
    "get_character_agent_type",
    "get_editor",
    "get_narrator",
    "list_architects",
    "list_character_agent_types",
    "list_editors",
    "list_narrators",
    # Built-in implementations
    "DefaultArchitect",
    "DefaultEditor",
    "DefaultNarrator",
    # Character agent protocols and models
    "AnswerInput",
    "CharacterAgent",
    "CharacterAgentType",
    "CharacterRegistry",
    "CharacterResponse",
    "ChooseInput",
    "SpeakInput",
    "ThinkInput",
    # Character agent implementations
    "DefaultCharacterAgent",
    "DefaultCharacterAgentType",
    "MBTICharacterAgent",
    "MBTICharacterAgentType",
]
