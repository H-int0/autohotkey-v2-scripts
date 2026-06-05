import os
import subprocess

# =============================================================================
# Centralzed place to manage all AHK scripts processess
# =============================================================================

INSTALL_DIR = os.path.join(os.environ.get("APPDATA", ""), "Strap")

def stop_ahk() -> None:
    subprocess.run('taskkill /F /IM "AutoHotkey*"', shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_ahk() -> None:
    target = os.path.join(INSTALL_DIR, "core", "source.ahk")
    if os.path.exists(target):
        try:
            os.startfile(target)
        except Exception:
            pass
