"""State schema for story generation graph."""

import operator
from typing import Annotated

from typing_extensions import TypedDict

from models import NarratedStory, StoryArchitecture, StoryInput
from tools.registry import ToolRegistry


class StoryGenerationState(TypedDict):
    """State for the story generation graph."""

    story_input: StoryInput
    tool_registry: ToolRegistry | None
    architecture: StoryArchitecture | None
    narrated_story: NarratedStory | None
    edited_narrations: Annotated[list[str], operator.add]  # Reducer for append
    current_narration_index: int
    output_dir: str
    architecture_saved: bool
    narrative_saved: bool
