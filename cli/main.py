# GNU GENERAL PUBLIC LICENSE
#
# Copyright (C) 2026 H-int0
# GitHub: <https://github.com/H-int0/>
# License: <https://github.com/H-int0/autohotkey-v2-scripts/blob/main/LICENSE/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ====================================================================================

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
