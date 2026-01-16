"""Node functions for story generation graph."""

from pathlib import Path
from typing import Literal

import structlog

from agents.discovery import get_architect, get_editor, get_narrator
from graph.state import StoryGenerationState
from models import ArchitectInput, EditorInput, NarratorInput
from tools.registry import ToolRegistry

log = structlog.get_logger(__name__)


def load_input_node(state: StoryGenerationState) -> dict:
    """Initialize tool_registry and tracking flags."""
    story_input = state["story_input"]
    tool_registry = ToolRegistry(story_input.tools) if story_input.tools else None

    return {
        "tool_registry": tool_registry,
    }


def architect_node(state: StoryGenerationState) -> dict:
    """Run the architect agent to generate story architecture."""
    story_input = state["story_input"]
    tool_registry = state["tool_registry"]

    architect = get_architect(story_input.architect)
    log.info("running_architect", architect=story_input.architect)

    architect_input = ArchitectInput(
        story_idea=story_input.story_idea,
        characters=story_input.characters,
        num_plot_events=story_input.num_plot_events,
        beats_per_event=story_input.beats_per_event,
        tone=story_input.tone,
    )
    architecture = architect.generate(architect_input, tools=tool_registry)

    return {"architecture": architecture}


def save_architecture_node(state: StoryGenerationState) -> dict:
    """Save architecture to JSON file (idempotent)."""
    if state["architecture_saved"]:
        return {}

    story_input = state["story_input"]
    architecture = state["architecture"]
    output_dir = Path(state["output_dir"])

    output_dir.mkdir(exist_ok=True)
    arch_path = output_dir / f"{story_input.output_file}_architecture.json"
    arch_path.write_text(architecture.model_dump_json(indent=2))
    log.info("architecture_saved", path=str(arch_path))

    return {"architecture_saved": True}


def narrator_node(state: StoryGenerationState) -> dict:
    """Run the narrator agent to generate narrations."""
    story_input = state["story_input"]
    architecture = state["architecture"]
    tool_registry = state["tool_registry"]

    narrator = get_narrator(story_input.narrator)
    log.info("running_narrator", narrator=story_input.narrator)

    narrator_input = NarratorInput(
        story_architecture=architecture,
        characters=story_input.characters,
        tone=story_input.tone,
    )
    narrated_story = narrator.generate(narrator_input, tools=tool_registry)

    return {"narrated_story": narrated_story}


def editor_node(state: StoryGenerationState) -> dict:
    """Edit one narration at a time for checkpoint granularity."""
    narrated_story = state["narrated_story"]
    current_index = state["current_narration_index"]

    narration = narrated_story.narrations[current_index]

    log.info("running_editor", editor="simile-smasher")
    editor = get_editor("simile-smasher")
    editor_input = EditorInput(text=narration.narrative_text)
    edited = editor.edit(editor_input)
    log.info("narration_edited", beat_reference=narration.beat_reference)

    return {
        "edited_narrations": [edited.text],  # Uses reducer to append
        "current_narration_index": current_index + 1,
    }


def save_narrative_node(state: StoryGenerationState) -> dict:
    """Save narrative to text file (idempotent)."""
    if state["narrative_saved"]:
        return {}

    story_input = state["story_input"]
    edited_narrations = state["edited_narrations"]
    output_dir = Path(state["output_dir"])

    output_dir.mkdir(exist_ok=True)
    narrative_path = output_dir / f"{story_input.output_file}_narrative.txt"
    narrative_text = "\n\n".join(edited_narrations)
    narrative_path.write_text(narrative_text)
    log.info("narrative_saved", path=str(narrative_path))

    return {"narrative_saved": True}


def should_continue_editing(
    state: StoryGenerationState,
) -> Literal["editor", "save_narrative"]:
    """Determine if there are more narrations to edit."""
    narrated_story = state["narrated_story"]
    current_index = state["current_narration_index"]

    if current_index < len(narrated_story.narrations):
        return "editor"
    return "save_narrative"
