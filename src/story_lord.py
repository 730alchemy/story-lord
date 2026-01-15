import argparse
from pathlib import Path

import structlog
import yaml

from config import settings  # noqa: F401
from models import ArchitectInput, EditorInput, NarratorInput, StoryInput
from agents.discovery import get_architect, get_editor, get_narrator
from tools.registry import ToolRegistry

log = structlog.get_logger(__name__)


def run_story_generation(input_file: str) -> None:
    """Generate a story from the given input file."""
    # Load input
    with open(input_file) as f:
        data = yaml.safe_load(f)
    story_input = StoryInput.model_validate(data)

    # Build tool registry from config
    tool_registry = ToolRegistry(story_input.tools) if story_input.tools else None

    # Get agents via entry point discovery
    architect = get_architect(story_input.architect)
    narrator = get_narrator(story_input.narrator)

    # Run architect
    log.info("running_architect", architect=story_input.architect)
    architect_input = ArchitectInput(
        story_idea=story_input.story_idea,
        characters=story_input.characters,
        num_plot_events=story_input.num_plot_events,
        beats_per_event=story_input.beats_per_event,
        tone=story_input.tone,
    )
    architecture = architect.generate(architect_input, tools=tool_registry)

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save architecture
    arch_path = output_dir / f"{story_input.output_file}_architecture.json"
    arch_path.write_text(architecture.model_dump_json(indent=2))
    log.info("architecture_saved", path=str(arch_path))

    # Run narrator
    log.info("running_narrator", narrator=story_input.narrator)
    narrator_input = NarratorInput(
        story_architecture=architecture,
        characters=story_input.characters,
        tone=story_input.tone,
    )
    narrated_story = narrator.generate(narrator_input, tools=tool_registry)

    # Run simile-smasher editor on each narration
    log.info("running_editor", editor="simile-smasher")
    editor = get_editor("simile-smasher")
    edited_narrations = []
    for narration in narrated_story.narrations:
        editor_input = EditorInput(text=narration.narrative_text)
        edited = editor.edit(editor_input)
        edited_narrations.append(edited.text)
        log.info("narration_edited", beat_reference=narration.beat_reference)

    # Save narrative
    narrative_path = output_dir / f"{story_input.output_file}_narrative.txt"
    narrative_text = "\n\n".join(edited_narrations)
    narrative_path.write_text(narrative_text)
    log.info("narrative_saved", path=str(narrative_path))


def run_tui() -> None:
    """Launch the TUI application."""
    from tui import StoryLordApp

    app = StoryLordApp()
    app.run()


def main():
    parser = argparse.ArgumentParser(description="AI-powered story generation")
    parser.add_argument("-f", "--file", help="YAML file with story parameters")
    args = parser.parse_args()

    if args.file:
        run_story_generation(args.file)
    else:
        run_tui()


if __name__ == "__main__":
    main()
