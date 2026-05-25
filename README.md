# Strap

Strap is a lightweight AutoHotkey_v2 script for Windows that adds keyboard shortcuts to devices that lack certain physical keys or need quick access to system-level features.

Currently, it ships with two features:

- A CapsLock-based numpad emulator.
- And a timezone switcher.

With more planned for the future.

---

- See [CHANGELOG.md](CHANGELOG.md) for the history of releases.
- See [RECOVERY.md](RECOVERY.md) to safely remove the script.

---

## Table of Contents

- [Installation](#installation)
- [Running the Script](#running-the-script)
- [Features](#features)
  - [Accessibility: Tray Icon Toggle](#accessibility-tray-icon-toggle)
  - [1. numpad Emulator](#1-numpad-emulator)
  - [2. Timezone Switcher](#2-timezone-switcher)
- [Modules](#modules)
- [Configuration](#configuration)
- [Building a Custom Script](#building-a-custom-script)
- [Auto-Start on Boot](#auto-start-on-boot)
- [Updating the Startup Copy](#updating-the-startup-copy)
- [Removing the Startup Copy](#removing-the-startup-copy)
- [Troubleshooting](#troubleshooting)

---

## Structure

```bash
\
|   .gitignore
|   CHANGELOG.md
|   CONFIGURE.md
|   README.md
|   RECOVERY.md
|
+---distribution
|       source.ahk                    # Combined script (both features)
|       custom.ahk                    # Template for building your own combination
|
\---modules
        numpad-emulator.ahk
        timezone-switcher.ahk
```

## OS Supported

- Windows 7
- Windows 8
- Windows 10
- Windows 11

---

## Requirements

- [AutoHotkey v2.0](https://www.autohotkey.com/) installed

---

## Installation

### Option A: Clone the repository

Open Command Prompt and run:

```cmd
git clone https://github.com/H-int0/autohotkey-scripts-bundle.git
```

### Option B: Download as ZIP

1. Go to [github.com/H-int0/AutoHotkey-scripts-bundle](https://github.com/H-int0/autohotkey-scripts-bundle)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the folder somewhere on your device

> Once you have the files, double-click `distribution/source.ahk` to run the script.

---

## Running the Script

To run Strap, simply double-click `distribution/source.ahk`.

A tray icon will briefly appear in the right bottom corner of your taskbar and then hide itself. That means it's running. You won't see any window or confirmation.

To stop it, make the tray icon visible first with `Win + Ctrl + \`, then right-click it and select **Exit**.

---

## Modules

The `modules/` folder contains each feature as a standalone script that you can run directly, or whose code you can copy into `distribution/custom.ahk` to build your own personalized combination.

| File | What it does |
| --- | --- |
| `modules/numpad-emulator.ahk` | CapsLock numpad emulator |
| `modules/timezone-switcher.ahk` | Timezone switcher with tooltip |

- Run any module the same way as `distribution/source.ahk` just double‑click the file.
- Each module includes the same tray icon toggle (`Win + Ctrl + \`) so you can exit it easily.
- **Do not run a module at the same time as `distribution/source.ahk`** they share hotkeys and will conflict.

> See [Building a Custom Script](CONFIGURE.md#building-a-custom-script) to learn how to combine modules into your own `custom.ahk`.

---

## Features

### Accessibility: Tray Icon Toggle

**Hotkey:** `Win + Ctrl + \`

- The tray icon is hidden by default to keep your system tray clean.
- Press `Win + Ctrl + \` to show or hide it at any time.

When visible, right‑clicking it lets you reload or exit the script.

> To change the default tray icon visibility, see [CONFIGURE.md](CONFIGURE.md#changing-the-default-tray-icon-visibility).

---

### 1. numpad Emulator

Behavior:

- When CapsLock is **enabled**:
  - Number row keys `0-9` behave like numpad keys.
  - Holding Shift keeps the normal shifted symbols: `! @ # $ % ^ & * ( )`.
- When CapsLock is **disabled**:
  - Number row keys behave normally.

> To change the Shift behavior, see [CONFIGURE.md](CONFIGURE.md#changing-capslock-numpad-shift-behavior).

---

### 2. Timezone Switcher

**Hotkeys:**

- `Win + Alt + `` ` switch to the next timezone in your list.
- `Win + Ctrl + `` ` show the current timezone.

Each time you cycle, a small tooltip appears near your cursor showing the new timezone.

- Changes are applied instantly and saved to Windows Settings.
- Your preferences persist through restarts.

> Add custom timezones or set a startup timezone in [CONFIGURE.md](CONFIGURE.md#adding-a-timezone-not-in-the-list).

---

**Note:** If switching does not work, go to **Settings > Time & Language > Date & Time** and turn off **Set time zone automatically**. Windows will override manual timezone changes if that is enabled.

---

## Active by Default

Out of the box, Strap cycles through these six timezones:

| Label | UTC Offset |
| --- | --- |
| UTC | +0 |
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

## Building a Custom Script

- If you want only one feature, run its module directly.
- If you want a different combination (e.g., only numpad emulator and timezone switcher, but nothing else), you can build your own script using `distribution/custom.ahk` as a template.

> Full instructions are in [CONFIGURE.md](CONFIGURE.md#building-a-custom-script).

---

## Configuration

Refer to [CONFIGURE.md](CONFIGURE.md) for detailed steps on:

- [Changing the Default Tray Icon Visibility](CONFIGURE.md#changing-the-default-tray-icon-visibility)
- [Changing CapsLock numpad Shift Behavior](CONFIGURE.md#changing-capslock-numpad-shift-behavior)
- [Adding a Timezone Not in the List](CONFIGURE.md#adding-a-timezone-not-in-the-list)
- [Setting a Startup Timezone](CONFIGURE.md#setting-a-startup-timezone)
- [Adding a Custom Timezone to Startup](CONFIGURE.md#adding-a-custom-timezone-to-startup-not-in-the-list)
- [Building a Custom Script](CONFIGURE.md#building-a-custom-script)

---

## Auto-Start on Boot

> By default, you need to manually run the script every time your computer restarts.

If you'd rather have it launch automatically on startup, you can add a copy of it to the Windows startup folder.

**Why a copy and not a shortcut?**

- If you ever move or rename the original file, a shortcut would stop working.
- A copy in the startup folder is self-contained and always runs regardless of what happens to the original.

### Option A: Command Prompt

Open Command Prompt and run the following, replacing `YOUR_PATH` with the full path to your `distribution/source.ahk` or `distribution/custom.ahk`:

- For the combined script (`distribution/source.ahk`):

```cmd
copy "YOUR_PATH\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

- For a custom script (`distribution/custom.ahk`):

```cmd
copy "YOUR_PATH\distribution\custom.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

**Example:**

```cmd
copy "C:\Users\YourName\scripts\strap\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Copy your script (`source.ahk` or `custom.ahk`) into the folder that opens.
3. (optional) Rename it to `strap.ahk`.

---

## Updating the Startup Copy

After editing your script, the copy in the startup folder does not update automatically. You'll need to replace it manually.

### Option-A: Command Prompt

Run the following, replacing `YOUR_PATH` with the full path to your `source/source.ahk`:

- For the combined script:

```cmd
copy /Y "YOUR_PATH\distribution\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

- For a custom build:

```cmd
copy /Y "YOUR_PATH\distribution\custom.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

> The `/Y` flag overwrites without asking for confirmation.

**Example:**

```cmd
copy /Y "C:\Users\YourName\scripts\strap\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option-B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Delete the existing `strap.ahk` from the folder.
3. Copy your updated `distribution/source.ahk` (or `distribution/custom.ahk` if you are using a personalized layout) into the same folder
4. (optional) Rename it to `strap.ahk`.

---

## Removing the Startup Copy

If you no longer want Strap to launch on startup:

### Option_A: Command Prompt

```cmd
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option_B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Find `strap.ahk` in the folder and delete it.

---

## Troubleshooting

- **numpad keys aren't working**: Make sure CapsLock is ON. If it still doesn't work, try reloading the script through the tray icon.

- **Timezone isn't switching**: Go to **Settings > Time & Language > Date & Time** and make sure that **"Set time zone automatically"** is turned off. Windows will override manual timezone changes if this is enabled.

- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**. If that doesn't help, **Exit** and double-click the script again.

> **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

---

~*H-int*
