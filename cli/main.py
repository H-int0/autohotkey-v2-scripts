import sys
import os
import subprocess
import shutil
import winreg
import ctypes
import requests

from tui.constants import TERMINAL_COMMANDS_TEXT
from ops.updater import GITHUB_API

# =============================================================================
# main.py
# Entry point for the Strap CLI.
# =============================================================================

INSTALL_DIR  = os.path.join(os.environ.get("APPDATA", ""), "Strap")
BIN_DIR      = os.path.join(INSTALL_DIR, "bin")
VERSIONS_DIR = os.path.join(os.environ.get("USERPROFILE", ""), ".strap_versions")
PROFILES_DIR = os.path.join(os.environ.get("USERPROFILE", ""), ".strap_profiles")

_YES = {"y", "yes", "yeah", "ya", "yep", "yup", "sure", "ok", "okay", "affirmative", "positive"}

def _print_help() -> None:
    print(TERMINAL_COMMANDS_TEXT)

def cli_install(target_version: str = "", from_ps: bool = False) -> None:
    from ops.installer import run as install_run, _check_python, _read_installed_version

    if not _check_python():
        return

    if target_version:
        # /install vX.X.X download specific version then run the same install tail
        from ops.updater import _download_and_archive, _do_switch, _sync_all_profiles, _load_new_defaults
        ver_clean   = target_version.lstrip("v")
        version_dir = os.path.join(VERSIONS_DIR, f"v{ver_clean}")

        # Always silently overwrite archive
        if os.path.exists(version_dir):
            print(f"Refreshing archive for v{ver_clean}...")
            shutil.rmtree(version_dir)
        zip_url = f"https://codeload.github.com/H-int0/autohotkey-v2-scripts/zip/refs/tags/v{ver_clean}"
        _download_and_archive(zip_url, ver_clean, version_dir)

        if not os.path.exists(version_dir):
            print("[×] Download failed, aborting.")
            return

        # Same install tail as normal install
        if os.path.exists(INSTALL_DIR):
            current = _read_installed_version()
            label   = f"v{current}" if current else "an existing version"
            ans = input(
                f"Strap {label} is already installed. Switch to v{ver_clean}? (y/n): "
            ).strip().lower()
            if ans not in _YES:
                print(f"Keeping current install. v{ver_clean} is archived in .strap_versions.")
                return
            _do_switch(ver_clean, version_dir)
        else:
            # Fresh install from the downloaded archive
            import shutil as _shutil
            print(f"Copying v{ver_clean} to %APPDATA%\\Strap...")
            os.makedirs(INSTALL_DIR, exist_ok=True)
            for item in os.listdir(version_dir):
                src = os.path.join(version_dir, item)
                dst = os.path.join(INSTALL_DIR, item)
                if os.path.isdir(src):
                    _shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    _shutil.copy2(src, dst)
            # Bootstrap profiles for fresh install
            from ops.installer import _ensure_bat, _add_to_user_path, _bootstrap_profiles, BIN_DIR
            _ensure_bat()
            _add_to_user_path(BIN_DIR)
            _bootstrap_profiles(ver_clean)

        print(f"\n[√] Strap v{ver_clean} installed successfully!")
        return

    ans = input("Do you want Strap to automatically start on boot? (y/n): ").strip().lower()
    install_run(from_ps=from_ps, enable_startup_flag=ans in _YES)

def cli_update() -> None:
    from ops.updater import run_update
    run_update()

def cli_switch(target_version: str) -> None:
    if not target_version:
        print("Usage: strap /switch <version>  (e.g., strap /switch v1.2.1)")
        return
    from ops.updater import run_switch
    run_switch(target_version)

def cli_version() -> None:
    try:
        with open(os.path.join(INSTALL_DIR, "VERSION"), "r", encoding="utf-8") as f:
            active_version = f.read().strip()
    except Exception:
        from config.schema import DEFAULT_CONFIG
        active_version = DEFAULT_CONFIG["version"]

    if not os.path.exists(VERSIONS_DIR):
        print("No archived versions found.")
        return

    versions = sorted(
        d for d in os.listdir(VERSIONS_DIR)
        if os.path.isdir(os.path.join(VERSIONS_DIR, d))
    )

    if not versions:
        print("No archived versions found.")
        return

    print("\nArchived versions:")
    for v in versions:
        tag = v.lstrip("v")
        marker = " (active)" if tag == active_version else ""
        print(f"  {v}{marker}")
    print()

def cli_profile(subargs: str) -> None:
    from config.manager import (
        get_active_profile_name, set_active_profile,
        create_profile, delete_profile, list_profiles,
        load_user_config
    )
    from ops.file_editor import update_config_ahk, update_timezones_variables_ahk

    parts = subargs.strip().split(" ", 1) if subargs.strip() else []
    sub   = parts[0].strip() if parts else ""
    arg   = parts[1].strip() if len(parts) > 1 else ""
    subl  = sub.lower()

    if not sub or subl == "--ls":
        active = get_active_profile_name()
        profiles = list_profiles()
        if not profiles:
            print("No profiles found.")
            return
        print("\nProfiles:")
        for p in profiles:
            marker = " (active)" if p == active else ""
            print(f"  {p}{marker}")
        print()
    elif subl == "--d":
        if not arg:
            print("Usage: strap /profile --d <name>")
            return
        try:
            delete_profile(arg)
            print(f"[√] Profile '{arg}' deleted.")
        except ValueError as e:
            print(f"[×] {e}")
    elif subl == "--use":
        if not arg:
            print("Usage: strap /profile --use <name>")
            return
        cfg_path = os.path.join(PROFILES_DIR, arg, "user-config.json")
        if os.path.exists(cfg_path):
            set_active_profile(arg)
            print(f"Switched to profile '{arg}'. Applying to AHK files...")
            cfg = load_user_config(arg)
            config_ahk = os.path.join(INSTALL_DIR, "core", "config.ahk")
            tz_vars    = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
            if os.path.exists(config_ahk):
                update_config_ahk(cfg, config_ahk)
            if os.path.exists(tz_vars):
                update_timezones_variables_ahk(cfg.get("timezones", []), tz_vars)
            print(f"[√] Profile '{arg}' is now active.")
        else:
            print(f"[×] Profile '{arg}' does not exist.")
    elif subl == "--cr":
        if not arg:
            print("Usage: strap /profile --cr <name>")
            return
        try:
            create_profile(arg)
            print(f"[√] Profile '{arg}' created.")
        except ValueError as e:
            print(f"[×] {e}")
    else:
        print(f"Unknown profile subcommand: '{sub}'. Use --ls, --cr, --use, --d.")

def cli_uninstall() -> None:
    print("\n>> STRAP UNINSTALLER\n")
    ans = input("This will remove Strap from your system. Continue? (y/n): ").strip().lower()
    if ans not in _YES:
        print("Uninstall aborted.")
        return

    print("Terminating AHK processes...")
    from ops.process import stop_ahk
    stop_ahk()

    print("Removing startup shortcut...")
    from ops.startup import disable_startup
    disable_startup()

    print("Removing from PATH...")
    _remove_from_user_path(BIN_DIR)

    print("Removing installation files...")
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR, ignore_errors=True)
    if os.path.exists(VERSIONS_DIR):
        shutil.rmtree(VERSIONS_DIR, ignore_errors=True)

    print("\n[√] Strap was uninstalled successfully.")
    print("До встречи!")

def cli_install_ls() -> None:
    PAGE = 10
    print("\nFetching version tags from GitHub...")
    try:
        resp = requests.get(GITHUB_API + "?per_page=100", timeout=10)
        resp.raise_for_status()
        tags = [t.get("name", "") for t in resp.json()]
    except Exception as e:
        print(f"Failed to fetch tags: {e}")
        return

    if not tags:
        print("No tags found.")
        return

    i = 0
    while i < len(tags):
        chunk = tags[i:i + PAGE]
        for t in chunk:
            print(f"  {t}")
        i += PAGE
        if i >= len(tags):
            print("END")
            break
        print("Press Enter for more, q to quit: ", end="", flush=True)
        try:
            ans = input()
        except (EOFError, KeyboardInterrupt):
            break
        if ans.strip().lower() == "q":
            break

def main() -> None:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    args = sys.argv[1:]
    if args and args[0].lower() in ("strap", "/strap", "starp", "/starp"):
        args = args[1:]

    if args:
        raw_arg = " ".join(args).strip()
        for prefix in ("strap ", "/strap ", "starp ", "/starp "):
            if raw_arg.lower().startswith(prefix):
                raw_arg = raw_arg[len(prefix):].strip()
                break

        parts = raw_arg.split(" ", 1)
        cmd   = parts[0].lower()
        rest  = parts[1].strip() if len(parts) > 1 else ""

        if not cmd.startswith("/"):
            cmd = "/" + cmd

        # Terminal execution without TUI
        if cmd == "/install":
            if rest == "--ls":
                cli_install_ls()
            else:
                from_ps = rest == "--from-ps"
                ver = rest if (rest and not rest.startswith("--")) else ""
                cli_install(target_version=ver, from_ps=from_ps)
        elif cmd == "/update":
            cli_update()
        elif cmd == "/switch":
            cli_switch(rest)
        elif cmd in ("/versions", "/version"):
            if rest == "--ls":
                cli_version()
            else:
                cli_version()
        elif cmd == "/profile":
            cli_profile(rest)
        elif cmd == "/uninstall":
            cli_uninstall()
        elif cmd == "/config":
            if rest:
                from headless import apply_headless_config
                print(apply_headless_config(rest))
            else:
                while True:
                    from tui.app import StrapApp
                    app = StrapApp(start_screen="config")
                    result = app.run()
                    if result != "reload":
                        break

        elif cmd in ("/help", "/?"):
            _print_help()
        elif cmd == "/run":
            if rest == "--cr shr":
                from ops.process import start_ahk
                start_ahk()
                print("[√] Startup shortcut created.")
            elif rest in ("--d shr", "-d shr"):
                from ops.startup import disable_startup
                disable_startup()
                print("Startup shortcut removed.")
            else:
                target = os.path.join(INSTALL_DIR, "core", "source.ahk")
                if os.path.exists(target):
                    print(f"Launching Strap: {target}")
                    try: os.startfile(target)
                    except Exception as e: print(f"Error launching Strap: {e}")
                else:
                    print("Strap does not appear to be installed. Run 'strap /install' first.")
        elif cmd == "/stop":
            from ops.process import stop_ahk
            stop_ahk()
            print("AHK scripts terminated.")
        elif cmd == "/clear":
            os.system("cls")
        elif cmd == "/restart":
            print("TUI is currently not running.")
        elif cmd == "/exit":
            sys.exit(0)
        else:
            print(f'\nUnknown command: "{raw_arg}"')
            _print_help()
            sys.exit(1)
    else:
        while True:
            from tui.app import StrapApp
            app    = StrapApp(start_screen="home")
            result = app.run()
            if result != "reload":
                break

def _remove_from_user_path(target_path: str) -> None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        entries = [e for e in current_path.split(";") if e.lower() != target_path.lower()]
        new_path = ";".join(entries)
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        HWND_BROADCAST   = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 2, 5000, None)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Warning: Could not remove from PATH automatically. ({e})")
        print(f"You may need to remove this manually: {target_path}")

if __name__ == "__main__":
    main()
