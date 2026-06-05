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
