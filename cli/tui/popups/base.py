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

from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input
from textual.app import ComposeResult

class _BasePopup(ModalScreen):
    def popup_title(self) -> str: return ""
    def help_text(self) -> str: return ""
    def input_placeholder(self) -> str: return "Type command..."

    def compose(self) -> ComposeResult:
        with Vertical(classes="popup-right-panel"):
            with Vertical(classes="config-popup", id="popup-outer"):
                yield Static(self.popup_title(), classes="popup-title")
                yield Static("─" * 40, classes="popup-divider")
                with ScrollableContainer(classes="popup-scroll"):
                    yield from self.compose_content()
                yield Static("─" * 40, classes="popup-divider")
                yield Static(self.help_text(), classes="popup-help")

                with Horizontal(classes="popup-prompt-row"):
                    yield Static(">>", classes="popup-prompt-prefix")
                    yield Input(placeholder=self.input_placeholder(), id="popup-cmd-input")

    def on_mount(self) -> None:
        try:
            self.query_one("#popup-cmd-input", Input).focus()
        except:
            pass

    def on_mouse_scroll_up(self, event) -> None:
        if getattr(event, "x", 0) < self.app.size.width * 0.45:
            if len(self.app.screen_stack) > 1:
                under = self.app.screen_stack[-2]
                for cid in ("#config-left-content", "#home-left-content"):
                    try:
                        node = under.query_one(cid)
                        node.scroll_y -= 2
                        node.scroll_up(animate=False)
                        self.refresh()  # Forces the popup to visually repaint the suspended background screen!
                        event.prevent_default()
                        event.stop()
                        return
                    except Exception:
                        pass

    def on_mouse_scroll_down(self, event) -> None:
        if getattr(event, "x", 0) < self.app.size.width * 0.45:
            if len(self.app.screen_stack) > 1:
                under = self.app.screen_stack[-2]
                for cid in ("#config-left-content", "#home-left-content"):
                    try:
                        node = under.query_one(cid)
                        node.scroll_y += 2
                        node.scroll_down(animate=False)
                        self.refresh()  # Forces the popup to visually repaint the suspended background screen!
                        event.prevent_default()
                        event.stop()
                        return
                    except Exception:
                        pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if getattr(event.input, "id", None) == "popup-cmd-input":
            raw = event.value.strip()
            event.input.value = ""
            if raw:
                cl = raw.lower()
                if cl in ("/back", "back"):
                    self.dismiss(None) # Strictly close the popup, no extra saves
                elif cl == "/exit":
                    self.app.exit(result="exit")
                elif cl == "/restart":
                    self.app.exit(result="reload")
                else:
                    handled = self.process_cmd_input(raw)
                    if not handled:
                        if cl.startswith("/") or cl.startswith("-"):
                            if len(self.app.screen_stack) > 1:
                                under = self.app.screen_stack[-2]
                                if hasattr(under, "route_command"):
                                    under.route_command(raw)

    def on_key(self, event) -> None:
        if event.key == "escape":
            event.prevent_default()
            self.dismiss(None) # Strictly close the popup, no extra saves

    def process_cmd_input(self, raw: str) -> bool:
        return False
