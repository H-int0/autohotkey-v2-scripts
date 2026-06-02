from textual.app import App

from tui.home   import HomeScreen
from tui.screen import ConfigScreen

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
