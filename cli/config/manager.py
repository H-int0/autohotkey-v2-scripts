import os
import json

from config.schema import DEFAULT_CONFIG, MIGRATIONS

# =============================================================================
# manager.py
# Handles reading, writing, and schema-syncing user-config.json.
# =============================================================================

# Dynamically point to AppData
USER_CONFIG_PATH = os.path.join(os.environ["APPDATA"], "Strap", "user", "user-config.json")

def load_user_config() -> dict:
    """
    Load user-config.json. If it doesn't exist or is corrupted,
    fall back to DEFAULT_CONFIG so the app always has valid data.
    """
    if not os.path.exists(USER_CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    try:
        with open(USER_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if isinstance(cfg, dict):
                cfg["version"] = DEFAULT_CONFIG["version"]
            return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_user_config(config_data: dict) -> None:
    """Write config_data to user-config.json, creating dirs if needed."""
    os.makedirs(os.path.dirname(USER_CONFIG_PATH), exist_ok=True)
    
    config_data["version"] = DEFAULT_CONFIG["version"]
    
    with open(USER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)


def sync_schema(current_config: dict) -> dict:
    """
    Bring current_config in line with DEFAULT_CONFIG:
      1. Apply any renames/deletions from MIGRATIONS
      2. Add keys present in DEFAULT_CONFIG but missing from current_config
      3. Drop keys present in current_config but no longer in DEFAULT_CONFIG
      4. Deep-merge one level for dict values (e.g. "features")
    Returns the synced config dict (does NOT save to disk   caller does that).

    Migration values of None mean the key was deleted   it is dropped outright.
    """
    # --- 1. Apply migrations ---
    for old_key, new_key in MIGRATIONS.items():
        if "." in old_key:
            # Nested key: "features.oldName" -> "features.newName" (or None = delete)
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
                # Deep-merge one level (handles "features" sub-dict)
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
