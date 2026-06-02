from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult
from tui.tz_catalog import TIMEZONE_CATALOG, _live_time, _fmt_tz_entry
from tui.help_text import POPUP_FORCE_KILL, POPUP_COLOR_PICKER, get_popup_tz_text, POPUP_UNSAVED

# =============================================================================
# Popups
# =============================================================================

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
        if event.x < self.app.console.width * 0.3:
            if len(self.app.screen_stack) > 1:
                under = self.app.screen_stack[-2]
                try: under.query_one("#config-left-content").scroll_up(animate=False)
                except:
                    try: under.query_one("#home-left-content").scroll_up(animate=False)
                    except: pass

    def on_mouse_scroll_down(self, event) -> None:
        if event.x < self.app.console.width * 0.3:
            if len(self.app.screen_stack) > 1:
                under = self.app.screen_stack[-2]
                try: under.query_one("#config-left-content").scroll_down(animate=False)
                except:
                    try: under.query_one("#home-left-content").scroll_down(animate=False)
                    except: pass

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
        win_id = self._resolve_tz_arg(raw)
        if win_id:
            self._toggle_tz(win_id)
            return True
        return False

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
