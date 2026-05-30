import os
import sys
from contextlib import redirect_stdout
from textual import work
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Input, RichLog

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

class InstallScreen(Screen):
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
        self.reinstall_confirmed = False
        self.startup_confirmed = False

        # Step 1: Check if already installed
        if os.path.exists(INSTALL_DIR):
            self.log_widget.write(f"Strap is already installed at {INSTALL_DIR}.")
            self.log_widget.write("Do you want to reinstall and overwrite it? (yes/no):")
            self.step = 1
        else:
            self.ask_startup()

    def ask_startup(self):
        self.log_widget.write("\nDo you want Strap to automatically start on boot? (yes/no):")
        self.step = 2

    def is_yes(self, text: str) -> bool:
        return text in {"yes", "ya", "yeah", "y", "yep", "yup"}

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

        # Handle Reinstall Question
        if self.step == 1:
            if self.is_yes(raw):
                self.reinstall_confirmed = True
                self.log_widget.write(f">> {raw}")
                self.ask_startup()
            elif self.is_no(raw):
                self.log_widget.write(f">> {raw}")
                self.log_widget.write("\nInstallation aborted. Press ESC or type /back to return.")
                self.step = 3 # Mark as done
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

        # Handle Startup Question
        elif self.step == 2:
            if self.is_yes(raw):
                self.startup_confirmed = True
                self.log_widget.write(f">> {raw}")
                self.start_install()
            elif self.is_no(raw):
                self.startup_confirmed = False
                self.log_widget.write(f">> {raw}")
                self.start_install()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

    def start_install(self):
        self.step = 3
        self.input_widget.disabled = True # Lock input while installing
        self.run_install()

    @work(exclusive=True, thread=True)
    def run_install(self) -> None:
        from ops.installer import run

        class OutputRedirector:
            def __init__(self, app, log_widget):
                self.app = app
                self.log_widget = log_widget
            def write(self, s):
                if s.strip():
                    self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run(reinstall=self.reinstall_confirmed, enable_startup_flag=self.startup_confirmed)
            self.app.call_from_thread(self.log_widget.write, "\nPress ESC or type /back to return.")
            
        self.app.call_from_thread(self.enable_input)

    def enable_input(self):
        self.input_widget.disabled = False
        self.input_widget.focus()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()
            self.app.push_screen("home")