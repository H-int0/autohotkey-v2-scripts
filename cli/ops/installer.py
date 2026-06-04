import os
import shutil
import winreg
import ctypes

from config.schema  import DEFAULT_CONFIG
from ops.startup    import enable_startup

INSTALL_DIR    = os.path.join(os.environ["APPDATA"], "Strap")
BIN_DIR        = os.path.join(INSTALL_DIR, "bin")
BAT_PATH       = os.path.join(BIN_DIR, "strap.bat")

VERSIONS_DIR   = os.path.join(os.environ["USERPROFILE"], ".strap_versions")
PROFILES_DIR   = os.path.join(os.environ["USERPROFILE"], ".strap_profiles")

PROFILE_DEFAULT = os.path.join(PROFILES_DIR, "default")
PROFILE_GHOST   = os.path.join(PROFILES_DIR, "ghost")
DEFAULT_CONFIG_PATH = os.path.join(PROFILE_DEFAULT, "user-config.json")
GHOST_CONFIG_PATH   = os.path.join(PROFILE_GHOST,   "user-config.json")

_SKIP_ON_COPY = {
    ".git", ".github", ".gitignore", "bin", "__pycache__",
    "CHANGELOG.md", "CONFIGURE.md", "CONTRIBUTING.md",
    "FEATURES.md", "INTEGRATION_GUIDE.md",
    "PULL_REQUEST_TEMPLATE.md",
}

def run(from_ps: bool = False, enable_startup_flag: bool = False) -> None:
    print("\n>> STRAP INSTALLER\n")

    if not _check_python():
        return

    version = DEFAULT_CONFIG["version"]

    if from_ps:
        if not os.path.exists(INSTALL_DIR):
            print("[×] Install directory not found. Something went wrong in the PS script.")
            return
        print(f"Continuing installation (v{version}) handed off from PowerShell...")
    else:
        if not _install_from_repo(version):
            return

    _ensure_bat()
    _add_to_user_path(BIN_DIR)
    _bootstrap_profiles(version)

    if enable_startup_flag:
        print("Creating startup shortcut...")
        enable_startup()

    print(f"\n[√] Strap v{version} installed successfully!")
    print("IMPORTANT: Close and restart your terminal to use the 'strap' command globally.")


def _check_python() -> bool:
    import subprocess
    try:
        subprocess.run(["python", "--version"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        print("[×] Python is not installed on your system.")
        print("    Strap could not complete installation.")
        print("    Download Python from: https://www.python.org/downloads/")
        return False


def _read_installed_version() -> str:
    path = os.path.join(INSTALL_DIR, "VERSION")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _install_from_repo(version: str) -> bool:
    """
    Archive repo → copy to APPDATA.
    Returns False if the user declines to overwrite an existing install.
    """
    repo_dir    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    version_dir = os.path.join(VERSIONS_DIR, f"v{version}")

    # Always silently overwrite the archive
    if os.path.exists(version_dir):
        print(f"Refreshing archive for v{version}...")
        shutil.rmtree(version_dir)
    else:
        print(f"Archiving v{version} to .strap_versions...")
    os.makedirs(version_dir, exist_ok=True)
    _copy_repo_contents(repo_dir, version_dir)

    if os.path.exists(INSTALL_DIR):
        current = _read_installed_version()
        label   = f"v{current}" if current else "an existing version"
        ans = input(
            f"Strap {label} is already installed. Overwrite with v{version}? (y/n): "
        ).strip().lower()
        if ans not in {"y", "yes", "yeah", "ya", "yep", "yup", "sure", "ok", "okay", "affirmative", "positive"}:
            print(f"Installation aborted. Archive for v{version} is saved in .strap_versions.")
            return False
        print("Overwriting existing installation...")
        for item in os.listdir(INSTALL_DIR):
            if item == "bin":
                continue
            target = os.path.join(INSTALL_DIR, item)
            shutil.rmtree(target) if os.path.isdir(target) else os.remove(target)

    print(f"Copying v{version} to %APPDATA%\\Strap...")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    _copy_repo_contents(repo_dir, INSTALL_DIR)
    return True

def _copy_repo_contents(src_dir: str, dst_dir: str) -> None:
    for item in os.listdir(src_dir):
        if item in _SKIP_ON_COPY:
            continue
        src = os.path.join(src_dir, item)
        dst = os.path.join(dst_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

def _ensure_bat() -> None:
    os.makedirs(BIN_DIR, exist_ok=True)
    if not os.path.exists(BAT_PATH):
        print("Creating strap.bat...")
        with open(BAT_PATH, "w") as f:
            f.write(f'@echo off\npython "{os.path.join(INSTALL_DIR, "cli", "main.py")}" %*\n')
    else:
        print("strap.bat already exists, skipping.")

def _bootstrap_profiles(version: str) -> None:
    import json
    print("Bootstrapping profiles...")

    os.makedirs(PROFILE_DEFAULT, exist_ok=True)
    os.makedirs(PROFILE_GHOST,   exist_ok=True)

    base = DEFAULT_CONFIG.copy()
    base["version"] = version

    tz_vars_path = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    if os.path.exists(tz_vars_path):
        from config.parser import parse_timezones_variables_ahk
        with open(tz_vars_path, "r", encoding="utf-8") as f:
            active_tzs = parse_timezones_variables_ahk(f.read())
        if active_tzs:
            base["timezones"] = active_tzs

    with open(DEFAULT_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4)
    print("  [√] default profile written.")

    if not os.path.exists(GHOST_CONFIG_PATH):
        with open(GHOST_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(base.copy(), f, indent=4)
        print("  [√] ghost profile created.")
    else:
        ghost = _load_json(GHOST_CONFIG_PATH)
        changed = _add_missing_keys(ghost, base)
        ghost["version"] = version
        if changed:
            with open(GHOST_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(ghost, f, indent=4)
            print("  [√] ghost profile updated with new keys.")
        else:
            print("  [√] ghost profile already up to date.")

    for profile_name in os.listdir(PROFILES_DIR):
        if profile_name in {"default", "ghost"}:
            continue
        cfg_path = os.path.join(PROFILES_DIR, profile_name, "user-config.json")
        if not os.path.exists(cfg_path):
            continue
        profile_cfg = _load_json(cfg_path)
        changed = _add_missing_keys(profile_cfg, base)
        profile_cfg["version"] = version
        if changed:
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(profile_cfg, f, indent=4)
            print(f"  [√] '{profile_name}' profile updated with new keys.")

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
    import json
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _add_to_user_path(new_path: str) -> None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        if new_path.lower() not in current_path.lower():
            if not current_path.endswith(";"):
                current_path += ";"
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, current_path + new_path)
            HWND_BROADCAST  = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 2, 5000, None)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"\nWarning: Could not add to PATH automatically. ({e})")
        print(f"You may need to add this manually: {new_path}")
