"""StoryLord TUI application."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Input, Static, TextArea

from agents.discovery import get_editor, list_architects, list_editors, list_narrators
from models import EditorInput


class EditorScreen(ModalScreen):
    """Screen for running the editor agent."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("ctrl+r", "run_editor", "Run"),
        Binding("ctrl+o", "load_file", "Open"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Editor - Enter text to improve", id="editor-title")
            yield Static("Input:", id="input-label")
            yield TextArea(id="editor-input")
            yield Static("Output:", id="output-label")
            yield TextArea(id="editor-output", read_only=True)
            yield Footer()

    def action_run_editor(self) -> None:
        """Run the editor agent on the input text."""
        input_area = self.query_one("#editor-input", TextArea)
        output_area = self.query_one("#editor-output", TextArea)
        text = input_area.text

        if not text.strip():
            output_area.text = "No input text provided."
            return

        editor = get_editor("default")
        result = editor.edit(EditorInput(text=text))
        output_area.text = result.text

    def action_load_file(self) -> None:
        """Prompt for a file path and load its contents."""
        self.app.push_screen(FileInputModal(), self._load_file_callback)

    def _load_file_callback(self, file_path: str | None) -> None:
        """Load the file contents into the input area."""
        if file_path:
            try:
                with open(file_path) as f:
                    content = f.read()
                input_area = self.query_one("#editor-input", TextArea)
                input_area.text = content
            except FileNotFoundError:
                output_area = self.query_one("#editor-output", TextArea)
                output_area.text = f"File not found: {file_path}"
            except Exception as e:
                output_area = self.query_one("#editor-output", TextArea)
                output_area.text = f"Error loading file: {e}"


class FileInputModal(ModalScreen[str | None]):
    """Modal for entering a file path."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical():
                yield Static("Enter file path:")
                yield Input(id="file-path-input", placeholder="/path/to/file.txt")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in the input."""
        self.dismiss(event.value)

    def action_cancel(self) -> None:
        """Cancel and return None."""
        self.dismiss(None)


class AgentsModal(ModalScreen):
    """Modal screen displaying available agents."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        architects = list_architects()
        narrators = list_narrators()
        editors = list_editors()

        content = ["Available Agents", ""]
        content.append("Architects:")
        content.extend(f"  - {name}" for name in architects)
        content.append("")
        content.append("Narrators:")
        content.extend(f"  - {name}" for name in narrators)
        content.append("")
        content.append("Editors:")
        content.extend(f"  - {name}" for name in editors)
        content.append("")
        content.append("Press ESC to close")

        with Center():
            with Vertical():
                yield Static("\n".join(content))


class StoryLordApp(App):
    """Main TUI application for StoryLord."""

    BINDINGS = [
        Binding("ctrl+a", "show_agents", "Agents"),
        Binding("ctrl+e", "show_editor", "Editor"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Welcome to storyland")
        yield Footer()

    def action_show_agents(self) -> None:
        """Show the agents modal."""
        self.push_screen(AgentsModal())

    def action_show_editor(self) -> None:
        """Show the editor screen."""
        self.push_screen(EditorScreen())
