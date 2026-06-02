import os
import shutil
import winreg

from config.manager import load_user_config, save_user_config
from config.parser  import parse_config_ahk, parse_timezones_variables_ahk

from ops.startup    import enable_startup

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")
BIN_DIR     = os.path.join(INSTALL_DIR, "bin")
BAT_PATH    = os.path.join(BIN_DIR, "strap.bat")

_SKIP_ON_COPY = {".git", "backup", "update", "user", "bin", "__pycache__"}

def run(reinstall: bool = False, enable_startup_flag: bool = False) -> None:
    print("\n>> STRAP INSTALLER\n")

    if os.path.exists(INSTALL_DIR):
        if reinstall:
            print("Removing old installation (saving user config)...")
            
            # Temporarily backup user config so they don't lose their settings
            user_backup = None
            user_dir = os.path.join(INSTALL_DIR, "user")
            if os.path.exists(user_dir):
                user_backup = os.path.join(os.environ["TEMP"], "strap_user_backup")
                if os.path.exists(user_backup):
                    shutil.rmtree(user_backup)
                shutil.copytree(user_dir, user_backup)

            shutil.rmtree(INSTALL_DIR, ignore_errors=True)
            os.makedirs(INSTALL_DIR, exist_ok=True)

            if user_backup:
                shutil.copytree(user_backup, os.path.join(INSTALL_DIR, "user"))
                shutil.rmtree(user_backup)
        else:
            print("Installation aborted.")
            return

    print("Creating directories...")
    for d in [INSTALL_DIR, BIN_DIR,
              os.path.join(INSTALL_DIR, "backup"),
              os.path.join(INSTALL_DIR, "update"),
              os.path.join(INSTALL_DIR, "user")]:
        os.makedirs(d, exist_ok=True)

    print("Copying core files...")
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    for item in os.listdir(repo_dir):
        if item in _SKIP_ON_COPY:
            continue
        src = os.path.join(repo_dir, item)
        dst = os.path.join(INSTALL_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    print("Registering commands to Windows PATH...")
    with open(BAT_PATH, "w") as f:
        f.write(f'@echo off\npython "{os.path.join(INSTALL_DIR, "cli", "main.py")}" %*\n')
    _add_to_user_path(BIN_DIR)

    print("Bootstrapping configurations...")
    config_ahk_path = os.path.join(INSTALL_DIR, "core", "config.ahk")
    cfg = load_user_config()

    if os.path.exists(config_ahk_path):
        with open(config_ahk_path, "r", encoding="utf-8") as f:
            cfg.update(parse_config_ahk(f.read()))

    tz_vars_path = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
    if os.path.exists(tz_vars_path):
        with open(tz_vars_path, "r", encoding="utf-8") as f:
            cfg["timezones"] = parse_timezones_variables_ahk(f.read())

    # Apply the startup choice passed from the TUI / CLI
    if enable_startup_flag:
        print("Creating startup shortcut...")
        enable_startup()
        cfg["startupEnabled"] = True
    else:
        cfg["startupEnabled"] = False

    save_user_config(cfg)
    print("\n[✔] Installation complete!")
    print("IMPORTANT: Close and restart your terminal to use the 'strap' command globally.")

def _add_to_user_path(new_path: str) -> None:
    try:
        import ctypes
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        
        if new_path.lower() not in current_path.lower():
            if not current_path.endswith(";"):
                current_path += ";"
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, current_path + new_path)
            
            # Broadcast the change globally so existing explorer sessions fetch the updated path
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 2, 5000, None)
            
        winreg.CloseKey(key)
    except Exception as e:
        print(f"\nWarning: Could not add to PATH automatically. ({e})")
        print(f"You may need to add this manually: {new_path}")
