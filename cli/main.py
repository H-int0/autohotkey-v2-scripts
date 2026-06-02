import sys
import os
import subprocess

from tui.help_text import TERMINAL_COMMANDS_TEXT

# =============================================================================
# main.py
# Entry point for the Strap CLI.
# =============================================================================

def _print_help() -> None:
    print(TERMINAL_COMMANDS_TEXT)

def cli_install():
    from ops.installer import run as install_run
    INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")
    
    reinstall = False
    if os.path.exists(INSTALL_DIR):
        ans = input(f"Strap is already installed at {INSTALL_DIR}.\n\nDo you want to reinstall and overwrite it? (y/n): ").strip().lower()
        if ans not in {"yes", "ya", "yeah", "y", "yep", "yup"}:
            print("Installation aborted.")
            return
        reinstall = True
        
    ans2 = input("Do you want Strap to automatically start on boot? (y/n): ").strip().lower()
    enable_startup = ans2 in {"yes", "ya", "yeah", "y", "yep", "yup"}
    
    install_run(reinstall=reinstall, enable_startup_flag=enable_startup)

def cli_update():
    from ops.updater import run as update_run
    from ops.startup import is_startup_enabled
    
    enable_startup = False
    if not is_startup_enabled():
        ans = input("Strap isn't configured to start on boot.\nDo you want to enable it now? (y/n): ").strip().lower()
        enable_startup = ans in {"yes", "ya", "yeah", "y", "yep", "yup"}
        
    update_run(enable_startup_flag=enable_startup)

def main() -> None:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # If the user typed an argument in the terminal (e.g., strap /install)
    if len(sys.argv) > 1:
        # Join all arguments so spaces don't break the command chain
        raw_arg = " ".join(sys.argv[1:]).strip()
        
        # Normalize command by splitting the main command from the rest
        parts = raw_arg.split(" ", 1)
        cmd = parts[0].lower()
        if not cmd.startswith("/"):
            cmd = "/" + cmd

        # Terminal execution without TUI
        if cmd == "/install":
            cli_install()
            
        elif cmd == "/update":
            cli_update()
            
        elif cmd == "/config":
            # Open TUI on config page, pass any trailing args as the initial popup command
            rest = parts[1].strip() if len(parts) > 1 else ""
            while True:
                from tui.app import StrapApp
                from tui.screen import ConfigScreen
                app = StrapApp(start_screen=ConfigScreen(open_popup=rest if rest else None))
                result = app.run()
                if result != "reload":
                    break

        elif cmd in ("/help", "/?"):
            _print_help()

        elif cmd == "/run":
            target = os.path.join(os.environ["APPDATA"], "Strap", "core", "source.ahk")
            if os.path.exists(target):
                print(f"Executing system shortcut: {target}")
                try:
                    os.startfile(target)
                except Exception as e:
                    print(f"Error executing file: {e}")
            else:
                print("Strap does not appear to be installed properly. Cannot run.")

        elif cmd == "/stop":
            subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("AHK scripts terminated.")

        elif cmd == "/clear":
            # Clears the native console window
            os.system('cls' if os.name == 'nt' else 'clear')

        elif cmd == "/restart":
            print("TUI is not currently running.")

        elif cmd == "/exit":
            sys.exit(0)

        else:
            print(f'\nUnknown command: "{raw_arg}"')
            _print_help()
            sys.exit(1)

    else:
        # No argument passed - launch the TUI
        while True:
            from tui.app import StrapApp
            app = StrapApp(start_screen="home")
            result = app.run()
            # If the user requested /restart (which exits with "reload"), loop restart. 
            # Otherwise, fully break.
            if result != "reload":
                break

if __name__ == "__main__":
    main()
