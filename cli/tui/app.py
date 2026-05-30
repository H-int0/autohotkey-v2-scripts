from textual.app import App
from .home    import HomeScreen
from .install import InstallScreen
from .update  import UpdateScreen
from .config  import ConfigScreen
from .help    import HelpScreen


class StrapApp(App):
    CSS = """
    Screen {
        background: $surface;
    }
    """

    SCREENS = {
        "home":    HomeScreen,
        "install": InstallScreen,
        "update":  UpdateScreen,
        "config":  ConfigScreen,
        "help":    HelpScreen,
    }

    def __init__(self, start_screen="home", **kwargs):
        super().__init__(**kwargs)
        self.start_screen = start_screen

    def on_mount(self) -> None:
        self.push_screen(self.start_screen)