import os
import subprocess

# =============================================================================
# startup.py
# Creates or removes the Strap Windows startup shortcut (.lnk).
# Uses PowerShell's WScript.Shell COM object same approach as the manual
# install method documented in README / RECOVERY.md.
# =============================================================================

STARTUP_DIR   = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "Strap.lnk")
TARGET_PATH   = os.path.join(os.environ["APPDATA"], "Strap", "core", "source.ahk")
WORKING_DIR   = os.path.join(os.environ["APPDATA"], "Strap", "core")


def is_startup_enabled() -> bool:
    """Return True if the Strap startup shortcut exists."""
    return os.path.exists(SHORTCUT_PATH)


def enable_startup() -> None:
    """Create (or refresh) the Strap startup shortcut via PowerShell WScript.Shell."""
    ps_script = (
        f'$ws = New-Object -ComObject WScript.Shell; '
        f'$s = $ws.CreateShortcut("{SHORTCUT_PATH}"); '
        f'$s.TargetPath = "{TARGET_PATH}"; '
        f'$s.WorkingDirectory = "{WORKING_DIR}"; '
        f'$s.Save()'
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def disable_startup() -> None:
    """Remove the Strap startup shortcut if it exists."""
    if os.path.exists(SHORTCUT_PATH):
        os.remove(SHORTCUT_PATH)

def run_from_startup_shortcut() -> bool:
    """Kill AHK if running, then launch from shell:startup shortcut if it exists. Returns True if launched."""
    import subprocess
    subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(SHORTCUT_PATH):
        try:
            os.startfile(SHORTCUT_PATH)
            return True
        except Exception:
            return False
    return False
