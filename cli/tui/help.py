from textual.screen     import Screen
from textual.app        import ComposeResult
from textual.containers import Horizontal
from textual.widgets    import Static, Input

HELP_TEXT = """\
COMMAND       DESCRIPTION
──────────────────────────────────────────────────────
/install      Install Strap to %APPDATA%\\Strap
/update       Check for and apply updates from GitHub
/config       Configure Strap settings (Phase 2)
/help         Show this help message
/exit         Close the Strap CLI

Press ESC or type  /back  to return.
"""


class HelpScreen(Screen):
    CSS = """
    Static { padding: 2; }
    #prompt-row {
        dock: bottom;
        border-top: solid $primary;
        height: 3;
        align: left middle;
    }
    #prompt-prefix {
        width: auto;
        padding: 0 1;
        color: $accent;
        text-style: bold;
    }
    #prompt { width: 1fr; border: none; background: transparent; }
    """

    def compose(self) -> ComposeResult:
        yield Static(HELP_TEXT, id="help-text")
        with Horizontal(id="prompt-row"):
            yield Static(">>", id="prompt-prefix")
            yield Input(placeholder="", id="prompt")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip().lower()
        event.input.value = ""
        if cmd in ("/back", "/exit"):
            self.app.pop_screen()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()