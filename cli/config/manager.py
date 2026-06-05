import os
import json

from config.schema import DEFAULT_CONFIG, MIGRATIONS

# =============================================================================
# manager.py
# Handles reading and writing user-config.json for the active profile.
#
# Profile layout:
#   C:\Users\USERNAME\.strap_profiles\
#       default\user-config.json     always full defaults, never user-edited
#       ghost\user-config.json       auto-created on first change, no named profile
#       <name>\user-config.json      user-named profiles
#
# Active profile is tracked in:
#   %APPDATA%\Strap\bin\active-profile.txt
#
# sync_schema is intentionally NOT used during version switches   the updater
# handles that directly. sync_schema is only for in-place schema drift
# (e.g., the user manually edited their config.json).
# =============================================================================

PROFILES_DIR    = os.path.join(os.environ["USERPROFILE"], ".strap_profiles")
ACTIVE_MARKER   = os.path.join(os.environ["APPDATA"], "Strap", "bin", "active-profile.txt")


# -----------------------------------------------------------------------------
# Active profile helpers
# -----------------------------------------------------------------------------

def get_active_profile_name() -> str:
    """
    Return the name of the currently active profile.
    Defaults to 'ghost' if the marker file is missing or empty.
    """
    if os.path.exists(ACTIVE_MARKER):
        try:
            with open(ACTIVE_MARKER, "r", encoding="utf-8") as f:
                name = f.read().strip()
            if name:
                return name
        except Exception:
            pass
    return "ghost"


def set_active_profile(profile_name: str) -> None:
    """
    Set the active profile by writing its name to active-profile.txt.
    Does not validate that the profile exists   caller's responsibility.
    """
    os.makedirs(os.path.dirname(ACTIVE_MARKER), exist_ok=True)
    with open(ACTIVE_MARKER, "w", encoding="utf-8") as f:
        f.write(profile_name)


def get_active_profile_config_path(profile_name: str | None = None) -> str:
    """
    Return the full path to user-config.json for the given profile name.
    If profile_name is None, uses the currently active profile.
    """
    name = profile_name or get_active_profile_name()
    return os.path.join(PROFILES_DIR, name, "user-config.json")


# -----------------------------------------------------------------------------
# Load / save
# -----------------------------------------------------------------------------

def load_user_config(profile_name: str | None = None) -> dict:
    """
    Load user-config.json from the active (or specified) profile.
    Falls back to DEFAULT_CONFIG if the file is missing or corrupted.
    """
    path = get_active_profile_config_path(profile_name)
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            return DEFAULT_CONFIG.copy()
        return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_user_config(config_data: dict, profile_name: str | None = None) -> None:
    """
    Write config_data to user-config.json in the active (or specified) profile.
    Stamps the version from DEFAULT_CONFIG before saving.
    Will not write to the 'default' profile   that is read-only.
    """
    name = profile_name or get_active_profile_name()

    if name == "default":
        raise ValueError(
            "The 'default' profile is read-only. "
            "Switch to 'ghost' or a named profile before saving."
        )

    path = get_active_profile_config_path(name)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    config_data["version"] = DEFAULT_CONFIG["version"]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)


# -----------------------------------------------------------------------------
# Profile management
# -----------------------------------------------------------------------------

def list_profiles() -> list[str]:
    """Return all profile names found in .strap_profiles, sorted."""
    if not os.path.exists(PROFILES_DIR):
        return []
    return sorted(
        name for name in os.listdir(PROFILES_DIR)
        if os.path.isdir(os.path.join(PROFILES_DIR, name))
        and os.path.exists(os.path.join(PROFILES_DIR, name, "user-config.json"))
    )


def create_profile(profile_name: str) -> None:
    """
    Create a new named profile with default values for all current options.
    Raises ValueError if the name is reserved or already exists.
    """
    if profile_name in {"default", "ghost"}:
        raise ValueError(f"'{profile_name}' is a reserved profile name.")

    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    cfg_path    = os.path.join(profile_dir, "user-config.json")

    if os.path.exists(cfg_path):
        raise ValueError(f"Profile '{profile_name}' already exists.")

    os.makedirs(profile_dir, exist_ok=True)
    base = DEFAULT_CONFIG.copy()
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4)


def delete_profile(profile_name: str) -> None:
    """
    Delete a named profile. Reserved profiles and the active profile
    cannot be deleted.
    Raises ValueError on violations.
    """
    if profile_name in {"default", "ghost"}:
        raise ValueError(f"'{profile_name}' is a reserved profile and cannot be deleted.")

    if profile_name == get_active_profile_name():
        raise ValueError(
            f"'{profile_name}' is the active profile. Switch to another profile first."
        )

    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    if not os.path.exists(profile_dir):
        raise ValueError(f"Profile '{profile_name}' does not exist.")

    import shutil
    shutil.rmtree(profile_dir)


# -----------------------------------------------------------------------------
# Schema sync (in-place drift correction only)
# -----------------------------------------------------------------------------

def sync_schema(current_config: dict) -> dict:
    """
    Bring current_config in line with DEFAULT_CONFIG.
    Used when a config.json has drifted (e.g., manual edits)   NOT for version
    switches (the updater handles that via _add_missing_keys + _sync_all_profiles).

    Steps:
      1. Apply any renames/deletions from MIGRATIONS
      2. Add keys present in DEFAULT_CONFIG but missing from current_config
      3. Drop keys present in current_config but no longer in DEFAULT_CONFIG
      4. Deep-merge one level for dict values (e.g., "features")

    Returns the synced dict. Does NOT save to disk   caller does that.
    Migration values of None mean the key was deleted outright.
    """
    # --- 1. Apply migrations ---
    for old_key, new_key in MIGRATIONS.items():
        if "." in old_key:
            parent, child_old = old_key.split(".", 1)
            if parent in current_config and isinstance(current_config[parent], dict):
                if child_old in current_config[parent]:
                    if new_key is None:
                        del current_config[parent][child_old]
                    else:
                        _, child_new = new_key.split(".", 1)
                        current_config[parent][child_new] = current_config[parent].pop(child_old)
        else:
            if old_key in current_config:
                if new_key is None:
                    del current_config[old_key]
                else:
                    current_config[new_key] = current_config.pop(old_key)

    # --- 2 & 3. Add new keys, drop removed keys ---
    synced = {}
    for key, default_val in DEFAULT_CONFIG.items():
        if key in current_config:
            if isinstance(default_val, dict) and isinstance(current_config[key], dict):
                synced[key] = {
                    k: current_config[key].get(k, v)
                    for k, v in default_val.items()
                }
            else:
                synced[key] = current_config[key]
        else:
            synced[key] = default_val

    synced["version"] = DEFAULT_CONFIG["version"]
    return synced

def apply_headless_config(args: str) -> str:
    """Parse headless config arguments and apply them directly to the active profile."""
    import re, os, subprocess
    from config.schema import DEFAULT_CONFIG
    from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
    from data.timezones import TIMEZONE_CATALOG

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
        arg = arg.strip()
        if arg.startswith("-set--"): arg = arg[6:]
        if arg.isdigit() and 0 <= int(arg)-1 < len(TIMEZONE_CATALOG): return TIMEZONE_CATALOG[int(arg)-1][0]
        norm = arg.replace("_", " ").lower()
        for win_id, display, _, utc in TIMEZONE_CATALOG:
            if win_id.lower() == norm or display.lower() == norm or utc.lower() == norm: return win_id
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
                if win_id in current: current.remove(win_id)
                else: current.append(win_id)
                cfg["timezones"] = current
        elif no == 4:
            win_id = _resolve_tz(sub if sub else v)
            if win_id:
                cfg["startupTZID"] = "" if cfg.get("startupTZID", "") == win_id else win_id
    elif flag == "z":
        fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation"}
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

    if get_active_profile_name() == "default":
        set_active_profile("ghost")

    save_user_config(cfg)
    c_ahk = os.path.join(INSTALL_DIR, "core", "config.ahk")
    t_vars = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    if os.path.exists(c_ahk): update_config_ahk(cfg, c_ahk)
    if os.path.exists(t_vars): update_timezones_variables_ahk(cfg.get("timezones", []), t_vars)
    
    subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shortcut = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup\Strap.lnk")
    if os.path.exists(shortcut):
        try: os.startfile(shortcut)
        except Exception: pass

    return f"Config updated successfully: -{flag} -{no}"
