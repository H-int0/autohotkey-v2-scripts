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

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

# =============================================================================
# parser.py
# Reads config.ahk and timezones-variables.ahk and returns Python dicts.
# Used during first install to bootstrap user-config.json from the actual files.
# =============================================================================

def parse_config_ahk(ahk_content: str) -> dict:
    """
    Parse config.ahk content and return a dict of config values.
    Only extracts keys that are tracked in user-config.json.

    Mapping:
        A_IconHidden := 0  ->  trayIconVisible: True   (visible)
        A_IconHidden := 1  ->  trayIconVisible: False  (hidden)
        AHK value is the logical inverse of the UI flag.
    """
    result = {}

    def find(pattern, cast=str):
        m = re.search(pattern, ahk_content, re.IGNORECASE)
        if m:
            try:
                return cast(m.group(1))
            except Exception:
                return None
        return None

    # [u1] Tray Icon   inverted: AHK 1 = hidden = UI False
    val = find(r"A_IconHidden\s*:=\s*(\d+)", int)
    if val is not None:
        result["trayIconVisible"] = (val == 0)

    # [u2] Tooltip Timeout
    val = find(r"Config_TooltipDuration\s*:=\s*(\d+)", int)
    if val is not None:
        result["tooltipDuration"] = val

    # [u4] Timezone on Startup
    val = find(r'StartupTZID\s*:=\s*"(.*?)"')
    if val is not None:
        result["startupTZID"] = val

    # [z1-z6] Feature toggles   AHK 1 = enabled = True
    features = {}
    for f in FEATURE_REGISTRY:
        val = find(rf"{f['ahk_var']}\s*:=\s*(\d+)", int)
        if val is not None:
            features[f["key"]] = bool(val)
    if features:
        result["features"] = features

    # [y1] Force Kill tooltip text
    val = find(r'Msg_EndTask\s*:=\s*"(.*?)"')
    if val is not None:
        result["msgEndTask"] = val

    # [y2] Color Picker settings
    val = find(r"ColorPickerMsgBox\s*:=\s*(\d+)", int)
    if val is not None:
        result["colorPickerMsgBox"] = bool(val)

    val = find(r'Msg_ColorPicker\s*:=\s*"(.*?)"')
    if val is not None:
        result["msgColorPicker"] = val

    return result


def parse_timezones_variables_ahk(ahk_content: str) -> list:
    from data.timezones_catalog import TIMEZONE_CATALOG

    var_to_id = {
        tz_id.replace(" ", "_").replace(".", "_").replace("-", "_"): tz_id
        for tz_id, *_ in TIMEZONE_CATALOG
    }

    active = []
    pattern = re.compile(
        r"^[ \t]*TZ_([A-Za-z0-9_]+)\s*:=\s*([01])",
        re.MULTILINE
    )
    for m in pattern.finditer(ahk_content):
        underscore_name = m.group(1)
        enabled         = m.group(2) == "1"
        tz_id           = var_to_id.get(underscore_name)
        if enabled and tz_id:
            active.append(tz_id)

    return active
