"""StoryLord TUI application."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static


class StoryLordApp(App):
    """Main TUI application for StoryLord."""

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Welcome to storyland")
        yield Footer()
