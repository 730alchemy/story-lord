"""Graph construction for story generation workflow."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    architect_node,
    editor_node,
    load_input_node,
    narrator_node,
    save_architecture_node,
    save_narrative_node,
    should_continue_editing,
)
from graph.state import StoryGenerationState


def build_story_generation_graph(checkpointer=None):
    """Build the story generation graph.

    Args:
        checkpointer: Optional checkpointer for persistence.
                     Defaults to MemorySaver if not provided.

    Returns:
        Compiled graph ready for invocation.
    """
    builder = StateGraph(StoryGenerationState)

    # Add nodes
    builder.add_node("load_input", load_input_node)
    builder.add_node("architect", architect_node)
    builder.add_node("save_architecture", save_architecture_node)
    builder.add_node("narrator", narrator_node)
    builder.add_node("editor", editor_node)
    builder.add_node("save_narrative", save_narrative_node)

    # Linear flow with editor loop
    builder.add_edge(START, "load_input")
    builder.add_edge("load_input", "architect")
    builder.add_edge("architect", "save_architecture")
    builder.add_edge("save_architecture", "narrator")
    builder.add_edge("narrator", "editor")
    builder.add_conditional_edges(
        "editor",
        should_continue_editing,
        {"editor": "editor", "save_narrative": "save_narrative"},
    )
    builder.add_edge("save_narrative", END)

    return builder.compile(checkpointer=checkpointer or MemorySaver())
