"""Agent discovery via Python entry points.

This module provides functions to discover and load agent implementations
from installed packages that register entry points.
"""

from importlib.metadata import entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents.protocols import Architect, Narrator


def discover_architects() -> dict[str, type]:
    """Discover all registered architects from installed packages.

    Returns:
        A dictionary mapping architect names to their classes.
    """
    eps = entry_points(group="storylord.architects")
    return {ep.name: ep.load() for ep in eps}


def discover_narrators() -> dict[str, type]:
    """Discover all registered narrators from installed packages.

    Returns:
        A dictionary mapping narrator names to their classes.
    """
    eps = entry_points(group="storylord.narrators")
    return {ep.name: ep.load() for ep in eps}


def get_architect(name: str) -> "Architect":
    """Get an architect instance by name.

    Args:
        name: The registered name of the architect.

    Returns:
        An instance of the requested architect.

    Raises:
        ValueError: If the architect name is not found.
    """
    architects = discover_architects()
    if name not in architects:
        available = ", ".join(sorted(architects.keys())) or "(none)"
        raise ValueError(f"Unknown architect '{name}'. Available: {available}")
    return architects[name]()


def get_narrator(name: str) -> "Narrator":
    """Get a narrator instance by name.

    Args:
        name: The registered name of the narrator.

    Returns:
        An instance of the requested narrator.

    Raises:
        ValueError: If the narrator name is not found.
    """
    narrators = discover_narrators()
    if name not in narrators:
        available = ", ".join(sorted(narrators.keys())) or "(none)"
        raise ValueError(f"Unknown narrator '{name}'. Available: {available}")
    return narrators[name]()


def list_architects() -> list[str]:
    """List all available architect names.

    Returns:
        A sorted list of registered architect names.
    """
    return sorted(discover_architects().keys())


def list_narrators() -> list[str]:
    """List all available narrator names.

    Returns:
        A sorted list of registered narrator names.
    """
    return sorted(discover_narrators().keys())
