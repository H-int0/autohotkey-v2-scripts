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

import re
import os
from config.manager import load_user_config, save_user_config, get_active_profile_name, set_active_profile
from config.schema import DEFAULT_CONFIG
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
from data.timezones_catalog import TIMEZONE_CATALOG

# ==============================================================================
# HEADLESS CONFIGURATION ROUTING
# - Handles the execution of headless config commands passed via the CLI.
#
# ==============================================================================

def apply_headless_config(args: str) -> str:
    """Parse headless config arguments and apply them directly to the active profile."""

    INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")
    cfg = load_user_config()
    
    args = args.strip()
    if args in ("--save", "--abort", "--!save", "--save --exit"):
        return "No pending changes in headless mode."
    
    auto_save = args.startswith("-!")
    if auto_save:
        args = "-" + args[2:]

    m = re.match(r"^-([uzy])\s+-(\d+)(?:--(.+?))?(?:\s+(.+))?$", args, re.IGNORECASE)
    if not m:
        m = re.match(r"^-([uzy])\s+-(\d+)\s+(.+)$", args, re.IGNORECASE)
        if not m: return f"Invalid config arguments: {args}"
        flag, no, sub, value = m.group(1).lower(), int(m.group(2)), "", m.group(3).strip()
    else:
        flag, no, sub, value = m.group(1).lower(), int(m.group(2)), m.group(3), (m.group(4) or "").strip()

    if flag == "u" and no in (3, 4) and not value and sub:
        value = sub
        sub = None

    if not value and not sub:
        return f"Value required for headless config: {args}"

    v, vl = value.strip(), value.strip().lower()
    def parse_bool(s: str) -> bool | None:
        if s in {"1", "t", "true", "enable", "enabled", "active", "yes", "show", "visible"}: return True
        if s in {"0", "f", "false", "disable", "disabled", "inactive", "no", "hide", "hidden"}: return False
        return None

    def _resolve_tz(arg):
        arg = arg.strip(' "\'')
        # Strip all spaces and underscores to make "UTC_+3", "UTC +3", and "UTC+3" identical
        norm = arg.replace("_", "").replace(" ", "").lower()
        for win_id, display, _, utc in TIMEZONE_CATALOG:
            if win_id.replace(" ", "").lower() == norm or utc.replace(" ", "").lower() == norm:
                return win_id
        return None

    if flag == "u":
        if no == 1:
            if vl == "--!": cfg["trayIconVisible"] = not cfg.get("trayIconVisible", True)
            elif parse_bool(vl) is not None: cfg["trayIconVisible"] = parse_bool(vl)
        elif no == 2 and v.isdigit() and int(v) > 0: cfg["tooltipDuration"] = int(v)
        elif no == 3:
            win_id = _resolve_tz(sub if sub else v)
            if win_id:
                current = list(cfg.get("timezones", []))
                # Heal config: Convert any broken strings like "UTC_+3" into actual Windows IDs
                healed_current = []
                for tz in current:
                    resolved = _resolve_tz(tz)
                    if resolved and resolved not in healed_current:
                        healed_current.append(resolved)
                
                healed_lower = [tz.lower() for tz in healed_current]
                if win_id.lower() in healed_lower:
                    healed_current = [tz for tz in healed_current if tz.lower() != win_id.lower()]
                else:
                    healed_current.append(win_id)
                cfg["timezones"] = healed_current
        elif no == 4:
            win_id = _resolve_tz(sub if sub else v)
            if win_id:
                current_st = cfg.get("startupTZID", "")
                resolved_st = _resolve_tz(current_st) if current_st else ""
                cfg["startupTZID"] = "" if resolved_st and resolved_st.lower() == win_id.lower() else win_id
                
    elif flag == "z":
        fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation", 7:"vimNavigation"}
        fk = fk_map.get(no)
        if fk:
            c_feats = cfg.get("features", DEFAULT_CONFIG["features"])
            if vl == "--!": c_feats[fk] = not c_feats.get(fk, True)
            elif parse_bool(vl) is not None: c_feats[fk] = parse_bool(vl)
            cfg["features"] = c_feats
    elif flag == "y":
        if no == 1 and (not sub or sub == "1"):
            if vl == '""' or vl == "''": v = ""
            cfg["msgEndTask"] = v
        elif no == 2:
            if sub == "1":
                if vl == "--!": cfg["colorPickerMsgBox"] = not cfg.get("colorPickerMsgBox", False)
                elif parse_bool(vl) is not None: cfg["colorPickerMsgBox"] = parse_bool(vl)
            elif sub == "2":
                if vl == '""' or vl == "''": v = ""
                cfg["msgColorPicker"] = v
        elif no == 3:
            if sub == "1":
                if vl == "--!": cfg["vimUseLeftAlt"] = not cfg.get("vimUseLeftAlt", True)
                elif parse_bool(vl) is not None: cfg["vimUseLeftAlt"] = parse_bool(vl)
            elif sub == "2":
                if vl == "--!": cfg["vimUseRightAlt"] = not cfg.get("vimUseRightAlt", True)
                elif parse_bool(vl) is not None: cfg["vimUseRightAlt"] = parse_bool(vl)

    if get_active_profile_name() == "default":
        set_active_profile("ghost")

    save_user_config(cfg)
    c_ahk = os.path.join(INSTALL_DIR, "core", "config.ahk")
    t_vars = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    if os.path.exists(c_ahk): update_config_ahk(cfg, c_ahk)
    if os.path.exists(t_vars): update_timezones_variables_ahk(cfg.get("timezones", []), t_vars)
    
    from commands import relaunch_ahk_from_shortcut
    relaunch_ahk_from_shortcut()

    return f"Config updated successfully: -{flag} -{no}"
