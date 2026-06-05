import os
import json
import shutil
import zipfile
import requests

import importlib
import features
importlib.reload(features)

from config.schema   import DEFAULT_CONFIG
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk
from ops.startup     import is_startup_enabled, enable_startup, disable_startup

INSTALL_DIR  = os.path.join(os.environ["APPDATA"], "Strap")
BIN_DIR      = os.path.join(INSTALL_DIR, "bin")
VERSIONS_DIR = os.path.join(os.environ["USERPROFILE"], ".strap_versions")
PROFILES_DIR = os.path.join(os.environ["USERPROFILE"], ".strap_profiles")

GITHUB_API   = "https://api.github.com/repos/H-int0/autohotkey-v2-scripts/tags"

_SWITCH_KEEP = {"bin"}
_SKIP_ON_COPY = {
    ".git", ".github", ".gitignore", "bin", "__pycache__",
    "CHANGELOG.md", "CONFIGURE.md", "CONTRIBUTING.md",
    "FEATURES.md", "INTEGRATION_GUIDE.md",
    "PULL_REQUEST_TEMPLATE.md",
}

def run_update() -> None:
    print("\n>> STRAP UPDATER\n")
    current_version = _load_active_version()

    print("Checking GitHub for updates...")
    try:
        resp = requests.get(GITHUB_API, timeout=10)
        resp.raise_for_status()
        tags = resp.json()
        if not tags:
            print("No tags found in the repository.")
            return
        latest_tag = tags[0].get("name", "")
        zip_url    = tags[0].get("zipball_url", "")
        latest_ver = latest_tag.lstrip("v")
    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return

    if _parse_version(current_version) >= _parse_version(latest_ver):
        print(f"You're already on the latest version (v{current_version}).")
        return

    print(f"Update found: {latest_tag}")
    version_dir = os.path.join(VERSIONS_DIR, f"v{latest_ver}")

    # Always silently overwrite archive
    if os.path.exists(version_dir):
        print(f"Refreshing archive for v{latest_ver}...")
        shutil.rmtree(version_dir)
    _download_and_archive(zip_url, latest_ver, version_dir)

    ans = input(f"\nYou're on v{current_version}. Switch to v{latest_ver} now? (y/n): ").strip().lower()
    if ans in {"y", "yes", "yeah", "ya", "yep", "yup", "sure", "ok", "okay", "affirmative", "positive"}:
        _do_switch(latest_ver, version_dir)
    else:
        print(f"v{latest_ver} is archived. Run 'strap /switch v{latest_ver}' whenever you're ready.")

def run_switch(target_version: str) -> None:
    print(f"\n>> STRAP VERSION SWITCH\n")
    ver_clean = target_version.lstrip("v")
    ver_tag   = f"v{ver_clean}"
    current_version = _load_active_version()

    if ver_clean == current_version:
        print(f"v{ver_clean} is already the active version.")
        return

    version_dir = os.path.join(VERSIONS_DIR, ver_tag)
    if not os.path.exists(version_dir):
        print(f"[×] v{ver_clean} is not archived in .strap_versions.")
        print(f"    Run 'strap /update' to download the latest, or check available versions with 'strap /versions'.")
        return

    _do_switch(ver_clean, version_dir)

def _load_active_version() -> str:
    path = os.path.join(INSTALL_DIR, "VERSION")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return DEFAULT_CONFIG["version"]

def _do_switch(version: str, version_dir: str) -> None:
    print(f"Switching to v{version}...")
    print("Clearing current active version...")
    for item in os.listdir(INSTALL_DIR):
        if item in _SWITCH_KEEP:
            continue
        target = os.path.join(INSTALL_DIR, item)
        shutil.rmtree(target) if os.path.isdir(target) else os.remove(target)

    print(f"Copying v{version} into active install...")
    for item in os.listdir(version_dir):
        src = os.path.join(version_dir, item)
        dst = os.path.join(INSTALL_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    new_defaults = _load_new_defaults(version)
    if new_defaults is None:
        print("[×] Could not load schema from new version. Switch aborted.")
        return

    new_defaults["version"] = version
    _sync_all_profiles(new_defaults, version)

    active_cfg = _load_active_profile_config()
    if active_cfg:
        _apply_config_to_ahk(active_cfg)

    if is_startup_enabled():
        print("Refreshing startup shortcut...")
        disable_startup()
        enable_startup()

    print(f"\n[√] Switched to v{version} successfully!")

def _download_and_archive(zip_url: str, version: str, version_dir: str) -> None:
    tmp_zip = os.path.join(VERSIONS_DIR, "tmp_download.zip")
    tmp_extract = os.path.join(VERSIONS_DIR, "tmp_extract")
    os.makedirs(VERSIONS_DIR, exist_ok=True)

    print(f"Downloading v{version}...")
    try:
        with requests.get(zip_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(tmp_zip, "wb") as f:
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print(f"Download failed: {e}")
        return

    print("Extracting...")
    os.makedirs(tmp_extract, exist_ok=True)
    with zipfile.ZipFile(tmp_zip, "r") as zf:
        zf.extractall(tmp_extract)
    os.remove(tmp_zip)

    extracted_roots = [
        os.path.join(tmp_extract, d) for d in os.listdir(tmp_extract)
        if os.path.isdir(os.path.join(tmp_extract, d))
    ]
    if not extracted_roots:
        print("[×] Could not find extracted files.")
        shutil.rmtree(tmp_extract, ignore_errors=True)
        return

    extracted_root = extracted_roots[0]
    os.makedirs(version_dir, exist_ok=True)
    for item in os.listdir(extracted_root):
        if item in _SKIP_ON_COPY:
            continue
        src = os.path.join(extracted_root, item)
        dst = os.path.join(version_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    shutil.rmtree(tmp_extract, ignore_errors=True)
    print(f"  [√] v{version} archived to .strap_versions\\v{version}\\")

def _sync_all_profiles(new_defaults: dict, version: str) -> None:
    if not os.path.exists(PROFILES_DIR):
        return
    for profile_name in os.listdir(PROFILES_DIR):
        cfg_path = os.path.join(PROFILES_DIR, profile_name, "user-config.json")
        if not os.path.exists(cfg_path):
            continue
        if profile_name == "default":
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(new_defaults, f, indent=4)
            print(f"  [√] default profile reset to v{version} defaults.")
            continue

        profile_cfg = _load_json(cfg_path)
        changed = _add_missing_keys(profile_cfg, new_defaults)
        profile_cfg["version"] = version
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(profile_cfg, f, indent=4)
        if changed:
            print(f"  [√] '{profile_name}' profile updated with new keys.")
        else:
            print(f"  [√] '{profile_name}' profile stamped v{version}.")

def _load_new_defaults(version: str) -> dict | None:
    schema_path = os.path.join(INSTALL_DIR, "cli", "config", "schema.py")
    if not os.path.exists(schema_path):
        return None
    try:
        namespace = {"__file__": schema_path}
        with open(schema_path, "r", encoding="utf-8") as f:
            exec(compile(f.read(), schema_path, "exec"), namespace)
        return namespace.get("DEFAULT_CONFIG", {}).copy()
    except Exception as e:
        print(f"Warning: could not load new schema: {e}")
        return None

def _load_active_profile_config() -> dict | None:
    active_profile = _get_active_profile_name()
    cfg_path = os.path.join(PROFILES_DIR, active_profile, "user-config.json")
    if os.path.exists(cfg_path):
        return _load_json(cfg_path)
    fallback = os.path.join(PROFILES_DIR, "ghost", "user-config.json")
    if os.path.exists(fallback):
        return _load_json(fallback)
    return None

def _get_active_profile_name() -> str:
    marker = os.path.join(BIN_DIR, "active-profile.txt")
    if os.path.exists(marker):
        try:
            with open(marker, "r", encoding="utf-8") as f:
                return f.read().strip() or "ghost"
        except Exception:
            pass
    return "ghost"

def _apply_config_to_ahk(cfg: dict) -> None:
    config_ahk_path = os.path.join(INSTALL_DIR, "core", "config.ahk")
    tz_vars_path    = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    if os.path.exists(config_ahk_path):
        update_config_ahk(cfg, config_ahk_path)
        print("  [√] config.ahk rewritten from active profile.")
    if os.path.exists(tz_vars_path):
        update_timezones_variables_ahk(cfg.get("timezones", []), tz_vars_path)
        print("  [√] timezones-variables.ahk rewritten from active profile.")

def _add_missing_keys(target: dict, source: dict) -> bool:
    changed = False
    for key, default_val in source.items():
        if key not in target:
            target[key] = default_val
            changed = True
        elif isinstance(default_val, dict) and isinstance(target[key], dict):
            for subkey, subval in default_val.items():
                if subkey not in target[key]:
                    target[key][subkey] = subval
                    changed = True
    return changed

def _load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _parse_version(version_str: str) -> tuple:
    try:
        return tuple(map(int, version_str.lstrip("v").split(".")))
    except ValueError:
        return (0, 0, 0)
