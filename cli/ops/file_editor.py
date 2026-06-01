import re


def update_config_ahk(config_data: dict, ahk_path: str) -> None:
    """
    Re-apply user-config values onto config.ahk.
    Called after every --save or update to keep config.ahk in sync with
    user-config.json.

    Writes:
        A_IconHidden            <- inverted: trayIconVisible True  -> 0
                                                              False -> 1
        Config_TooltipDuration  <- tooltipDuration (int)
        NumpadEmulatorEnabled   <- features.numpadEmulator   (0/1)
        AltCodesEnabled         <- features.altCodes         (0/1)
        TimezoneSwitcherEnabled <- features.timezoneSwitcher (0/1)
        ForceKillEnabled        <- features.forceKillTask    (0/1)
        ColorPickerEnabled      <- features.colorPicker      (0/1)
        LineNavEnabled          <- features.lineNavigation   (0/1)
        Msg_EndTask             <- msgEndTask   (string)
        Msg_ColorPicker         <- msgColorPicker (string)
        ColorPickerMsgBox       <- colorPickerMsgBox (0/1)
        StartupTZID             <- startupTZID (string)
    """
    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- [u1] Tray Icon ---
    # UI True (visible) -> AHK 0; UI False (hidden) -> AHK 1
    ahk_icon = 0 if config_data.get("trayIconVisible", True) else 1
    content = re.sub(
        r"(A_IconHidden\s*:=\s*)\d+",
        rf"\g<1>{ahk_icon}",
        content, flags=re.IGNORECASE
    )

    # --- [u2] Tooltip Timeout ---
    content = re.sub(
        r"(Config_TooltipDuration\s*:=\s*)\d+",
        rf"\g<1>{config_data.get('tooltipDuration', 2500)}",
        content, flags=re.IGNORECASE
    )

    # --- [u4] Timezone on Startup ---
    content = re.sub(
        r'(StartupTZID\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("startupTZID", "")}"',
        content, flags=re.IGNORECASE
    )

    # --- [z1-z6] Feature toggles ---
    feature_map = {
        "numpadEmulator":   "NumpadEmulatorEnabled",
        "altCodes":         "AltCodesEnabled",
        "timezoneSwitcher": "TimezoneSwitcherEnabled",
        "forceKillTask":    "ForceKillEnabled",
        "colorPicker":      "ColorPickerEnabled",
        "lineNavigation":   "LineNavEnabled",
    }
    features = config_data.get("features", {})
    for cfg_key, ahk_var in feature_map.items():
        ahk_val = 1 if features.get(cfg_key, True) else 0
        content = re.sub(
            rf"({re.escape(ahk_var)}\s*:=\s*)\d+",
            rf"\g<1>{ahk_val}",
            content, flags=re.IGNORECASE
        )

    # --- [y1] Force Kill tooltip text ---
    content = re.sub(
        r'(Msg_EndTask\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("msgEndTask", "EVAPORATED!")}"',
        content, flags=re.IGNORECASE
    )

    # --- [y2] Color Picker settings ---
    content = re.sub(
        r'(Msg_ColorPicker\s*:=\s*)".*?"',
        rf'\g<1>"{config_data.get("msgColorPicker", "Copied to Clipboard")}"',
        content, flags=re.IGNORECASE
    )
    ahk_msgbox = 1 if config_data.get("colorPickerMsgBox", False) else 0
    content = re.sub(
        r"(ColorPickerMsgBox\s*:=\s*)\d+",
        rf"\g<1>{ahk_msgbox}",
        content, flags=re.IGNORECASE
    )

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_timezones_variables_ahk(timezones: list, ahk_path: str) -> None:
    """
    Re-apply the active timezone list onto timezones-variables.ahk.

    `timezones` is the list of active Windows TZ ID strings from user-config.json,
    e.g. ["Eastern Standard Time", "Russian Standard Time"].

    For each TZ_* var in the file:
        - Set to 1 if its reconstructed TZ ID is in the active list.
        - Set to 0 otherwise.

    The TZ var name is derived by replacing spaces with underscores and
    prepending TZ_, which is exactly how the file was originally generated.
    E.g. "Eastern Standard Time" <-> TZ_Eastern_Standard_Time
    """
    # Build a lookup set of underscore-form names for O(1) membership checks
    # e.g. "Eastern Standard Time" -> "Eastern_Standard_Time"
    active_set = {tz.replace(" ", "_") for tz in timezones}

    pattern = re.compile(
        r"^([ \t]*TZ_([A-Za-z0-9_]+)\s*:=\s*)([01])",
        re.MULTILINE
    )

    with open(ahk_path, "r", encoding="utf-8") as f:
        content = f.read()

    def _replace(m):
        prefix   = m.group(1)          # everything up to and including ":= "
        var_name = m.group(2)          # e.g. "Eastern_Standard_Time"
        new_val  = "1" if var_name in active_set else "0"
        return prefix + new_val

    content = pattern.sub(_replace, content)

    with open(ahk_path, "w", encoding="utf-8") as f:
        f.write(content)
