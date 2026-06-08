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
  | **Install/Update/Uninstall** | Control all of them from TUI |

> [!NOTE]
> Strap is still in active development. The AHK scripts are stable, but the CLI may behave unexpectedly.
> Don't worry it won't NUKE your system. But if something breaks, see [RECOVERY.md](RECOVERY.md) for safe removal instructions.

---

<!-- markdownlint-disable-next-line -->
### Houston, we have problems!!!

Something ain't working? [open a bug report](https://github.com/H-int0/autohotkey-v2-scripts/issues/new?template=bug_report.md) and we'll look forward into it.

---

### Got a big brain idea?

If you have an idea for something new, adding new features or think an existing feature could be better, [open a feature request](https://github.com/H-int0/autohotkey-v2-scripts/issues/new?template=feature_request.md).

> [!TIP]
> Wondering what else you can do? [REFERENCE.md](REFERENCE.md) covers every command and how the TUI works.

---

## Perquisite

### OS Supported

- [Windows 7](https://www.microsoft.com/en-us/download/details.aspx?id=53332)*
- [Windows 8](https://www.microsoft.com/en-us/download/details.aspx?id=40745)*
- [Windows 10](https://www.microsoft.com/en-us/software-download/windows10)
- [Windows 11](https://www.microsoft.com/en-us/software-download/windows11)

### Requirements

- [AutoHotkey v2.0](https://www.autohotkey.com/)

  ```bat
  winget install -e --id AutoHotkey.AutoHotkey
  ```

- [Python3](https://www.python.org/downloads/)

  ```bat
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

- With **Zip**:

  ```bash
  # Replace with your file path
  cd C:\path_to_strap\autohotkey-v2-scripts-main

  # use this to hook up the CLI/TUI:
  python cli/main.py /install
  ```

> [!TIP]
> Prefer the ZIP version? Simply extract the ZIP file, open the setup folder, and double-click `install.bat` to set up Strap Automatically.

---

## After Installation

```bash
# verify installation (launches the TUI):
strap

# Try running AHK scripts
strap /run
```

> Try pressing `win + /` to see all the hotkeys.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Repo Structure](#repo-structure)
- [Features](#features)
- [Strap's CLI/TUI](#straps-clitui)
- [Contributing](#contributing)
- [LICENSE](#license)

> See [CHANGELOG.md](CHANGELOG.md) for the history of versions.

---

## Getting Started

Check all the Hotkeys and Commands here:

<details>
  <summary> Full Hotkeys </summary>

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

</details>

<br>

<details>
  <summary> Full Commands </summary>

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

</details>

---

### Repo Structure

<details>
  <summary></summary>

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

</details>

---

## Features

> [!TIP]
> Curious what's going on behind the scenes? Or, Wondering what's actually happening when you press that hotkey? Make sure to checkout [REFERENCE.md](REFERENCE.md).

### 1. Numpad Emulator

<details>
  <summary></summary>

A hardware-level numpad substitute for Ten-key-less (TKL), 60%, and laptop keyboards, mapping the standard number row to actual Numpad keycodes.

**Hotkeys:**

- **Toggle:** `CapsLock`
- **Use:** Toggles number row keys between normal mode and Numpad mode with `Caps Lock` state **off** and **on** respectively.

</details>

---

### 2. ALT Codes

<details>
  <summary></summary>

Type Alt codes directly from your number row. (Try pressing `ALT + 9825` for a `♡`)

</details>

---

### 3. Timezone Switcher

<details>
  <summary></summary>

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

<details>
  <summary>Supported Timezones:</summary>

  | Label | UTC Offset | Windows ID |
  | --- | --- | --- |
  | Dateline Standard Time | -12 | `Dateline Standard Time` |
  | UTC-11 | -11 | `UTC-11` |
  | Hawaiian Standard Time | -10 | `Hawaiian Standard Time` |
  | Marquesas Standard Time | -9:30 | `Marquesas Standard Time` |
  | Alaskan Standard Time | -9 | `Alaskan Standard Time` |
  | Pacific Standard Time | -8 | `Pacific Standard Time` |
  | US Mountain Standard Time | -7 | `US Mountain Standard Time` |
  | Central Standard Time | -6 | `Central Standard Time` |
  | Eastern Standard Time | -5 | `Eastern Standard Time` |
  | Atlantic Standard Time | -4 | `Atlantic Standard Time` |
  | Venezuela Standard Time | -4 | `Venezuela Standard Time` |
  | E. South America Standard Time | -3 | `E. South America Standard Time` |
  | Argentina Standard Time | -3 | `Argentina Standard Time` |
  | UTC-02 | -2 | `UTC-02` |
  | Azores Standard Time | -1 | `Azores Standard Time` |
  | GMT Standard Time | +0 | `GMT Standard Time` |
  | W. Europe Standard Time | +1 | `W. Europe Standard Time` |
  | Israel Standard Time | +2 | `Israel Standard Time` |
  | Russian Standard Time | +3 | `Russian Standard Time` |
  | Iran Standard Time | +3:30 | `Iran Standard Time` |
  | Arabian Standard Time | +4 | `Arabian Standard Time` |
  | Afghanistan Standard Time | +4:30 | `Afghanistan Standard Time` |
  | Pakistan Standard Time | +5 | `Pakistan Standard Time` |
  | India Standard Time | +5:30 | `India Standard Time` |
  | Nepal Standard Time | +5:45 | `Nepal Standard Time` |
  | Central Asia Standard Time | +6 | `Central Asia Standard Time` |
  | Myanmar Standard Time | +6:30 | `Myanmar Standard Time` |
  | SE Asia Standard Time | +7 | `SE Asia Standard Time` |
  | China Standard Time | +8 | `China Standard Time` |
  | Tokyo Standard Time | +9 | `Tokyo Standard Time` |
  | Cen. Australia Standard Time | +9:30 | `Cen. Australia Standard Time` |
  | AUS Eastern Standard Time | +10 | `AUS Eastern Standard Time` |
  | Central Pacific Standard Time | +11 | `Central Pacific Standard Time` |
  | New Zealand Standard Time | +12 | `New Zealand Standard Time` |
  | Tonga Standard Time | +13 | `Tonga Standard Time` |
  | Line Islands Standard Time | +14 | `Line Islands Standard Time` |

</details>

</details>

---

### 4. Force Kill Task

<details>
  <summary></summary>

A smart, context-aware window closer that gracefully exits healthy programs and ruthlessly terminates frozen ones.

**Hotkey:** `Win + Ctrl + K`

- Closes the active window
- If the window is frozen or unresponsive, it force‑kills the process.
- A tooltip appears confirming the action.

</details>

---

### 5. Color Picker

<details>
  <summary></summary>

A developer-centric, floating live color picker that captures screen pixels, translates them into Hex and RGB, and copies them to your clipboard.

**Hotkey:** `Win + Ctrl + C`

- Press once to open a live color picker that follows your mouse.
- Press again to close the picker and instantly copy the color (Hex, RGB, and screen coordinates) to the clipboard.
- By default, a tooltip confirms the copy. You can optionally enable a summary Message Box.

</details>

---

### 6. Line Navigation

<details>
  <summary></summary>

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

</details>

---

## Strap's CLI/TUI

Run `strap` in your terminal to launch the TUI, a lightweight terminal interface for managing everything in Strap. From here you can run and stop the AHK scripts, configure features, manage profiles, install and switch between versions, and handle startup behavior, all without touching a config file directly.

> [!NOTE]
> All commands work in both the TUI and terminal. In the terminal, always prefix commands with `strap`. Inside the TUI, the prefix is optional.

<!-- markdownlint-disable-next-line -->

> [!TIP]
> Chain commands with `^`. Example: `/run ^ /config`

<details>
  <summary>Commands</summary>

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

</details>

---

### Profiles

<details>
  <summary></summary>

Profiles store your config separately so you can switch between different setups without losing settings.

When you switch versions, all profiles are automatically updated new config keys are added at their defaults, and unknown keys from older versions are left alone.

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

</details>

---

### Management

<details>
  <summary></summary>

Installed versions are archived locally and never modified. You can install multiple versions and switch between them without re-downloading.

```bash
/install --ls                       # List available versions on GitHub
/install vX.X.X                     # Download and install a specific version
/update                             # Check for and download the latest version

/switch vX.X.X                      # Switch to a locally installed version
/version                            # Show current active version
/version --ls                       # List locally installed versions
```

</details>

---

### Layout

<details>
  <summary></summary>

The TUI has two screens.

- **Home screen:**
  - the default screen on launch. Has a command prompt (`>>`) on the right and a status/help panel on the left. The right side outputs command results into a scrollable log.
  - The left panel shows your current status and available commands, and updates its hints contextually as the user type.
- **Config screen:**
  - opened via `/config`. Has the same left panel layout (status + contextual hints) but the right side is replaced by an interactive settings list instead of a log.
  - Changes are staged as pending and only written to disk when user explicitly save.

</details>

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

<details>
  <summary>Config Commands Structure</summary>

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

</details>

<br>
  
---

<details>
  <summary>Configure settings with -u {flag}</summary>

```bash
/config -u -1 value                 # Tray icon (visible | hidden)
/config -u -2 time                  # Tooltip timeout in ms
/config -u -3 "UTC_+/-No."          # Toggle a timezone in the switcher cycle
/config -u -3 "UTC_+/-No."          # Set startup timezone (same value again = reset)
```

</details>

<details>
<summary>Configure settings with -z {flag}</summary>

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

</details>

<details>
<summary>Configure settings with -y {flag}</summary>

```bash
/config -y -1--1 text               # Force Kill set tooltip text
/config -y -2--1 value              # Color Picker msgbox toggle (enable | disable)
/config -y -2--2 text               # Color Picker set tooltip text
```

</details>

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

<details>
  <summary>Troubleshooting</summary>

- **Numpad keys aren't working**: Make sure CapsLock is ON. If it still doesn't work, try reloading the script through the tray icon.
- **Timezone isn't switching**: Go to **Settings > Time & Language > Date & Time** and make sure **"Set time zone automatically"** is turned off.
- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**.

> **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

</details>

---

## LICENSE

This [Project](https://github.com/H-int0/autohotkey-v2-scripts) is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) - see the [LICENSE](LICENSE) for more details.

Copyright (C) 2026 [H-int0](https://github.com/H-int0)

---

~*[@H-int0](https://github.com/H-int0)*
