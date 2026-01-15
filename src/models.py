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


class StoryInput(BaseModel):
    """Input for the complete story generation pipeline."""

    story_idea: str
    characters: list[CharacterProfile]
    num_plot_events: int
    beats_per_event: tuple[int, int]  # (min, max) range
    tone: str
    output_file: str

    # Agent and tool selection (discovered via entry points)
    architect: str = "default"
    narrator: str = "default"
    tools: list[str] | None = None


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


# Narrator agent models


class NarratorInput(BaseModel):
    """Input parameters for the narrator agent."""

    story_architecture: StoryArchitecture
    characters: list[CharacterProfile]
    tone: str


class BeatNarration(BaseModel):
    """Narrative text for a single story beat."""

    narrative_text: str
    beat_reference: str  # e.g., "Event 1, Beat 2"


class ConflictEvaluation(BaseModel):
    """Result of evaluating narrative against the story corpus."""

    conflicts_found: list[str]
    revised_narrative: str


class NarratedStory(BaseModel):
    """Complete narrated story output."""

    narrations: list[BeatNarration]


# Editor agent models


class EditorInput(BaseModel):
    """Input parameters for the editor agent."""

    text: str


class EditedText(BaseModel):
    """Output from the editor agent."""

    text: str
