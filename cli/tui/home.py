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

INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")

# =============================================================================
# Home Screen
# =============================================================================

class HomeScreen(Screen):
    CSS_PATH = "home.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.command_queue = []
        self.state = "idle" 
        self.reinstall_confirmed = False
        self.startup_confirmed = False

    def _get_installed_version(self) -> str:
        try:
            with open(os.path.join(INSTALL_DIR, "VERSION"), "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return DEFAULT_CONFIG["version"]

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
        
        for prefix in ("strap ", "/strap ", "starp ", "/starp "):
            if cmd.lower().startswith(prefix):
                cmd = cmd[len(prefix):].strip()
                break
            
        if not cmd.startswith("/"):
            self.log_widget.write(f">> {cmd}")
            self.log_widget.write("Invalid command format. Commands must strictly begin with '/' (e.g.,, /help).")
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
            try:
                from tui.screen import ConfigScreen
                self.app.push_screen(ConfigScreen(open_popup=rest if rest else None))
            except Exception as e:
                self.log_widget.write(f"Error launching screen: {e}")
                self.process_next_command()

        elif c in ("/help", "/?"):
            clean_commands = COMMANDS_TEXT.replace("[b]", "").replace("[/b]", "")
            self.log_widget.write(f"Available Commands:\n\n{clean_commands}")
            self.log_widget.write("")
            self.process_next_command()

        elif c in ("/back", "back"):
            self.log_widget.write("")
            self.process_next_command()

        elif c == "/run":
            self.run_strap_shortcut()
            self.log_widget.write("")

        elif c == "/run shr":
            self._run_create_startup_shortcut()
            self.log_widget.write("")
            self.process_next_command()
            
        elif c == "/run -d shr":
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

        elif c in ("/version", "/versions"):
            self._show_versions()
            self.log_widget.write("")
            self.process_next_command()

        elif c.startswith("/profile"):
            rest = cmd[8:].strip()
            self._handle_profile(rest)

        elif c == "/uninstall":
            self.state = "uninstall_confirm"
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

    def _run_create_startup_shortcut(self):
        import winreg
        try:
            startup_folder = os.path.join(
                os.environ["APPDATA"],
                r"Microsoft\Windows\Start Menu\Programs\Startup"
            )
            lnk_path   = os.path.join(startup_folder, "Strap.lnk")
            target_ahk = os.path.join(INSTALL_DIR, "core", "source.ahk")
            working_dir = os.path.join(INSTALL_DIR, "core")

            if os.path.exists(lnk_path):
                os.remove(lnk_path)

            ps_cmd = (
                f'$ws = New-Object -ComObject WScript.Shell; '
                f'$s = $ws.CreateShortcut("{lnk_path}"); '
                f'$s.TargetPath = "{target_ahk}"; '
                f'$s.WorkingDirectory = "{working_dir}"; '
                f'$s.Save()'
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            self.log_widget.write(f"[√] Startup shortcut created: {lnk_path}")
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

        elif self.state == "uninstall_confirm":
            if is_yes:
                self.state = "uninstalling"
                self.input_widget.disabled = True
                self.run_uninstall_worker()
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
            
        self.app.call_from_thread(self.finish_worker)

    @work(exclusive=True, thread=True)
    def run_install_specific_worker(self, target_version: str) -> None:
        import shutil
        from ops.updater import _download_and_archive, _do_switch
        from ops.installer import _ensure_bat, _add_to_user_path, _bootstrap_profiles, BIN_DIR

        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        with redirect_stdout(OutputRedirector(self.app, self.log_widget)):
            ver_clean   = target_version.lstrip("v")
            version_dir = os.path.join(os.environ["USERPROFILE"], ".strap_versions", f"v{ver_clean}")

            # Always silently overwrite archive
            if os.path.exists(version_dir):
                print(f"Refreshing archive for v{ver_clean}...")
                shutil.rmtree(version_dir)
            zip_url = f"https://codeload.github.com/H-int0/autohotkey-v2-scripts/zip/refs/tags/v{ver_clean}"
            _download_and_archive(zip_url, ver_clean, version_dir)

            if not os.path.exists(version_dir):
                print("[×] Download failed.")
            elif os.path.exists(INSTALL_DIR):
                # Strap already installed switch to the new version
                _do_switch(ver_clean, version_dir)
            else:
                # Fresh install from the downloaded archive
                print(f"Copying v{ver_clean} to %APPDATA%\\Strap...")
                os.makedirs(INSTALL_DIR, exist_ok=True)
                for item in os.listdir(version_dir):
                    src = os.path.join(version_dir, item)
                    dst = os.path.join(INSTALL_DIR, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
                _ensure_bat()
                _add_to_user_path(BIN_DIR)
                _bootstrap_profiles(ver_clean)

            print(f"\n[√] Strap v{ver_clean} installed successfully!")

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

        self.app.call_from_thread(self.finish_worker)

    def _show_versions(self) -> None:
        active = self._get_installed_version()
        versions_dir = os.path.join(os.environ["USERPROFILE"], ".strap_versions")
        if not os.path.exists(versions_dir):
            self.log_widget.write("No archived versions found.")
            return
        versions = sorted(
            d for d in os.listdir(versions_dir)
            if os.path.isdir(os.path.join(versions_dir, d))
        )
        if not versions:
            self.log_widget.write("No archived versions found.")
            return
        self.log_widget.write("Archived versions:")
        for v in versions:
            tag = v.lstrip("v")
            marker = " (active)" if tag == active else ""
            self.log_widget.write(f"  {v}{marker}")

    def _handle_profile(self, subargs: str) -> None:
        from config.manager import (
            get_active_profile_name, set_active_profile,
            create_profile, delete_profile, list_profiles,
            load_user_config as _load
        )
        from ops.file_editor import update_config_ahk, update_timezones_variables_ahk

        parts = subargs.strip().split(" ", 1) if subargs.strip() else []
        sub   = parts[0].strip() if parts else ""
        arg   = parts[1].strip() if len(parts) > 1 else ""
        subl  = sub.lower()

        if not sub or subl == "--ls":
            active   = get_active_profile_name()
            profiles = list_profiles()
            if not profiles:
                self.log_widget.write("No profiles found.")
            else:
                self.log_widget.write("Profiles:")
                for p in profiles:
                    marker = " (active)" if p == active else ""
                    self.log_widget.write(f"  {p}{marker}")

        elif subl == "--d":
            if not arg:
                self.log_widget.write("Usage: /profile --d <name>")
            else:
                try:
                    delete_profile(arg)
                    self.log_widget.write(f"[√] Profile '{arg}' deleted.")
                except ValueError as e:
                    self.log_widget.write(f"[×] {e}")

        elif subl == "--use":
            if not arg:
                self.log_widget.write("Usage: /profile --use <name>")
            else:
                profiles_dir = os.path.join(os.environ["USERPROFILE"], ".strap_profiles")
                cfg_path = os.path.join(profiles_dir, arg, "user-config.json")
                if os.path.exists(cfg_path):
                    set_active_profile(arg)
                    cfg = _load(arg)
                    c_ahk  = os.path.join(INSTALL_DIR, "core", "config.ahk")
                    t_vars = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
                    if os.path.exists(c_ahk):
                        update_config_ahk(cfg, c_ahk)
                    if os.path.exists(t_vars):
                        update_timezones_variables_ahk(cfg.get("timezones", []), t_vars)
                    self.log_widget.write(f"[√] Switched to profile '{arg}'.")
                    self.state = "profile_switch"
                else:
                    self.log_widget.write(f"[×] Profile '{arg}' does not exist.")

        else:
            try:
                create_profile(sub)
                self.log_widget.write(f"[√] Profile '{sub}' created.")
            except ValueError as e:
                self.log_widget.write(f"[×] {e}")

        self.log_widget.write("")
        self.process_next_command()

    @work(exclusive=True, thread=True)
    def run_uninstall_worker(self) -> None:
        import shutil, winreg, ctypes
        from ops.startup import disable_startup

        install_dir  = os.path.join(os.environ["APPDATA"], "Strap")
        bin_dir      = os.path.join(install_dir, "bin")
        versions_dir = os.path.join(os.environ["USERPROFILE"], ".strap_versions")

        class OutputRedirector:
            def __init__(self, app, log_widget): self.app = app; self.log_widget = log_widget
            def write(self, s):
                if s.strip(): self.app.call_from_thread(self.log_widget.write, s.strip('\r\n'))
            def flush(self): pass

        redir = OutputRedirector(self.app, self.log_widget)
        subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        disable_startup()

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
            current_path, _ = winreg.QueryValueEx(key, "Path")
            entries = [e for e in current_path.split(";") if e.lower() != bin_dir.lower()]
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, ";".join(entries))
            ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 2, 5000, None)
            winreg.CloseKey(key)
        except Exception:
            pass

        if os.path.exists(install_dir):
            shutil.rmtree(install_dir, ignore_errors=True)
        if os.path.exists(versions_dir):
            shutil.rmtree(versions_dir, ignore_errors=True)

        redir.write("[√] Strap was uninstalled." + " До встречи!")
        self.app.call_from_thread(self.finish_worker)

    def finish_worker(self):
        self.log_widget.write("")
        self.input_widget.disabled = False
        self.input_widget.focus()
        
        if self.state in ("switching", "installing", "updating", "profile_switch"):
            self.app.exit(result="reload")
            return
            
        self.state = "idle"
        self.process_next_command()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.exit(result="exit")

    def on_resize(self, event) -> None:
        if hasattr(self, "input_widget"):
            self.input_widget.refresh()

    def on_click(self, event) -> None:
        if hasattr(self, "input_widget"):
            self.input_widget.focus()
