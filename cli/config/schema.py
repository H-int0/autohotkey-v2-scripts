# =============================================================================
# schema.py
# Defines the canonical structure of user-config.json.
# - DEFAULT_CONFIG : baseline values used when bootstrapping a fresh install
#                    or when a new key appears after an update
# - MIGRATIONS     : rename table for keys that changed names between versions
#                    format: { "old_key": "new_key" }
# =============================================================================

import os

DEFAULT_CONFIG = {
    # Strap version currently installed
    "version": "0.4.0",

    # Absolute path to the Strap install directory
    "installedPath": os.path.join(os.environ["APPDATA"], "Strap"),

    # Whether a startup shortcut exists in shell:startup
    "startupEnabled": False,

    # --- Tooltip settings ---
    "tooltipDuration": 2500,
    "msgColorPicker": "Copied to Clipboard",
    "msgEndTask": "EVAPORATED!",

    # --- Numpad Emulator settings ---
    "numpadShiftSymbols": True,

    # --- Color Picker settings ---
    "colorPickerMsgBox": False,

    # --- Timezone settings ---
    "startupTZID": "",
    "timezones": [
        {"id": "W. Europe Standard Time",   "label": "(UTC +1) \"Berlin / Paris\""},
        {"id": "Russian Standard Time",     "label": "(UTC +3) \"Moscow\""},
        {"id": "Tokyo Standard Time",       "label": "(UTC +9) \"Tokyo\""},
        {"id": "AUS Eastern Standard Time", "label": "(UTC +10) \"Sydney\""},
        {"id": "Eastern Standard Time",     "label": "(UTC -5) \"Eastern Time\""},
    ],

    # --- Feature toggles ---
    # True  = #Include line is active in source.ahk
    # False = #Include line is commented out in source.ahk
    "features": {
        "numpadEmulator":   True,
        "timezoneSwitcher": True,
        "forceKillTask":    True,
        "colorPicker":      False,
        "lineNavigation":   True,
    },
}

# -----------------------------------------------------------------------------
# Migration table
# Add an entry here whenever a key is renamed between Strap versions.
# The manager runs this on startup before doing anything else.
#
# Format:
#   "old_key_name": "new_key_name"
#
# For nested keys (e.g. inside "features"), use dot notation:
#   "features.oldName": "features.newName"
# -----------------------------------------------------------------------------
MIGRATIONS = {
    # Example (not real shows the format):
    # "tooltipDuration": "Config_TooltipDuration",
    # "features.forceKill": "features.forceKillTask",
}
