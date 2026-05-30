from textual.screen     import Screen
from textual.app        import ComposeResult
from textual.containers import Horizontal
from textual.widgets    import Static, Input


class ConfigScreen(Screen):
    CSS = """
    Static { padding: 2; }
    #prompt-row {
        dock: bottom;
        border-top: solid $primary;
        height: 3;
        align: left middle;
    }
    #prompt-prefix { width: auto; padding: 0 1; color: $accent; text-style: bold; }
    #prompt { width: 1fr; border: none; background: transparent; }
    """

    def compose(self) -> ComposeResult:
        yield Static(
            "/config is coming in Phase 2.\nStay tuned.\n\n"
            "Press ESC or type  /back  to return.",
            id="msg"
        )
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