from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from textual.app      import ComposeResult
from textual.screen   import Screen, ModalScreen
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets  import Static, Input, Button, Label
from textual.reactive import reactive

from config.manager  import load_user_config, save_user_config
from config.schema   import DEFAULT_CONFIG
from ops.startup     import is_startup_enabled
from ops.file_editor import update_config_ahk, update_timezones_variables_ahk

INSTALL_DIR = os.path.join(os.environ["APPDATA"], "Strap")

# ---------------------------------------------------------------------------
# Windows TZ ID  ->  IANA tz name mapping (subset used for live clock)
# Only the most common ones; falls back gracefully if not found.
# ---------------------------------------------------------------------------
_WIN_TO_IANA: dict[str, str] = {
    "Eastern Standard Time":       "America/New_York",
    "Central Standard Time":       "America/Chicago",
    "Mountain Standard Time":      "America/Denver",
    "Pacific Standard Time":       "America/Los_Angeles",
    "W. Europe Standard Time":     "Europe/Berlin",
    "GMT Standard Time":           "Europe/London",
    "Russian Standard Time":       "Europe/Moscow",
    "Tokyo Standard Time":         "Asia/Tokyo",
    "China Standard Time":         "Asia/Shanghai",
    "AUS Eastern Standard Time":   "Australia/Sydney",
    "UTC":                         "UTC",
}

# Full list of Windows TZ IDs with their display metadata.
# Each entry: (windows_id, display_name, city_hint, utc_label)
# fmt: off
TIMEZONE_CATALOG: list[tuple[str, str, str, str]] = [
    # (Windows TZ ID,               Display Name,                    Cities,                      UTC label)
    ("Dateline Standard Time",       "Dateline Standard Time",        "International Date Line West","UTC -12"),
    ("UTC-11",                       "UTC-11",                        "Coordinated Universal Time -11","UTC -11"),
    ("Aleutian Standard Time",       "Aleutian Standard Time",        "Aleutian Islands",          "UTC -10"),
    ("Hawaiian Standard Time",       "Hawaiian Standard Time",        "Hawaii",                    "UTC -10"),
    ("Marquesas Standard Time",      "Marquesas Standard Time",       "Marquesas Islands",         "UTC -9:30"),
    ("Alaskan Standard Time",        "Alaskan Standard Time",         "Alaska",                    "UTC -9"),
    ("UTC-09",                       "UTC-09",                        "Coordinated Universal Time -9","UTC -9"),
    ("Pacific Standard Time (Mexico)","Pacific Standard Time (Mexico)","Baja California",          "UTC -8"),
    ("UTC-08",                       "UTC-08",                        "Coordinated Universal Time -8","UTC -8"),
    ("Pacific Standard Time",        "Pacific Standard Time",         "Pacific Time (US & Canada)","UTC -8"),
    ("US Mountain Standard Time",    "US Mountain Standard Time",     "Arizona",                   "UTC -7"),
    ("Mountain Standard Time (Mexico)","Mountain Standard Time (Mexico)","La Paz, Mazatlan",       "UTC -7"),
    ("Mountain Standard Time",       "Mountain Standard Time",        "Mountain Time (US & Canada)","UTC -7"),
    ("Yukon Standard Time",          "Yukon Standard Time",           "Yukon",                     "UTC -7"),
    ("Central America Standard Time","Central America Standard Time", "Central America",           "UTC -6"),
    ("Central Standard Time",        "Central Standard Time",         "Central Time (US & Canada)","UTC -6"),
    ("Easter Island Standard Time",  "Easter Island Standard Time",   "Easter Island",             "UTC -6"),
    ("Central Standard Time (Mexico)","Central Standard Time (Mexico)","Guadalajara, Mexico City", "UTC -6"),
    ("Canada Central Standard Time", "Canada Central Standard Time",  "Saskatchewan",              "UTC -6"),
    ("SA Pacific Standard Time",     "SA Pacific Standard Time",      "Bogota, Lima, Quito",       "UTC -5"),
    ("Eastern Standard Time (Mexico)","Eastern Standard Time (Mexico)","Chetumal",                 "UTC -5"),
    ("Eastern Standard Time",        "Eastern Standard Time",         "Eastern Time (US & Canada)","UTC -5"),
    ("Haiti Standard Time",          "Haiti Standard Time",           "Haiti",                     "UTC -5"),
    ("Cuba Standard Time",           "Cuba Standard Time",            "Havana",                    "UTC -5"),
    ("US Eastern Standard Time",     "US Eastern Standard Time",      "Indiana (East)",            "UTC -5"),
    ("Turks And Caicos Standard Time","Turks And Caicos Standard Time","Turks and Caicos",         "UTC -5"),
    ("Paraguay Standard Time",       "Paraguay Standard Time",        "Asuncion",                  "UTC -4"),
    ("Atlantic Standard Time",       "Atlantic Standard Time",        "Atlantic Time (Canada)",    "UTC -4"),
    ("Venezuela Standard Time",      "Venezuela Standard Time",       "Caracas",                   "UTC -4"),
    ("Central Brazilian Standard Time","Central Brazilian Standard Time","Cuiaba",                 "UTC -4"),
    ("SA Western Standard Time",     "SA Western Standard Time",      "Georgetown, La Paz, Manaus","UTC -4"),
    ("Pacific SA Standard Time",     "Pacific SA Standard Time",      "Santiago",                  "UTC -4"),
    ("Tocantins Standard Time",      "Tocantins Standard Time",       "Araguaina",                 "UTC -3"),
    ("E. South America Standard Time","E. South America Standard Time","Brasilia",                 "UTC -3"),
    ("SA Eastern Standard Time",     "SA Eastern Standard Time",      "Cayenne, Fortaleza",        "UTC -3"),
    ("Argentina Standard Time",      "Argentina Standard Time",       "Buenos Aires",              "UTC -3"),
    ("Greenland Standard Time",      "Greenland Standard Time",       "Greenland",                 "UTC -3"),
    ("Montevideo Standard Time",     "Montevideo Standard Time",      "Montevideo",                "UTC -3"),
    ("Magallanes Standard Time",     "Magallanes Standard Time",      "Punta Arenas",              "UTC -3"),
    ("Saint Pierre Standard Time",   "Saint Pierre Standard Time",    "Saint Pierre and Miquelon", "UTC -3"),
    ("Bahia Standard Time",          "Bahia Standard Time",           "Salvador",                  "UTC -3"),
    ("UTC-02",                       "UTC-02",                        "Coordinated Universal Time -2","UTC -2"),
    ("Mid-Atlantic Standard Time",   "Mid-Atlantic Standard Time",    "Mid-Atlantic",              "UTC -2"),
    ("Azores Standard Time",         "Azores Standard Time",          "Azores",                    "UTC -1"),
    ("Cape Verde Standard Time",     "Cape Verde Standard Time",      "Cabo Verde Islands",        "UTC -1"),
    ("UTC",                          "UTC",                           "Coordinated Universal Time","UTC +0"),
    ("GMT Standard Time",            "GMT Standard Time",             "Dublin, Edinburgh, Lisbon, London","UTC +0"),
    ("Greenwich Standard Time",      "Greenwich Standard Time",       "Monrovia, Reykjavik",       "UTC +0"),
    ("Sao Tome Standard Time",       "Sao Tome Standard Time",        "Sao Tome",                  "UTC +0"),
    ("Morocco Standard Time",        "Morocco Standard Time",         "Casablanca",                "UTC +1"),
    ("W. Europe Standard Time",      "W. Europe Standard Time",       "Amsterdam, Berlin, Rome, Vienna","UTC +1"),
    ("Central Europe Standard Time", "Central Europe Standard Time",  "Belgrade, Bratislava, Budapest","UTC +1"),
    ("Romance Standard Time",        "Romance Standard Time",         "Brussels, Copenhagen, Madrid, Paris","UTC +1"),
    ("Central European Standard Time","Central European Standard Time","Sarajevo, Skopje, Warsaw", "UTC +1"),
    ("W. Central Africa Standard Time","W. Central Africa Standard Time","West Central Africa",    "UTC +1"),
    ("Jordan Standard Time",         "Jordan Standard Time",          "Amman",                     "UTC +2"),
    ("GTB Standard Time",            "GTB Standard Time",             "Athens, Bucharest",         "UTC +2"),
    ("Middle East Standard Time",    "Middle East Standard Time",     "Beirut",                    "UTC +2"),
    ("Egypt Standard Time",          "Egypt Standard Time",           "Cairo",                     "UTC +2"),
    ("E. Europe Standard Time",      "E. Europe Standard Time",       "Chisinau",                  "UTC +2"),
    ("Syria Standard Time",          "Syria Standard Time",           "Damascus",                  "UTC +2"),
    ("West Bank Standard Time",      "West Bank Standard Time",       "Gaza, Hebron",              "UTC +2"),
    ("South Africa Standard Time",   "South Africa Standard Time",    "Harare, Pretoria",          "UTC +2"),
    ("FLE Standard Time",            "FLE Standard Time",             "Helsinki, Kyiv, Riga, Sofia","UTC +2"),
    ("Israel Standard Time",         "Israel Standard Time",          "Jerusalem",                 "UTC +2"),
    ("Kaliningrad Standard Time",    "Kaliningrad Standard Time",     "Kaliningrad",               "UTC +2"),
    ("Sudan Standard Time",          "Sudan Standard Time",           "Khartoum",                  "UTC +2"),
    ("Libya Standard Time",          "Libya Standard Time",           "Tripoli",                   "UTC +2"),
    ("Namibia Standard Time",        "Namibia Standard Time",         "Windhoek",                  "UTC +2"),
    ("Arabic Standard Time",         "Arabic Standard Time",          "Baghdad",                   "UTC +3"),
    ("Turkey Standard Time",         "Turkey Standard Time",          "Istanbul",                  "UTC +3"),
    ("Arab Standard Time",           "Arab Standard Time",            "Kuwait, Riyadh",            "UTC +3"),
    ("Belarus Standard Time",        "Belarus Standard Time",         "Minsk",                     "UTC +3"),
    ("Russian Standard Time",        "Russian Standard Time",         "Moscow, St. Petersburg",    "UTC +3"),
    ("E. Africa Standard Time",      "E. Africa Standard Time",       "Nairobi",                   "UTC +3"),
    ("Iran Standard Time",           "Iran Standard Time",            "Tehran",                    "UTC +3:30"),
    ("Arabian Standard Time",        "Arabian Standard Time",         "Abu Dhabi, Muscat",         "UTC +4"),
    ("Astrakhan Standard Time",      "Astrakhan Standard Time",       "Astrakhan, Ulyanovsk",      "UTC +4"),
    ("Azerbaijan Standard Time",     "Azerbaijan Standard Time",      "Baku",                      "UTC +4"),
    ("Russia Time Zone 3",           "Russia Time Zone 3",            "Izhevsk, Samara",           "UTC +4"),
    ("Mauritius Standard Time",      "Mauritius Standard Time",       "Port Louis",                "UTC +4"),
    ("Saratov Standard Time",        "Saratov Standard Time",         "Saratov",                   "UTC +4"),
    ("Georgian Standard Time",       "Georgian Standard Time",        "Tbilisi",                   "UTC +4"),
    ("Volgograd Standard Time",      "Volgograd Standard Time",       "Volgograd",                 "UTC +4"),
    ("Caucasus Standard Time",       "Caucasus Standard Time",        "Yerevan",                   "UTC +4"),
    ("Afghanistan Standard Time",    "Afghanistan Standard Time",     "Kabul",                     "UTC +4:30"),
    ("West Asia Standard Time",      "West Asia Standard Time",       "Ashgabat, Tashkent",        "UTC +5"),
    ("Ekaterinburg Standard Time",   "Ekaterinburg Standard Time",    "Ekaterinburg",              "UTC +5"),
    ("Pakistan Standard Time",       "Pakistan Standard Time",        "Islamabad, Karachi",        "UTC +5"),
    ("Qyzylorda Standard Time",      "Qyzylorda Standard Time",       "Qyzylorda",                 "UTC +5"),
    ("India Standard Time",          "India Standard Time",           "Chennai, Kolkata, Mumbai",  "UTC +5:30"),
    ("Sri Lanka Standard Time",      "Sri Lanka Standard Time",       "Sri Jayawardenepura",       "UTC +5:30"),
    ("Nepal Standard Time",          "Nepal Standard Time",           "Kathmandu",                 "UTC +5:45"),
    ("Central Asia Standard Time",   "Central Asia Standard Time",    "Astana",                    "UTC +6"),
    ("Bangladesh Standard Time",     "Bangladesh Standard Time",      "Dhaka",                     "UTC +6"),
    ("Omsk Standard Time",           "Omsk Standard Time",            "Omsk",                      "UTC +6"),
    ("Myanmar Standard Time",        "Myanmar Standard Time",         "Yangon (Rangoon)",          "UTC +6:30"),
    ("SE Asia Standard Time",        "SE Asia Standard Time",         "Bangkok, Hanoi, Jakarta",   "UTC +7"),
    ("Altai Standard Time",          "Altai Standard Time",           "Barnaul, Gorno-Altaysk",    "UTC +7"),
    ("W. Mongolia Standard Time",    "W. Mongolia Standard Time",     "Hovd",                      "UTC +7"),
    ("North Asia Standard Time",     "North Asia Standard Time",      "Krasnoyarsk",               "UTC +7"),
    ("N. Central Asia Standard Time","N. Central Asia Standard Time", "Novosibirsk",               "UTC +7"),
    ("Tomsk Standard Time",          "Tomsk Standard Time",           "Tomsk",                     "UTC +7"),
    ("China Standard Time",          "China Standard Time",           "Beijing, Chongqing, Hong Kong","UTC +8"),
    ("North Asia East Standard Time","North Asia East Standard Time", "Irkutsk",                   "UTC +8"),
    ("Singapore Standard Time",      "Singapore Standard Time",       "Kuala Lumpur, Singapore",   "UTC +8"),
    ("W. Australia Standard Time",   "W. Australia Standard Time",    "Perth",                     "UTC +8"),
    ("Taipei Standard Time",         "Taipei Standard Time",          "Taipei",                    "UTC +8"),
    ("Ulaanbaatar Standard Time",    "Ulaanbaatar Standard Time",     "Ulaanbaatar",               "UTC +8"),
    ("Aus Central W. Standard Time", "Aus Central W. Standard Time",  "Eucla",                     "UTC +8:45"),
    ("Transbaikal Standard Time",    "Transbaikal Standard Time",     "Chita",                     "UTC +9"),
    ("Tokyo Standard Time",          "Tokyo Standard Time",           "Osaka, Sapporo, Tokyo",     "UTC +9"),
    ("North Korea Standard Time",    "North Korea Standard Time",     "Pyongyang",                 "UTC +9"),
    ("Korea Standard Time",          "Korea Standard Time",           "Seoul",                     "UTC +9"),
    ("Yakutsk Standard Time",        "Yakutsk Standard Time",         "Yakutsk",                   "UTC +9"),
    ("Cen. Australia Standard Time", "Cen. Australia Standard Time",  "Adelaide",                  "UTC +9:30"),
    ("AUS Central Standard Time",    "AUS Central Standard Time",     "Darwin",                    "UTC +9:30"),
    ("E. Australia Standard Time",   "E. Australia Standard Time",    "Brisbane",                  "UTC +10"),
    ("AUS Eastern Standard Time",    "AUS Eastern Standard Time",     "Canberra, Melbourne, Sydney","UTC +10"),
    ("West Pacific Standard Time",   "West Pacific Standard Time",    "Guam, Port Moresby",        "UTC +10"),
    ("Tasmania Standard Time",       "Tasmania Standard Time",        "Hobart",                    "UTC +10"),
    ("Vladivostok Standard Time",    "Vladivostok Standard Time",     "Vladivostok",               "UTC +10"),
    ("Lord Howe Standard Time",      "Lord Howe Standard Time",       "Lord Howe Island",          "UTC +10:30"),
    ("Bougainville Standard Time",   "Bougainville Standard Time",    "Bougainville Island",       "UTC +11"),
    ("Russia Time Zone 10",          "Russia Time Zone 10",           "Chokurdakh",                "UTC +11"),
    ("Magadan Standard Time",        "Magadan Standard Time",         "Magadan",                   "UTC +11"),
    ("Norfolk Standard Time",        "Norfolk Standard Time",         "Norfolk Island",            "UTC +11"),
    ("Sakhalin Standard Time",       "Sakhalin Standard Time",        "Sakhalin",                  "UTC +11"),
    ("Central Pacific Standard Time","Central Pacific Standard Time", "Solomon Islands, New Caledonia","UTC +11"),
    ("Russia Time Zone 11",          "Russia Time Zone 11",           "Anadyr, Petropavlovsk-Kamchatsky","UTC +12"),
    ("New Zealand Standard Time",    "New Zealand Standard Time",     "Auckland, Wellington",      "UTC +12"),
    ("UTC+12",                       "UTC+12",                        "Coordinated Universal Time +12","UTC +12"),
    ("Fiji Standard Time",           "Fiji Standard Time",            "Fiji",                      "UTC +12"),
    ("Kamchatka Standard Time",      "Kamchatka Standard Time",       "Petropavlovsk-Kamchatsky",  "UTC +12"),
    ("Chatham Islands Standard Time","Chatham Islands Standard Time", "Chatham Islands",           "UTC +12:45"),
    ("UTC+13",                       "UTC+13",                        "Coordinated Universal Time +13","UTC +13"),
    ("Tonga Standard Time",          "Tonga Standard Time",           "Nuku'alofa",                "UTC +13"),
    ("Samoa Standard Time",          "Samoa Standard Time",           "Samoa",                     "UTC +13"),
    ("Line Islands Standard Time",   "Line Islands Standard Time",    "Kiritimati Island",         "UTC +14"),
]
# fmt: on

_UTC_OFFSETS: list[str] = sorted(
    set(entry[3] for entry in TIMEZONE_CATALOG),
    key=lambda s: float(s.replace("UTC", "").replace("+", "").replace(":30", ".5").replace(":45", ".75") or "0")
)


def _live_time(windows_tz_id: str) -> str:
    """Return 'HH:MM, MMM-DD-YYYY' for a Windows TZ ID, or '' on failure."""
    iana = _WIN_TO_IANA.get(windows_tz_id)
    if not iana:
        return ""
    try:
        now = datetime.now(ZoneInfo(iana))
        return now.strftime("%H:%M, %b-%d-%Y")
    except (ZoneInfoNotFoundError, Exception):
        return ""


def _fmt_tz_entry(idx: int, win_id: str, display: str, cities: str, utc: str, selected: bool = False) -> str:
    time_str = _live_time(win_id)
    time_part = f"{{{time_str}}}" if time_str else ""
    mark = "[bold yellow]*[/bold yellow]" if selected else " "

    # Format: [24] Russian Standard Time {17:36, Apr-21-2029}      [UTC +3]
    raw_left = f"[{idx}] {display} {time_part}"
    left = f"{mark}{raw_left}"

    # Pad so UTC lines up at ~75
    padding = max(1, 75 - len(raw_left))
    row = f"{left}{' ' * padding}[{utc}]"

    if cities:
        row += f"\n   ({cities})"
    return row

# =============================================================================
# Popups
# =============================================================================

class _BasePopup(ModalScreen):
    DEFAULT_CSS = """
    _BasePopup {
        align: center middle;
    }
    """
    def compose(self) -> ComposeResult:
        with Vertical(classes="config-popup", id="popup-outer"):
            yield Static(self.popup_title(), classes="popup-title")
            yield Static("─" * 40, classes="popup-divider")
            with ScrollableContainer(classes="popup-scroll"):
                yield from self.compose_content()
            yield Static("─" * 40, classes="popup-divider")
            yield Static(self.help_text(), classes="popup-help")

    def popup_title(self) -> str: return "Configure"
    def compose_content(self): yield Static("")
    def help_text(self) -> str: return ""

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if raw.lstrip("/").lower() == "back":
            self.dismiss(None)

class BooleanPopup(_BasePopup):
    def __init__(self, title: str, options: list[str], current: str, help_txt: str, **kwargs):
        super().__init__(**kwargs)
        self._title = title
        self._options = options
        self._current = current
        self._help_txt = help_txt

    def popup_title(self) -> str:
        return self._title

    def compose_content(self):
        for i, opt in enumerate(self._options, 1):
            marker = "[bold yellow]>[/bold yellow] " if opt == self._current else "  "
            yield Static(f"{marker}[{i}] {opt}", classes="option-row", id=f"opt-{i}")
        yield Static("")
        yield Input(placeholder="Enter value or use command...", id="bool-input")

    def help_text(self) -> str:
        return self._help_txt

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip().lower()
        event.input.value = ""
        if raw in {"back", "/back"}:
            self.dismiss(None)
            return
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

    def popup_title(self) -> str:
        return self._title

    def compose_content(self):
        yield Static(f"Current value: [bold]{self._current}[/bold]  ({self._hint})")
        yield Static("")
        yield Static("Enter new value:")
        yield Input(placeholder=str(self._current), id="int-input")

    def help_text(self) -> str:
        return self._help_txt

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if raw.lower() in {"back", "/back"}:
            self.dismiss(None)
            return
        if raw.startswith("/") or raw.startswith("-"):
            self.dismiss(("cmd", raw))
            return
        if raw.isdigit() and int(raw) > 0:
            self.dismiss(int(raw))

class ForceKillPopup(_BasePopup):
    def __init__(self, current: str, **kwargs):
        super().__init__(**kwargs)
        self._current = current

    def popup_title(self) -> str:
        return "Configure - Tooltip Text"

    def compose_content(self):
        val = self._current if self._current else "(disabled)"
        yield Static(f"[1] Tooltip Text                      [{val}]  (leave it empty to disable Tooltip)", id="fk-opt-1")
        yield Static("")
        yield Input(placeholder="/config -y -1 <value>", id="fk-input")

    def help_text(self) -> str:
        return (
            "[b]CONFIG · [y1] Force Kill[/b]\n"
            "───────────────────────\n"
            "/config -y -1 <text>    Set text\n"
            "/config -y -1           Disable (leave empty)\n"
            "Esc / /back             Close popup"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if raw.lower() in {"back", "/back"}:
            self.dismiss(None)
        else:
            self.dismiss(("cmd", raw))

class ColorPickerPopup(_BasePopup):
    def __init__(self, msgbox: bool, msg: str, **kwargs):
        super().__init__(**kwargs)
        self._msgbox = msgbox
        self._msg = msg

    def popup_title(self) -> str:
        return "Configure - Color Picker"

    def compose_content(self):
        box_val = "enable" if self._msgbox else "disable"
        tt_val = self._msg if self._msg else "(disabled)"
        yield Static(f"[1] Summary Box                     [{box_val}]", id="cp-opt-1")
        yield Static(f"[2] Tooltip Text                    [{tt_val}]  (leave it empty to disable Tooltip)", id="cp-opt-2")
        yield Static("")
        yield Input(placeholder="/config -y -2--1 enable  or  /config -y -2--2 <text>", id="cp-input")

    def help_text(self) -> str:
        return (
            "[b]CONFIG · [y2] Color Picker[/b]\n"
            "───────────────────────\n"
            "/config -y -2--1 enable|disable|true|false|--!\n"
            "/config -y -2--2 <text>   (empty = disable tooltip)\n"
            "Esc / /back               Close popup"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        if raw.lower() in {"back", "/back"}:
            self.dismiss(None)
        else:
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

    def _render_saved(self) -> str:
        if not self._active:
            return "  none"
        lines = []
        for win_id in self._active:
            idx = next((i + 1 for i, e in enumerate(TIMEZONE_CATALOG) if e[0] == win_id), "?")
            time_str = _live_time(win_id)
            time_part = f"[{time_str}]" if time_str else ""
            utc = next((e[3] for e in TIMEZONE_CATALOG if e[0] == win_id), "")

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
            f"/config {flag_no} <No.>          Toggle by index (e.g. 24)\n"
            f"/config {flag_no} <tz_name>      Toggle by name (spaces or underscores)\n"
            f"Esc / /back                   Close popup"
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

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)

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
        if arg.isdigit():
            idx = int(arg) - 1
            if 0 <= idx < len(TIMEZONE_CATALOG):
                return TIMEZONE_CATALOG[idx][0]
            return None
        normalized = arg.replace("_", " ").lower()
        for win_id, display, _, _ in TIMEZONE_CATALOG:
            if win_id.lower() == normalized or display.lower() == normalized:
                return win_id
        return None

    def handle_set_command(self, set_arg: str) -> None:
        win_id = self._resolve_tz_arg(set_arg)
        if win_id:
            self._toggle_tz(win_id)

class UnsavedChangesPopup(_BasePopup):
    def __init__(self, changes: dict[str, tuple], **kwargs):
        super().__init__(**kwargs)
        self._changes = changes

    def popup_title(self) -> str: return "Unsaved Changes"

    def compose_content(self):
        yield Static("You have unsaved changes:")
        yield Static("")
        for label, (old, new) in self._changes.items():
            yield Static(f"  {label}: {old}  →  {new}")
        yield Static("")
        yield Input(placeholder="--save / --save --exit / --abort", id="unsaved-input")

    def help_text(self) -> str:
        return (
            "--save          Save changes and stay on config page\n"
            "--save --exit   Save changes and return\n"
            "--abort         Discard all changes and stay\n"
            "Esc / /back     Return to config page (changes kept pending)"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip().lower()
        event.input.value = ""
        if raw in {"--save"}: self.dismiss("save")
        elif raw in {"--!save", "--save --exit"}: self.dismiss("save_exit")
        elif raw in {"--abort"}: self.dismiss("abort")
        elif raw in {"back", "/back"}: self.dismiss(None)


# =============================================================================
# ConfigPanel
# =============================================================================

class ConfigPanel(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cfg = load_user_config()
        self.pending: dict[str, object] = {}

    def _effective(self, key: str, default=None):
        return self.pending.get(key, self.cfg.get(key, default))

    def render_list(self) -> str:
        cfg, p = self.cfg, self._effective

        tray = "visible" if p("trayIconVisible", True) else "hidden"
        ttdur = p("tooltipDuration", 2500)

        tzs: list[str] = p("timezones", [])
        utc_labels = [next((e[3] for e in TIMEZONE_CATALOG if e[0] == win_id), win_id) for win_id in tzs]
        tz_display = ", ".join(utc_labels) if utc_labels else "none"

        startup_tz = p("startupTZID", "")
        startup_tz_display = startup_tz if startup_tz else "default"

        feat = p("features", DEFAULT_CONFIG["features"])
        def fl(k): return "active" if feat.get(k, True) else "inactive"

        def p_line(prefix, title, value, extra=""):
            eprefix = prefix.replace("[", "\\[").replace("]", "\\]")
            raw_left = f"{eprefix} {title}"
            pad = max(1, 37 - len(f"{prefix} {title}")) # calculate padding on unescaped len
            mark = "[bold yellow]*[/bold yellow]" if self._mark_bool(prefix[1:3]) else " "
            return f"{mark}{raw_left}{' ' * pad}\\[{value}\\]{extra}"

        lines = [
            "[bold blue]Customize STRAP[/bold blue]",
            "─" * 60,
            "Configure - Globals\n",
            p_line("[u1]", "Tray Icon", tray),
            p_line("[u2]", "Tooltip Timeout", ttdur, "  (1sec = 1000ms)"),
            p_line("[u3]", "Switching Timezones", tz_display),
            p_line("[u4]", "TimeZone on Startup", startup_tz_display),
            "",
            p_line("[z1]", "NumPad Emulator", fl('numpadEmulator')),
            p_line("[z2]", "ALT Codes", fl('altCodes')),
            p_line("[z3]", "TimeZone Switcher", fl('timezoneSwitcher')),
            p_line("[z4]", "Force Kill", fl('forceKillTask')),
            p_line("[z5]", "Color Picker", fl('colorPicker')),
            p_line("[z6]", "Line Navigation", fl('lineNavigation')),
            "",
            "─" * 60,
            "Configure - Features\n",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y1') else ' '}\\[y1\\] Force Kill",
            f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('y2') else ' '}\\[y2\\] Color Picker",
        ]
        return "\n".join(lines)

    def _mark_bool(self, flag_no: str) -> bool:
        keys = {
            "u1": ["trayIconVisible"], "u2": ["tooltipDuration"], "u3": ["timezones"], "u4": ["startupTZID"],
            "z1": ["features"], "z2": ["features"], "z3": ["features"], "z4": ["features"], "z5": ["features"], "z6": ["features"],
            "y1": ["msgEndTask"], "y2": ["colorPickerMsgBox", "msgColorPicker"]
        }
        for k in keys.get(flag_no, []):
            if k in self.pending: return True
        return False

    def refresh_display(self) -> None:
        self.update(self.render_list())

    def on_mount(self) -> None:
        self.refresh_display()

    def pending_count(self) -> int: return len(self.pending)

    def pending_summary(self) -> dict[str, tuple]:
        summary = {}
        label_map = {
            "trayIconVisible": "Tray Icon", "tooltipDuration": "Tooltip Timeout",
            "timezones": "Switching Timezones", "startupTZID": "TimeZone on Startup",
            "features.numpadEmulator": "NumPad Emulator", "features.altCodes": "ALT Codes",
            "features.timezoneSwitcher":"TimeZone Switcher", "features.forceKillTask": "Force Kill",
            "features.colorPicker": "Color Picker", "features.lineNavigation": "Line Navigation",
            "msgEndTask": "Force Kill Tooltip", "colorPickerMsgBox": "Color Picker Box", "msgColorPicker": "Color Picker Tooltip",
        }
        for key, new_val in self.pending.items():
            summary[label_map.get(key, key)] = (str(self.cfg.get(key, "(not set)")), str(new_val))
        return summary

    def apply_pending(self) -> None:
        for key, val in self.pending.items():
            if "." in key:
                parent, child = key.split(".", 1)
                if parent not in self.cfg: self.cfg[parent] = {}
                self.cfg[parent][child] = val
            else: self.cfg[key] = val
        self.pending.clear()

    def discard_pending(self) -> None: self.pending.clear()

    def write_to_disk(self) -> None:
        save_user_config(self.cfg)
        c_ahk = os.path.join(INSTALL_DIR, "core", "config.ahk")
        t_vars = os.path.join(INSTALL_DIR, "core", "config-dependencies", "timezones-variables.ahk")
        if os.path.exists(c_ahk): update_config_ahk(self.cfg, c_ahk)
        if os.path.exists(t_vars): update_timezones_variables_ahk(self.cfg.get("timezones", []), t_vars)

# =============================================================================
# ConfigScreen
# =============================================================================

class ConfigScreen(Screen):
    CSS_PATH = "config.tcss"
    _active_tz_popup: TimezonePopup | None = None

    def __init__(self, open_popup: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._open_popup_cmd = open_popup

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="left-panel"):
                yield Static("", id="config-status-text")
                yield Static("", id="config-commands-text")
                yield Static("", id="config-hints-text")
                yield Static("SPDX-License-Identifier: GPL-3.0-or-later\nCopyright (C) 2026 H-int0", id="config-footer-text")
            with Vertical(id="right-panel"):
                yield ConfigPanel(id="config-panel")
                with Horizontal(id="config-prompt-row"):
                    yield Static(">>", id="config-prompt-prefix")
                    yield Input(placeholder="", id="config-prompt")

    def on_mount(self) -> None:
        self.panel = self.query_one("#config-panel", ConfigPanel)
        self.input = self.query_one("#config-prompt", Input)
        self._update_left_panel()
        self.input.focus()
        if self._open_popup_cmd:
            self.call_after_refresh(self.route_command, self._open_popup_cmd)

    def _is_ahk_running(self) -> bool:
        try:
            return "AutoHotkey" in subprocess.check_output('tasklist /FI "IMAGENAME eq AutoHotkey*"', shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except: return False

    def _update_left_panel(self, focused_flag: str = "", focused_no: int = 0) -> None:
        cfg = load_user_config()
        st_tz = cfg.get("startupTZID", "")
        pending = self.panel.pending_count() if hasattr(self, "panel") else 0

        status = (
            f"[b]STATUS[/b]\n───────────────────────\n"
            f"Installed:   {'Yes' if os.path.exists(INSTALL_DIR) else 'No'}\n"
            f"Version:     v{cfg.get('version', DEFAULT_CONFIG['version'])}\n"
            f"Startup:     {'Enabled' if is_startup_enabled() else 'Disabled'}\n"
            f"Auto start:  {'Yes' if is_startup_enabled() else 'No'}\n"
            f"AHK running: {'Yes' if self._is_ahk_running() else 'No'}\n"
            f"Startup TZ:  {st_tz if st_tz else 'default'}\n\n"
            f"{f'Pending:     {pending} change(s)' if pending else ''}\n"
        )

        commands = (
            "[b]COMMANDS[/b]\n───────────────────────\n"
            "/install   Install Strap\n/update    Update Strap\n/config    Configure\n"
            "/help      Show commands\n/run       Launch Startup\n/stop      Stop AHK script\n"
            "/clear     Clear terminal\n/restart   Restart TUI\n/exit      Quit application\n"
        )

        hints = self._build_hints(focused_flag, focused_no)
        self.query_one("#config-status-text", Static).update(status)
        self.query_one("#config-commands-text", Static).update(commands)
        self.query_one("#config-hints-text", Static).update(hints)

    def _build_hints(self, flag: str, no: int) -> str:
        if not flag or not no:
            return (
                "[b]CONFIG COMMANDS[/b]\n───────────────────────\n"
                "--save          Save changes\n--save --exit   Save & go back\n--abort         Discard changes\n"
                "/config -u -1   Open global setting\n/config -z -1   Toggle feature\n/config -y -1   Open feature cfg"
            )
        if flag == "z":
            names = {1:"NumPad Emulator", 2:"ALT Codes", 3:"TimeZone Switcher", 4:"Force Kill", 5:"Color Picker", 6:"Line Navigation"}
            return (
                f"[b]CONFIG · [z{no}] {names.get(no, '')}[/b]\n───────────────────────\n"
                f"--!             Flip toggle\n/config -z -{no} 1/0\n"
                f"/config -z -{no} true/false\n/config -z -{no} enable/disable\n/config -z -{no} active/inactive"
            )
        if flag == "u":
            if no == 1: return "[b]CONFIG · [u1] Tray Icon[/b]\n───────────────────────\n/config -u -1 visible/hidden\n/config -u -1 true/false\n/config -u -1 --!"
            if no == 2: return "[b]CONFIG · [u2] Tooltip Timeout[/b]\n───────────────────────\n/config -u -2 <ms>\n  e.g. /config -u -2 3000\n  (positive integer)"
            if no == 3: return "[b]CONFIG · [u3] Switching Timezones[/b]\n───────────────────────\n/config -u -3 <No.>\n/config -u -3 <tz_name>\n  (toggle: add if absent, remove if present)"
            if no == 4: return "[b]CONFIG · [u4] TimeZone on Startup[/b]\n───────────────────────\n/config -u -4 <No.>\n/config -u -4 <tz_name>\n  (same TZ again = reset to default)"
        if flag == "y":
            if no == 1: return "[b]CONFIG · [y1] Force Kill[/b]\n───────────────────────\n/config -y -1 <text>\n  (empty = disable tooltip)"
            if no == 2: return "[b]CONFIG · [y2] Color Picker[/b]\n───────────────────────\n/config -y -2--1 enable/disable\n/config -y -2--2 <text>"
        return ""

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "config-prompt":
            val = event.value.strip().lower()
            for prefix in ("strap ", "/strap ", "/config "):
                if val.startswith(prefix):
                    val = val[len(prefix):].strip()
                    break
            m = re.match(r"^-([uzy])\s+-(\d+)", val)
            if m: self._update_left_panel(m.group(1), int(m.group(2)))
            else: self._update_left_panel("", 0)

    def on_key(self, event) -> None:
        if event.key == "escape": self._try_leave()
        elif event.key == "tab":
            if self.input.has_focus:
                event.prevent_default()
                self._autocomplete()

    def _autocomplete(self) -> None:
        val = self.input.value
        if not val: return
        keywords = ["/install", "/update", "/config", "/help", "/run", "/stop", "/clear", "/restart", "/exit", "--save", "--save --exit", "--abort", "true", "false", "active", "inactive", "enable", "disable", "visible", "hidden"]

        if val.endswith("--save --e") or val.endswith("--save --ex") or val.endswith("--save --exi"):
            self.input.value = val.rsplit("--save", 1)[0] + "--save --exit"
            self.input.cursor_position = len(self.input.value)
            return

        parts = val.split()
        if not parts: return
        last_word = parts[-1].lower()
        matches = [w for w in keywords if w.startswith(last_word)]
        if matches:
            parts[-1] = matches[0]
            self.input.value = " ".join(parts) + " "
            self.input.cursor_position = len(self.input.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "config-prompt": return
        raw = event.value.strip()
        event.input.value = ""
        if not raw: return
        for p in ("strap ", "/strap "):
            if raw.lower().startswith(p):
                raw = raw[len(p):].strip()
                break
        self.route_command(raw)

    def route_command(self, raw: str) -> None:
        cmd = raw.strip()
        cl = cmd.lower()

        if cl == "/exit": self.app.exit(result="exit"); return
        if cl == "/restart": self.app.exit(result="reload"); return
        if cl in ("/run", "run"): self._run_strap(); return
        if cl in ("/stop", "stop"): self._stop_strap(); return
        if cl in ("/back", "back"): self._try_leave(); return

        if cl in ("--save", "/config --save"): self._do_save(exit_after=False); return
        if cl in ("--save --exit", "--!save", "/config --save --exit", "/config --!save"): self._do_save(exit_after=True); return
        if cl in ("--abort", "/config --abort"): self.panel.discard_pending(); self.panel.refresh_display(); self._update_left_panel(); return

        if cl.startswith("/config"):
            self._handle_config_args(cmd[7:].strip())
            return
        if cl.startswith("-"):
            self._handle_config_args(cmd)
            return

    def _handle_config_args(self, args: str) -> None:
        args = args.strip()
        if not args: return
        m = re.match(r"^-([uzy])\s+-(\d+)(?:--(.+?))?(?:\s+(.+))?$", args, re.IGNORECASE)
        if not m:
            m = re.match(r"^-([uzy])\s+-(\d+)\s+(.+)$", args, re.IGNORECASE)
            if not m: return
            flag, no, sub, value = m.group(1).lower(), int(m.group(2)), "", m.group(3).strip()
        else:
            flag, no, sub, value = m.group(1).lower(), int(m.group(2)), m.group(3), (m.group(4) or "").strip()

        self._update_left_panel(flag, no)
        if not value and not sub: self._open_popup(flag, no); return

        if flag == "u" and no in (3, 4) and not value and sub:
            value = sub
            sub = None

        self._apply_value(flag, no, sub, value)

    def _apply_value(self, flag: str, no: int, sub: str | None, value: str) -> None:
        v, vl = value.strip(), value.strip().lower()
        def parse_bool(s: str) -> bool | None:
            if s in {"1", "t", "true", "enable", "enabled", "active", "yes", "show", "visible"}: return True
            if s in {"0", "f", "false", "disable", "disabled", "inactive", "no", "hide", "hidden"}: return False
            return None

        if flag == "u":
            if no == 1:
                if vl == "--!": self.panel.pending["trayIconVisible"] = not self.panel._effective("trayIconVisible", True)
                elif parse_bool(vl) is not None: self.panel.pending["trayIconVisible"] = parse_bool(vl)
            elif no == 2 and v.isdigit() and int(v) > 0: self.panel.pending["tooltipDuration"] = int(v)
            elif no == 3: self._toggle_tz("timezones", v)
            elif no == 4: self._toggle_startup_tz(v)
        elif flag == "z":
            fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation"}
            fk = fk_map.get(no)
            if fk:
                c_feats = dict(self.panel._effective("features", DEFAULT_CONFIG["features"]))
                if vl == "--!": c_feats[fk] = not c_feats.get(fk, True)
                elif parse_bool(vl) is not None: c_feats[fk] = parse_bool(vl)
                self.panel.pending["features"] = c_feats
        elif flag == "y":
            if no == 1 and (not sub or sub == "1"):
                if vl == '""' or vl == "''": v = ""
                self.panel.pending["msgEndTask"] = v
            elif no == 2:
                if sub == "1":
                    if vl == "--!": self.panel.pending["colorPickerMsgBox"] = not self.panel._effective("colorPickerMsgBox", False)
                    elif parse_bool(vl) is not None: self.panel.pending["colorPickerMsgBox"] = parse_bool(vl)
                elif sub == "2":
                    if vl == '""' or vl == "''": v = ""
                    self.panel.pending["msgColorPicker"] = v

        self.panel.refresh_display()
        self._update_left_panel(flag, no)

    def _toggle_tz(self, cfg_key: str, tz_arg: str) -> None:
        win_id = self._resolve_tz_arg(tz_arg)
        if not win_id: return
        current: list[str] = list(self.panel._effective(cfg_key, []))
        if win_id in current: current.remove(win_id)
        else: current.append(win_id)
        self.panel.pending[cfg_key] = current

    def _toggle_startup_tz(self, tz_arg: str) -> None:
        win_id = self._resolve_tz_arg(tz_arg)
        if not win_id: return
        self.panel.pending["startupTZID"] = "" if self.panel._effective("startupTZID", "") == win_id else win_id

    def _resolve_tz_arg(self, arg: str) -> str | None:
        arg = arg.strip()
        if arg.startswith("-set--"): arg = arg[6:]
        if arg.isdigit() and 0 <= int(arg)-1 < len(TIMEZONE_CATALOG): return TIMEZONE_CATALOG[int(arg)-1][0]
        norm = arg.replace("_", " ").lower()
        for win_id, display, _, _ in TIMEZONE_CATALOG:
            if win_id.lower() == norm or display.lower() == norm: return win_id
        return None

    def _open_popup(self, flag: str, no: int) -> None:
        cfg = self.panel._effective
        if flag == "u":
            if no == 1: self.app.push_screen(BooleanPopup("Configure - Tray Icon", ["visible", "hidden"], "visible" if cfg("trayIconVisible", True) else "hidden", "[b]CONFIG · [u1] Tray Icon[/b]\n───────────────────────\n/config -u -1 visible|hidden\n/config -u -1 --!\nEsc / /back  Close"), lambda r: self._apply_result("trayIconVisible", r=="visible", r))
            elif no == 2: self.app.push_screen(IntegerPopup("Configure - Tooltip Timeout", cfg("tooltipDuration", 2500), "1sec = 1000ms", "[b]CONFIG · [u2] Tooltip Timeout[/b]\n───────────────────────\n/config -u -2 <ms>\nEsc / /back  Close"), lambda r: self._apply_result("tooltipDuration", r, r))
            elif no == 3: self._active_tz_popup = TimezonePopup("u", 3, cfg("timezones", []), False); self.app.push_screen(self._active_tz_popup, lambda r: self._apply_result("timezones", r, r))
            elif no == 4: st = cfg("startupTZID", ""); self._active_tz_popup = TimezonePopup("u", 4, [st] if st else [], True); self.app.push_screen(self._active_tz_popup, lambda r: self._apply_result("startupTZID", r[0] if r else "", r))
        elif flag == "z":
            f_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation"}
            names = {1:"NumPad Emulator", 2:"ALT Codes", 3:"TimeZone Switcher", 4:"Force Kill", 5:"Color Picker", 6:"Line Navigation"}
            if fk := f_map.get(no):
                self.app.push_screen(BooleanPopup(f"Configure - {names[no]}", ["active", "inactive"], "active" if cfg("features", DEFAULT_CONFIG["features"]).get(fk, True) else "inactive", f"[b]CONFIG · [z{no}] {names[no]}[/b]\n───────────────────────\n/config -z -{no} active|inactive|--!\nEsc / /back  Close"), lambda r, _fk=fk: self._apply_feat_result(_fk, r))
        elif flag == "y":
            if no == 1: self.app.push_screen(ForceKillPopup(cfg("msgEndTask", "EVAPORATED!")), lambda r: self._apply_route_result("msgEndTask", r))
            elif no == 2: self.app.push_screen(ColorPickerPopup(cfg("colorPickerMsgBox", False), cfg("msgColorPicker", "Copied to Clipboard")), lambda r: self._apply_route_result(None, r))

    def _apply_result(self, key, val, check_none):
        if check_none is None: return
        if isinstance(check_none, tuple) and check_none[0] == "cmd":
            self.route_command(check_none[1])
            return
        self.panel.pending[key] = val
        self.panel.refresh_display()
        self._update_left_panel()

    def _apply_feat_result(self, feat_key, result):
        if result is None: return
        if isinstance(result, tuple) and result[0] == "cmd":
            self.route_command(result[1])
            return
        c = dict(self.panel._effective("features", DEFAULT_CONFIG["features"]))
        c[feat_key] = (result == "active")
        self.panel.pending["features"] = c
        self.panel.refresh_display()
        self._update_left_panel()

    def _apply_route_result(self, direct_key, result):
        if result is None: return
        if isinstance(result, tuple) and result[0] == "cmd": self.route_command(result[1])
        else: self.panel.pending[direct_key] = result
        self.panel.refresh_display(); self._update_left_panel()

    def _do_save(self, exit_after: bool) -> None:
        self.panel.apply_pending()
        self.panel.write_to_disk()
        self.panel.refresh_display()
        self._update_left_panel()
        if exit_after: self.app.pop_screen()

    def _try_leave(self) -> None:
        if self.panel.pending_count() == 0: self.app.pop_screen(); return
        self.app.push_screen(UnsavedChangesPopup(self.panel.pending_summary()), lambda r: self._do_save(exit_after=False) if r=="save" else self._do_save(exit_after=True) if r=="save_exit" else self.panel.discard_pending() or self.panel.refresh_display() or self._update_left_panel() if r=="abort" else None)

    def _run_strap(self) -> None:
        if os.path.exists(t:=os.path.join(INSTALL_DIR, "core", "source.ahk")):
            try: os.startfile(t)
            except: pass

    def _stop_strap(self) -> None:
        subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
