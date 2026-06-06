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

import os
import subprocess

# =============================================================================
# startup.py
# Creates or removes the Strap Windows startup shortcut (.lnk).
# Uses PowerShell's WScript.Shell COM object same approach as the manual
# install method documented in README / RECOVERY.md.
# =============================================================================

STARTUP_DIR   = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "Strap.lnk")
TARGET_PATH   = os.path.join(os.environ["APPDATA"], "Strap", "core", "source.ahk")
WORKING_DIR   = os.path.join(os.environ["APPDATA"], "Strap", "core")


def is_startup_enabled() -> bool:
    """Return True if the Strap startup shortcut exists."""
    return os.path.exists(SHORTCUT_PATH)


def enable_startup() -> None:
    """Create (or refresh) the Strap startup shortcut via PowerShell WScript.Shell."""
    ps_script = (
        f'$ws = New-Object -ComObject WScript.Shell; '
        f'$s = $ws.CreateShortcut("{SHORTCUT_PATH}"); '
        f'$s.TargetPath = "{TARGET_PATH}"; '
        f'$s.WorkingDirectory = "{WORKING_DIR}"; '
        f'$s.Save()'
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def disable_startup() -> None:
    """Remove the Strap startup shortcut if it exists."""
    if os.path.exists(SHORTCUT_PATH):
        os.remove(SHORTCUT_PATH)

def run_from_startup_shortcut() -> bool:
    """Kill AHK if running, then launch from shell:startup shortcut if it exists. Returns True if launched."""
    import subprocess
    subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(SHORTCUT_PATH):
        try:
            os.startfile(SHORTCUT_PATH)
            return True
        except Exception:
            return False
    return False
