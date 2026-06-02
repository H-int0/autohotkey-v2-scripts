# =============================================================================
# all help texts are in here
# =============================================================================

COMMANDS_TEXT = (
    "[b]COMMANDS[/b]\n"
    "─────────────────────────\n"
    "^ to chain    Ex: /run ^ /config\n\n"
    "/install      Install Strap\n"
    "/update       Update Strap\n"
    "/config       Configure\n"
    "/help, /?     Show commands\n"
    "/run          Launch Startup\n"
    "/stop         Stop AHK script\n"
    "/clear        Clear terminal\n"
    "/restart      Restart TUI\n"
    "/exit         Quit application\n\n"
)

TERMINAL_COMMANDS_TEXT = (
    "\nCOMMAND         DESCRIPTION\n"
    "──────────────────────────────────\n"
    "strap /install  Install Strap to %APPDATA%\\Strap\n"
    "strap /update   Check for and apply updates from GitHub\n"
    "strap /config   Configure Strap settings\n"
    "strap /help     Show this help message\n"
    "strap /run      Launch Startup\n"
    "strap /stop     Stop running AHK scripts\n"
    "strap /clear    Clear terminal\n"
    "strap /restart  Restart TUI\n"
    "strap /exit     Exit immediately\n"
)

CONFIG_COMMANDS_TEXT = (
    "[b]CONFIG COMMANDS[/b]\n"
    "─────────────────────────\n"
    "/config --save             Save changes\n"
    "/config --save --exit      Save & go back\n"
    "/config --abort            Discard changes\n"
    "/config -flag -No.         Open popup\n"
    "/config -flag -No. value   Modify setting\n\n"
)

def get_status_text(version: str, is_installed: bool, startup_enabled: bool, ahk_running: bool, st_tz: str, pending_count: int = None) -> str:
    base = (
        f"[b]STATUS[/b]\n"
        f"─────────────────────────\n"
        f"Version:      v{version}\n"
        f"Installed:    {'Yes' if is_installed else 'No'}\n"
        f"Startup:      {'Enabled' if startup_enabled else 'Disabled'}\n"
        f"Auto start:   {'Yes' if startup_enabled else 'No'}\n"
        f"AHK running:  {'Yes' if ahk_running else 'No'}\n"
        f"Startup TZ:   {st_tz if st_tz else 'default'}\n\n"
    )
    if pending_count is not None:
        base += f"Pending:      {pending_count}\n\n"
    return base

def get_config_z_text(no: int) -> str:
    from config.schema import FEATURE_REGISTRY
    name = FEATURE_REGISTRY[no - 1]["label"] if 0 < no <= len(FEATURE_REGISTRY) else ""
    return (
        f"[b]CONFIG - [z{no}] {name}[/b]\n"
        f"─────────────────────────\n"
        f"/config -z -{no}              Open popup\n"
        f"/config -z -{no} --!          Flip value\n"
        f"/config -z -{no} value        active | inactive\n\n"
    )

CONFIG_U1_TEXT = (
    "[b]CONFIG - [u1] Tray Icon[/b]\n"
    "─────────────────────────\n"
    "/config -u -1              Open popup\n"
    "/config -u -1 --!          Flip value\n"
    "/config -u -1 value        visible | hidden\n\n"
)

CONFIG_U2_TEXT = (
    "[b]CONFIG - [u2] Tooltip Timeout[/b]\n"
    "─────────────────────────\n"
    "/config -u -2              Open popup\n"
    "/config -u -2 time(in ms)  Set value\n\n"
)

CONFIG_U3_TEXT = (
    "[b]CONFIG - [u3] Switching Timezones[/b]\n"
    "─────────────────────────\n"
    "/config -u -3              Open popup\n"
    "/config -u -3--<TZ No.>    Toggle timezone\n"
    "  (adds if absent, removes if present)\n\n"
)

CONFIG_U4_TEXT = (
    "[b]CONFIG - [u4] TimeZone on Startup[/b]\n"
    "─────────────────────────\n"
    "/config -u -4              Open popup\n"
    "/config -u -4--<TZ No.>    Set startup TZ\n"
    "  (same TZ again = reset to default)\n\n"
)

POPUP_FORCE_KILL = (
    "[b]CONFIG - [y1] Force Kill[/b]\n"
    "─────────────────────────\n"
    "/config -y -1--1 text      Set text\n\n"
    "/back or Esc               Close\n\n"
)

POPUP_COLOR_PICKER = (
    "[b]CONFIG - [y2] Color Picker[/b]\n"
    "─────────────────────────\n"
    "/config -y -2--1 --!       Flip value\n"
    "/config -y -2--1 value     enable|disable\n\n"
    "/config -y -2--2 text      Set Text\n\n"
    "/back or Esc               Close\n\n"
)

def get_popup_tz_text(flag: str, no: int, is_single: bool, title: str) -> str:
    flag_no = f"-{flag} -{no}"
    tag = 'u4' if is_single else 'u3'
    clean_title = title.split(" - ")[-1] if " - " in title else title
    return (
        f"[b]CONFIG - [{tag}] {clean_title}[/b]\n"
        f"─────────────────────────\n"
        f"/config {flag_no}--TZ_No. UTC_No.  Toggle by UTC\n\n"
        f"/back or Esc                       Close\n\n"
    )

POPUP_UNSAVED = (
    "/config --save             Save changes\n"
    "/config --save --exit      Save & go back\n"
    "/config --abort            Discard changes\n\n"
    "/back or Esc               Close\n\n"
)
