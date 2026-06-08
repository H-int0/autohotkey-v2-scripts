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

from textual.widgets import Static
from config.manager import load_user_config, save_user_config
from config.schema import DEFAULT_CONFIG
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
from data.timezones_catalog import TIMEZONE_CATALOG
from features import FEATURE_REGISTRY

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

# =============================================================================
# Config Panel
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
        
        registry = FEATURE_REGISTRY
        feat = p("features", {f["key"]: f["default"] for f in registry})

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
            *[p_line(f"[z{i}]", f["label"], "active" if feat.get(f["key"], f["default"]) else "inactive") for i, f in enumerate(registry, 1)],
            "",
            "─" * 60,
            "Configure - Features\n",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y1') else ' '}\\[y1] Force Kill",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y2') else ' '}\\[y2] Color Picker",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y3') else ' '}\\[y3] Vim Navigation",
        ]
        return "\n".join(lines)

    def _mark_bool(self, flag_no: str) -> bool:
        z_map = {f"z{i+1}": f["key"] for i, f in enumerate(FEATURE_REGISTRY)}
        
        if flag_no in z_map:
            feat = z_map[flag_no]
            if "features" in self.pending:
                orig = self.cfg.get("features", DEFAULT_CONFIG["features"]).get(feat, True)
                pend = self.pending["features"].get(feat, True)
                return orig != pend
            return False

        keys = {
            "u1": ["trayIconVisible"],
            "u2": ["tooltipDuration"],
            "u3": ["timezones"],
            "u4": ["startupTZID"],

            "y1": ["msgEndTask"],
            "y2": ["colorPickerMsgBox", "msgColorPicker"],
            "y3": ["vimUseLeftAlt", "vimUseRightAlt"]
        }
        for k in keys.get(flag_no, []):
            if k in self.pending: return True
        return False

    def refresh_display(self) -> None:
        self.update(self.render_list())

    def on_mount(self) -> None:
        self.refresh_display()

    def pending_count(self) -> int:
        count = 0
        for key, val in self.pending.items():
            if key == "features":
                orig = self.cfg.get("features", {f["key"]: f["default"] for f in FEATURE_REGISTRY})
                count += sum(1 for k, v in val.items() if orig.get(k) != v)
            else:
                count += 1
        return count

    def pending_summary(self) -> dict[str, tuple]:
        summary = {}
        registry = FEATURE_REGISTRY
        feature_labels = {f["key"]: f["label"] for f in registry}
        label_map = {
            "trayIconVisible": "Tray Icon",
            "tooltipDuration": "Tooltip Timeout",
            "timezones": "Switching Timezones",
            "startupTZID": "TimeZone on Startup",
            "msgEndTask": "Force Kill Tooltip",
            "colorPickerMsgBox": "Color Picker Box",
            "msgColorPicker": "Color Picker Tooltip",
            "vimUseLeftAlt":  "Vim Nav - Left Alt",
            "vimUseRightAlt": "Vim Nav - Right Alt",
        }
        for key, new_val in self.pending.items():
            if key == "features":
                orig_feats = self.cfg.get("features", {f["key"]: f["default"] for f in registry})
                for fkey, fval in new_val.items():
                    if orig_feats.get(fkey) != fval:
                        label = feature_labels.get(fkey, fkey)
                        summary[label] = (
                            "active" if orig_feats.get(fkey, True) else "inactive",
                            "active" if fval else "inactive",
                        )
            else:
                label = label_map.get(key, key)
                summary[label] = (str(self.cfg.get(key, "(not set)")), str(new_val))
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
