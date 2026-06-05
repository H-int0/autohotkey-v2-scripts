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
