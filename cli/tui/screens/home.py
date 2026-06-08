# GNU GENERAL PUBLIC LICENSE
#
# Copyright (C) 2026 H-int0
# GitHub: <https://github.com/H-int0/>
# License: <https://github.com/H-int0/autohotkey-v2-scripts/blob/main/LICENSE/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ====================================================================================

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
from commands import get_installed_version, is_ahk_running, relaunch_ahk_from_shortcut, cli_profile, cli_version
from ops.startup import is_startup_enabled
from tui.constants import (
    COMMANDS_TEXT, CONFIG_COMMANDS_TEXT, get_status_text, 
    get_config_z_text, CONFIG_U1_TEXT, CONFIG_U2_TEXT, 
    CONFIG_U3_TEXT, CONFIG_U4_TEXT
)

INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")

# =============================================================================
# Home Screen
# =============================================================================

class HomeScreen(Screen):
    CSS_PATH = "../styles/home.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.command_queue = []
        self.state = "idle" 
        self.reinstall_confirmed = False
        self.startup_confirmed = False

    def _get_installed_version(self) -> str:
        return get_installed_version()

    def _is_ahk_running(self) -> bool:
        return is_ahk_running()

    def update_status(self, focused_flag: str = "", focused_no: int = 0):
        cfg = load_user_config()
        st_tz = cfg.get("startupTZID", "")
        pending = self.panel.pending_count() if hasattr(self, "panel") else 0
        
        status_text = get_status_text(
            version=self._get_installed_version(),
            is_installed=os.path.exists(INSTALL_DIR),
            startup_enabled=is_startup_enabled(),
            ahk_running=self._is_ahk_running(),
            st_tz=st_tz,
            pending_count=pending
        )

        hints = self._build_hints(focused_flag, focused_no)
        try:
            self.query_one("#status-text", Static).update(status_text)
            self.query_one("#commands-text", Static).update(COMMANDS_TEXT)
            self.query_one("#hints-text", Static).update(hints)
        except Exception:
            pass

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
        self.log_widget.write("[bold blue]Welcome to Strap CLI![/bold blue]\n\n[italic green](Open in full screen for a better experience)[italic /green]")

    def on_input_changed(self, event: Input.Changed) -> None:
        if getattr(event.input, "id", None) == "prompt":
            import re
            val = event.value.strip().lower()
            for prefix in ("strap ", "/strap ", "starp ", "/starp ", "/config "):
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
        
        # Reject fused prefix, must have exactly one space after prefix
        _raw_cmd = cmd
        for prefix in ("strap ", "/strap ", "starp ", "/starp "):
            if cmd.lower().startswith(prefix):
                cmd = cmd[len(prefix):]  # don't strip preserve original spacing
                break

        # Reject double-spaces anywhere in the command
        if "  " in cmd:
            self.log_widget.write(f">> {_raw_cmd}")
            self.log_widget.write("Invalid: only single spaces are allowed between command parts.")
            self.process_next_command()
            return

        cmd = cmd.strip()

        if not cmd.startswith("/"):
            self.log_widget.write(f">> {_raw_cmd}")
            self.log_widget.write("Invalid command format. Commands must strictly begin with '/' (e.g., /help).")
            self.process_next_command()
            return
            
        c = cmd.lower()

        # Clear welcome banner on first successful command executed
        if not hasattr(self, 'welcome_cleared'):
            self.log_widget.clear()
            self.welcome_cleared = True
            
        self.log_widget.write(f">> {cmd}")

        if c == "/install" or c.startswith("/install "):
            rest = cmd[8:].strip()
            if rest == "--ls":
                self.state = "installing_ls"
                self.input_widget.disabled = True
                self.run_install_ls_worker()
            elif rest.startswith("v"):
                self.state = "installing"
                self.input_widget.disabled = True
                self.run_install_specific_worker(rest)
            else:
                self.state = "install_start"
                self._handle_install_start()

        elif c == "/update":
            self.state = "updating"
            self.input_widget.disabled = True
            self.run_update_worker()

        elif c == "/config" or c.startswith("/config "):
            rest = cmd[7:].strip()
            if rest:
                from headless import apply_headless_config
                res = apply_headless_config(rest)
                self.log_widget.write(res)
                self.log_widget.write("")
                self.process_next_command()
            else:
                try:
                    from tui.screens.config import ConfigScreen
                    self.app.push_screen(ConfigScreen())
                except Exception as e:
                    self.log_widget.write(f"Error launching screen: {e}")
                    self.process_next_command()

        elif c in ("/help", "/?"):
            clean_commands = COMMANDS_TEXT.replace("[b]", "").replace("[/b]", "")
            self.log_widget.write(f"Available Commands:\n\n{clean_commands}")
            self.log_widget.write("")
            self.process_next_command()

        elif c in ("/back", "back"):
            self.log_widget.write("Already on home screen.")
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/run":
            self.run_strap_shortcut()
            self.log_widget.write("")

        elif c == "/run --cr shr":
            self._run_create_startup_shortcut()
            self.log_widget.write("")
            self.process_next_command()

        elif c in ("/run --d shr", "/run -d shr"):
            from ops.startup import disable_startup
            disable_startup()
            self.log_widget.write("Startup shortcut removed.")
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/home":
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/stop":
            try:
                subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log_widget.write("AHK scripts terminated.")
            except Exception as e:
                self.log_widget.write(f"Failed to stop scripts: {e}")
            self.log_widget.write("")
            self.process_next_command()

        elif c.startswith("/switch"):
            rest = cmd[7:].strip()
            if not rest:
                self.log_widget.write("Usage: /switch <version>  (e.g., /switch v1.2.1)")
                self.log_widget.write("")
                self.process_next_command()
            else:
                self.state = "switching"
                self.input_widget.disabled = True
                self.run_switch_worker(rest)

        elif c in ("/version", "/versions") or c in ("/version --ls", "/versions --ls"):
            self._show_versions()
            self.log_widget.write("")
            self.process_next_command()

        elif c.startswith("/profile"):
            rest = cmd[8:].strip()
            self._handle_profile(rest)

        elif c == "/uninstall --fr":
            self.app.exit(result="exit")
            import subprocess
            subprocess.Popen(["cmd", "/k", "echo y | strap /uninstall --fr"])

        elif c == "/uninstall":
            self.state = "uninstall_confirm"
            self._uninstall_hard = False
            self.log_widget.write("This will remove Strap from your system.")
            self.log_widget.write("Continue? (y/n):")

        elif c == "/clear":
            self.log_widget.clear()
            self.log_widget.write("[bold blue]Welcome to Strap CLI![/bold blue]\n\n[italic green](Open in full screen for a better experience)[italic /green]")
            delattr(self, 'welcome_cleared')
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/restart":
            self.app.exit(result="reload")

        elif c == "/exit":
            self.app.exit(result="exit")

        else:
            self.log_widget.write(f'Unknown command: "{cmd}"\nType /help for available commands.')
            self.log_widget.write("")
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

    def _relaunch_ahk_from_shortcut(self) -> None:
        relaunch_ahk_from_shortcut()

    def _run_create_startup_shortcut(self):
        try:
            from ops.startup import enable_startup, SHORTCUT_PATH
            enable_startup()
            self.log_widget.write(f"[√] Startup shortcut created: {SHORTCUT_PATH}")
        except Exception as e:
            self.log_widget.write(f"[×] Failed to create shortcut: {e}")

    def _handle_install_start(self):
        if os.path.exists(INSTALL_DIR):
            self.log_widget.write(f"Strap is already installed at {INSTALL_DIR}.")
            self.log_widget.write("Do you want to reinstall and overwrite it? (y/n):")
            self.state = "install_ask_reinstall"
        else:
            self.reinstall_confirmed = False
            self.log_widget.write("Do you want Strap to automatically start on boot? (y/n):")
            self.state = "install_ask_startup"

    def _handle_prompt(self, raw: str):
        ans = raw.lstrip("/").lower()
        is_yes = ans in {"y", "yes", "yeah", "ya", "yep", "yup", "sure", "ok", "okay", "affirmative", "positive"}
        is_no = ans in {"no", "nah", "n", "nope", "negative", "naw", "nay", "nyet"}

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

        elif self.state == "ask_restart":
            if is_yes:
                self.app.exit(result="reload")
            elif is_no:
                self.log_widget.write("TUI not restarted. Restart it with `/restart` if the changes aren't reflected.")
                self.state = "idle"
                self.process_next_command()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")
            return

        elif self.state == "uninstall_confirm":
            if is_yes:
                self.state = "uninstalling"
                self.input_widget.disabled = True
                self.run_uninstall_worker(hard=getattr(self, "_uninstall_hard", False))
            elif is_no:
                self.log_widget.write("Uninstall aborted.")
                self.state = "idle"
                self.process_next_command()
            else:
                self.log_widget.write("Please answer 'yes' or 'no':")

    def start_install(self):
        self.state = "installing"
        self.input_widget.disabled = True
        self.run_install_worker()

    @work(exclusive=True, thread=True)
    def run_install_worker(self) -> None:
        from ops.installer import run
        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run(from_ps=False, enable_startup_flag=self.startup_confirmed)

        self._relaunch_ahk_from_shortcut()
        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_install_specific_worker(self, target_version: str) -> None:
        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            from commands import cli_install
            cli_install(target_version=target_version)

        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_install_ls_worker(self) -> None:
        import requests, time
        from ops.updater import GITHUB_API
        try:
            resp = requests.get(GITHUB_API + "?per_page=100", timeout=10)
            resp.raise_for_status()
            tags = [t.get("name", "") for t in resp.json()]
            if not tags:
                self.app.call_from_thread(self.log_widget.write, "No tags found.")
            else:
                self.app.call_from_thread(self.log_widget.write, "\nVersions available:")
                for tag in tags:
                    self.app.call_from_thread(self.log_widget.write, f"  {tag}")
                    time.sleep(0.01)
                self.app.call_from_thread(self.log_widget.write, "END")
        except Exception as e:
            self.app.call_from_thread(self.log_widget.write, f"Failed to fetch tags: {e}")
        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_update_worker(self) -> None:
        from ops.updater import run_update
        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run_update()

        self._relaunch_ahk_from_shortcut()
        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_switch_worker(self, version: str) -> None:
        from ops.updater import run_switch
        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            run_switch(version)

        self._relaunch_ahk_from_shortcut()
        self.app.call_from_thread(self.finish_worker)

    def _show_versions(self) -> None:
        from contextlib import redirect_stdout
        import io
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli_version()
        for line in buf.getvalue().splitlines():
            if line.strip():
                self.log_widget.write(line)

    def _handle_profile(self, subargs: str) -> None:
        from contextlib import redirect_stdout
        import io
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli_profile(subargs)
        for line in buf.getvalue().splitlines():
            if line.strip():
                self.log_widget.write(line)

        self.log_widget.write("")

        parts = subargs.strip().split(" ", 1) if subargs.strip() else []
        sub = parts[0].strip().lower() if parts else ""
        if sub == "--use":
            self.log_widget.write("Do you want to restart the TUI to reflect the changes? (y/n):")
            self.state = "ask_restart"
        else:
            self.process_next_command()

    @work(exclusive=True, thread=True)
    def run_uninstall_worker(self, hard: bool = False) -> None:
        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            from commands import cli_uninstall
            cli_uninstall(hard=hard, skip_confirm=True)

        self.app.call_from_thread(self.finish_worker)

    def finish_worker(self):
        self.log_widget.write("")
        self.input_widget.disabled = False
        
        if self.state in ("switching", "installing", "updating", "profile_switch"):
            self.state = "idle"
            self.log_widget.write("\nDo you want to restart the TUI to reflect the changes? (y/n):")
            self.state = "ask_restart"
            return
            
        self.state = "idle"
        self.process_next_command()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.exit(result="exit")

    def on_resize(self, _event) -> None:
        pass

    def on_click(self, _event) -> None:
        pass
