# =============================================================================
# main.py
# Entry point for the Strap CLI.
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _print_help() -> None:
    print(
        "\nCOMMAND         DESCRIPTION\n"
        "──────────────────────────────────────────────────────\n"
        "strap /install  Install Strap to %APPDATA%\\Strap\n"
        "strap /update   Check for and apply updates from GitHub\n"
        "strap /config   Configure Strap settings (Phase 2)\n"
        "strap /help     Show this help message\n"
        "strap /exit     Exit immediately\n"
    )


def main() -> None:
    # If the user typed an argument in the terminal (e.g., strap /install)
    if len(sys.argv) > 1:
        raw_arg = sys.argv[1].strip()
        
        # Normalize command
        cmd = raw_arg.lower()
        if not cmd.startswith("/"):
            cmd = "/" + cmd

        # We route these directly into the TUI now!
        from tui.app import StrapApp

        if cmd == "/install":
            StrapApp(start_screen="install").run()
            
        elif cmd == "/update":
            StrapApp(start_screen="update").run()
            
        elif cmd == "/config":
            StrapApp(start_screen="config").run()

        elif cmd == "/help":
            _print_help()

        elif cmd == "/exit":
            sys.exit(0)

        else:
            print(f'\nUnknown command: "{raw_arg}"')
            _print_help()
            sys.exit(1)

    else:
        # No argument passed launch the TUI home screen
        from tui.app import StrapApp
        StrapApp(start_screen="home").run()


if __name__ == "__main__":
    main()