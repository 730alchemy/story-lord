import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import settings
from models import ArchitectInput, CharacterProfile, NarratorInput
from agents.architect import generate_story_architecture
from agents.narrator import generate_narration

# Define characters
characters = [
    CharacterProfile(
        name="Elijah Boondog",
        description="32 year old dentist with a passion for history. He is fit and smart, but also naive.",
        role="protagonist",
        motivations="Curiosity and passion for the truth sometimes get the better of him",
        relationships="Best friends with Jasper, but also a bit of a rival",
        backstory="Sometimes Elijah loses track of the world around him.",
    ),
    CharacterProfile(
        name="Jasper Dilsack",
        description="30 year old lawyer with a passion for winning more than justice. He is smart and charismatic, but also a bit of a know-it-all.",
        role="protagonist",
        motivations="To keep Elijah safe from the town's secrets",
        relationships="Best friends with Elijah. Although quite competitive with Elijah, he very much wants Elijah to be happy.",
        backstory="Jumped two grades in school, putting him in the same 7th grade class as Elijah.",
    ),
    CharacterProfile(
        name="Riley Thorn",
        description="A subtle manipulator. Plays chess in the small town park, hiding his alterior motives.",
        role="antagonist",
        motivations="Toy with Elijah and Jasper like a cat with a mouse, with no other purpose than to watch them squirm.",
        relationships="None",
        backstory="Made millions developing robots used in mining. Grew up in Greece.",
    ),
]

tone = "Tense thriller that uses dark humor to highlight the absurdity of the situation"

# Step 1: Generate story architecture
print("Step 1: Generating story architecture...")
print("=" * 60)

architect_input = ArchitectInput(
    story_idea="Two frenemies in their 30s, Elijah Boondog and Jasper Dilsack, get trapped in a small town while on vacation. Each setback that keeps them from leaving seems innocuous but add up to something sinister. Although Riley Thorn is behind the entrapment, in the end we find a 10 year old boy has been pulling the strings all along.",
    characters=characters,
    num_plot_events=2,
    beats_per_event=(1, 2),
    tone=tone,
)

story_architecture = generate_story_architecture(architect_input)

print("\nArchitecture generated:")
for i, event in enumerate(story_architecture.plot_events, 1):
    print(f"\n  Plot Event {i}: {event.title}")
    print(f"  Beats: {len(event.beats)}")

for i, event in enumerate(story_architecture.plot_events, 1):
    print(f"\n## Plot Event {i}: {event.title}")
    print(f"Summary: {event.summary}")
    print(f"\nBeats ({len(event.beats)}):")
    for j, beat in enumerate(event.beats, 1):
        chars = (
            ", ".join(beat.characters_involved) if beat.characters_involved else "None"
        )
        print(f"  {j}. [{beat.beat_type}] {beat.description}")
        print(f"     Characters: {chars}")

# Step 2: Generate narration
print("\n" + "=" * 60)
print("Step 2: Generating narration (3 iterations per beat)...")
print("=" * 60)

narrator_input = NarratorInput(
    story_architecture=story_architecture,
    characters=characters,
    tone=tone,
)

narrated_story = generate_narration(narrator_input)

# Display the complete narrated story
print("\n" + "=" * 60)
print("THE COMPLETE NARRATED STORY")
print("=" * 60)

for narration in narrated_story.narrations:
    print(f"\n--- {narration.beat_reference} ---\n")
    print(narration.narrative_text)

print("\n" + "=" * 60)
print("Narration complete!")
print(f"Total beats narrated: {len(narrated_story.narrations)}")
