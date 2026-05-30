import os
import sys
from contextlib import redirect_stdout
from textual import work
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Input, RichLog
from ops.startup import is_startup_enabled

class UpdateScreen(Screen):
    CSS = """
    RichLog { width: 1fr; height: 1fr; border: solid $primary; padding: 1; background: $surface; }
    #prompt-row { dock: bottom; border-top: solid $primary; height: 3; align: left middle; }
    #prompt-prefix { width: auto; padding: 0 1; color: $accent; text-style: bold; }
    #prompt { width: 1fr; border: none; background: transparent; }
    """

    def compose(self) -> ComposeResult:
        yield RichLog(id="term-log", highlight=True, markup=True)
        with Horizontal(id="prompt-row"):
            yield Static(">>", id="prompt-prefix")
            yield Input(placeholder="", id="prompt")

    def on_mount(self) -> None:
        self.log_widget = self.query_one("#term-log", RichLog)
        self.input_widget = self.query_one("#prompt", Input)
        
        self.step = 0
        self.startup_confirmed = False

        # If startup is not enabled, ask. If it is, skip directly to updating.
        if not is_startup_enabled():
            self.log_widget.write("Strap isn't configured to start on boot.")
            self.log_widget.write("Do you want to enable it now? (yes/no):")
            self.step = 1
        else:
            self.start_update()

    def is_yes(self, text: str) -> bool:
        return text in {"yes", "ya", "yeah", "yea","y", "yep", "yup", "sure"}

    def is_no(self, text: str) -> bool:
        return text in {"no", "nah", "n", "nope"}

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip().lower()
        event.input.value = ""

        # Global exit commands
        if raw.lstrip("/") in ("back", "exit"):
            self.app.pop_screen()
            self.app.push_screen("home")
            return

        # Handle Startup Question
        if self.step == 1:
            if self.is_yes(raw):
                self.startup_confirmed = True
                self.log_widget.write(f">> {raw}")
                self.start_update()
            elif self.is_no(raw):
                self.startup_confirmed = False
                self.log_widget.write(f">> {raw}")
                self.start_update()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

    def start_update(self):
        self.step = 2
        self.input_widget.disabled = True # Lock input while updating
        self.run_update()

    @work(exclusive=True, thread=True)
    def run_update(self) -> None:
        from ops.updater import run

        class OutputRedirector:
            def __init__(self, app, log_widget):
                self.app = app
                self.log_widget = log_widget
            def write(self, s):
                if s.strip():
                    self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run(enable_startup_flag=self.startup_confirmed)
            self.app.call_from_thread(self.log_widget.write, "\nPress ESC or type /back to return.")
            
        self.app.call_from_thread(self.enable_input)

    def enable_input(self):
        self.input_widget.disabled = False
        self.input_widget.focus()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()
            self.app.push_screen("home")