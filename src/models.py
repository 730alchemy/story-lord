from pydantic import BaseModel


class CharacterProfile(BaseModel):
    """A character in the story with their profile details."""

    name: str
    description: str
    role: str  # protagonist, antagonist, supporting, etc.
    motivations: str
    relationships: str  # relationships to other characters
    backstory: str


class ArchitectInput(BaseModel):
    """Input parameters for the architect agent."""

    story_idea: str
    characters: list[CharacterProfile]
    num_plot_events: int
    beats_per_event: tuple[int, int]  # (min, max) range
    tone: str


class StoryBeat(BaseModel):
    """A narrative event within a plot event."""

    description: str
    beat_type: str  # conversation, action, occurrence, internal_dialogue, etc.
    characters_involved: list[str]


class PlotEvent(BaseModel):
    """A major plot point containing story beats."""

    title: str
    summary: str
    beats: list[StoryBeat]


class StoryArchitecture(BaseModel):
    """Complete story structure with all plot events and their beats."""

    plot_events: list[PlotEvent]
