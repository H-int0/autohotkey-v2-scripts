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
from features import FEATURE_REGISTRY

# =============================================================================
# file_editor.py
# Rewrites config.ahk and timezones-variables.ahk from a user-config dir
#
# Version-safety rules:
#
#   - Every write is gated on the key actually existing in config_data.
#     If the active profile has a key the current version doesn't know about
#     (e.g., user is on an older version), that key is simply skipped.
#
#   - FEATURE_REGISTRY is loaded from the active version's schema.py at
#     runtime (not via import) to avoid stale cache when versions are switched.
#
#   - re.sub only fires when the pattern is found in the AHK file, so unknown
#     vars in config_data that have no counterpart in config.ahk are harmless.
# =============================================================================

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

def update_config_ahk(config_data: dict, ahk_path: str) -> None:
    """
    Re-apply user-config values onto config.ahk.
    Only writes a value if the corresponding key exists in config_data  
    missing keys (e.g., profile from a newer version on an older install, or
    vice versa) are silently skipped so the AHK file keeps its existing value.

    Mapping:
        trayIconVisible     -> A_IconHidden            (inverted: True->0, False->1)
        tooltipDuration     -> Config_TooltipDuration
        startupTZID         -> StartupTZID
        features.*          -> FeatureNameEnabled vars (via FEATURE_REGISTRY)
        msgEndTask          -> Msg_EndTask
        msgColorPicker      -> Msg_ColorPicker
        colorPickerMsgBox   -> ColorPickerMsgBox
    """
    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- [u1] Tray Icon ---
    if "trayIconVisible" in config_data:
        ahk_icon = 0 if config_data["trayIconVisible"] else 1
        content = re.sub(
            r"(A_IconHidden\s*:=\s*)\d+",
            rf"\g<1>{ahk_icon}",
            content, flags=re.IGNORECASE
        )

    # --- [u2] Tooltip Duration ---
    if "tooltipDuration" in config_data:
        content = re.sub(
            r"(Config_TooltipDuration\s*:=\s*)\d+",
            rf"\g<1>{config_data['tooltipDuration']}",
            content, flags=re.IGNORECASE
        )

    # --- [u4] Startup Timezone ---
    if "startupTZID" in config_data:
        content = re.sub(
            r'(StartupTZID\s*:=\s*)".*?"',
            rf'\g<1>"{config_data["startupTZID"]}"',
            content, flags=re.IGNORECASE
        )

    # --- [z1-z6] Feature toggles ---
    # Load registry from the active version's schema so we never write a toggle that doesn't exist in the currently installed AHK files
    features = config_data.get("features", {})
    if features:
        for entry in FEATURE_REGISTRY:
            key     = entry.get("key")
            ahk_var = entry.get("ahk_var")
            default = entry.get("default", True)
            if key not in features:
                # This feature doesn't exist in the profile's config   skip it
                continue
            ahk_val = 1 if features[key] else 0
            content = re.sub(
                rf"({re.escape(ahk_var)}\s*:=\s*)\d+",
                rf"\g<1>{ahk_val}",
                content, flags=re.IGNORECASE
            )

    # --- [y1] Force Kill message ---
    if "msgEndTask" in config_data:
        content = re.sub(
            r'(Msg_EndTask\s*:=\s*)".*?"',
            rf'\g<1>"{config_data["msgEndTask"]}"',
            content, flags=re.IGNORECASE
        )

    # --- [y2] Color Picker settings ---
    if "msgColorPicker" in config_data:
        content = re.sub(
            r'(Msg_ColorPicker\s*:=\s*)".*?"',
            rf'\g<1>"{config_data["msgColorPicker"]}"',
            content, flags=re.IGNORECASE
        )

    if "colorPickerMsgBox" in config_data:
        ahk_msgbox = 1 if config_data["colorPickerMsgBox"] else 0
        content = re.sub(
            r"(ColorPickerMsgBox\s*:=\s*)\d+",
            rf"\g<1>{ahk_msgbox}",
            content, flags=re.IGNORECASE
        )

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)

    # --- [y3] Vim Arrow Keys settings ---
    if "vimUseLeftAlt" in config_data:
        ahk_lalt = 1 if config_data["vimUseLeftAlt"] else 0
        content = re.sub(
            r"(VimNavigationUseLeftAlt\s*:=\s*)\d+",
            rf"\g<1>{ahk_lalt}",
            content, flags=re.IGNORECASE
        )
    
    if "vimUseRightAlt" in config_data:
        ahk_ralt = 1 if config_data["vimUseRightAlt"] else 0
        content = re.sub(
            r"(VimNavigationUseRightAlt\s*:=\s*)\d+",
            rf"\g<1>{ahk_ralt}",
            content, flags=re.IGNORECASE
        )


def update_timezones_variables_ahk(timezones: list, ahk_path: str) -> None:
    """
    Re-apply the active timezone list onto timezones-variables.ahk.

    For each TZ_* var in the file:
        - Set to 1 if its reconstructed TZ ID is in the active list.
        - Set to 0 otherwise.

    TZ var name convention:
        "Eastern Standard Time" <-> TZ_Eastern_Standard_Time

    Vars in the file that have no match in the timezones list are set to 0,
    not removed   the file structure is always preserved.
    """
    active_set = {tz.replace(" ", "_") for tz in timezones}

    pattern = re.compile(
        r"^([ \t]*TZ_([A-Za-z0-9_]+)\s*:=\s*)([01])",
        re.MULTILINE
    )

    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    def _replace(m):
        prefix   = m.group(1)
        var_name = m.group(2)
        return prefix + ("1" if var_name in active_set else "0")

    content = pattern.sub(_replace, content)

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)
