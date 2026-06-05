import sys
import os

# =============================================================================
# main.py
# Entry point for the Strap CLI.
# =============================================================================

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

        from commands import execute_terminal_command
        execute_terminal_command(cmd, rest, raw_arg)
        
    else:
        # Launch TUI if no arguments are provided
        while True:
            from tui.app import StrapApp
            app = StrapApp(start_screen="home")
            result = app.run()
            if result != "reload":
                break

if __name__ == "__main__":
    main()
