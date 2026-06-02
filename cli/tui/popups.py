import re

from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult

from tui.tz_catalog import TIMEZONE_CATALOG, _UTC_OFFSETS, _live_time, _fmt_tz_entry

# =============================================================================
# Popups
# =============================================================================

class _BasePopup(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical(classes="popup-right-panel"):
            with Vertical(classes="config-popup", id="popup-outer"):
                yield Static(self.popup_title(), classes="popup-title")
                yield Static("─" * 40, classes="popup-divider")
                with ScrollableContainer(classes="popup-scroll"):
                    yield from self.compose_content()
                yield Static("─" * 40, classes="popup-divider")
                yield Static(self.help_text(), classes="popup-help")
            
            # Recreate the exact command prompt at the bottom of the popup!
            with Horizontal(classes="popup-prompt-row"):
                yield Static(">>", classes="popup-prompt-prefix")
                yield Input(placeholder=self.input_placeholder(), id="popup-cmd-input")

    def input_placeholder(self) -> str: return "Enter value or command..."
    def popup_title(self) -> str: return "Configure"
    def compose_content(self): yield Static("")
    def help_text(self) -> str: return ""

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Route the bottom command line inputs
        if event.input.id == "popup-cmd-input":
            raw = event.value.strip()
            event.input.value = ""
            if raw.lstrip("/").lower() == "back":
                self.dismiss(None)
            elif raw:
                self.process_cmd_input(raw)
        else:
            self.handle_other_input(event)

    def process_cmd_input(self, raw: str) -> None: pass
    def handle_other_input(self, event: Input.Submitted) -> None: pass

    def on_mount(self) -> None:
        # Auto-focus the bottom command line so the user can type immediately
        try: self.query_one("#popup-cmd-input", Input).focus()
        except Exception: pass

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

    def process_cmd_input(self, raw: str) -> None:
        raw = raw.lower()
        if raw.startswith("/") or raw.startswith("-"):
            self.dismiss(("cmd", raw))
            return
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(self._options):
                self.dismiss(self._options[idx])
                return
        if raw in self._options:
            self.dismiss(raw)
            return

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

    def process_cmd_input(self, raw: str) -> None:
        if raw.startswith("/") or raw.startswith("-"):
            self.dismiss(("cmd", raw))
            return
        if raw.isdigit() and int(raw) > 0:
            self.dismiss(int(raw))

class ForceKillPopup(_BasePopup):
    def __init__(self, current: str, **kwargs):
        super().__init__(**kwargs)
        self._current = current

    def popup_title(self) -> str: return "Configure - Tooltip Text"
    def input_placeholder(self) -> str: return "/config -y -1 <value>"

    def compose_content(self):
        val = self._current if self._current else "(disabled)"
        yield Static(f"[1] Tooltip Text                      [{val}]  (leave it empty to disable Tooltip)", id="fk-opt-1")

    def help_text(self) -> str:
        return (
            "[b]CONFIG · [y1] Force Kill[/b]\n"
            "───────────────────────\n"
            "/config -y -1 <text>    Set text\n"
            "/config -y -1           Disable (leave empty)\n"
            "Esc / /back             Close popup"
        )

    def process_cmd_input(self, raw: str) -> None:
        self.dismiss(("cmd", raw))

class ColorPickerPopup(_BasePopup):
    def __init__(self, msgbox: bool, msg: str, **kwargs):
        super().__init__(**kwargs)
        self._msgbox = msgbox
        self._msg = msg

    def popup_title(self) -> str: return "Configure - Color Picker"
    def input_placeholder(self) -> str: return "/config -y -2--1 enable  or  /config -y -2--2 <text>"

    def compose_content(self):
        box_val = "enable" if self._msgbox else "disable"
        tt_val = self._msg if self._msg else "(disabled)"
        yield Static(f"[1] Summary Box                     [{box_val}]", id="cp-opt-1")
        yield Static(f"[2] Tooltip Text                    [{tt_val}]  (leave it empty to disable Tooltip)", id="cp-opt-2")

    def help_text(self) -> str:
        return (
            "[b]CONFIG · [y2] Color Picker[/b]\n"
            "───────────────────────\n"
            "/config -y -2--1 enable|disable|true|false|--!\n"
            "/config -y -2--2 <text>   (empty = disable tooltip)\n"
            "Esc / /back               Close popup"
        )

    def process_cmd_input(self, raw: str) -> None:
        self.dismiss(("cmd", raw))

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

                with Vertical(id="tz-saved-section"):
                    yield Static("Saved TimeZones\n", id="tz-saved-title")
                    yield Static(self._render_saved(), id="tz-saved-list")
                    yield Static("")

                with Horizontal(id="tz-search-row"):
                    yield Static("", id="tz-filter-tags")
                    yield Input(placeholder="Search timezones...", id="tz-search-input")
                    yield Button("Filter ▾", id="tz-filter-btn")

                with Vertical(id="tz-filter-dropdown"):
                    for offset in _UTC_OFFSETS:
                        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', offset)
                        yield Static(offset, classes="filter-option", id=f"fopt-{safe_id}")

                with ScrollableContainer(id="tz-list"):
                    yield Static(self._render_list(), id="tz-list-content")

                yield Static("─" * 40, classes="popup-divider")
                yield Static(self.help_text(), classes="popup-help")
                
            # Identical bottom command prompt
            with Horizontal(classes="popup-prompt-row"):
                yield Static(">>", classes="popup-prompt-prefix")
                yield Input(placeholder="Type timezone name, No., or command...", id="popup-cmd-input")

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
            
            # Format: [24] (UTC +3) Russian Standard Time               [05:28, Dec-31-2029]
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
            if self._active_filter and utc != self._active_filter:
                continue
            selected = win_id in self._active
            lines.append(_fmt_tz_entry(i, win_id, display, cities, utc, selected))
        return "\n\n".join(lines) if lines else "(no results)"

    def help_text(self) -> str:
        flag_no = f"-{self._flag} -{self._no}"
        return (
            f"[b]CONFIG · [{'u3' if not self._single else 'u4'}] {self.popup_title().split(' - ')[1]}[/b]\n"
            f"───────────────────────\n"
            f"/config {flag_no}--<TZ_No.> <UTC_No.>    Toggle by UTC\n"
            f"Esc / /back                             Close popup"
        )

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

    def _resolve_tz_arg(self, arg: str) -> str | None:
        arg = arg.strip()
        if arg.startswith("-set--"): arg = arg[6:]
        if arg.isdigit() and 0 <= int(arg)-1 < len(TIMEZONE_CATALOG): return TIMEZONE_CATALOG[int(arg)-1][0]
        
        # Normalize to spaces (e.g., "utc_+3" -> "utc +3")
        norm = arg.replace("_", " ").lower()
        
        # Search by Windows ID, Display Name, OR UTC value!
        for win_id, display, _, utc in TIMEZONE_CATALOG:
            if win_id.lower() == norm or display.lower() == norm or utc.lower() == norm: 
                return win_id
        return None

    def handle_other_input(self, event: Input.Submitted) -> None:
        pass # tz-search-input ignores enter and won't close

    def process_cmd_input(self, raw: str) -> None:
        if raw.startswith("/") or raw.startswith("-"):
            self.dismiss(("cmd", raw))
            return
        win_id = self._resolve_tz_arg(raw)
        if win_id:
            self._toggle_tz(win_id)

class UnsavedChangesPopup(_BasePopup):
    def __init__(self, changes: dict[str, tuple], **kwargs):
        super().__init__(**kwargs)
        self._changes = changes

    def popup_title(self) -> str: return "Unsaved Changes"
    def input_placeholder(self) -> str: return "--save / --save --exit / --abort"

    def compose_content(self):
        yield Static("You have unsaved changes:")
        yield Static("")
        for label, (old, new) in self._changes.items():
            yield Static(f"  {label}: {old}  →  {new}")

    def help_text(self) -> str:
        return (
            "--save          Save changes and stay on config page\n"
            "--save --exit   Save changes and return\n"
            "--abort         Discard all changes and stay\n"
            "Esc / /back     Return to config page (changes kept pending)"
        )

    def process_cmd_input(self, raw: str) -> None:
        raw = raw.lower()
        if raw in {"--save"}: self.dismiss("save")
        elif raw in {"--!save", "--save --exit"}: self.dismiss("save_exit")
        elif raw in {"--abort"}: self.dismiss("abort")
