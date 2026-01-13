import argparse
from pathlib import Path

import structlog
import yaml

from config import settings
from models import ArchitectInput, NarratorInput, StoryInput
from agents import generate_story_architecture, generate_narration

log = structlog.get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Generate a story from input parameters")
    parser.add_argument("input_file", help="YAML file with story parameters")
    args = parser.parse_args()

    # Load input
    with open(args.input_file) as f:
        data = yaml.safe_load(f)
    story_input = StoryInput.model_validate(data)

    # Run architect
    log.info("running_architect")
    architect_input = ArchitectInput(
        story_idea=story_input.story_idea,
        characters=story_input.characters,
        num_plot_events=story_input.num_plot_events,
        beats_per_event=story_input.beats_per_event,
        tone=story_input.tone,
    )
    architecture = generate_story_architecture(architect_input)

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save architecture
    arch_path = output_dir / f"{story_input.output_file}_architecture.json"
    arch_path.write_text(architecture.model_dump_json(indent=2))
    log.info("architecture_saved", path=str(arch_path))

    # Run narrator
    log.info("running_narrator")
    narrator_input = NarratorInput(
        story_architecture=architecture,
        characters=story_input.characters,
        tone=story_input.tone,
    )
    narrated_story = generate_narration(narrator_input)

    # Save narrative
    narrative_path = output_dir / f"{story_input.output_file}_narrative.txt"
    narrative_text = "\n\n".join(n.narrative_text for n in narrated_story.narrations)
    narrative_path.write_text(narrative_text)
    log.info("narrative_saved", path=str(narrative_path))


if __name__ == "__main__":
    main()
