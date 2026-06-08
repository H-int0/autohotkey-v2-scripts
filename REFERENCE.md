# Reference

This document provides an in-depth look at each feature included in Strap. It explains not only *what* the features do, but *how* they work under the hood, their built-in safety mechanisms, and their specific use cases.

---

## Quick View

Check all the Hotkeys and Commands here:

### Hotkeys

- **Utilities:**

  | *Hotkey* | *Description* |
  | :--- | :--- |
  | `Win + Ctrl + \` | Toggle Tray Icon visibility |
  | `Win + Ctrl + /` | Reload script |
  | `Win + Shift + /` | Exit script |
  | `Win + /` | Toggle Dynamic Help Box |

- **Features:**

  | *Hotkey* | *Description* |
  | :--- | :--- |
  | `Win + Alt + `` ` | Switch between timezones |
  | `Win + Ctrl + `` ` | Show current timezone |
  | `Win + Ctrl + K` | Force kill active window |
  | `Win + Ctrl + C` | Toggle Color Picker |
  | `Shift + Alt + Left/Right Arrow` | Move cursor to start/end of line |
  | `Shift + Win + Left/Right Arrow` | Select text to start/end of line |
  | `Alt + Backspace/Delete` | Delete text to start/end of line |

### Strap Commands

> [!NOTE]
> All commands work in both the TUI and terminal. In the terminal, always prefix commands with `strap`. Inside the TUI, the prefix is optional.

- **General Commands**

  ```bash
  strap /help, /?                     # Show all available strap commands

  strap /run                          # Runs AHK scripts
  strap /stop                         # Stops AHK scripts
  strap /run --cr shr                 # Create startup shortcut (enables auto-boot on login)
  strap /run --d sh                   # Delete startup shortcut (disables auto-boot)

  strap /config                       # Configure Strap settings

  strap /clear                        # Clear TUI
  strap /restart                      # Restart TUI
  strap /exit                         # Exit immediately

  strap /profile                      # Manage profiles
  strap /profile --ls                 # List all profiles
  strap /profile --cr name            # Create new profile
  strap /profile --use name           # Switch active profile
  strap /profile --d name             # Delete profile

  strap /install --ls                 # List all available versions on GitHub
  strap /install vX.X.X               # Install a specific version from GitHub
  strap /update                       # Check for and download updates from GitHub

  strap /version                      # Current versions
  strap /version --ls                 # List local versions

  strap /switch vX.X.X                # Switch your active version

  strap /uninstall                    # Uninstall Strap
  strap /uninstall --fr               # Fully Remove Strap
  ```

> [!TIP]
> Chain commands with `^`. Example: `/run ^ /config`

- **Config Commands Structure**

  ```bash
  # Opens a Popup
  /config -{flag} -{Config No.}

  # Quickly flip a boolean setting
  /config -{flag} -{Config No.} --!

  # Configure the setting
  /config -{flag} -{Config No.} {Value}
  
  # Configure the sub-setting
  /config -{flag} -{Config No.}--{Sub-Config No.} {Value}

  # Using `!` before the flag Auo-saves the configuration
  /config -!{flag}...

  # Stage → write to disk → relaunch AHK
  /config --save

  # Same as above, except it goes back to home
  /config --save --exit  or  /config --!save

  # Discard all pending changes
  /config --abort
  ```

---

## Table of Contents

- [Quick View](#quick-view)
  - [Hotkeys](#hotkeys)
  - [Strap Commands](#strap-commands)
- [Installation](#installation)
- [Utilities](#utilities)
  - [1. Tray Icon Toggle](#1-tray-icon-toggle)
  - [2. Reloading the Script](#2-reloading-the-script)
  - [3. Exiting the Script](#3-exiting-the-script)
  - [4. Dynamic Help Box](#4-dynamic-help-box)
- [Features](#features)
  - [1. Numpad Emulator](#1-numpad-emulator)
  - [2. Alt Codes](#2-alt-codes)
  - [3. Timezone Switcher](#3-timezone-switcher)
  - [4. Force Kill Task](#4-force-kill-task)
  - [5. Color Picker](#5-color-picker)
  - [6. Line Navigation](#6-line-navigation)
- [Strap CLI/TUI](#strap-clitui)
  - [Profiles](#profiles)
  - [Management](#management)
  - [Layout](#layout)
  - [Home Screen](#home-screen)
  - [Config Screen](#config-screen)
  - [Config Commands](#config-commands)
    - [Utility settings (`u`)](#utility-settings-u)
    - [Feature toggles (`z`)](#feature-toggles-z)
    - [Feature sub-settings (`y`)](#feature-sub-settings-y)
- [Uninstallation](#uninstallation)

---

## Installation

- With **Command Prompt (CMD)**:

  ```bat
  powershell -ExecutionPolicy Bypass -Command "irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex"
  ```

- With **PowerShell**:

  ```pwsh
  irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex
  ```

> [!TIP]
> Prefer the ZIP version? Simply extract the ZIP file, open the setup folder, and double-click `install.bat` inside `setup`directory to set up the TUI.

  ```bash
  # Replace with your file path to the root directory of the project after extracting the zip
  cd C:\path_to_strap\autohotkey-v2-scripts-main
  
  # use this to hook up the CLI/TUI:
  python cli/main.py /install
  ```

---

### How Installations work behind the scenes

When you run the one-liner above, `install.ps1` takes over and does the following:

1. **Checks for Python** exits immediately if Python 3 isn't found.
2. **Fetches the latest tag from GitHub** hits the GitHub tags API and grabs the latest tag name and its zip URL.
3. **Archives the release** creates `~/.strap_versions/vX.X.X/` and downloads the release zip into it. If that version folder already exists, the download is skipped entirely.
4. **Copies to `%APPDATA%\Strap\`** if a previous installation exists, everything except `bin\` is wiped first. Then the archived version is copied in fresh.
5. **Creates `strap.bat`** only if it doesn't already exist. Points permanently to `%APPDATA%\Strap\cli\main.py` and never gets touched again, even across version switches.
6. **Adds `bin\` to PATH** modifies the user-level `PATH` registry key and broadcasts `WM_SETTINGCHANGE` so open terminals pick up the new `strap` command without needing a restart.
7. **Installs Python dependencies** runs `pip install -r requirements.txt` quietly.
8. **Hands off to Python** calls `python cli/main.py /install --from-ps`.

---

### The `--from-ps` flag

`--from-ps` is an internal flag passed automatically by `install.ps1` in step 8. It tells the CLI that file copying, `strap.bat` creation, and PATH setup are already done so it skips those and only handles:

```bash
python cli/main.py /install --from-ps
```

- Bootstrapping the `default` and `ghost` profiles
- Stamping the active version into the profile
- Writing `config.ahk` and `timezones-variables.ahk` from the active profile
- Prompting the user for startup shortcut preference

You will never need to type this flag manually unless you are testing the Python-side of the install flow without re-running the full PowerShell script.

---

### Running `/install` directly

If you're not using the PowerShell bootstrapper, you can run the installer manually after cloning the repo:

```bash
python cli/main.py /install
```

Without `--from-ps`, the CLI assumes it is running in a fresh environment and handles the full install flow itself creating `strap.bat`, adding `bin\` to PATH, bootstrapping profiles, and prompting for startup. Use this when setting up manually from a ZIP or a cloned repo instead of the one-liner.

---

## Utilities

Strap includes built-in quality-of-life utilities that manage how the script interacts with you.

- All Utility Hotkeys

  | *Hotkey* | *Description* |
  | :--- | :--- |
  | `Win + Ctrl + \` | Toggle Tray Icon visibility |
  | `Win + Ctrl + /` | Reload script |
  | `Win + Shift + /` | Exit script |
  | `Win + /` | Toggle Dynamic Help Box |

---

### 1. Tray Icon Toggle

To keep your taskbar clean, Strap hides its AutoHotkey tray icon by default.

**Hotkey:** `Win + Ctrl + \`

- This hotkey flips the `A_IconHidden` state, allowing you to reveal the icon temporarily if you need to right-click it to Suspend, Reload, or Exit the script.

---

### 2. Reloading the Script

To reload your script, Use the **Hotkey:** `Win+Ctrl+/`

- This hotkey is tied to AHk's own Reload script feature.

---

### 3. Exiting the Script

To Exit your script, use the **Hotkey:** `Win+Shift+/`

- This hotkey is tied to AHK's own Exit script feature.

---

### 4. Dynamic Help Box

A lightweight, semi-transparent (`Opacity: 225`) black overlay that follows your mouse and lists your active shortcuts.

**Hotkey:** `Win + /`

- **Dynamic Aggregation:**

  - The Help Box is not hardcoded. Whenever a feature is enabled, it pushes its specific instructions into a global array called `HelpEntries`.
  - The Help Box dynamically loops through this array to build the UI. If you disable a feature, it instantly disappears from the Help Box.
- **Mouse Tracking:**
  - Like the Color Picker, the Help Box updates its position every 10ms and clamps to the edges of your screen.

---

## Features

- All Features Hotkeys

  | *Hotkey* | *Description* |
  | :--- | :--- |
  | `Win + Alt + `` ` | Switch between timezones |
  | `Win + Ctrl + `` ` | Show current timezone |
  | `Win + Ctrl + K` | Force kill active window |
  | `Win + Ctrl + C` | Toggle Color Picker |
  | `Shift + Alt + Left/Right Arrow` | Move cursor to start/end of line |
  | `Shift + Win + Left/Right Arrow` | Select text to start/end of line |
  | `Alt + Backspace/Delete` | Delete text to start/end of line |

---

### 1. Numpad Emulator

A hardware-level numpad substitute for Ten-key-less (TKL), 60%, and laptop keyboards, mapping the standard number row to actual Numpad keycodes.

**Hotkeys:**

- **Toggle:** `CapsLock`
- **Use:** `0-9` on the number row
- **Shift Behavior:** `Shift + 0-9` (Configurable)

**How it Works:**

Unlike simple text replacement scripts that just send the characters "1", "2", "3", this feature sends `{Blind}{Numpad1}`, `{Blind}{Numpad2}`, etc.

- **The `{Blind}` Modifier:**
  - This allows the emulated numpad keys to respect standard modifier keys.
  - If you hold `Ctrl` and press the `1` key while CapsLock is ON, the computer registers `Ctrl + Numpad1`.
  - This is critical for software that relies on specific numpad shortcuts (like Blender or certain IDEs).
- **Shift Fallback:**
  - By default, holding `Shift` while CapsLock is ON suspends the numpad emulation and sends the standard symbols (`!`, `@`, `#`, etc.).
  - This means you don't have to toggle CapsLock off just to type an exclamation mark. This behavior can be disabled in `config.ahk`.

---

### 2. Alt Codes

The Alt Code feature replicates Windows alt code input without a physical numpad by intercepting Alt key events and building a number buffer from the numrow.

**How it works:**

Input flow:

1. Pressing `LAlt` or `RAlt` clears any existing buffer
2. While `Alt` is held, pressing `0–9` on the numrow appends that digit to the buffer CapsLock state is ignored
3. Releasing `Alt` fires the conversion and sends the character via `{Text}` mode

If Shift, Ctrl, or Win are held alongside a digit, the append is aborted those are not alt code inputs and shouldn't interfere with native OS shortcuts.

**Conversion of two modes based on whether the input has a leading zero:**

| Input | Mode | Encoding |
| --- | --- | --- |
| No leading zero | OEM / CP437 | 1–31: CP437 symbol glyphs (☺ ♥ ♦ ...) · 32–255: CP437 printable · 256+: Unicode code-point via `Chr()` |
| Leading zero | ANSI / Windows-1252 | `0128`–`0255`: Windows-1252 chars (€ ™ © ...) |

- The CP437 control range (1–31) is special instead of sending actual control characters, it maps to their graphical CP437 symbol equivalents (e.g., `1` → ☺ `U+263A`, `3` → ♥ `U+2665`).
- Unicode inputs above 1,114,111 and surrogate values (U+D800–U+DFFF) are silently discarded to prevent `Chr()` errors.

**Why a buffer and not individual key presses?**

- `Alt` combinations are heavily used by the OS and applications for menu shortcuts and hotkeys. The feature hooks into Alt press/release events passively using `~*` (tilde-wildcard) the underlying key events still pass through. Only on Alt release does it check the buffer and fire, so normal Alt behavior is never broken.

---

### 3. Timezone Switcher

A system-level utility to instantly cycle your Windows clock between different global timezones without navigating through the Windows Settings app.

**Hotkeys:**

- `Win + Alt + `` ` switch to the next timezone in your list.
- `Win + Ctrl + `` ` show the current timezone.

**How it works:**

Strap bypasses the UI entirely and interacts directly with the Windows command-line utility `tzutil.exe`.

- **State Reading:**
  - When checking the current timezone, Strap reads the Windows Timezone ID directly from the registry key:  
    `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation\TimeZoneKeyName`  
  - This is instant, avoids creating temporary files, and is mapped to your human-readable label.
- **Sequential Cycling:**
  - The script maintains an ordered array (`TZOrder`) and a dictionary (`TZData`).
  - It identifies your current timezone, calculates the next one in the array, and executes `tzutil /s "Next Timezone"`.
- **Instant Feedback:**
  - A mouse-tracking tooltip instantly confirms the newly applied timezone so you never have to guess what your clock is set to.

---

### 4. Force Kill Task

A smart, context-aware window closer that gracefully exits healthy programs and ruthlessly terminates frozen ones.

**Hotkey:** `Win + Ctrl + K`

**How It Works:**

This is not a blind `taskkill` command. It is a multi-stage evaluation of the active window to ensure stability and prevent accidental system damage:

1. **Safety Checks:**
    - It first captures the active window's Class and Process ID (PID).
    - If the active window is the Desktop (`Progman`, `WorkerW`) or
    - the Taskbar (`Shell_TrayWnd`), it immediately aborts.
    - You cannot accidentally crash your Windows shell.
2. **Responsiveness Evaluation:**
    - It checks if Windows has already flagged the app as unresponsive using `DllCall("IsHungAppWindow")`.
    - If not flagged, it pings the window's main thread using `SendMessage(0x0)` (a `WM_NULL` message) with a strict 250-millisecond timeout.
3. **Execution:**
   - **Healthy (Responding):** If the ping returns successfully, Strap sends a standard `WinClose` request. This is equivalent to pressing `Alt+F4` or clicking the "X", allowing the app to prompt you to save your work.
   - **Frozen (Not Responding):** If the ping times out, Strap bypasses the window entirely and executes `taskkill /PID [pid] /F` via the command line, evaporating the frozen process instantly.

---

### 5. Color Picker

A developer-centric, floating live color picker that captures screen pixels, translates them into Hex and RGB, and copies them to your clipboard.

**Hotkey:** `Win + Ctrl + C` (Press to open, press again to capture/close)

**how it works:**

The Color Picker operates in a continuous, high-priority 5ms loop while active.

- **Cursor Override:**
  - Upon activation, it uses a deep Windows API call (`User32.dll\SetSystemCursor`) to replace your standard mouse pointers with a precise precision crosshair (`id: 32515`), copying and storing your original cursors in memory to restore them later.
- **Live GUI:**
  - It spawns a border-less, always-on-top GUI containing a live color swatch.  
  - A high‑priority timer (`SetTimer`, **20 ms interval**) continuously polls `PixelGetColor` and `MouseGetPos` relative to your screen, giving smooth, real‑time updates.
- **Math & Formatting:**
  - It strips the `0x` from the raw color string, formats it to lowercase Hex, and runs Integer conversions to calculate the exact `R`, `G`, and `B` values.
- **Boundary Clamping:**
  - The script actively reads your monitor's Work Area (`MonitorGetWorkArea`) and recalculates the GUI's `X` and `Y` coordinates on the fly. If you move your mouse to the absolute bottom-right edge of your screen, the GUI will push itself upward and leftward so it never clips off-screen.
- **Capture:**
  - On the second press, the GUI is destroyed, original cursors are restored, and the data is piped to `A_Clipboard`.
  - If `ColorPickerMsgBox` is enabled in `config.ahk`, a summary window will appear displaying the Hex, RGB, and coordinates before closing. Otherwise, it closes silently.

---

### 6. Line Navigation

Translates modern text-editor navigation shortcuts into standard Windows keystrokes, allowing for rapid text manipulation without reaching for the physical `Home` or `End` keys.

**Hotkeys:**

- **Move Cursor:** `Shift + Alt + Left/Right`
- **Select Text:** `Shift + Win + Left/Right`
- **Delete Text:** `Alt + Backspace/Delete`

**How it Works?**

It leverages standard OS-level text inputs.

- Moving sends `{Home}` or `{End}`.
- Selecting sends `+{Home}` (Shift+Home) or `+{End}` (Shift+End).
- Deleting evaluates the cursor position and sends a selection command followed immediately by `{Backspace}` or `{Delete}`.
This provides universally compatible text navigation across almost every Windows application, browser, and IDE.

---

## Strap CLI/TUI

Run `strap` in your terminal to launch the TUI. If you pass arguments directly, it runs headlessly without opening the TUI.

```cmd
strap             # no args opens the TUI
strap /command    # headless runs the command and exits
```

- All Commands

  ```bash
  strap /help, /?                     # Show all available strap commands

  strap /run                          # Runs AHK scripts
  strap /stop                         # Stops AHK scripts
  strap /run --cr shr                 # Create startup shortcut (enables auto-boot on login)
  strap /run --d sh                   # Delete startup shortcut (disables auto-boot)

  strap /config                       # Configure Strap settings

  strap /clear                        # Clear TUI
  strap /restart                      # Restart TUI
  strap /exit                         # Exit immediately

  strap /profile                      # Manage profiles
  strap /profile --ls                 # List all profiles
  strap /profile --cr name            # Create new profile
  strap /profile --use name           # Switch active profile
  strap /profile --d name             # Delete profile

  strap /install --ls                 # List all available versions on GitHub
  strap /install vX.X.X               # Install a specific version from GitHub
  strap /update                       # Check for and download updates from GitHub

  strap /version                      # Current versions
  strap /version --ls                 # List local versions
  strap /switch vX.X.X                # Switch your active version

  strap /uninstall                    # Uninstall Strap
  strap /uninstall --fr               # Fully Remove Strap
  ```

---

- Creating the shortcut places `Strap.lnk` in `shell:startup` (`%APPDATA%\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`).
- Removing it deletes `Strap.lnk` from that same folder.
- The shortcut points to `source.ahk` with its working directory set to `%APPDATA%\Strap\` this is what ensures the script resolves its `#Include` paths correctly on boot.
- The startup shortcut is automatically refreshed on every version switch if one already exists.

---

### Profiles

Profiles store a complete snapshot of your config so you can switch between different setups without losing settings. Each profile has its own `user-config.json` stored at `~/.strap_profiles/<name>/`.

**Three profile types:**

| Type | Behavior |
| --- | --- |
| `default` | Always full defaults. Read-only automatically reset on every version switch. Cannot be edited or deleted. |
| `ghost` | Automatically created the first time you make a config change without a named profile active. Persists across version switches. |
| named | User-created. Persists across version switches. |

On every version switch or install, all profiles are automatically migrated new config keys are added at their defaults, unknown keys from older versions are left in place (older install won't break), and the `version` field is stamped to match the active version.

If you switch profiles while AHK is running, it is relaunched after receiving confirmation from the user for the new profile's config applied.

```bash
/profile                    # Manage profiles
/profile --ls               # List all profiles (active one marked)
/profile --cr name          # Create a new named profile (starts at defaults)
/profile --use name         # Switch active profile (prompts TUI restart)
/profile --d name           # Delete a named profile
```

**Constraints:**

- `default` and `ghost` cannot be deleted
- You cannot delete the currently active profile switch first
- `default` cannot be written to; any config change automatically promotes you to `ghost` if no named profile is active

---

### Management

Installed versions are archived locally in `~/.strap_versions/` and never modified. You can install multiple versions and switch between them without re-downloading.

```bash
/install --ls               # List all available versions on GitHub
/install vX.X.X             # Download a specific version and install/switch to it
/update                     # Check GitHub for the latest version and download it

/switch vX.X.X              # witch to a locally archived version (no download)
/version                    # Show current active version
/version --ls               # List locally archived versions (active one marked)
```

---

#### 1. `/install vX.X.X`

Downloads and archives a specific version from GitHub, then optionally switches to it.

**Behind the scenes:**

1. Builds the zip URL directly from the tag: `https://codeload.github.com/H-int0/autohotkey-v2-scripts/zip/refs/tags/vX.X.X`
2. If that version is already archived in `.strap_versions`, the existing archive is wiped and re-downloaded fresh.
3. Extracts the zip and copies it into `~/.strap_versions/vX.X.X/`, skipping `.git`, `.github`, `bin`, and `__pycache__`.
4. If Strap is already installed, asks whether to switch to the downloaded version. If you decline, it stays archived and available for later via `/switch`.
5. If Strap is not installed, performs a fresh install from the archive copies files to `%APPDATA%\Strap`, creates `strap.bat`, adds `bin\` to PATH, and bootstraps profiles.

---

#### 2. `/update`

Checks GitHub for a newer version and downloads it if one exists.

**Behind the scenes:**

1. Hits the GitHub tags API and grabs the latest tag.
2. Compares it against the active version by parsing the version string into a tuple and doing a numeric comparison so `1.10.0` correctly beats `1.9.0`.
3. If already up to date, exits early.
4. If a newer version exists, wipes any existing archive for that version and re-downloads it fresh into `.strap_versions/`.
5. Asks whether to switch now. If you decline, the version sits in `.strap_versions` and you can switch later with `/switch`.

---

#### 3. `/switch vX.X.X`

Switches to a version already archived locally. No download happens.

**Behind the scenes:**

1. Verifies the target version exists in `~/.strap_versions/`. Exits early if not found.
2. Wipes everything in `%APPDATA%\Strap\` except `bin\` `strap.bat` is never touched.
3. Copies the target version from `~/.strap_versions/vX.X.X/` into `%APPDATA%\Strap\`.
4. Loads `DEFAULT_CONFIG` from the new version's `schema.py` using `exec()` not `import`, to avoid stale module cache.
5. Resets the `default` profile to the new version's defaults entirely.
6. For every other profile (`ghost` and named), adds any missing keys at their defaults and stamps the new version. Extra keys from older versions are left alone.
7. Rewrites `core/config.ahk` and `core/config-dependencies/timezones-variables.ahk` from the active profile.
8. If a startup shortcut exists, removes and recreates it so it points to the correct version.

> [!NOTE]
> `strap.bat` is never touched during a version switch. It always points to `%APPDATA%\Strap\cli\main.py`, which gets overwritten with the new version's files in step 3.

---

#### 4. `/install --ls`

Hits the GitHub tags API and prints all available tags in pages of 10. Press Enter to load more, `q` to quit. Does not download anything.

---

#### 5. `/version` and `/version --ls`

Both commands read `%APPDATA%\Strap\VERSION` for the active version, then scan `~/.strap_versions/` for all archived folders. `/version --ls` lists all of them with the active one marked. `/version` alone shows only the active version.

---

### Layout

The TUI has two screens.

- **Home screen:**
  - the default screen on launch. Has a command prompt (`>>`) on the right and a status/help panel on the left. The right side outputs command results into a scrollable log.
  - The left panel shows your current status and available commands, and updates its hints contextually as the user type.
- **Config screen:**
  - opened via `/config`. Has the same left panel layout (status + contextual hints) but the right side is replaced by an interactive settings list instead of a log.
  - Changes are staged as pending and only written to disk when user explicitly save.

---

### Home Screen

Type any command into the `>>` prompt. Commands must start with `/`. Inside the TUI the `strap` prefix is optional.

- **Left panel:**
  - Shows live status at the top:

    ```bash
    Version:      vX.X.X

    Installed:    Yes
    Startup:      Enabled
    Auto start:   Yes
    AHK running:  Yes
    Startup TZ:   default

    Pending:      0
    ```

  - The panel also updates its hint text contextually as you type a config command if you type `-z -1`, the left panel immediately shows the commands relevant to that setting.

- **Command chaining:**
  - use `^` to run multiple commands in sequence:
  - Commands in a chain execute one after another. If a command requires a y/n prompt (like `/install` or `/uninstall`), the chain pauses and waits for your answer before continuing.
  - Example:

    ```bash
    /run ^ /config
    /profile --use work ^ /restart
    ```

---

### Config Screen

- Open with `/config`. All settings are listed in the right panel. Each setting has a flag tag that identifies its type and number:

  | Flag | Type | Example |
  | --- | --- | --- |
  | `u` | Utility / global settings | `[u1]` Tray Icon |
  | `z` | Feature toggles (enable/disable) | `[z1]` NumPad Emulator |
  | `y` | Feature sub-settings | `[y1]` Force Kill options |

---

- Settings with a pending unsaved change are marked with a `*` next to their tag.

- **Saving** changes are staged and not applied until you explicitly save. AHK is automatically killed and relaunched after a save so changes take effect immediately.

  ```bash
  /config --save              # Stage → write to disk → relaunch AHK
  /config --save --exit       # Same as above, except it goes back to home
  /config --!save             # Alternative for `/config --save --exit`
  /config --abort             # Discard all pending changes
  ```

- If you try to leave the config screen (`/back`, `Esc`) with unsaved changes, an **Unsaved Changes popup** appears listing every pending change with its old and new value. You can save, save and exit, or abort from within it.

---

- **Auto-save flag** prefix any config command with `-!{flag}` to apply and save in one step:

  ```bash
  /config -!z -1 active       # Set z1 to active and immediately save it
  ```

---

### Config Commands

- **Config Commands Structure**

  ```bash
  # Opens a Popup
  /config -{flag} -{Config No.}

  # Quickly flip a boolean setting
  /config -{flag} -{Config No.} --!

  # Configure the setting
  /config -{flag} -{Config No.} {Value}
  
  # Configure the sub-setting
  /config -{flag} -{Config No.}--{Sub-Config No.} {Value}

  # Using `!` before the flag Auo-saves the configuration
  /config -!{flag}...

  # Stage → write to disk → relaunch AHK
  /config --save

  # Same as above, except it goes back to home
  /config --save --exit  or  /config --!save

  # Discard all pending changes
  /config --abort
  ```

#### Utility settings (`u`)

- **`[u1]` Tray Icon** controls whether the AHK tray icon is visible.

  ```bash
  /config -u -1                   # Open popup
  /config -u -1 visible           # Set to visible
  /config -u -1 hidden            # Set to hidden
  /config -u -1 --!               # Flip current boolean value
  ```

  > HERE Accepted values: `visible`, `show`, `1`, `true`, `yes` / `hidden`, `hide`, `0`, `false`, `no`

---

- **`[u2]` Tooltip Timeout** how long tooltips stay on screen, in milliseconds.

  ```bash
  /config -u -2                   # Open popup (shows current value)
  /config -u -2 3000              # Set to 3000ms (3 seconds)
  ```

  > Value HERE must be a positive integer. `1 sec = 1000ms`.

---

- **`[u3]` Switching Timezones** the ordered list of timezones the Timezone Switcher cycles through. Toggling a timezone that is already in the list removes it; toggling one that isn't adds it.

  ```bash
  /config -u -3                   # Open timezone picker popup
  /config -u -3 "UTC_+/-No."      # Toggle a timezone in the switcher cycle
  ```

- The timezone picker popup shows a searchable list of all timezones with live current times for active ones. You can search by name, UTC offset, or city. Opening the popup and using commands inside it both update pending state in real time.

---

- **`[u4]` Timezone on Startup** the timezone AHK switches to automatically when Strap starts. Setting the same timezone again resets it to default (no override).

  ```bash
  /config -u -4                   # Open timezone picker popup (single-select)
  /config -u -3 "UTC_+/-No."      # Set startup timezone (same value again = reset)
  ```

---

#### Feature toggles (`z`)

- Each feature has a `z` number. All take the same commands:

  ```bash
  /config -z -N                   # Open popup (shows current state)
  /config -z -N active            # Enable
  /config -z -N inactive          # Disable
  /config -z -N --!               # Flip current value
  ```

  > HERE Accepted values: `active`, `enable`, `1`, `true`, `yes` / `inactive`, `disable`, `0`, `false`, `no`

  | Flag | Feature |
  | --- | --- |
  | `z1` | NumPad Emulator |
  | `z2` | ALT Codes |
  | `z3` | TimeZone Switcher |
  | `z4` | Force Kill |
  | `z5` | Color Picker |
  | `z6` | Line Navigation |

---

#### Feature sub-settings (`y`)

- **`[y1]` Force Kill** configure the tooltip text shown after a process is killed. Leave it empty to disable the tooltip entirely.

  ```bash
  /config -y -1                   # Open popup
  /config -y -1--1 TERMINATED     # Set tooltip text to "TERMINATED"
  /config -y -1--1 ""             # Clear tooltip text (disables tooltip)
  ```

---

- **`[y2]` Color Picker** two sub-settings: the summary msgbox shown after picking, and the tooltip text.

  ```bash
  /config -y -2                   # Open popup

  /config -y -2--1 enable         # Enable the summary msgbox
  /config -y -2--1 disable        # Disable the summary msgbox
  /config -y -2--1 --!            # Flip msgbox toggle

  /config -y -2--2 Copied!        # Set tooltip text
  /config -y -2--2 ""             # Clear tooltip text (disables tooltip)
  ```

---

## Uninstallation

  ```bash
  /uninstall                      # Uninstall Strap
  /uninstall --fr                 # Fully Remove Strap
  ```

- Stops AHK, removes the startup shortcut, removes `strap` from your PATH, and deletes `%APPDATA%\Strap`and Version archives.
- Profiles are preserved for future use case.
- If `--fr` flag is used profiles are also deleted.

---

~*[@H-int0](https://github.com/H-int0)*
