# =============================================================================
# parser.py
# Reads config.ahk and source.ahk and returns Python dicts.
# Used during first install to bootstrap user-config.json from the actual files.
#
# =============================================================================

import re


def parse_config_ahk(ahk_content: str) -> dict:
    """
    Parse config.ahk content and return a dict of config values.
    Only extracts keys that are tracked in user-config.json.
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

    val = find(r"Config_TooltipDuration\s*:=\s*(\d+)", int)
    if val is not None:
        result["tooltipDuration"] = val

    val = find(r'Msg_ColorPicker\s*:=\s*"(.*?)"')
    if val is not None:
        result["msgColorPicker"] = val

    val = find(r'Msg_EndTask\s*:=\s*"(.*?)"')
    if val is not None:
        result["msgEndTask"] = val

    val = find(r"NumpadShiftSymbols\s*:=\s*(true|false)")
    if val is not None:
        result["numpadShiftSymbols"] = val.lower() == "true"

    val = find(r"ColorPickerMsgBox\s*:=\s*(true|false)")
    if val is not None:
        result["colorPickerMsgBox"] = val.lower() == "true"

    val = find(r'StartupTZID\s*:=\s*"(.*?)"')
    if val is not None:
        result["startupTZID"] = val

    # Extract active timezones skip the empty template entry TZData[""] := ...
    tzs = []
    for m in re.finditer(r'TZData\["(?!")([^"]+)"\]\s*:=\s*"(.*?)"', ahk_content):
        tzs.append({"id": m.group(1), "label": m.group(2)})
    if tzs:
        result["timezones"] = tzs

    return result


def parse_source_ahk(ahk_content: str) -> dict:
    """
    Parse the SELECT FEATURES TO LOAD block in source.ahk.
    Returns a dict of { camelCaseFeatureName: bool (True = enabled) }.
    A line starting with '; #Include' is disabled; '#Include' alone is enabled.
    """
    features = {}

    # Matches both:
    #   #Include features/numpad-emulator.ahk        (enabled)
    #   ; #Include features/numpad-emulator.ahk      (disabled)
    pattern = r"^[ \t]*(;?\s*)#Include\s+features/([a-zA-Z0-9_-]+)\.ahk"
    for m in re.finditer(pattern, ahk_content, re.MULTILINE):
        disabled = m.group(1).strip().startswith(";")
        filename = m.group(2)  # e.g. "numpad-emulator"

        # dash-case -> camelCase
        parts = filename.split("-")
        camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
        features[camel] = not disabled

    return features
