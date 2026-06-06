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

from textual.widgets import Static
from tui.popups.base import _BasePopup
from tui.constants import POPUP_UNSAVED

class UnsavedChangesPopup(_BasePopup):
    def __init__(self, changes: dict[str, tuple], **kwargs):
        super().__init__(**kwargs)
        self._changes = changes

    def popup_title(self) -> str: return "Unsaved Changes"
    def input_placeholder(self) -> str: return "/config --save | --save --exit | --abort"

    def compose_content(self):
        yield Static("You have unsaved changes:")
        yield Static("")
        for label, (old, new) in self._changes.items():
            yield Static(f"  {label}: {old}  →  {new}")

    def help_text(self) -> str:
        return POPUP_UNSAVED

    def process_cmd_input(self, raw: str) -> bool:
        raw_lower = raw.lower()
        if raw_lower in {"/config --save"}: 
            self.dismiss("save")
            return True
        elif raw_lower in {"/config --!save", "/config --save --exit"}: 
            self.dismiss("save_exit")
            return True
        elif raw_lower in {"/config --abort"}: 
            self.dismiss("abort")
            return True
        return False
