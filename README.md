# Strap

**Strap** adds keyboard shortcuts for quick system-level actions at your finger tips, configurable with a Python based CLI/TUI.

- Currently, it ships with Six features with more planned for the future!

  | Feature | What it does |
  | --- | --- |
  | NumPad Emulator | Turns the number row into a real Numpad when Caps Lock is ON. |
  | ALT Code | Makes ALT codes work with Number Row keys. (Type ALT + 9825 for ♡) |
  | TimeZone Switcher | Switch your Timezone with a single keyboard shortcut. |
  | Force Kill | Instantly kills the active window, even the frozen ones with a single shortcut. |
  | Color Picker | Opens up a floating Color Picker. |
  | Line Navigation | Instantly navigate or select an entire line at once. |

- Strap also ships with a terminal UI for managing everything without touching config files directly.

  | | |
  | --- | --- |
  | **Configure** | Toggle features and tweak settings |
  | **Profiles** | Save and switch between named configurations |
  | **Versions** | Install, archive, and switch between multiple versions |
  | **Startup** | Control whether Strap auto-boots with Windows |
  | **Run / Stop** | Launch and stop the AHK scripts on demand |

> Strap is still in active development. The AHK scripts are stable, but the CLI may behave unexpectedly.
> Don't worry it won't NUKE your system. But if something breaks, see [RECOVERY.md](RECOVERY.md) for safe removal instructions.

---

<!-- markdownlint-disable-next-line -->
### Houston, we have problems!!!

If something ain't working, [open a bug report](https://github.com/H-int0/autohotkey-v2-scripts/issues/new?template=bug_report.md) and we'll look forward into it.

---

### Got a big brain idea?

If you have an idea for something new, adding new features or think an existing feature could be better, [open a feature request](https://github.com/H-int0/autohotkey-v2-scripts/issues/new?template=feature_request.md).

---

## Table of Contents

- [Quickly Install Strap](#quickly-install-strap)
- [Getting Started](#getting-started)
  - [Hotkeys](#hotkeys)
  - [Strap Commands](#strap-commands)
- [Repo Structure](#repo-structure)
- [Features](#features)
  - [1. Numpad Emulator](#1-numpad-emulator)
  - [2. ALT Codes](#2-alt-codes)
  - [3. Timezone Switcher](#3-timezone-switcher)
  - [4. Force Kill Task](#4-force-kill-task)
  - [5. Color Picker](#5-color-picker)
  - [6. Line Navigation](#6-line-navigation)
- [Strap's CLI/TUI](#straps-clitui)
  - [Startup Shortcut](#startup-shortcut)
  - [Profiles](#profiles)
  - [Management](#management)
  - [Layout](#layout)
  - [Home Screen](#home-screen)
  - [Config Screen](#config-screen)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [LICENSE](#license)

## OS Supported

- [Windows 7](https://www.microsoft.com/en-us/download/details.aspx?id=53332)*
- [Windows 8](https://www.microsoft.com/en-us/download/details.aspx?id=40745)*
- [Windows 10](https://www.microsoft.com/en-us/software-download/windows10)
- [Windows 11](https://www.microsoft.com/en-us/software-download/windows11)

## Requirements

- [AutoHotkey v2.0](https://www.autohotkey.com/) installed

  ```cmd
  winget install -e --id AutoHotkey.AutoHotkey
  ```

- [Python3](https://www.python.org/downloads/) installed

  ```cmd
  winget install Python.Python.3
  ```

---

## Quickly Install Strap

- With **Command Prompt (CMD)**:

  ```bat
  powershell -ExecutionPolicy Bypass -Command "irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex"
  ```

- With **PowerShell**:

  ```pwsh
  irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex
  ```

> [!TIP]
> Prefer the ZIP version? Simply extract the ZIP file, open the setup folder, and double-click `install.bat` inside `setup`directory to set up the TUI Automatically.

```bash
# Replace with your file path
cd C:\path_to_strap\autohotkey-v2-scripts-main
  
# use this to hook up the CLI/TUI:
python cli/main.py /install
```

### After Installation

```bash
# verify installation (launches the TUI):
strap

# Try running AHK scripts
strap /run
```

> Try pressing `win + /` to see all the hotkeys.

---

## Getting Started

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
  strap /run --cr shr                 # Enable auto-boot (creates a startup shortcut)
  strap /run --d shr                  # Disable auto-boot (removes from startup)

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

### Repo Structure

```bash
\:.
|   CHANGELOG.md                        # version history
|   CONTRIBUTING.md
|   REFERENCE.md                        # documentation of how everything actually work
|   install.ps1                         # bootstrap installer (run via irm | iex)
|   LICENSE
|   README.md
|   RECOVERY.md                         # safe removal instructions
|   VERSION                             # current version string
|
+---setup
|       install.bat                     # to manually setup strap's TUI
|
+---cli                                 # holds the entire CLI
|   |   commands.py                     # Handles command parsing
|   |   features.py                     # Holds the FEATURE_REGISTRY list
|   |   headless.py                     # Shared config parser for main.py and TUI screens
|   |   main.py                         # THE entry point for the TUI
|   |   requirements.txt
|   |
|   +---config
|   |       manager.py                  # reads/writes .JSON
|   |       parser.py                   # reads config.ahk into .JSON
|   |       schema.py                   # defines the structure of the .JSON
|   |
|   +---data
|   |       timezones_catalog.py        # full timezone list for TUI picker
|   |
|   +---ops
|   |       file_editor.py              # writes JSON config back to config.ahk via regex
|   |       installer.py                # install logic (from PowerShell or in-app)
|   |       process.py                  # AHK process management (run/stop/restart)
|   |       startup.py                  # Windows startup shortcut management
|   |       updater.py                  # version switching and profile migrations
|   |
|   \---tui
|       |   app.py                      # Textual app root
|       |   constants.py                # shared UI strings and hint text
|       |
|       +---popups
|       |       alerts.py               # generic alert dialogs
|       |       base.py                 # base popup class
|       |       settings.py             # boolean toggle popup
|       |       timezones.py            # timezone selector popup
|       |
|       +---screens                     # holds all screens in the TUI
|       |       config.py
|       |       home.py
|       |
|       +---styles                      # holds the TUI's stylesheets
|       |       config.tcss
|       |       home.tcss
|       |
|       \---widgets
|               config_panel.py         # config feature list widget
|
\---core                                # holds all the ahk scripts
    |   config.ahk                      # user-facing config variables
    |   source.ahk                      # entry point of .ahk scripts, loads all features
    |
    +---config-dependencies             # holds catalogs of data
    |       timezones-list.ahk
    |       timezones-variables.ahk
    |
    \---features                        # holds the script of all individual script
            alt-codes.ahk
            color-picker.ahk
            force-kill-task.ahk
            line-navigation.ahk
            numpad-emulator.ahk
            timezone-switcher.ahk
```

## Features

> [!TIP]
> Curious what's going on behind the scenes? Or, Wondering what's actually happening when you press that hotkey? Make sure to checkout [REFERENCE.md](REFERENCE.md).

### 1. Numpad Emulator

A hardware-level numpad substitute for Ten-key-less (TKL), 60%, and laptop keyboards, mapping the standard number row to actual Numpad keycodes.

**Hotkeys:**

- **Toggle:** `CapsLock`
- **Use:** Toggles number row keys between normal mode and Numpad mode with `Caps Lock` state **off** and **on** respectively.

---

### 2. ALT Codes

- Type Alt codes directly from your number row. (Try pressing `ALT + 9825` for a `♡`)

---

### 3. Timezone Switcher

A system-level utility to instantly cycle your Windows clock between different global timezones without navigating through the Windows Settings app.

**Hotkeys:**

- `Win + Alt + `` ` : switch to the next timezone in your list.
- `Win + Ctrl + `` ` : show the current timezone.

Each time you cycle, a small tooltip appears near your cursor showing the new Timezone.

- Changes are applied instantly and saved to Windows Settings.
- Your preferences persist through restarts.

> [!NOTE]
> If switching does not work, go to **Settings > Time & Language > Date & Time** and turn off **Set time zone automatically**.

**Active by Default:**

- Out of the box, Strap comes pre-configured to cycle through these five timezones:

  | Label | UTC Offset |
  | --- | --- |
  | Berlin/Paris | +1 |
  | Moscow | +3 |
  | Tokyo | +9 |
  | Sydney | +10 |
  | Eastern Time | -5 |

---

> [!WARNING]
> Be careful the List below is Long. It contains 139 different TimeZones supported by Strap.

<details>
  <summary>Supported Timezones</summary>

  | Label | UTC Offset | Windows ID |
  | --- | --- | --- |
  | Dateline Standard Time | -12 | `Dateline Standard Time` |
  | UTC-11 | -11 | `UTC-11` |
  | Aleutian Standard Time | -10 | `Aleutian Standard Time` |
  | Hawaiian Standard Time | -10 | `Hawaiian Standard Time` |
  | Marquesas Standard Time | -9:30 | `Marquesas Standard Time` |
  | Alaskan Standard Time | -9 | `Alaskan Standard Time` |
  | UTC-09 | -9 | `UTC-09` |
  | Pacific Standard Time (Mexico) | -8 | `Pacific Standard Time (Mexico)` |
  | UTC-08 | -8 | `UTC-08` |
  | Pacific Standard Time | -8 | `Pacific Standard Time` |
  | US Mountain Standard Time | -7 | `US Mountain Standard Time` |
  | Mountain Standard Time (Mexico) | -7 | `Mountain Standard Time (Mexico)` |
  | Mountain Standard Time | -7 | `Mountain Standard Time` |
  | Yukon Standard Time | -7 | `Yukon Standard Time` |
  | Central America Standard Time | -6 | `Central America Standard Time` |
  | Central Standard Time | -6 | `Central Standard Time` |
  | Easter Island Standard Time | -6 | `Easter Island Standard Time` |
  | Central Standard Time (Mexico) | -6 | `Central Standard Time (Mexico)` |
  | Canada Central Standard Time | -6 | `Canada Central Standard Time` |
  | SA Pacific Standard Time | -5 | `SA Pacific Standard Time` |
  | Eastern Standard Time (Mexico) | -5 | `Eastern Standard Time (Mexico)` |
  | Eastern Standard Time | -5 | `Eastern Standard Time` |
  | Haiti Standard Time | -5 | `Haiti Standard Time` |
  | Cuba Standard Time | -5 | `Cuba Standard Time` |
  | US Eastern Standard Time | -5 | `US Eastern Standard Time` |
  | Turks And Caicos Standard Time | -5 | `Turks And Caicos Standard Time` |
  | Paraguay Standard Time | -4 | `Paraguay Standard Time` |
  | Atlantic Standard Time | -4 | `Atlantic Standard Time` |
  | Venezuela Standard Time | -4 | `Venezuela Standard Time` |
  | Central Brazilian Standard Time | -4 | `Central Brazilian Standard Time` |
  | SA Western Standard Time | -4 | `SA Western Standard Time` |
  | Pacific SA Standard Time | -4 | `Pacific SA Standard Time` |
  | Tocantins Standard Time | -3 | `Tocantins Standard Time` |
  | E. South America Standard Time | -3 | `E. South America Standard Time` |
  | SA Eastern Standard Time | -3 | `SA Eastern Standard Time` |
  | Argentina Standard Time | -3 | `Argentina Standard Time` |
  | Greenland Standard Time | -3 | `Greenland Standard Time` |
  | Montevideo Standard Time | -3 | `Montevideo Standard Time` |
  | Magallanes Standard Time | -3 | `Magallanes Standard Time` |
  | Saint Pierre Standard Time | -3 | `Saint Pierre Standard Time` |
  | Bahia Standard Time | -3 | `Bahia Standard Time` |
  | UTC-02 | -2 | `UTC-02` |
  | Mid-Atlantic Standard Time | -2 | `Mid-Atlantic Standard Time` |
  | Azores Standard Time | -1 | `Azores Standard Time` |
  | Cape Verde Standard Time | -1 | `Cape Verde Standard Time` |
  | UTC | +0 | `UTC` |
  | GMT Standard Time | +0 | `GMT Standard Time` |
  | Greenwich Standard Time | +0 | `Greenwich Standard Time` |
  | Sao Tome Standard Time | +0 | `Sao Tome Standard Time` |
  | Morocco Standard Time | +1 | `Morocco Standard Time` |
  | W. Europe Standard Time | +1 | `W. Europe Standard Time` |
  | Central Europe Standard Time | +1 | `Central Europe Standard Time` |
  | Romance Standard Time | +1 | `Romance Standard Time` |
  | Central European Standard Time | +1 | `Central European Standard Time` |
  | W. Central Africa Standard Time | +1 | `W. Central Africa Standard Time` |
  | Jordan Standard Time | +2 | `Jordan Standard Time` |
  | GTB Standard Time | +2 | `GTB Standard Time` |
  | Middle East Standard Time | +2 | `Middle East Standard Time` |
  | Egypt Standard Time | +2 | `Egypt Standard Time` |
  | E. Europe Standard Time | +2 | `E. Europe Standard Time` |
  | Syria Standard Time | +2 | `Syria Standard Time` |
  | West Bank Standard Time | +2 | `West Bank Standard Time` |
  | South Africa Standard Time | +2 | `South Africa Standard Time` |
  | FLE Standard Time | +2 | `FLE Standard Time` |
  | Israel Standard Time | +2 | `Israel Standard Time` |
  | Kaliningrad Standard Time | +2 | `Kaliningrad Standard Time` |
  | Sudan Standard Time | +2 | `Sudan Standard Time` |
  | Libya Standard Time | +2 | `Libya Standard Time` |
  | Namibia Standard Time | +2 | `Namibia Standard Time` |
  | Arabic Standard Time | +3 | `Arabic Standard Time` |
  | Turkey Standard Time | +3 | `Turkey Standard Time` |
  | Arab Standard Time | +3 | `Arab Standard Time` |
  | Belarus Standard Time | +3 | `Belarus Standard Time` |
  | Russian Standard Time | +3 | `Russian Standard Time` |
  | E. Africa Standard Time | +3 | `E. Africa Standard Time` |
  | Iran Standard Time | +3:30 | `Iran Standard Time` |
  | Arabian Standard Time | +4 | `Arabian Standard Time` |
  | Astrakhan Standard Time | +4 | `Astrakhan Standard Time` |
  | Azerbaijan Standard Time | +4 | `Azerbaijan Standard Time` |
  | Russia Time Zone 3 | +4 | `Russia Time Zone 3` |
  | Mauritius Standard Time | +4 | `Mauritius Standard Time` |
  | Saratov Standard Time | +4 | `Saratov Standard Time` |
  | Georgian Standard Time | +4 | `Georgian Standard Time` |
  | Volgograd Standard Time | +4 | `Volgograd Standard Time` |
  | Caucasus Standard Time | +4 | `Caucasus Standard Time` |
  | Afghanistan Standard Time | +4:30 | `Afghanistan Standard Time` |
  | West Asia Standard Time | +5 | `West Asia Standard Time` |
  | Ekaterinburg Standard Time | +5 | `Ekaterinburg Standard Time` |
  | Pakistan Standard Time | +5 | `Pakistan Standard Time` |
  | Qyzylorda Standard Time | +5 | `Qyzylorda Standard Time` |
  | India Standard Time | +5:30 | `India Standard Time` |
  | Sri Lanka Standard Time | +5:30 | `Sri Lanka Standard Time` |
  | Nepal Standard Time | +5:45 | `Nepal Standard Time` |
  | Central Asia Standard Time | +6 | `Central Asia Standard Time` |
  | Bangladesh Standard Time | +6 | `Bangladesh Standard Time` |
  | Omsk Standard Time | +6 | `Omsk Standard Time` |
  | Myanmar Standard Time | +6:30 | `Myanmar Standard Time` |
  | SE Asia Standard Time | +7 | `SE Asia Standard Time` |
  | Altai Standard Time | +7 | `Altai Standard Time` |
  | W. Mongolia Standard Time | +7 | `W. Mongolia Standard Time` |
  | North Asia Standard Time | +7 | `North Asia Standard Time` |
  | N. Central Asia Standard Time | +7 | `N. Central Asia Standard Time` |
  | Tomsk Standard Time | +7 | `Tomsk Standard Time` |
  | China Standard Time | +8 | `China Standard Time` |
  | North Asia East Standard Time | +8 | `North Asia East Standard Time` |
  | Singapore Standard Time | +8 | `Singapore Standard Time` |
  | W. Australia Standard Time | +8 | `W. Australia Standard Time` |
  | Taipei Standard Time | +8 | `Taipei Standard Time` |
  | Ulaanbaatar Standard Time | +8 | `Ulaanbaatar Standard Time` |
  | Aus Central W. Standard Time | +8:45 | `Aus Central W. Standard Time` |
  | Transbaikal Standard Time | +9 | `Transbaikal Standard Time` |
  | Tokyo Standard Time | +9 | `Tokyo Standard Time` |
  | North Korea Standard Time | +9 | `North Korea Standard Time` |
  | Korea Standard Time | +9 | `Korea Standard Time` |
  | Yakutsk Standard Time | +9 | `Yakutsk Standard Time` |
  | Cen. Australia Standard Time | +9:30 | `Cen. Australia Standard Time` |
  | AUS Central Standard Time | +9:30 | `AUS Central Standard Time` |
  | E. Australia Standard Time | +10 | `E. Australia Standard Time` |
  | AUS Eastern Standard Time | +10 | `AUS Eastern Standard Time` |
  | West Pacific Standard Time | +10 | `West Pacific Standard Time` |
  | Tasmania Standard Time | +10 | `Tasmania Standard Time` |
  | Vladivostok Standard Time | +10 | `Vladivostok Standard Time` |
  | Lord Howe Standard Time | +10:30 | `Lord Howe Standard Time` |
  | Bougainville Standard Time | +11 | `Bougainville Standard Time` |
  | Russia Time Zone 10 | +11 | `Russia Time Zone 10` |
  | Magadan Standard Time | +11 | `Magadan Standard Time` |
  | Norfolk Standard Time | +11 | `Norfolk Standard Time` |
  | Sakhalin Standard Time | +11 | `Sakhalin Standard Time` |
  | Central Pacific Standard Time | +11 | `Central Pacific Standard Time` |
  | Russia Time Zone 11 | +12 | `Russia Time Zone 11` |
  | New Zealand Standard Time | +12 | `New Zealand Standard Time` |
  | UTC+12 | +12 | `UTC+12` |
  | Fiji Standard Time | +12 | `Fiji Standard Time` |
  | Kamchatka Standard Time | +12 | `Kamchatka Standard Time` |
  | Chatham Islands Standard Time | +12:45 | `Chatham Islands Standard Time` |
  | UTC+13 | +13 | `UTC+13` |
  | Tonga Standard Time | +13 | `Tonga Standard Time` |
  | Samoa Standard Time | +13 | `Samoa Standard Time` |
  | Line Islands Standard Time | +14 | `Line Islands Standard Time` |

</details>

---

### 4. Force Kill Task

A smart, context-aware window closer that gracefully exits healthy programs and ruthlessly terminates frozen ones.

**Hotkey:** `Win + Ctrl + K`

- Closes the active window
- If the window is frozen or unresponsive, it force‑kills the process.
- A tooltip appears confirming the action.

---

### 5. Color Picker

A developer-centric, floating live color picker that captures screen pixels, translates them into Hex and RGB, and copies them to your clipboard.

**Hotkey:** `Win + Ctrl + C`

- Press once to open a live color picker that follows your mouse.
- Press again to close the picker and instantly copy the color (Hex, RGB, and screen coordinates) to the clipboard.
- By default, a tooltip confirms the copy. You can optionally enable a summary Message Box.

---

### 6. Line Navigation

Translates modern text-editor navigation shortcuts into standard Windows keystrokes, allowing for rapid text manipulation without reaching for the physical `Home` or `End` keys.

**Hotkeys:**

| Action | Shortcut |
| --- | --- |
| Move cursor to start of line | `Shift + Alt + Left` |
| Move cursor to end of line | `Shift + Alt + Right` |
| Select to start of line | `Shift + Win + Left` |
| Select to end of line | `Shift + Win + Right` |
| Delete from cursor to start of line | `Alt + Backspace` |
| Delete from cursor to end of line | `Alt + Delete` |

---

### Startup Shortcut

Controls whether Strap auto-launches on Windows login via a shortcut in the Windows Startup folder.

```bash
/run --cr shr               # Create startup shortcut (enables auto-boot on login)
/run --d shr                # Delete startup shortcut (disables auto-boot)
```

---

## Strap's CLI/TUI

- Run `strap` in your terminal to launch the TUI, a lightweight terminal interface for managing everything in Strap. From here you can run and stop the AHK scripts, configure features, manage profiles, install and switch between versions, and handle startup behavior, all without touching a config file directly.
- You can use all these commands directly inside your terminal with the prefix `strap`.

> [!TIP]
> Wondering what else you can do? [REFERENCE.md](REFERENCE.md) covers every command and how the TUI works.

```bash
strap /help, /?                     # Show all available strap commands

strap /run                          # Runs AHK scripts
strap /stop                         # Stops AHK scripts
strap /run --cr shr                 # Enable auto-boot (creates a startup shortcut)
strap /run --d shr                  # Disable auto-boot (removes from startup)

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
```

---

### Profiles

- Profiles store your config separately so you can switch between different setups without losing settings.
- When you switch versions, all profiles are automatically updated new config keys are added at their defaults, and unknown keys from older versions are left alone.

Three profile types:

| Type | Behavior |
| --- | --- |
| `default` | Always full defaults. Read-only resets on every version switch. |
| `ghost` | Auto-created on your first config change if no named profile is active. |
| named | User-created. And it persists across version switches. |

```bash
/profile --ls                       # List all profiles
/profile --cr name                  # Create a new profile
/profile --use name                 # Switch active profile
/profile --d name                   # Delete a profile
```

---

### Management

Installed versions are archived locally and never modified. You can install multiple versions and switch between them without re-downloading.

```bash
/install --ls                       # List available versions on GitHub
/install vX.X.X                     # Download and install a specific version
/update                             # Check for and download the latest version

/switch vX.X.X                      # Switch to a locally installed version
/version                            # Show current active version
/version --ls                       # List locally installed versions
```

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

Type any command into the `>>` prompt.

**Left panel:**

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

---

### Config Screen

- `/config` opens the config screen.
- Features are listed with flag tags (`z`, `y`, `u`) that identify what type of setting they are.

| Flag | Type |
| --- | --- |
| `u` | General utility settings |
| `z` | Feature toggle (enable / disable) |
| `y` | Feature toggle + sub-settings |

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

#### 1. Configure settings with -u {flag}

```bash
/config -u -1 value                 # Tray icon (visible | hidden)

/config -u -2 time                  # Tooltip timeout in ms

/config -u -3 UTC_No.               # Toggle a timezone in the switcher cycle
/config -u -3 --TZ_No. UTC_No.      # Toggle by TZ slot number

/config -u -4 UTC_No.               # Set startup timezone (same value again = reset)
/config -u -4 --TZ_No. UTC_No.      # Set startup TZ by slot number
```

#### 2. Configure settings with -z {flag}

> [!TIP]
> Use commands in the format `strap /config -!z -2 --!` to quickly change that setting. (Works with any flag)

```bash
/config -z -1 value                 # Numpad Emulator
/config -z -2 value                 # ALT Codes
/config -z -3 value                 # Timezone Switcher
/config -z -4 value                 # Force Kill
/config -z -5 value                 # Color Picker
/config -z -6 value                 # Line Navigation
```

#### 3. Configure settings with -y {flag}

```bash
/config -y -1--1 text               # Force Kill set tooltip text
/config -y -2--1 value              # Color Picker msgbox toggle (enable | disable)
/config -y -2--2 text               # Color Picker set tooltip text
```

---

## Contributing

Contributors are always welcome!

Bug fixes, new features, improvements to the CLI/TUI, whatever you've got. And remember, don't worry if you're not sure about something, or feel your changes aren't perfect. No changes ever are. open the PR anyway and we'll figure it out together!

> Check out [CONTRIBUTING.md](CONTRIBUTING.md) for the full development pipeline.

**Quick start:**

1. Fork the repo and clone your fork
2. Create a feature branch off `dev`
3. Write and test your AHK script
4. Integrate the feature into the CLI/TUI and test it
5. Open a PR against `dev` (**not `main`**).

> [!TIP]
> Want to understand the codebase first? Try checking out [REFERENCE.md](REFERENCE.md). It breaks down how every part of the codebase works, from the AHK core to the CLI/TUI internals.

---

## Troubleshooting

- **Numpad keys aren't working**: Make sure CapsLock is ON. If it still doesn't work, try reloading the script through the tray icon.
- **Timezone isn't switching**: Go to **Settings > Time & Language > Date & Time** and make sure **"Set time zone automatically"** is turned off.
- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**.

> **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

---

## LICENSE

This [Project](https://github.com/H-int0/autohotkey-v2-scripts) is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) - see the [LICENSE](LICENSE) for more details.

Copyright (C) 2026 [H-int0](https://github.com/H-int0)

---

~*[@H-int0](https://github.com/H-int0)*
