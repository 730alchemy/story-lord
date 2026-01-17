"""Character agents module for storylord.

This module provides character agent abstractions for story generation.
Character agents embody individual characters with personality-driven
dialogue, thoughts, decisions, and the ability to answer questions.

Character agent types can be discovered via entry points from installed packages.
"""

from agents.character.protocols import (
    AnswerInput,
    CharacterAgent,
    CharacterAgentType,
    CharacterResponse,
    ChooseInput,
    SpeakInput,
    ThinkInput,
)
from agents.character.registry import CharacterRegistry

__all__ = [
    # Protocols
    "CharacterAgent",
    "CharacterAgentType",
    # Input/Output models
    "AnswerInput",
    "CharacterResponse",
    "ChooseInput",
    "SpeakInput",
    "ThinkInput",
    # Registry
    "CharacterRegistry",
]
