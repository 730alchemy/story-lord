"""Protocol definitions for storylord agents.

These protocols define the contracts that all agent implementations must follow.
External packages can implement these protocols to create custom agents.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from models import ArchitectInput, NarratorInput, NarratedStory, StoryArchitecture
    from tools.registry import ToolRegistry


class Architect(Protocol):
    """Protocol for story architecture generators.

    Architects are responsible for creating the structural backbone of a story,
    including plot events and story beats.
    """

    name: str

    def generate(
        self,
        input: ArchitectInput,
        tools: ToolRegistry | None = None,
    ) -> StoryArchitecture:
        """Generate a story architecture from the given input.

        Args:
            input: The architect input parameters including story idea,
                   characters, and structural requirements.
            tools: Optional registry of tools the agent can use.

        Returns:
            A complete story architecture with plot events and beats.
        """
        ...


class Narrator(Protocol):
    """Protocol for narrative generators.

    Narrators transform story architectures into prose narratives,
    bringing the structural beats to life with descriptive text and dialogue.
    """

    name: str

    def generate(
        self,
        input: NarratorInput,
        tools: ToolRegistry | None = None,
    ) -> NarratedStory:
        """Generate narrative prose from a story architecture.

        Args:
            input: The narrator input including the story architecture,
                   characters, and tone.
            tools: Optional registry of tools the agent can use.

        Returns:
            A complete narrated story with prose for each beat.
        """
        ...
