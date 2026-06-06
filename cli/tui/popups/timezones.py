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

from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult
from tui.popups.base import _BasePopup
from data.timezones_catalog import TIMEZONE_CATALOG, _live_time, _fmt_tz_entry
from tui.constants import get_popup_tz_text

class TimezonePopup(_BasePopup):
    BINDINGS = []

    def __init__(self, setting_flag: str, setting_no: int, active_tzs: list[str], single_select: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._flag = setting_flag
        self._no = setting_no
        self._active = list(active_tzs)
        self._single = single_select
        self._search_query = ""
        self._active_filter = ""
        self._show_dropdown = False

    def popup_title(self) -> str:
        label = "TimeZone on Startup" if self._single else "Switching Timezones"
        return f"Configure - {label}"

    def compose(self) -> ComposeResult:
        with Vertical(classes="popup-right-panel"):
            with Vertical(classes="config-popup", id="popup-outer"):
                yield Static(self.popup_title(), classes="popup-title")
                yield Static("─" * 40, classes="popup-divider")

                with Horizontal(id="tz-search-row"):
                    yield Input(placeholder="Search timezones...", id="tz-search-input")

                with ScrollableContainer(id="tz-list"):
                    with Vertical(id="tz-saved-section"):
                        yield Static("Saved TimeZones\n", id="tz-saved-title")
                        yield Static(self._render_saved(), id="tz-saved-list")
                        yield Static("")
                    yield Static(self._render_list(), id="tz-list-content")

                yield Static("─" * 40, classes="popup-divider")
                yield Static(self.help_text(), classes="popup-help")
                
                with Horizontal(classes="popup-prompt-row"):
                    yield Static(">>", classes="popup-prompt-prefix")
                    yield Input(placeholder="Type command...", id="popup-cmd-input")

    def _render_saved(self) -> str:
        if not self._active:
            return "  none"
        lines = []
        for win_id in self._active:
            idx, utc = "?", ""
            for i, e in enumerate(TIMEZONE_CATALOG):
                if e[0].replace(".", "").lower() == win_id.replace(".", "").lower():
                    idx, utc = str(i + 1), e[3]
                    break
            
            time_str = _live_time(win_id)
            time_part = f"[{time_str}]" if time_str else ""
            
            raw_left = f"[{idx}] ({utc}) {win_id}"
            padding = max(1, 75 - len(raw_left))
            lines.append(f"{raw_left}{' ' * padding}{time_part}")
        return "\n".join(lines)

    def _render_list(self) -> str:
        lines = []
        for i, (win_id, display, cities, utc) in enumerate(TIMEZONE_CATALOG, 1):
            if self._search_query:
                q = self._search_query.lower()
                if not any(q in s.lower() for s in [win_id, display, cities, utc]):
                    continue
            selected = win_id in self._active
            lines.append(_fmt_tz_entry(i, win_id, display, cities, utc, selected))
        return "\n\n".join(lines) if lines else "no results"

    def help_text(self) -> str:
        return get_popup_tz_text(self._flag, self._no, self._single, self.popup_title())

    def _refresh_list(self) -> None:
        self.query_one("#tz-list-content", Static).update(self._render_list())
        self.query_one("#tz-saved-list",   Static).update(self._render_saved())

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "tz-search-input":
            self._search_query = event.value
            self._refresh_list()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "tz-filter-btn":
            self._show_dropdown = not self._show_dropdown
            dd = self.query_one("#tz-filter-dropdown")
            dd.styles.display = "block" if self._show_dropdown else "none"

    def on_static_clicked(self, event) -> None:
        if "filter-option" in (event.static.classes or set()):
            self._active_filter = event.static.renderable
            self._show_dropdown = False
            self.query_one("#tz-filter-dropdown").styles.display = "none"
            self.query_one("#tz-filter-tags", Static).update(f"[{self._active_filter} ×]" if self._active_filter else "")
            self._refresh_list()

    def _toggle_tz(self, win_id: str) -> None:
        if self._single:
            self._active = [] if win_id in self._active else [win_id]
        else:
            if win_id in self._active:
                self._active.remove(win_id)
            else:
                self._active.append(win_id)
        self._refresh_list()

        # Update pending state immediately so /config --save can be explicitly used while open
        if len(self.app.screen_stack) > 1:
            under = self.app.screen_stack[-2]
            if hasattr(under, "panel"):
                key = "startupTZID" if self._single else "timezones"
                val = self._active[0] if self._single and self._active else (list(self._active) if not self._single else "")
                under.panel.pending[key] = val
                under.panel.refresh_display()
                if hasattr(under, "_update_left_panel"):
                    under._update_left_panel()

    def _resolve_tz_arg(self, arg: str) -> str | None:
        arg = arg.strip()
        if arg.startswith("-set--"): arg = arg[6:]
        if arg.isdigit() and 0 <= int(arg)-1 < len(TIMEZONE_CATALOG): return TIMEZONE_CATALOG[int(arg)-1][0]
        
        norm = arg.replace("_", " ").lower()
        for win_id, display, _, utc in TIMEZONE_CATALOG:
            if win_id.lower() == norm or display.lower() == norm or utc.lower() == norm: 
                return win_id
        return None

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "tz-search-input":
            event.prevent_default()
            return
        super().on_input_submitted(event)

    def process_cmd_input(self, raw: str) -> bool:
        import re
        cmd = raw.strip()
        
        # Strip /config if present so we can match the core flag
        if cmd.lower().startswith("/config"):
            cmd = cmd[7:].strip()
            
        m = re.match(rf"^-!?u\s+-{self._no}(?:--(.+?))?(?:\s+(.+))?$", cmd, re.IGNORECASE)
        tz_arg = None
        if m:
            sub = m.group(1)
            value = (m.group(2) or "").strip()
            if not value and sub:
                tz_arg = sub
            elif value:
                tz_arg = value
                
        if tz_arg:
            win_id = self._resolve_tz_arg(tz_arg)
            if win_id:
                self._toggle_tz(win_id)
                if cmd.lower().startswith("-!") and len(self.app.screen_stack) > 1:
                    under = self.app.screen_stack[-2]
                    if hasattr(under, "_do_save"):
                        under._do_save(exit_after=False)
                return True
                
        win_id = self._resolve_tz_arg(raw)
        if win_id:
            self._toggle_tz(win_id)
            return True
            
        return False
