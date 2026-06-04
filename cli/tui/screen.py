import os
import re
import subprocess

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input
from config.manager import load_user_config
from config.schema import DEFAULT_CONFIG
from ops.startup import is_startup_enabled
from tui.panel import ConfigPanel
from tui.popups import BooleanPopup, IntegerPopup, ForceKillPopup, ColorPickerPopup, TimezonePopup, UnsavedChangesPopup
from tui.tz_catalog import TIMEZONE_CATALOG
from tui.help_text import (
    COMMANDS_TEXT, CONFIG_COMMANDS_TEXT, get_status_text, 
    get_config_z_text, CONFIG_U1_TEXT, CONFIG_U2_TEXT, 
    CONFIG_U3_TEXT, CONFIG_U4_TEXT
)

INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")

# =============================================================================
# ConfigScreen
# =============================================================================

class ConfigScreen(Screen):
    CSS_PATH = "config.tcss"
    _active_tz_popup: TimezonePopup | None = None

    def __init__(self, open_popup: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._open_popup_cmd = open_popup

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="left-panel"):
                with ScrollableContainer(id="config-left-content"):
                    yield Static("", id="config-status-text")
                    yield Static("", id="config-commands-text")
                    yield Static("", id="config-hints-text")
                yield Static("SPDX-License-Identifier: GPL-3.0-or-later\nCopyright (C) 2026 H-int0", id="config-footer-text")
            with Vertical(id="right-panel"):
                with ScrollableContainer(id="config-panel-container"):
                    yield ConfigPanel(id="config-panel")
                with Horizontal(id="config-prompt-row"):
                    yield Static(">>", id="config-prompt-prefix")
                    yield Input(placeholder="", id="config-prompt")

    def on_mount(self) -> None:
        self.panel = self.query_one("#config-panel", ConfigPanel)
        self.input = self.query_one("#config-prompt", Input)
        self._update_left_panel()
        self.input.focus()
        if self._open_popup_cmd:
            self.call_after_refresh(self.route_command, self._open_popup_cmd)

    def _get_installed_version(self) -> str:
        try:
            with open(os.path.join(INSTALL_DIR, "VERSION"), "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return DEFAULT_CONFIG["version"]

    def _is_ahk_running(self) -> bool:
        try:
            result = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq AutoHotkey*"',
                shell=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return "AutoHotkey" in result
        except:
            return False

    def _update_left_panel(self, focused_flag: str = "", focused_no: int = 0) -> None:
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
            self.query_one("#config-status-text", Static).update(status_text)
            self.query_one("#config-commands-text", Static).update(COMMANDS_TEXT)
            self.query_one("#config-hints-text", Static).update(hints)
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
    
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "config-prompt":
            val = event.value.strip().lower()
            for prefix in ("strap ", "/strap ", "starp ", "/starp ", "/config "):
                if val.startswith(prefix):
                    val = val[len(prefix):].strip()
                    break
            m = re.match(r"^-([uzy])\s+-(\d+)", val)
            if m: self._update_left_panel(m.group(1), int(m.group(2)))
            else: self._update_left_panel("", 0)

    def on_key(self, event) -> None:
        if event.key == "escape": 
            self._try_leave()

    def on_resize(self, event) -> None:
        if hasattr(self, "input"):
            self.input.refresh()

    def on_click(self, event) -> None:
        if hasattr(self, "input"):
            self.input.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "config-prompt": return
        raw = event.value.strip()
        event.input.value = ""
        if not raw: return
        for p in ("strap ", "/strap ", "starp ", "/starp "):
            if raw.lower().startswith(p):
                raw = raw[len(p):].strip()
                break
        self.route_command(raw)

    def route_command(self, raw: str) -> None:
        cmd = raw.strip()
        cl = cmd.lower()

        if cl == "/exit":
            self.app.exit(result="exit"); return
        
        if cl == "/restart":
            self.app.exit(result="reload"); return
        
        if cl in ("/run", "run"):
            self._run_strap(); return
        
        if cl in ("/stop", "stop"):
            self._stop_strap(); return
        
        if cl in ("/back", "back"):
            self._try_leave(); return
        
        if cl in ("/home", "home"):
            self.app.pop_screen()
            return
        
        if cl == "/config --save":
            self._do_save(exit_after=False); return
        
        if cl in ("/config --save --exit", "/config --!save"):
            self._do_save(exit_after=True); return
        
        if cl == "/config --abort":
            self.panel.discard_pending()
            self.panel.refresh_display()
            self._update_left_panel(); return

        if cl.startswith("/config"):
            self._handle_config_args(cmd[7:].strip()); return
        
        if cl.startswith("-"):
            self._handle_config_args(cmd); return

    def _handle_config_args(self, args: str) -> None:
        args = args.strip()
        if not args: return
        m = re.match(r"^-([uzy])\s+-(\d+)(?:--(.+?))?(?:\s+(.+))?$", args, re.IGNORECASE)
        if not m:
            m = re.match(r"^-([uzy])\s+-(\d+)\s+(.+)$", args, re.IGNORECASE)
            if not m: return
            flag, no, sub, value = m.group(1).lower(), int(m.group(2)), "", m.group(3).strip()
        else:
            flag, no, sub, value = m.group(1).lower(), int(m.group(2)), m.group(3), (m.group(4) or "").strip()

        self._update_left_panel(flag, no)
        if not value and not sub: self._open_popup(flag, no); return
        
        if flag == "u" and no in (3, 4) and not value and sub:
            value = sub
            sub = None

        self._apply_value(flag, no, sub, value)

    def _apply_value(self, flag: str, no: int, sub: str | None, value: str) -> None:
        v, vl = value.strip(), value.strip().lower()
        def parse_bool(s: str) -> bool | None:
            if s in {"1", "t", "true", "enable", "enabled", "active", "yes", "show", "visible"}: return True
            if s in {"0", "f", "false", "disable", "disabled", "inactive", "no", "hide", "hidden"}: return False
            return None

        if flag == "u":
            if no == 1:
                if vl == "--!": self.panel.pending["trayIconVisible"] = not self.panel._effective("trayIconVisible", True)
                elif parse_bool(vl) is not None: self.panel.pending["trayIconVisible"] = parse_bool(vl)
            elif no == 2 and v.isdigit() and int(v) > 0: self.panel.pending["tooltipDuration"] = int(v)
            elif no == 3: self._toggle_tz("timezones", sub if sub else v)
            elif no == 4: self._toggle_startup_tz(sub if sub else v)
        elif flag == "z":
            fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation"}
            fk = fk_map.get(no)
            if fk:
                c_feats = dict(self.panel._effective("features", DEFAULT_CONFIG["features"]))
                if vl == "--!": c_feats[fk] = not c_feats.get(fk, True)
                elif parse_bool(vl) is not None: c_feats[fk] = parse_bool(vl)
                self.panel.pending["features"] = c_feats
        elif flag == "y":
            if no == 1 and (not sub or sub == "1"):
                if vl == '""' or vl == "''": v = ""
                self.panel.pending["msgEndTask"] = v
            elif no == 2:
                if sub == "1":
                    if vl == "--!": self.panel.pending["colorPickerMsgBox"] = not self.panel._effective("colorPickerMsgBox", False)
                    elif parse_bool(vl) is not None: self.panel.pending["colorPickerMsgBox"] = parse_bool(vl)
                elif sub == "2":
                    if vl == '""' or vl == "''": v = ""
                    self.panel.pending["msgColorPicker"] = v

        self.panel.refresh_display()
        self._update_left_panel(flag, no)

    def _toggle_tz(self, cfg_key: str, tz_arg: str) -> None:
        win_id = self._resolve_tz_arg(tz_arg)
        if not win_id: return
        current: list[str] = list(self.panel._effective(cfg_key, []))
        if win_id in current: current.remove(win_id)
        else: current.append(win_id)
        self.panel.pending[cfg_key] = current

    def _toggle_startup_tz(self, tz_arg: str) -> None:
        win_id = self._resolve_tz_arg(tz_arg)
        if not win_id: return
        self.panel.pending["startupTZID"] = "" if self.panel._effective("startupTZID", "") == win_id else win_id

    def _resolve_tz_arg(self, arg: str) -> str | None:
        arg = arg.strip()
        if arg.startswith("-set--"): arg = arg[6:]
        if arg.isdigit() and 0 <= int(arg)-1 < len(TIMEZONE_CATALOG): return TIMEZONE_CATALOG[int(arg)-1][0]
        norm = arg.replace("_", " ").lower()
        for win_id, display, _, utc in TIMEZONE_CATALOG:
            if win_id.lower() == norm or display.lower() == norm or utc.lower() == norm: return win_id
        return None

    def _open_popup(self, flag: str, no: int) -> None:
        cfg = self.panel._effective
        try:
            if flag == "u":
                if no == 1:
                    self.app.push_screen(
                        BooleanPopup(
                            "Configure - Tray Icon", ["visible", "hidden"],
                            "visible" if cfg("trayIconVisible", True) else "hidden",
                            CONFIG_U1_TEXT.rstrip() + "\n\n/back or Esc               (Close)\n\n"
                        ),
                        lambda r: self._apply_result("trayIconVisible", r == "visible", r)
                    )
                elif no == 2:
                    self.app.push_screen(
                        IntegerPopup(
                            "Configure - Tooltip Timeout", cfg("tooltipDuration", 2500), "1sec = 1000ms",
                            CONFIG_U2_TEXT.rstrip() + "\n\n/back or Esc               (Close)\n\n"
                        ),
                        lambda r: self._apply_result("tooltipDuration", r, r)
                    )
                elif no == 3:
                    self._active_tz_popup = TimezonePopup("u", 3, cfg("timezones", []), False)
                    self.app.push_screen(self._active_tz_popup, lambda r: self._apply_result("timezones", r, r))
                elif no == 4:
                    st = cfg("startupTZID", "")
                    self._active_tz_popup = TimezonePopup("u", 4, [st] if st else [], True)
                    self.app.push_screen(self._active_tz_popup, lambda r: self._apply_result("startupTZID", r[0] if r else "", r))
            elif flag == "z":
                f_map = {1: "numpadEmulator", 2: "altCodes", 3: "timezoneSwitcher", 4: "forceKillTask", 5: "colorPicker", 6: "lineNavigation"}
                names = {1: "NumPad Emulator", 2: "ALT Codes", 3: "TimeZone Switcher", 4: "Force Kill", 5: "Color Picker", 6: "Line Navigation"}
                if fk := f_map.get(no):
                    self.app.push_screen(
                        BooleanPopup(
                            f"Configure - {names[no]}", ["active", "inactive"],
                            "active" if cfg("features", DEFAULT_CONFIG["features"]).get(fk, True) else "inactive",
                            get_config_z_text(no).rstrip() + "\n\n/back or Esc                  (Close)\n\n"
                        ),
                        lambda r, _fk=fk: self._apply_feat_result(_fk, r)
                    )
            elif flag == "y":
                if no == 1:
                    self.app.push_screen(
                        ForceKillPopup(cfg("msgEndTask", "EVAPORATED!")),
                        lambda r: self._apply_route_result("msgEndTask", r)
                    )
                elif no == 2:
                    self.app.push_screen(
                        ColorPickerPopup(cfg("colorPickerMsgBox", False), cfg("msgColorPicker", "Copied to Clipboard")),
                        lambda r: self._apply_route_result(None, r)
                    )
        except Exception:
            pass

    def _apply_result(self, key, val, check_none):
        if check_none is None: return
        self.panel.pending[key] = val
        self.panel.refresh_display()
        self._update_left_panel()

    def _apply_feat_result(self, feat_key, result):
        if result is None: return
        c = dict(self.panel._effective("features", DEFAULT_CONFIG["features"]))
        c[feat_key] = (result == "active")
        self.panel.pending["features"] = c
        self.panel.refresh_display()
        self._update_left_panel()

    def _apply_route_result(self, direct_key, result):
        if result is None: return
        if direct_key:
            self.panel.pending[direct_key] = result
        self.panel.refresh_display()
        self._update_left_panel()

    def _do_save(self, exit_after: bool) -> None:
        from config.manager import get_active_profile_name, set_active_profile
        if get_active_profile_name() == "default":
            set_active_profile("ghost")
            
        self.panel.apply_pending()
        self.panel.write_to_disk()
        self.panel.refresh_display()
        self._update_left_panel()
        if exit_after:
            while self.app.screen_stack:
                top = self.app.screen_stack[-1]
                self.app.pop_screen()
                if top == self:
                    break

    def _try_leave(self) -> None:
        if self.panel.pending_count() == 0:
            self.app.pop_screen(); return
        def handle(r):
            if r == "save":        self._do_save(exit_after=False)
            elif r == "save_exit": self._do_save(exit_after=True)
            elif r == "abort":
                self.panel.discard_pending()
                self.panel.refresh_display()
                self._update_left_panel()
        try:
            self.app.push_screen(UnsavedChangesPopup(self.panel.pending_summary()), handle)
        except Exception:
            self.app.pop_screen()

    def _run_strap(self) -> None:
        if os.path.exists(t:=os.path.join(INSTALL_DIR, "core", "source.ahk")):
            try: os.startfile(t)
            except: pass

    def _stop_strap(self) -> None:
        subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
