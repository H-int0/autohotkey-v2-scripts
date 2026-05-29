# Strap

Strap is a lightweight AutoHotkey_v2 script for Windows that adds keyboard shortcuts to devices that lack certain physical keys or need quick access to system-level features.

Currently, it ships with five features:

- CapsLock-based Num-pad Emulator
- Timezone switcher
- Force Kill Task
- Color Picker
- Line Navigation

With more planned for the future.

---

- See [CHANGELOG.md](CHANGELOG.md) for the history of releases.
- See [RECOVERY.md](RECOVERY.md) to safely remove the script.

---

## Table of Contents

- [Installation](#installation)
- [Running the Script](#running-the-script)
- [Auto-Start on Boot](#auto-start-on-boot)
- [Updating the Script](#updating-the-script)
- [All Hotkeys](#all-hotkeys)
- [Utilities](#utilities)
  - [Tray Icon Toggle](#tray-icon-toggle)
  - [Reloading the Script](#reloading-the-script)
  - [Existing Script](#existing-script)
  - [Help Box](#help-box)
- [Features](#features)
  - [1. Numpad Emulator](#1-numpad-emulator)
  - [2. Timezone Switcher](#2-timezone-switcher)
  - [3. Force Kill Task](#3-force-kill-task)
  - [4. Color Picker](#4-color-picker)
  - [5. Line Navigation](#5-line-navigation)
- [Modules](#modules)
- [Script Structure and Configuration](#script-structure-and-configuration)
- [Configuration Guide](#configuration-guide)
- [Removing the Startup Shortcut](#removing-the-startup-shortcut)
- [Troubleshooting](#troubleshooting)
- [LICENSE](#license)

---

## Structure

```bash
\
|   CHANGELOG.md
|   CONFIGURE.md
|   CONTRIBUTING.md
|   FEATURES.md
|   INTEGRATION_GUIDE.md
|   LICENSE
|   README.md
|   RECOVERY.md
|
+---.github
|   \---ISSUE_TEMPLATE
|           bug_report.md
|           feature_request.md
|
+---distribution
|   |   source.ahk
|   |
|   \---source-dependencies
|           config.ahk
|           source-color-picker.ahk
|           source-force-kill-task.ahk
|           source-line-navigation.ahk
|           source-numpad-emulator.ahk
|           source-timezone-switcher.ahk
|
\---modules
        color-picker.ahk
        force-kill-task.ahk
        line-navigation.ahk
        numpad-emulator.ahk
        timezone-switcher.ahk
```

---

## OS Supported

- Windows 7*
- Windows 8*
- Windows 10
- Windows 11*

---

## Requirements

- [AutoHotkey v2.0](https://www.autohotkey.com/) installed

---

## Installation

### Option A: Clone the repository

```cmd
git clone https://github.com/H-int0/autohotkey-v2-scripts.git
```

### Option B: Download as ZIP

1. Go to [github.com/H-int0/AutoHotkey-v2-scripts.git](https://github.com/H-int0/autohotkey-v2-scripts.git)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the folder somewhere on your device

---

## Running the Script

To run Strap, simply double-click `distribution/source.ahk`.

A tray icon will briefly appear in the right bottom corner of your taskbar and then hide itself. That means it's running. You won't see any window or confirmation.

To stop it, make the tray icon visible first with `Win + Ctrl + \`, then right-click it and select **Exit**.

---

## Auto-Start on Boot

> By default, you need to manually run the script every time your computer restarts.

**To make Strap launch automatically on startup:**

### Option A: Command Prompt

1. Open Command Prompt and run the following,
2. Replacing `YOUR_PATH` with the full path to the root of your local fork of the repository. (e.g., `C:\Users\Layer\Desktop\autohotkey-v2-scripts-main`)

```cmd
cd YOUR_PATH
```

```cmd
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Strap.lnk'); $Shortcut.TargetPath = '%CD%\distribution\source.ahk'; $Shortcut.WorkingDirectory = '%CD%\distribution'; $Shortcut.Save()"
```

### Option B: Manual

1. Navigate to the `distribution` folder inside your local Strap repository.
2. Right-click `source.ahk` and select **Create shortcut**.
3. Copy or cut the newly created shortcut file (it will be named something like `source.ahk - Shortcut`).
4. Press `Win + R`, type `shell:startup`, and press Enter to open the Windows Startup folder.
5. Paste the shortcut file directly into that folder.
6. *(Optional, recommended for consistency)* Rename the shortcut file to **Strap**.

---

## Updating the Script

- Since, Strap runs via a native Windows shortcut pointing directly to your local repository, **no manual updates are required.**
- Whenever you pull updates from Git or modify your local `config.ahk`or `source.ahk`, your changes are instantly active the next time the script loads.

## Removing the Startup Shortcut

If you no longer want Strap to launch on startup:

### Option A: Command prompt

1. Open **Command Prompt** (any folder context is fine).
2. Paste and run the following command:

```cmd
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Strap.lnk"
```

> [!NOTE]
> If you have named the shortcut to something other than `Strap.lnk` make sure to replace that in the command above.

### Option_B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Locate the shortcut named Strap (it may just look like a standard application link).
3. Right-click it and select Delete.

---

## Modules

The `modules/` folder contains each feature as a standalone script that you can run directly

| File | What it does |
| --- | --- |
| `modules/numpad-emulator.ahk` | Remaps the Number Row keys To Num-pad keys |
| `modules/timezone-switcher.ahk` | Timezone switcher |
| `modules/force-kill-task.ahk` | Ends task of the active Window |
| `modules/color-picker.ahk` | Opens a floating Color Picker |
| `modules/line-navigation.ahk` | Navigate through the line |

- Run any module the same way as `distribution/source.ahk` just double‑click the file.
- Each module includes the same tray icon toggle (`Win + Ctrl + \`) so you can exit it easily.
- **Do not run a module at the same time as `distribution/source.ahk`** they share hotkeys and will conflict.

---

## All Hotkeys

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
  | `CapsLock` | Toggle Numpad Emulator |
  | `0` - `9` | Type Numpad digits *(with CapsLock ON)* |
  | `Shift` + `0` - `9` | Type standard symbols *(with CapsLock ON)* |
  | `Win + Alt + `` ` | Switch to next timezone |
  | `Win + Ctrl + `` ` | Show current timezone |
  | `Win + Ctrl + K` | Force kill active task |
  | `Win + Ctrl + C` | Toggle Color Picker |
  | `Shift + Alt + Left / Right` | Move cursor to start/end of line |
  | `Shift + Win + Left / Right` | Select text to start/end of line |
  | `Alt + Backspace / Delete` | Delete text to start/end of line |

---

## Utilities

### Tray Icon Toggle

**Hotkey:** `Win + Ctrl + \`

- The AHK tray icon is hidden by default to keep your system tray clean.
- Press `Win + Ctrl + \` to show or hide it at any time.

When visible, right‑clicking it lets you reload or exit the script.

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#3-tray-icon-toggle).

---

### Reloading the Script

To reload your script, use the **Hotkey:** `Win+Ctrl+/`

---

### Existing Script

To Exit your script, use the **Hotkey:** `Win+Shift+/`

---

### Help Box

A lightweight, semi-transparent help box that follows your mouse and lists your active shortcuts.

**Hotkey:** `Win + /`

- Toggles a small, always‑on‑top window that lists **all active hotkeys** for the running script.
- The window follows your cursor and is slightly transparent, so it doesn’t get in the way.
- The help box automatically shows the shortcuts for only the features you included.

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#1-dynamic-help-box).

---

## Features

### 1. Numpad Emulator

A hardware-level numpad substitute for Ten-key-less (TKL), 60%, and laptop keyboards, mapping the standard number row to actual Numpad keycodes.

**Hotkeys:**

- **Toggle:** `CapsLock`
- **Use:** `0-9` on the number row
- **Shift Behavior:** `Shift + 0-9` (Configurable)

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#1-numpad-emulator).

---

### 2. Timezone Switcher

A system-level utility to instantly cycle your Windows clock between different global timezones without navigating through the Windows Settings app.

**Hotkeys:**

- `Win + Alt + `` ` switch to the next timezone in your list.
- `Win + Ctrl + `` ` show the current timezone.

Each time you cycle, a small tooltip appears near your cursor showing the new timezone.

- Changes are applied instantly and saved to Windows Settings.
- Your preferences persist through restarts.

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#2-timezone-switcher).

---

> [!NOTE]
> If switching does not work, go to **Settings > Time & Language > Date & Time** and turn off **Set time zone automatically**.

---

## Active by Default

Out of the box, Strap cycles through these six timezones:

| Label | UTC Offset |
| --- | --- |
| Berlin / Paris | +1 |
| Moscow | +3 |
| Tokyo | +9 |
| Sydney | +10 |
| Eastern Time | -5 |

---

## Available Timezones

| Label | UTC Offset | Windows ID |
| --- | --- | --- |
| UTC | +0 | `UTC` |
| London | +0 | `GMT Standard Time` |
| Berlin / Paris | +1 | `W. Europe Standard Time` |
| Cairo | +2 | `Egypt Standard Time` |
| Riyadh | +3 | `Arab Standard Time` |
| Moscow | +3 | `Russian Standard Time` |
| Tehran | +3:30 | `Iran Standard Time` |
| Dubai | +4 | `Arabian Standard Time` |
| Kabul | +4:30 | `Afghanistan Standard Time` |
| Karachi | +5 | `Pakistan Standard Time` |
| India | +5:30 | `India Standard Time` |
| Dhaka | +6 | `Bangladesh Standard Time` |
| Bangkok / Jakarta | +7 | `SE Asia Standard Time` |
| Beijing | +8 | `China Standard Time` |
| Singapore | +8 | `Singapore Standard Time` |
| Tokyo | +9 | `Tokyo Standard Time` |
| Sydney | +10 | `AUS Eastern Standard Time` |
| Auckland | +12 | `New Zealand Standard Time` |
| Azores | -1 | `Azores Standard Time` |
| Cape Verde | -1 | `Cape Verde Standard Time` |
| Buenos Aires | -3 | `SA Eastern Standard Time` |
| Brasilia | -3 | `E. South America Standard Time` |
| Caracas | -4 | `Venezuela Standard Time` |
| La Paz | -4 | `SA Western Standard Time` |
| Eastern Time | -5 | `Eastern Standard Time` |
| Central Time | -6 | `Central Standard Time` |
| Mountain Time | -7 | `Mountain Standard Time` |
| Pacific Time | -8 | `Pacific Standard Time` |
| Alaska | -9 | `Alaskan Standard Time` |
| Hawaii | -10 | `Hawaiian Standard Time` |

---

### 3. Force Kill Task

A smart, context-aware window closer that gracefully exits healthy programs and ruthlessly terminates frozen ones.

**Hotkey:** `Win + Ctrl + K`

- Closes the active window
- If the window is frozen or unresponsive, it force‑kills the process.
- A tooltip appears confirming the action.

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#3-force-kill-task).

---

### 4. Color Picker

A developer-centric, floating live color picker that captures screen pixels, translates them into Hex and RGB, and copies them to your clipboard.

**Hotkey:** `Win + Ctrl + C`

- Press once to open a live color picker that follows your mouse.
- Press again to close the picker and instantly copy the color (Hex, RGB, and screen coordinates) to the clipboard.
- By default, a tooltip confirms the copy. You can optionally enable a summary Message Box.

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#4-color-picker).

---

### 5. Line Navigation

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

> To know more about this feature, checkout [FEATURES.md](FEATURES.md#5-line-navigation).

---

## Script Structure and Configuration

The `distribution/` folder contains everything you need to run or customize Strap.

### Configuration Guide

Refer to [CONFIGURE.md](CONFIGURE.md) for detailed step-by-step instructions on:

- Inside `source.ahk`
  - [Enabling and Disabling Features](CONFIGURE.md#enabling-and-disabling-features)
- Inside `config.ahk`
  - [Changing the Default Tray Icon Visibility](CONFIGURE.md#changing-the-default-tray-icon-visibility)
  - [Customizing Tooltips](CONFIGURE.md#customizing-tooltips)
  - [Changing CapsLock Numpad Shift Behavior](CONFIGURE.md#changing-capslock-numpad-shift-behavior)
  - [Configuring the Color Picker Summary MsgBox](CONFIGURE.md#configuring-the-color-picker-summary-msgbox)
  - [Adding a Timezone Not in the List](CONFIGURE.md#adding-a-timezone-not-in-the-list)
  - [Setting a Startup Timezone](CONFIGURE.md#setting-a-startup-timezone)
  - [Adding a Custom Timezone to Startup (not in the list)](CONFIGURE.md#adding-a-custom-timezone-to-startup-not-in-the-list)

### 1. `config.ahk` central configuration file

**Edit this file to customize Strap** you never need to touch the feature files themselves.

### 2. `source.ahk` main script

- Double‑click this to run Strap. It automatically includes `config.ahk` and every file inside `source-dependencies/`.
- From `source.ahk` you can **[Enable/disable any feature](CONFIGURE.md#enabling-and-disabling-features)** entirely

> See [CONFIGURE.md](CONFIGURE.md#enabling-and-disabling-features), for exact steps.

### 3. `source-dependencies/` feature code

Each `source-dependencies-*.ahk` file implements one feature. They rely on the global helpers and settings defined in `source.ahk` and `config.ahk`.  

> [!NOTE]
> You normally **should NOT edit these files**, use `config.ahk` instead.

---

## Troubleshooting

- **Numpad keys aren't working**: Make sure CapsLock is ON. If it still doesn't work, try reloading the script through the tray icon.
- **Timezone isn't switching**: Go to **Settings > Time & Language > Date & Time** and make sure **"Set time zone automatically"** is turned off.
- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**.

> **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

---

## LICENSE

This [project](https://github.com/H-int0/autohotkey-v2-scripts) is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) - see the [LICENSE](LICENSE) file for more details.

Copyright (C) 2026 [H-int0](https://github.com/H-int0)

---

~*[@H-int0](https://github.com/H-int0)*
