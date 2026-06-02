import os
import shutil
import zipfile
import requests

from config.manager import load_user_config, save_user_config, sync_schema
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
from ops.startup     import is_startup_enabled, enable_startup, disable_startup

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")
GITHUB_API  = "https://api.github.com/repos/H-int0/autohotkey-v2-scripts/releases/latest"

_KEEP_DIRS = {"backup", "update", "user", "bin"}

def run(enable_startup_flag: bool = False) -> None:
    print("\n>> STRAP UPDATER\n")

    cfg = load_user_config()
    current_version = cfg.get("version", "0.0.0")

    print("Checking GitHub for updates...")
    try:
        resp = requests.get(GITHUB_API, timeout=10)
        resp.raise_for_status()
        data        = resp.json()
        latest_tag  = data.get("tag_name", "")
        zip_url     = data.get("zipball_url", "")
        latest_ver  = latest_tag.lstrip("v")
    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return

    if current_version == latest_ver:
        print(f"You're already on the latest version (v{current_version}).")
        return

    print(f"Update found! Downloading {latest_tag}...")
    update_dir = os.path.join(INSTALL_DIR, "update")
    zip_path   = os.path.join(update_dir, "update.zip")
    os.makedirs(update_dir, exist_ok=True)

    try:
        with requests.get(zip_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print(f"Download failed: {e}")
        return

    print("Extracting...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(update_dir)
    os.remove(zip_path)

    extracted_roots = [
        os.path.join(update_dir, d) for d in os.listdir(update_dir)
        if os.path.isdir(os.path.join(update_dir, d))
    ]
    if not extracted_roots:
        print("Error: Could not find extracted files.")
        return
    extracted_root = extracted_roots[0]

    print("Backing up current version...")
    backup_dir = os.path.join(INSTALL_DIR, "backup")
    os.makedirs(backup_dir, exist_ok=True)

    for item in os.listdir(INSTALL_DIR):
        if item in _KEEP_DIRS:
            continue
        src = os.path.join(INSTALL_DIR, item)
        dst = os.path.join(backup_dir, item)
        if os.path.exists(dst):
            shutil.rmtree(dst) if os.path.isdir(dst) else os.remove(dst)
        shutil.move(src, backup_dir)

    print("Installing new version...")
    for item in os.listdir(extracted_root):
        shutil.move(os.path.join(extracted_root, item), INSTALL_DIR)
    shutil.rmtree(extracted_root)

    print("Applying your settings...")
    cfg = sync_schema(cfg)
    cfg["version"] = latest_ver
    update_config_ahk(cfg, os.path.join(INSTALL_DIR, "core", "config.ahk"))
    update_timezones_variables_ahk(
        cfg["timezones"],
        os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    )

    # --- Interactive/Refresh Startup Flow ---
    if is_startup_enabled():
        print("Refreshing existing startup shortcut...")
        disable_startup()
        enable_startup()
        cfg["startupEnabled"] = True
    elif enable_startup_flag:
        print("Creating startup shortcut...")
        enable_startup()
        cfg["startupEnabled"] = True
    else:
        cfg["startupEnabled"] = False

    save_user_config(cfg)
    print("\n[✔] Update complete!")
