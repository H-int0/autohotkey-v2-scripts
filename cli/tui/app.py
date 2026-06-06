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

from textual.app import App

from tui.screens.home   import HomeScreen
from tui.screens.config import ConfigScreen

class StrapApp(App):
    CSS = """
    Screen {
        background: $surface;
    }
    """

    BINDINGS = []

    SCREENS = {
        "home":   HomeScreen,
        "config": ConfigScreen,
    }

    def __init__(self, start_screen="home", **kwargs):
        super().__init__(**kwargs)
        self.start_screen = start_screen

    def on_mount(self) -> None:
        self.push_screen(self.start_screen)

    def action_exit_app(self) -> None:
        self.exit(result="exit")
