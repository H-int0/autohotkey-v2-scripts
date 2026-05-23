# Strap

Strap is a lightweight AutoHotkey_v2 script for Windows that adds keyboard shortcuts to devices that lack certain physical keys or need quick access to system-level features.

Currently, it ships with two features:

- A CapsLock-based numpad emulator.
- And a timezone switcher.

With more planned for the future.

- *More features coming in future versions. See [CHANGELOG.md](CHANGELOG.md) for history and features in all previous versions.*

---

## Requirements

- Windows OS
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

Once you have the files, double-click `source.ahk` to run the script.

---

## Running the Script

To run Strap, simply double-click `source.ahk`.

A tray icon will briefly appear in the right bottom corner of your taskbar and then hide itself. That means it's running. You won't see any window or confirmation.

To stop it, make the tray icon visible first with `Win + Ctrl + \`, then right-click it and select **Exit**.

---

## Features

### Accessibility: Tray Icon Toggle

**Hotkey:** `Win + Ctrl + \`

- The tray icon is hidden by default to keep your system tray clean.
- Press `Win + Ctrl + \` to show or hide it at any time. When visible, right-clicking it lets you reload or exit the script and much more.

---

### 1. Numpad Emulator

**Hotkey:** `CapsLock ON` + any number key `0`–`9`

When CapsLock is on, the number row at the top of your keyboard stops typing numbers and starts behaving exactly like the dedicated numpad keys on a full-size keyboard the same keys that most compact keyboards leave out.

**Usage:**

1. Turn CapsLock on.
2. Now pressing any number key `0`–`9` and it will behave as the corresponding numpad key.
3. Turn CapsLock off to restore normal number row behavior.

**Note:** This only activates when CapsLock is ON. If it doesn't seem to be working, ensure that your **CapsLock** key is actually **ON**.

---

### 2. Timezone Switcher

**Hotkeys:**

- Use `Win + Alt + `` ` to switch to the next timezone in your list.
- Use `Win + Ctrl + `` ` to show what timezone your system is currently on.

Each time you cycle, a small tooltip appears near your cursor showing the timezone you just switched to.

Changes are applied instantly and saved directly to Windows Settings. Your preferences will persist through restarts and won’t randomly reset on their own.

---

**Note:** If switching doesn't seem to work, go to **Settings → Time & Language → Date & Time** and turn off **"Set time zone automatically"**. Windows will override any manual changes if that's enabled.

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

## Configuring Timezones

- Open `source.ahk` in any text editor and find the **TIMEZONE LIST** section.
- Each timezone takes two lines.
- Both lines together make up one entry, the first stores the label, the second adds it to the cycle.
- To enable a timezone, remove the semicolons from both lines.
- To disable one, put them back.

---

**Example:**

Before (disabled):

```ahk
; Tokyo
; TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
; TZOrder.Push("Tokyo Standard Time")
```

After (enabled):

```ahk
; Tokyo
TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
TZOrder.Push("Tokyo Standard Time")
```

The cycle order follows the order of enabled entries, top to bottom in the file.

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

## Adding a Timezone Not in the List

If the timezone you want isn't in the list above, you can add it manually.

### Step 1: Find the Windows timezone ID

Open Command Prompt and run:

```cmd
tzutil /l
```

This prints every timezone Windows supports. Each entry looks like this:

```cmd
(UTC+09:00) Osaka, Sapporo, Tokyo
Tokyo Standard Time
```

---

### Step 2: Add it to `source.ahk`

Open `source.ahk` in a text editor and find the TIMEZONE LIST section. Pick a spot in the list that matches roughly where it falls by UTC offset, then add two lines following this format:

```ahk
; Your City
TZData["Windows ID Here"] := "(UTC +X) `"Your Label`""
TZOrder.Push("Windows ID Here")
```

**Example adding Tokyo manually:**

```ahk
; Tokyo
TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
TZOrder.Push("Tokyo Standard Time")
```

---

### Step 3: Reload the script

- Make the tray icon visible with `Win + Ctrl + \`.
- Right-click it.
- Select **Reload**

Your new timezone will now be part of the cycle.

---

## Auto-Start on Boot

By default, you need to manually run `source.ahk` every time your computer restarts. If you'd rather have it launch automatically on startup, you can add a copy of it to the Windows startup folder.

**Why a copy and not a shortcut?**

If you ever move or rename the original file, a shortcut would silently stop working. A copy in the startup folder is self-contained and always runs regardless of what happens to the original.

### Option A: Command Prompt

Open Command Prompt and run the following, replacing `YOUR_PATH` with the full path to your `source.ahk`:

```cmd
copy "YOUR_PATH\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

**Example:**

```cmd
copy "C:\Users\YourName\scripts\strap\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Copy your `source.ahk` file into the folder that opens.

Yup, that's it.

---

## Updating the Startup Copy

After editing `source.ahk`, the copy in the startup folder won't update automatically. You'll need to replace it manually.

---

### Option-A: Command Prompt

Run the following, replacing `YOUR_PATH` with the full path to your `source.ahk`:

```cmd
copy /Y "YOUR_PATH\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

The `/Y` flag overwrites without asking for confirmation.

**Example:**

```cmd
copy /Y "C:\Users\YourName\scripts\strap\source.ahk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\strap.ahk"
```

### Option-B: Manual

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Delete the existing `strap.ahk` from the folder.
3. Copy your updated `source.ahk` into the same folder and rename it to `strap.ahk`.

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

- **Script seems to be running but nothing works**: Right-click the tray icon (make it visible first with `Win + Ctrl + \`) and select **Reload**. If that doesn't help, **Exit** and double-click `source.ahk` again.

- **Keyboard is behaving strangely after installing the script**: See [RECOVERY.md](RECOVERY.md) for step-by-step instructions to safely remove the script.

---

~*H-int*
