# Strap Features: Deep Dive

This document provides an in-depth look at each feature included in Strap. It explains not only *what* the features do, but *how* they work under the hood, their built-in safety mechanisms, and their specific use cases.

---

## Table of Contents

- [Utilities](#utilities)
  - [1. Tray Icon Toggle](#1-tray-icon-toggle)
  - [2. Reloading the Script](#2-reloading-the-script)
  - [3. Exiting the Script](#3-exiting-the-script)
  - [4. Dynamic Help Box](#4-dynamic-help-box)
- [Features](#features)
  - [1. Numpad Emulator](#1-numpad-emulator)
  - [2. Timezone Switcher](#2-timezone-switcher)
  - [3. Force Kill Task](#3-force-kill-task)
  - [4. Color Picker](#4-color-picker)
  - [5. Line Navigation](#5-line-navigation)

---

## Utilities

Strap includes built-in quality-of-life utilities that manage how the script interacts with you.

### 1. Tray Icon Toggle

To keep your taskbar clean, Strap hides its AutoHotkey tray icon by default.

**Hotkey:** `Win + Ctrl + \`

- This hotkey flips the `A_IconHidden` state, allowing you to reveal the icon temporarily if you need to right-click it to Suspend, Reload, or Exit the script.

---

### 2. Reloading the Script

To reload your script, Use the **Hotkey:** `Win+Ctrl+/`

---

### 3. Exiting the Script

To Exit your script, use the **Hotkey:** `Win+Shift+/`

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

### 1. Numpad Emulator

A hardware-level numpad substitute for Ten-key-less (TKL), 60%, and laptop keyboards, mapping the standard number row to actual Numpad keycodes.

**Hotkeys:**

- **Toggle:** `CapsLock`
- **Use:** `0-9` on the number row
- **Shift Behavior:** `Shift + 0-9` (Configurable)

#### How it Works

Unlike simple text replacement scripts that just send the characters "1", "2", "3", this feature sends `{Blind}{Numpad1}`, `{Blind}{Numpad2}`, etc.

- **The `{Blind}` Modifier:**
  - This allows the emulated numpad keys to respect standard modifier keys.
  - If you hold `Ctrl` and press the `1` key while CapsLock is ON, the computer registers `Ctrl + Numpad1`.
  - This is critical for software that relies on specific numpad shortcuts (like Blender or certain IDEs).
- **Shift Fallback:**
  - By default, holding `Shift` while CapsLock is ON suspends the numpad emulation and sends the standard symbols (`!`, `@`, `#`, etc.).
  - This means you don't have to toggle CapsLock off just to type an exclamation mark. This behavior can be disabled in `config.ahk`.

---

### 2. Timezone Switcher

A system-level utility to instantly cycle your Windows clock between different global timezones without navigating through the Windows Settings app.

**Hotkeys:**

- `Win + Alt + `` ` switch to the next timezone in your list.
- `Win + Ctrl + `` ` show the current timezone.

#### How it works

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

### 3. Force Kill Task

A smart, context-aware window closer that gracefully exits healthy programs and ruthlessly terminates frozen ones.

**Hotkey:** `Win + Ctrl + K`

#### How It Works

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

### 4. Color Picker

A developer-centric, floating live color picker that captures screen pixels, translates them into Hex and RGB, and copies them to your clipboard.

**Hotkey:** `Win + Ctrl + C` (Press to open, press again to capture/close)

#### how it works

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

### 5. Line Navigation

Translates modern text-editor navigation shortcuts into standard Windows keystrokes, allowing for rapid text manipulation without reaching for the physical `Home` or `End` keys.

**Hotkeys:**

- **Move Cursor:** `Shift + Alt + Left/Right`
- **Select Text:** `Shift + Win + Left/Right`
- **Delete Text:** `Alt + Backspace/Delete`

#### How it Works?

It leverages standard OS-level text inputs.

- Moving sends `{Home}` or `{End}`.
- Selecting sends `+{Home}` (Shift+Home) or `+{End}` (Shift+End).
- Deleting evaluates the cursor position and sends a selection command followed immediately by `{Backspace}` or `{Delete}`.
This provides universally compatible text navigation across almost every Windows application, browser, and IDE.

---

~*[@H-int0](https://github.com/H-int0)*
