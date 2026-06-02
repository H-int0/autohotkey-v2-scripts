import os

from textual.widgets import Static
from config.manager import load_user_config, save_user_config
from config.schema import DEFAULT_CONFIG
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
from tui.tz_catalog import TIMEZONE_CATALOG

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

# =============================================================================
# ConfigPanel
# =============================================================================

class ConfigPanel(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cfg = load_user_config()
        self.pending: dict[str, object] = {}

    def _effective(self, key: str, default=None):
        return self.pending.get(key, self.cfg.get(key, default))

    def render_list(self) -> str:
        cfg, p = self.cfg, self._effective

        tray = "visible" if p("trayIconVisible", True) else "hidden"
        ttdur = p("tooltipDuration", 2500)
        
        tzs: list[str] = p("timezones", [])
        utc_labels = []
        for win_id in tzs:
            matched = win_id
            for e in TIMEZONE_CATALOG:
                if e[0].replace(".", "").lower() == win_id.replace(".", "").lower():
                    matched = e[3]
                    break
            utc_labels.append(matched)
        tz_display = ", ".join(utc_labels) if utc_labels else "none"
        
        startup_tz = p("startupTZID", "")
        startup_tz_display = startup_tz if startup_tz else "default"
        
        feat = p("features", DEFAULT_CONFIG["features"])
        def fl(k): return "active" if feat.get(k, True) else "inactive"

        def p_line(prefix, title, value, extra=""):
            eprefix = prefix.replace("[", "\\[")
            raw_left = f"{eprefix} {title}"
            pad = max(1, 37 - len(f"{prefix} {title}"))
            mark = "[bold yellow]*[/bold yellow]" if self._mark_bool(prefix[1:3]) else " "
            return f"{mark}{raw_left}{' ' * pad}\\[{value}]{extra}"

        lines = [
            "[bold blue]Customize STRAP[/bold blue]",
            "─" * 60,
            "Configure - Globals\n",
            p_line("[u1]", "Tray Icon", tray),
            p_line("[u2]", "Tooltip Timeout", ttdur, "  (1sec = 1000ms)"),
            p_line("[u3]", "Switching Timezones", tz_display),
            p_line("[u4]", "TimeZone on Startup", startup_tz_display),
            "",
            p_line("[z1]", "NumPad Emulator", fl('numpadEmulator')),
            p_line("[z2]", "ALT Codes", fl('altCodes')),
            p_line("[z3]", "TimeZone Switcher", fl('timezoneSwitcher')),
            p_line("[z4]", "Force Kill", fl('forceKillTask')),
            p_line("[z5]", "Color Picker", fl('colorPicker')),
            p_line("[z6]", "Line Navigation", fl('lineNavigation')),
            "",
            "─" * 60,
            "Configure - Features\n",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y1') else ' '}\\[y1] Force Kill",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y2') else ' '}\\[y2] Color Picker",
        ]
        return "\n".join(lines)

    def _mark_bool(self, flag_no: str) -> bool:
        z_map = {
            "z1": "numpadEmulator", "z2": "altCodes", "z3": "timezoneSwitcher",
            "z4": "forceKillTask", "z5": "colorPicker", "z6": "lineNavigation"
        }
        
        if flag_no in z_map:
            feat = z_map[flag_no]
            if "features" in self.pending:
                orig = self.cfg.get("features", DEFAULT_CONFIG["features"]).get(feat, True)
                pend = self.pending["features"].get(feat, True)
                return orig != pend
            return False

        keys = {
            "u1": ["trayIconVisible"], "u2": ["tooltipDuration"], "u3": ["timezones"], "u4": ["startupTZID"],
            "y1": ["msgEndTask"], "y2": ["colorPickerMsgBox", "msgColorPicker"]
        }
        for k in keys.get(flag_no, []):
            if k in self.pending: return True
        return False

    def refresh_display(self) -> None:
        self.update(self.render_list())

    def on_mount(self) -> None:
        self.refresh_display()

    def pending_count(self) -> int: return len(self.pending)

    def pending_summary(self) -> dict[str, tuple]:
        summary = {}
        label_map = {
            "trayIconVisible": "Tray Icon", "tooltipDuration": "Tooltip Timeout",
            "timezones": "Switching Timezones", "startupTZID": "TimeZone on Startup",
            "features.numpadEmulator": "NumPad Emulator", "features.altCodes": "ALT Codes",
            "features.timezoneSwitcher":"TimeZone Switcher", "features.forceKillTask": "Force Kill",
            "features.colorPicker": "Color Picker", "features.lineNavigation": "Line Navigation",
            "msgEndTask": "Force Kill Tooltip", "colorPickerMsgBox": "Color Picker Box", "msgColorPicker": "Color Picker Tooltip",
        }
        for key, new_val in self.pending.items():
            summary[label_map.get(key, key)] = (str(self.cfg.get(key, "(not set)")), str(new_val))
        return summary

    def apply_pending(self) -> None:
        for key, val in self.pending.items():
            if "." in key:
                parent, child = key.split(".", 1)
                if parent not in self.cfg: self.cfg[parent] = {}
                self.cfg[parent][child] = val
            else: self.cfg[key] = val
        self.pending.clear()

    def discard_pending(self) -> None: self.pending.clear()

    def write_to_disk(self) -> None:
        save_user_config(self.cfg)
        c_ahk = os.path.join(INSTALL_DIR, "core", "config.ahk")
        t_vars = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
        if os.path.exists(c_ahk): update_config_ahk(self.cfg, c_ahk)
        if os.path.exists(t_vars): update_timezones_variables_ahk(self.cfg.get("timezones", []), t_vars)
