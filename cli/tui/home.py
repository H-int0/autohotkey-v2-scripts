import os
import subprocess

from contextlib import redirect_stdout
from textual import work
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input, RichLog
from config.manager import load_user_config
from config.schema import DEFAULT_CONFIG
from ops.startup import is_startup_enabled
from tui.help_text import (
    COMMANDS_TEXT, CONFIG_COMMANDS_TEXT, get_status_text, 
    get_config_z_text, CONFIG_U1_TEXT, CONFIG_U2_TEXT, 
    CONFIG_U3_TEXT, CONFIG_U4_TEXT
)

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

class HomeScreen(Screen):
    CSS_PATH = "home.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.command_queue = []
        self.state = "idle" 
        self.reinstall_confirmed = False
        self.startup_confirmed = False

    def _is_ahk_running(self) -> bool:
        try:
            out = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq AutoHotkey*"', 
                shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            return "AutoHotkey" in out
        except Exception:
            return False

    def update_status(self, focused_flag: str = "", focused_no: int = 0):
        cfg = load_user_config()
        st_tz = cfg.get("startupTZID", "")
        
        status_text = get_status_text(
            version=cfg.get('version', DEFAULT_CONFIG['version']),
            is_installed=os.path.exists(INSTALL_DIR),
            startup_enabled=is_startup_enabled(),
            ahk_running=self._is_ahk_running(),
            st_tz=st_tz
        )

        hints = self._build_hints(focused_flag, focused_no)
        self.query_one("#status-text", Static).update(status_text)
        self.query_one("#commands-text", Static).update(COMMANDS_TEXT)
        self.query_one("#hints-text", Static).update(hints)

    def _build_hints(self, flag: str, no: int) -> str:
        if not flag or not no:
            return CONFIG_COMMANDS_TEXT
        if flag == "z":
            return get_config_z_text(no)
        if flag == "u":
            if no == 1: return CONFIG_U1_TEXT
            if no == 2: return CONFIG_U2_TEXT
            if no == 3: return CONFIG_U3_TEXT
            if no == 4: return CONFIG_U4_TEXT
        return ""

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="left-panel"):
                # Wraps the text so it scrolls, but leaves the footer outside to pin it
                with ScrollableContainer(id="home-left-content"):
                    yield Static("", id="status-text")
                    yield Static("", id="commands-text")
                    yield Static("", id="hints-text")
                yield Static("SPDX-License-Identifier: GPL-3.0-or-later\nCopyright (C) 2026 H-int0", id="footer-text")
            
            with Vertical(id="right-panel"):
                yield RichLog(id="term-log", highlight=True, markup=True)
                with Horizontal(id="prompt-row"):
                    yield Static(">>", id="prompt-prefix")
                    yield Input(placeholder="", id="prompt")

    def on_mount(self) -> None:
        self.log_widget = self.query_one("#term-log", RichLog)
        self.input_widget = self.query_one("#prompt", Input)
        self.update_status()
        self.log_widget.write("[bold blue]Welcome to Strap CLI![/bold blue]")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "prompt":
            import re
            val = event.value.strip().lower()
            for prefix in ("strap ", "/strap ", "/config "):
                if val.startswith(prefix):
                    val = val[len(prefix):].strip()
                    break
            m = re.match(r"^-([uzy])\s+-(\d+)", val)
            if m: self.update_status(m.group(1), int(m.group(2)))
            else: self.update_status("", 0)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if not raw:
            return
        
        # If we are in the middle of a Y/N prompt, feed it directly
        if self.state != "idle":
            self.log_widget.write(f">> {raw}")
            self._handle_prompt(raw)
            return

        # Split multiple commands chained with `^` and execute sequentially
        cmds = [c.strip() for c in raw.split("^") if c.strip()]
        self.command_queue.extend(cmds)
        self.process_next_command()

    def process_next_command(self):
        if not self.command_queue or self.state != "idle":
            self.update_status()  # Refresh left panel when idle
            return

        cmd = self.command_queue.pop(0)
        
        if cmd.lower().startswith("strap "):
            cmd = cmd[6:].strip()
            
        # Handle strict format constraint
        if not cmd.startswith("/"):
            self.log_widget.write(f">> {cmd}")
            self.log_widget.write("Invalid command format. Commands must strictly begin with '/' (e.g., /help).")
            self.process_next_command()
            return
            
        c = cmd.lower()

        # Clear welcome banner on first successful command executed
        if not hasattr(self, 'welcome_cleared'):
            self.log_widget.clear()
            self.welcome_cleared = True
            
        self.log_widget.write(f">> {cmd}")

        if c == "/install":
            self.state = "install_start"
            self._handle_install_start()

        elif c == "/update":
            self.state = "update_start"
            self._handle_update_start()

        elif c == "/config" or c.startswith("/config "):
            rest = cmd[7:].strip()   # everything after "/config"
            from tui.screen import ConfigScreen
            self.app.push_screen(ConfigScreen(open_popup=rest if rest else None))

        elif c in ("/help", "/?"):
            clean_commands = COMMANDS_TEXT.replace("[b]", "").replace("[/b]", "")
            self.log_widget.write(f"Available Commands:\n\n{clean_commands}")
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/run":
            self.run_strap_shortcut()
            self.log_widget.write("") # Blank line

        elif c == "/stop":
            try:
                subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log_widget.write("AHK scripts terminated.")
            except Exception as e:
                self.log_widget.write(f"Failed to stop scripts: {e}")
            self.log_widget.write("") # Blank line
            self.process_next_command()

        elif c == "/clear":
            self.log_widget.clear()
            self.log_widget.write("[bold blue]Welcome to Strap CLI![/bold blue]")
            delattr(self, 'welcome_cleared')
            self.log_widget.write("") # Blank line
            self.process_next_command()

        elif c == "/restart":
            self.app.exit(result="reload") # keep "reload" string so main.py catches it

        elif c == "/exit":
            self.app.exit(result="exit")

        else:
            self.log_widget.write(f'Unknown command: "{cmd}"\nType /help for available commands.')
            self.log_widget.write("") # Blank line
            self.process_next_command()

    def run_strap_shortcut(self):
        target = os.path.join(INSTALL_DIR, "core", "source.ahk")
        if os.path.exists(target):
            self.log_widget.write(f"Executing system shortcut: {target}")
            try:
                os.startfile(target)
            except Exception as e:
                self.log_widget.write(f"Error executing file: {e}")
        else:
            self.log_widget.write("Strap does not appear to be installed properly. Cannot run.")
        self.process_next_command()

    def _handle_install_start(self):
        if os.path.exists(INSTALL_DIR):
            self.log_widget.write(f"Strap is already installed at {INSTALL_DIR}.")
            self.log_widget.write("Do you want to reinstall and overwrite it? (y/n):")
            self.state = "install_ask_reinstall"
        else:
            self.reinstall_confirmed = False
            self.log_widget.write("Do you want Strap to automatically start on boot? (y/n):")
            self.state = "install_ask_startup"

    def _handle_update_start(self):
        if not is_startup_enabled():
            self.log_widget.write("Strap isn't configured to start on boot.")
            self.log_widget.write("Do you want to enable it now? (y/n):")
            self.state = "update_ask_startup"
        else:
            self.startup_confirmed = True
            self.start_update()

    def _handle_prompt(self, raw: str):
        # We allow ignoring the '/' strict rule for prompt y/n answers specifically
        ans = raw.lstrip("/").lower()
        is_yes = ans in {"yes", "ya", "yeah", "y", "yep", "yup", "sure"}
        is_no = ans in {"no", "nah", "n", "nope"}

        if self.state == "install_ask_reinstall":
            if is_yes:
                self.reinstall_confirmed = True
                self.log_widget.write("Do you want Strap to automatically start on boot? (y/n):")
                self.state = "install_ask_startup"
            elif is_no:
                self.log_widget.write("Installation aborted.")
                self.state = "idle"
                self.process_next_command()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

        elif self.state == "install_ask_startup":
            if is_yes or is_no:
                self.startup_confirmed = is_yes
                self.start_install()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

        elif self.state == "update_ask_startup":
            if is_yes or is_no:
                self.startup_confirmed = is_yes
                self.start_update()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

    def start_install(self):
        self.state = "installing"
        self.input_widget.disabled = True
        self.run_install_worker()

    def start_update(self):
        self.state = "updating"
        self.input_widget.disabled = True
        self.run_update_worker()

    @work(exclusive=True, thread=True)
    def run_install_worker(self) -> None:
        from ops.installer import run
        class OutputRedirector:
            def __init__(self, app, log_widget):
                self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run(reinstall=self.reinstall_confirmed, enable_startup_flag=self.startup_confirmed)
            
        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_update_worker(self) -> None:
        from ops.updater import run
        class OutputRedirector:
            def __init__(self, app, log_widget):
                self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run(enable_startup_flag=self.startup_confirmed)
            
        self.app.call_from_thread(self.finish_worker)

    def finish_worker(self):
        self.log_widget.write("") # Add blank line here
        self.input_widget.disabled = False
        self.input_widget.focus()
        self.state = "idle"
        self.process_next_command()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.exit(result="exit")
