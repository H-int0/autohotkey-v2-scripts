import os

# =============================================================================
# schema.py
# Defines the canonical structure of user-config.json.
# - DEFAULT_CONFIG : baseline values used when bootstrapping a fresh install
#                    or when a new key appears after an update
# - MIGRATIONS     : rename table for keys that changed names between versions
#                    format: { "old_key": "new_key" }
# =============================================================================

DEFAULT_CONFIG = {
    # Strap version currently installed
    "version": "0.4.0",

    # Absolute path to the Strap install directory
    "installedPath": os.path.join(os.environ["APPDATA"], "Strap"),

    # Whether a startup shortcut exists in shell:startup
    "startupEnabled": False,

    # --- [u1] Tray Icon ---
    # UI:  True  = Visible  (A_IconHidden := 0 in AHK)
    # UI:  False = Hidden   (A_IconHidden := 1 in AHK)
    # Note: AHK's value is the logical inverse of this flag.
    "trayIconVisible": True,

    # --- [u2] Tooltip Timeout ---
    # Positive integer, milliseconds. 1 sec = 1000 ms.
    "tooltipDuration": 2500,

    # --- [u3] Switching Timezones ---
    # Ordered list of active Windows TZ IDs for the timezone cycler.
    # Maps directly to which TZ_* vars are 1 in timezones-variables.ahk.
    "timezones": [
        "W. Europe Standard Time",
        "Russian Standard Time",
        "Tokyo Standard Time",
        "AUS Eastern Standard Time",
        "Eastern Standard Time",
    ],

    # --- [u4] Timezone on Startup ---
    # Single Windows TZ ID string, or "" for no override (default Windows TZ).
    "startupTZID": "",

    # --- [z1-z6] Feature toggles ---
    # True  = enabled  (FeatureNameEnabled := 1 in config.ahk)
    # False = inactive (FeatureNameEnabled := 0 in config.ahk)
    "features": {
        "numpadEmulator":   True,
        "altCodes":         True,
        "timezoneSwitcher": True,
        "forceKillTask":    True,
        "colorPicker":      True,
        "lineNavigation":   True,
    },

    # --- [y1] Force Kill feature settings ---
    "msgEndTask": "EVAPORATED!",

    # --- [y2] Color Picker feature settings ---
    "colorPickerMsgBox": False,
    "msgColorPicker":    "Copied to Clipboard",
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
    "numpadShiftSymbols": None,   # deleted
}
