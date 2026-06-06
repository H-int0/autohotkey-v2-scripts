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
# Centralzed place to manage all AHK scripts processess
# =============================================================================

INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")

def stop_ahk() -> None:
    subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_ahk() -> None:
    target = os.path.join(INSTALL_DIR, "core", "source.ahk")
    if os.path.exists(target):
        try:
            os.startfile(target)
        except Exception:
            pass
