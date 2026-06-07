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

from features import FEATURE_REGISTRY

# =============================================================================
# all help texts are in here
# =============================================================================

COMMANDS_TEXT = (
    "[b]COMMANDS[/b]\n"
    "─────────────────────────\n"
    "/help, /?            (Show commands)\n"
    "Use ^ to chain       (e.g., /run ^ /config)\n\n"
    "/run                 (Launch strap)\n"
    "/stop                (Stop strap)\n"
    "/run --cr shr        (Add to startup)\n"
    "/run --d shr         (Remove from startup)\n\n"
    "/config              (Configure)\n\n"
    "/home                (Go to home screen)\n"
    "/back                (Go back)\n"
    "/clear               (Clear terminal)\n"
    "/restart             (Restart TUI)\n"
    "/exit                (Exit immediately)\n\n"
    "/profile             (Manage profiles)\n"
    "/profile --ls        (List all profiles)\n"
    "/profile --cr name   (Create new profile)\n"
    "/profile --use name  (Switch profile)\n"
    "/profile --d name    (Delete profile)\n\n"
    "/install             (Install Strap)\n"
    "/update              (Check for updates)\n"
    "/install --ls        (List versions on GitHub)\n"
    "/install vX.X.X      (Install specific version)\n\n"
    "/version             (Current versions)\n"
    "/version --ls        (List local versions)\n"
    "/switch vX.X.X       (Switch version)\n\n"
    "/uninstall           (Uninstall Strap)\n"
    "/uninstall --fr      (Fully wipe Strap)\n\n"
)

TERMINAL_COMMANDS_TEXT = (
    "\nCOMMAND                        DESCRIPTION\n"
    "────────────────────────────────────────────────────────\n"
    "strap /help, /?                Show commands\n\n"
    "strap /run                     Run strap\n"
    "strap /stop                    Stop strap\n"
    "strap /clear                   Clear terminal\n"
    "strap /run --cr shr            Add to startup\n"
    "strap /run --d shr             Remove from startup\n\n"
    "strap /config                  Configure Strap settings\n\n"
    "strap /profile                 Manage profiles\n"
    "strap /profile --ls            List all profiles\n"
    "strap /profile --cr name       Create new profile\n"
    "strap /profile --use name      Switch active profile\n"
    "strap /profile --d name        Delete profile\n\n"
    "strap /install                 Install Strap\n"
    "strap /update                  Check for and download updates from GitHub\n"
    "strap /install --ls            List available versions on GitHub\n"
    "strap /install vX.X.X          Install specific version from GitHub\n\n"
    "strap /version                 Current versions\n"
    "strap /version --ls            List local versions\n"
    "strap /switch vX.X.X           Switch active version\n\n"
    "strap /uninstall               Uninstall Strap\n"
    "strap /uninstall --fr          Fully wipe Strap\n\n"
)


CONFIG_COMMANDS_TEXT = (
    "[b]CONFIG COMMANDS[/b]\n"
    "─────────────────────────\n"
    "/config --save             (Save changes)\n"
    "/config --save --exit      (Save & go back)\n"
    "/config --abort            (Discard changes)\n"
    "/config -flag -No.         (Open popup)\n"
    "/config -flag -No. value   (Modify setting)\n\n"
)

def get_status_text(version: str, is_installed: bool, startup_enabled: bool, ahk_running: bool, st_tz: str, pending_count: int = None) -> str:
    base = (
        f"[b]STATUS[/b]\n"
        f"─────────────────────────\n"
        f"Version:      v{version}\n\n"
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
    # Safely get the label if the feature exists
    name = FEATURE_REGISTRY[no - 1]["label"] if 0 < no <= len(FEATURE_REGISTRY) else ""
    
    return (
        f"[b]CONFIG - [z{no}] {name}[/b]\n"
        f"─────────────────────────\n"
        f"/config -z -{no}              (Open popup)\n"
        f"/config -z -{no} --!          (Flip value)\n"
        f"/config -z -{no} value        (active | inactive)\n\n"
    )

CONFIG_U1_TEXT = (
    "[b]CONFIG - [u1] Tray Icon[/b]\n"
    "─────────────────────────\n"
    "/config -u -1              (Open popup)\n"
    "/config -u -1 --!          (Flip value)\n"
    "/config -u -1 value        visible | hidden)\n\n"
)

CONFIG_U2_TEXT = (
    "[b]CONFIG - [u2] Tooltip Timeout[/b]\n"
    "─────────────────────────\n"
    "/config -u -2              (Open popup)\n"
    "/config -u -2 time(in ms)  (Set value)\n\n"
)

CONFIG_U3_TEXT = (
    "[b]CONFIG - [u3] Switching Timezones[/b]\n"
    "─────────────────────────\n"
    "/config -u -3                  (Open popup)\n"
    '/config -u -3 "UTC_+/-No."     (Add timezone)\n'
    "  (adds if absent, removes if present)\n\n"
)

CONFIG_U4_TEXT = (
    "[b]CONFIG - [u4] TimeZone on Startup[/b]\n"
    "─────────────────────────\n"
    "/config -u -4                  (Open popup)\n"
    '/config -u -4 "UTC_+/-No."     (Set startup TZ)\n'
    "  (same TZ again = reset to default)\n\n"
)

POPUP_FORCE_KILL = (
    "[b]CONFIG - [y1] Force Kill[/b]\n"
    "─────────────────────────\n"
    "/config -y -1--1 text      (Set text)\n\n"
    "/back or Esc               (Close)\n\n"
)

POPUP_COLOR_PICKER = (
    "[b]CONFIG - [y2] Color Picker[/b]\n"
    "─────────────────────────\n"
    "/config -y -2--1 --!       (Flip value)\n"
    "/config -y -2--1 value     (enable|disable)\n\n"
    "/config -y -2--2 text      (Set Text)\n\n"
    "/back or Esc               (Close)\n\n"
)

def get_popup_tz_text(flag: str, no: int, is_single: bool, title: str) -> str:
    flag_no = f"-{flag} -{no}"
    tag = 'u4' if is_single else 'u3'
    clean_title = title.split(" - ")[-1] if " - " in title else title
    return (
        f"[b]CONFIG - [{tag}] {clean_title}[/b]\n"
        f"─────────────────────────\n"
        f'/config {flag_no} "UTC_+/-No." (Toggle by UTC)\n\n'
        f"/back or Esc                       (Close)\n\n"
    )

POPUP_UNSAVED = (
    "/config --save             (Save changes)\n"
    "/config --save --exit      (Save & go back)\n"
    "/config --abort            (Discard changes)\n\n"
    "/back or Esc               (Close)\n\n"
)
