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
  - [1. Numpad Emulator](#1-numpad-emulator)
  - [2. Timezone Switcher](#2-timezone-switcher)
- [Configuration](#configuration)
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
+---source
|       source.ahk
|
\---standalone-scripts
        numpad-emulator.ahk
        timezone-switcher.ahk 
```

## Supported OS

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
git clone https://github.com/H-int0/Strap.git
```

### Option B: Download as ZIP

1. Go to [github.com/H-int0/Strap](https://github.com/H-int0/Strap)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the folder somewhere on your device

Once you have the files, double-click `source/source.ahk` to run the script.

---

## Running the Script

To run Strap, simply double-click `source/source.ahk`.

A tray icon will briefly appear in the right bottom corner of your taskbar and then hide itself. That means it's running. You won't see any window or confirmation.

To stop it, make the tray icon visible first with `Win + Ctrl + \`, then right-click it and select **Exit**.

---

## Standalone Scripts

The `standalone-scripts/` folder contains standalone versions of each feature. These are useful if you only want one feature running without the other.

| File | What it does |
| --- | --- |
| `standalone-scripts/numpad-emulator.ahk` | CapsLock numpad |
| `standalone-scripts/timezone-switcher.ahk` | Timezone switcher |

- Run them the same way as `source/source.ahk` just double-click the file.
- They include the same tray icon toggle (`Win + Ctrl + \`) so you can exit them the same way.

---

**Note:** Don't run any standalone script at the same time as `source/source.ahk`. They share the same hotkeys and may conflict with each other. Furthermore, if your intent was to run a particular feature and not others that might not work since source/source.ahk is running.

---

## Features

### Accessibility: Tray Icon Toggle

**Hotkey:** `Win + Ctrl + \`

- The tray icon is hidden by default to keep your system tray clean.
- Press `Win + Ctrl + \` to show or hide it at any time.

When visible, right-clicking it lets you reload or exit the script and much more.

→ To change the default tray icon visibility, see [CONFIGURE.md](CONFIGURE.md#changing-the-default-tray-icon-visibility).

---

### 1. Numpad Emulator

Behavior:

- When CapsLock is enabled:
  - Number row keys `0-9` behave like numpad keys.
  - Holding Shift keeps the normal shifted symbols: `! @ # $ % ^ & * ( )`.

- When CapsLock is disabled:
  - Number row keys behave normally.

→ To change the Shift behavior, see [CONFIGURE.md](CONFIGURE.md#changing-capslock-numpad-shift-behavior).

---

### 2. Timezone Switcher

**Hotkeys:**

- Use `Win + Alt + `` ` to switch to the next timezone in your list.
- Use `Win + Ctrl + `` ` to show what timezone your system is currently on.

Each time you cycle, a small tooltip appears near your cursor showing the timezone you just switched to.

- Changes are applied instantly and saved directly to Windows Settings.
- Your preferences will persist through restarts and won't randomly reset on their own.

→ Add custom timezones or set a startup timezone, see [CONFIGURE.md](CONFIGURE.md#adding-a-timezone-not-in-the-list).

---

**Note:** If switching does not work, go to **Settings → Time & Language → Date & Time** and turn off **Set time zone automatically**. Windows will override manual timezone changes if that is enabled.

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

## Configuration

Refer [CONFIGURE.md](CONFIGURE.md) for the exact steps for:

- [Changing the Default Tray Icon Visibility](CONFIGURE.md#changing-the-default-tray-icon-visibility)
- [Changing CapsLock Numpad Shift Behavior](CONFIGURE.md#changing-capslock-numpad-shift-behavior)
- [Adding a Timezone Not in the List](CONFIGURE.md#adding-a-timezone-not-in-the-list)
- [Setting a Startup Timezone](CONFIGURE.md#setting-a-startup-timezone)
- [Adding a Timezone Not in the List for Startup](CONFIGURE.md#adding-a-custom-timezone-to-startup-not-in-the-list)

---

## Auto-Start on Boot

By default, you need to manually run `source/source.ahk` every time your computer restarts.

If you'd rather have it launch automatically on startup, you can add a copy of it to the Windows startup folder.

**Why a copy and not a shortcut?**

- If you ever move or rename the original file, a shortcut would stop working.
- A copy in the startup folder is self-contained and always runs regardless of what happens to the original.

### Option A: Command Prompt

Open Command Prompt and run the following, replacing `YOUR_PATH` with the full path to your `source/source.ahk`:

```cmd
copy "YOUR_PATH\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

**Example:**

```cmd
copy "C:\Users\YourName\scripts\strap\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Copy your `source/source.ahk` file into the folder that opens.

Yup, that's it.

---

## Updating the Startup Copy

After editing `source/source.ahk`, the copy in the startup folder won't update automatically. You'll need to replace it manually.

---

### Option-A: Command Prompt

Run the following, replacing `YOUR_PATH` with the full path to your `source/source.ahk`:

```cmd
copy /Y "YOUR_PATH\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

The `/Y` flag overwrites without asking for confirmation.

**Example:**

```cmd
copy /Y "C:\Users\YourName\scripts\strap\source\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option-B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Delete the existing `strap.ahk` from the folder.
3. Copy your updated `source/source.ahk` into the same folder and rename it to `strap.ahk`.

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

- **Numpad keys aren't working**: Make sure CapsLock is ON. If it still doesn't work, try reloading the script through the tray icon.

- **Timezone isn't switching**: Go to **Settings → Time & Language → Date & Time** and make sure that **"Set time zone automatically"** is turned off. Windows will override manual timezone changes if this is enabled.

- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**. If that doesn't help, **Exit** and double-click `source/source.ahk` again.

- **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

---

~*H-int*
