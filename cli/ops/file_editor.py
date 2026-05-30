# =============================================================================
# file_editor.py
# Surgically edits config.ahk and source.ahk in-place.
# Never rewrites the whole file only touches the specific values that changed.
# =============================================================================

import re


def update_config_ahk(config_data: dict, ahk_path: str) -> None:
    """
    Re-apply user-config values onto config.ahk.
    Called after every update to keep config.ahk in sync with user-config.json.
    """
    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- Scalar replacements ---
    content = re.sub(
        r"(Config_TooltipDuration\s*:=\s*)\d+",
        rf"\g<1>{config_data.get('tooltipDuration', 2500)}",
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r'(Msg_ColorPicker\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("msgColorPicker", "Copied to Clipboard")}"',
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r'(Msg_EndTask\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("msgEndTask", "EVAPORATED!")}"',
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r"(NumpadShiftSymbols\s*:=\s*)(true|false)",
        rf"\g<1>{'true' if config_data.get('numpadShiftSymbols', True) else 'false'}",
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r"(ColorPickerMsgBox\s*:=\s*)(true|false)",
        rf"\g<1>{'true' if config_data.get('colorPickerMsgBox', False) else 'false'}",
        content, flags=re.IGNORECASE
    )
    content = re.sub(
        r'(StartupTZID\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("startupTZID", "")}"',
        content, flags=re.IGNORECASE
    )

    # --- Timezone block replacement ---
    # Remove all existing active TZData/TZOrder pairs (leaves the empty template untouched)
    content = re.sub(
        r'TZData\["(?!")([^"]+)"\]\s*:=\s*".*?"\s*\nTZOrder\.Push\("[^"]+"\)\s*\n*',
        "",
        content
    )

    # Build replacement timezone block
    tz_block = ""
    for tz in config_data.get("timezones", []):
        tz_block += f'TZData["{tz["id"]}"] := "{tz["label"]}"\n'
        tz_block += f'TZOrder.Push("{tz["id"]}")\n\n'

    # Inject just before the template comment anchor
    template_anchor = r"(; the CLI tool should make copies of this and add values to it to add a new timezone)"
    content = re.sub(template_anchor, tz_block + r"\1", content)

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_source_ahk(features: dict, ahk_path: str) -> None:
    """
    Comment or uncomment #Include lines in source.ahk based on the features dict.
    Only touches lines inside the SELECT FEATURES TO LOAD block.
    """
    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    for feature_camel, enabled in features.items():
        # camelCase -> dash-case  (e.g. numpadEmulator -> numpad-emulator)
        dash = re.sub(r"(?<!^)(?=[A-Z])", "-", feature_camel).lower()

        # Match the line whether it's currently enabled or disabled
        pattern = rf"^([ \t]*)(;?\s*)(#Include\s+features/{re.escape(dash)}\.ahk)"
        if enabled:
            replacement = r"\1\3"        # remove any leading '; '
        else:
            replacement = r"\1; \3"      # add '; ' prefix

        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)
