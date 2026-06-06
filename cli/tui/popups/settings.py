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
from tui.constants import POPUP_FORCE_KILL, POPUP_COLOR_PICKER

class BooleanPopup(_BasePopup):
    def __init__(self, title: str, options: list[str], current: str, help_txt: str, **kwargs):
        super().__init__(**kwargs)
        self._title = title
        self._options = options
        self._current = current
        self._help_txt = help_txt

    def popup_title(self) -> str: return self._title

    def compose_content(self):
        for i, opt in enumerate(self._options, 1):
            marker = "[bold yellow]>[/bold yellow] " if opt == self._current else "  "
            yield Static(f"{marker}[{i}] {opt}", classes="option-row", id=f"opt-{i}")
        yield Static("")

    def help_text(self) -> str: return self._help_txt

    def process_cmd_input(self, raw: str) -> bool:
        raw_lower = raw.lower()
        if raw_lower.isdigit():
            idx = int(raw_lower) - 1
            if 0 <= idx < len(self._options):
                self.dismiss(self._options[idx])
                return True
        if raw_lower in self._options:
            self.dismiss(raw_lower)
            return True
        return False

class IntegerPopup(_BasePopup):
    def __init__(self, title: str, current: int, hint: str, help_txt: str, **kwargs):
        super().__init__(**kwargs)
        self._title = title
        self._current = current
        self._hint = hint
        self._help_txt = help_txt

    def popup_title(self) -> str: return self._title
    def input_placeholder(self) -> str: return str(self._current)

    def compose_content(self):
        yield Static(f"Current value: [bold]{self._current}[/bold]  ({self._hint})")

    def help_text(self) -> str: return self._help_txt

    def process_cmd_input(self, raw: str) -> bool:
        if raw.isdigit() and int(raw) > 0:
            self.dismiss(int(raw))
            return True
        return False

class ForceKillPopup(_BasePopup):
    def __init__(self, current: str, **kwargs):
        super().__init__(**kwargs)
        self._current = current

    def popup_title(self) -> str: return "Configure - Tooltip Text"
    def input_placeholder(self) -> str: return "/config -y -1--No. value"

    def compose_content(self):
        val = self._current if self._current else "disabled"
        yield Static(f"[1] Tooltip Text                    \\[{val}]  (leave it empty to disable Tooltip)", id="fk-opt-1")

    def help_text(self) -> str:
        return POPUP_FORCE_KILL

    def process_cmd_input(self, raw: str) -> bool:
        return False

class ColorPickerPopup(_BasePopup):
    def __init__(self, msgbox: bool, msg: str, **kwargs):
        super().__init__(**kwargs)
        self._msgbox = msgbox
        self._msg = msg

    def popup_title(self) -> str: return "Configure - Color Picker"
    def input_placeholder(self) -> str: return "/config -y -2--No. value"

    def compose_content(self):
        box_val = "enable" if self._msgbox else "disable"
        tt_val = self._msg if self._msg else "disabled"
        yield Static(f"[1] Summary Box                   \\[{box_val}]", id="cp-opt-1")
        yield Static(f"[2] Tooltip Text                  \\[{tt_val}]  (leave it empty to disable Tooltip)", id="cp-opt-2")

    def help_text(self) -> str:
        return POPUP_COLOR_PICKER

    def process_cmd_input(self, raw: str) -> bool:
        return False
