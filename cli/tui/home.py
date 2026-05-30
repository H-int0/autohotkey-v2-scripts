import os
import subprocess
from textual.screen     import Screen
from textual.app        import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets    import Static, Input
from config.manager     import load_user_config
from config.schema      import DEFAULT_CONFIG
from ops.startup        import is_startup_enabled

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

class HomeScreen(Screen):
    CSS_PATH = "home.tcss"

    def _is_ahk_running(self) -> bool:
        try:
            out = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq AutoHotkey*"', shell=True, text=True
            )
            return "AutoHotkey" in out
        except Exception:
            return False

    def _feature_label(self, cfg: dict, key: str) -> str:
        return "ON " if cfg["features"].get(key, DEFAULT_CONFIG["features"].get(key, False)) else "OFF"

    def compose(self) -> ComposeResult:
        cfg      = load_user_config()
        version  = cfg.get("version", DEFAULT_CONFIG["version"])
        installed = "YES" if os.path.exists(INSTALL_DIR) else "NO"
        startup  = "ENABLED" if is_startup_enabled() else "DISABLED"
        ahk      = "YES"     if self._is_ahk_running() else "NO"
        tz_id    = cfg.get("startupTZID", "") or "Not set"

        status_text = (
            f"Installed:   {installed}\n"
            f"Version:     v{version}\n"
            f"Startup:     {startup}\n"
            f"AHK running: {ahk}\n\n"
            f"[b]FEATURES[/b]\n"
            f"───────────────────────\n"
            f"Numpad Emulator  [{self._feature_label(cfg, 'numpadEmulator')}]\n"
            f"Timezone Switch  [{self._feature_label(cfg, 'timezoneSwitcher')}]\n"
            f"Force Kill       [{self._feature_label(cfg, 'forceKillTask')}]\n"
            f"Color Picker     [{self._feature_label(cfg, 'colorPicker')}]\n"
            f"Line Navigation  [{self._feature_label(cfg, 'lineNavigation')}]\n\n"
            f"[b]TIMEZONE[/b]\n"
            f"───────────────────────\n"
            f"Active: {tz_id}"
        )

        welcome_text = (
            "Welcome to Strap CLI.\n\n"
            "Type a command below to get started,\n"
            "or type  /help  for a list of\n"
            "available commands.\n\n"
            "Commands:\n"
            "  /install   /update\n"
            "  /config    /help    /exit"
        )

        with Horizontal():
            with Vertical(id="status-panel"):
                yield Static("STATUS\n───────────────────────", classes="panel-title")
                yield Static(status_text, id="status-text")
            with Vertical(id="output-panel"):
                yield Static(welcome_text, id="output-text")

        with Horizontal(id="prompt-row"):
            yield Static(">>", id="prompt-prefix")
            yield Input(placeholder="", id="prompt")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        cmd = raw.lower()

        output = self.query_one("#output-text", Static)

        if cmd == "/install":
            self.app.push_screen("install") 
        elif cmd == "/update":
            self.app.push_screen("update")
        elif cmd == "/help":
            self.app.push_screen("help")
        elif cmd == "/config":
            self.app.push_screen("config")
        elif cmd == "/exit":
            self.app.exit()
        elif raw == "":
            pass
        else:
            output.update(
                f'Unknown command: "{raw}"\n\n'
                "Type  /help  for available commands."
            )