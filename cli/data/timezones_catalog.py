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

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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
    ("Dateline Standard Time", "Dateline Standard Time", "International Date Line West", "UTC -12"),
    ("UTC-11", "UTC-11", "Coordinated Universal Time -11", "UTC -11"),
    ("Hawaiian Standard Time", "Hawaiian Standard Time", "Hawaii", "UTC -10"),
    ("Marquesas Standard Time", "Marquesas Standard Time", "Marquesas Islands", "UTC -9:30"),
    ("Alaskan Standard Time", "Alaskan Standard Time", "Alaska", "UTC -9"),
    ("Pacific Standard Time", "Pacific Standard Time", "Pacific Time (US & Canada)", "UTC -8"),
    ("US Mountain Standard Time", "US Mountain Standard Time", "Arizona", "UTC -7"),
    ("Central Standard Time", "Central Standard Time", "Central Time (US & Canada)", "UTC -6"),
    ("Eastern Standard Time", "Eastern Standard Time", "Eastern Time (US & Canada)", "UTC -5"),
    ("Atlantic Standard Time", "Atlantic Standard Time", "Atlantic Time (Canada)", "UTC -4"),
    ("Venezuela Standard Time", "Venezuela Standard Time", "Caracas", "UTC -4"),
    ("E. South America Standard Time", "E. South America Standard Time", "Brasilia", "UTC -3"),
    ("Argentina Standard Time", "Argentina Standard Time", "Buenos Aires", "UTC -3"),
    ("UTC-02", "UTC-02", "Coordinated Universal Time -2", "UTC -2"),
    ("Azores Standard Time", "Azores Standard Time", "Azores", "UTC -1"),
    ("GMT Standard Time", "GMT Standard Time", "Dublin, Edinburgh, Lisbon, London", "UTC +0"),
    ("W. Europe Standard Time", "W. Europe Standard Time", "Amsterdam, Berlin, Rome, Vienna", "UTC +1"),
    ("Israel Standard Time", "Israel Standard Time", "Jerusalem", "UTC +2"),
    ("Russian Standard Time", "Russian Standard Time", "Moscow, St. Petersburg", "UTC +3"),
    ("Iran Standard Time", "Iran Standard Time", "Tehran", "UTC +3:30"),
    ("Arabian Standard Time", "Arabian Standard Time", "Abu Dhabi, Muscat", "UTC +4"),
    ("Afghanistan Standard Time", "Afghanistan Standard Time", "Kabul", "UTC +4:30"),
    ("Pakistan Standard Time", "Pakistan Standard Time", "Islamabad, Karachi", "UTC +5"),
    ("India Standard Time", "India Standard Time", "Chennai, Kolkata, Mumbai", "UTC +5:30"),
    ("Nepal Standard Time", "Nepal Standard Time", "Kathmandu", "UTC +5:45"),
    ("Central Asia Standard Time", "Central Asia Standard Time", "Astana", "UTC +6"),
    ("Myanmar Standard Time", "Myanmar Standard Time", "Yangon (Rangoon)", "UTC +6:30"),
    ("SE Asia Standard Time", "SE Asia Standard Time", "Bangkok, Hanoi, Jakarta", "UTC +7"),
    ("China Standard Time", "China Standard Time", "Beijing, Chongqing, Hong Kong", "UTC +8"),
    ("Tokyo Standard Time", "Tokyo Standard Time", "Osaka, Sapporo, Tokyo", "UTC +9"),
    ("Cen. Australia Standard Time", "Cen. Australia Standard Time", "Adelaide", "UTC +9:30"),
    ("AUS Eastern Standard Time", "AUS Eastern Standard Time", "Canberra, Melbourne, Sydney", "UTC +10"),
    ("Central Pacific Standard Time", "Central Pacific Standard Time", "Solomon Islands, New Caledonia", "UTC +11"),
    ("New Zealand Standard Time", "New Zealand Standard Time", "Auckland, Wellington", "UTC +12"),
    ("Tonga Standard Time", "Tonga Standard Time", "Nuku'alofa", "UTC +13"),
    ("Line Islands Standard Time", "Line Islands Standard Time", "Kiritimati Island", "UTC +14")
]
# fmt: on

_UTC_OFFSETS: list[str] = sorted(
    set(entry[3] for entry in TIMEZONE_CATALOG),
    key=lambda s: float(s.replace("UTC", "").replace("+", "").replace(":30", ".5").replace(":45", ".75") or "0")
)


def _live_time(windows_tz_id: str) -> str:
    """Return 'HH:MM, MMM-DD-YYYY' for a Windows TZ ID, or '' on failure."""
    iana = None
    
    for k, v in _WIN_TO_IANA.items():
        if k.replace(".", "").lower() == windows_tz_id.replace(".", "").lower():
            iana = v
            break
            
    if not iana: return ""
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
