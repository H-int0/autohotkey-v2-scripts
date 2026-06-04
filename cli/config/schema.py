import os

# =============================================================================
# schema.py
# Defines the canonical structure of user-config.json.
# - DEFAULT_CONFIG : baseline values used when bootstrapping a fresh install
#                    or when a new key appears after an update
# - MIGRATIONS     : rename table for keys that changed names between versions
#                    format: { "old_key": "new_key" }
# =============================================================================

FEATURE_REGISTRY = [
    {"key": "numpadEmulator",   "ahk_var": "NumpadEmulatorEnabled",  "label": "NumPad Emulator",    "default": True},
    {"key": "altCodes",         "ahk_var": "AltCodesEnabled",        "label": "ALT Codes",          "default": True},
    {"key": "timezoneSwitcher", "ahk_var": "TimezoneSwitcherEnabled","label": "TimeZone Switcher",  "default": True},
    {"key": "forceKillTask",    "ahk_var": "ForceKillEnabled",       "label": "Force Kill",         "default": True},
    {"key": "colorPicker",      "ahk_var": "ColorPickerEnabled",     "label": "Color Picker",       "default": True},
    {"key": "lineNavigation",   "ahk_var": "LineNavEnabled",         "label": "Line Navigation",    "default": True},
]

def _read_version() -> str:
    import os

    _here = os.path.dirname(os.path.abspath(__file__))
    for candidate in [
        os.path.join(_here, "..", "..", "VERSION"),
        os.path.join(os.environ["APPDATA"], "Strap", "VERSION"),
    ]:
        try:
            with open(os.path.normpath(candidate), "r", encoding="utf-8") as f:
                return f.read().strip()
        except OSError:
            pass
    return "0.0.0"

DEFAULT_CONFIG = {
    # Strap version currently installed
    "version": _read_version(),

    # Absolute path to the active Strap install directory.
    # This always points to %APPDATA%\Strap the running version.
    # Archived versions live in C:\Users\USERNAME\.strap_versions\
    "installedPath": os.path.join(os.environ["APPDATA"], "Strap"),

    # Whether a startup shortcut exists in shell:startup
    "startupEnabled": False,

    # --- [u1] Tray Icon ---
    # UI:  True  = Visible  (A_IconHidden := 0 in AHK)
    # UI:  False = Hidden   (A_IconHidden := 1 in AHK)
    # Note: AHK's value is the logical inverse of this flag.
    "trayIconVisible": False,

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
    "features": {f["key"]: f["default"] for f in FEATURE_REGISTRY},

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
# For nested keys (e.g., inside "features"), use dot notation:
#   "features.oldName": "features.newName"
# -----------------------------------------------------------------------------
MIGRATIONS = {
  
}
