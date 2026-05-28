# Configure Strap

This guide covers how to configure and customize Strap beyond its default behavior.

- It focuses primarily on the scripts inside the `distribution/` and `modules/` directories.
- You can configure the pre‑combined `distribution/source.ahk` directly via `source-dependencies/config.ahk`.
- Independent components inside `modules/` follow the same configuration principles inside their respective files.

---

## Table of Contents

- [Enabling and Disabling Features](#enabling-and-disabling-features)
- [Customizing Tooltips](#customizing-tooltips)
- [Changing the Default Tray Icon Visibility](#changing-the-default-tray-icon-visibility)
- [Changing CapsLock Numpad Shift Behavior](#changing-capslock-numpad-shift-behavior)
- [Configuring the Color Picker Summary MsgBox](#configuring-the-color-picker-summary-msgbox)
- [Adding a Timezone Not in the List](#adding-a-timezone-not-in-the-list)
- [Setting a Startup Timezone](#setting-a-startup-timezone)
- [Adding a Custom Timezone to Startup (not in the list)](#adding-a-custom-timezone-to-startup-not-in-the-list)

---

## Enabling and Disabling Features

You can completely disable specific features so their hotkeys revert to default Windows behavior.

### Step 1: Open your configuration file

- Combined script: Open `distribution/config.ahk`.
- Standalone modules: Open the specific file in `modules/`.

### Step 2: Find the specific feature config block+K does nothing

### Step 3: Choose the active line

To disable a feature, comment out the `true` line and uncomment the `false` line:

### Step 4: Save and reload

Right-click the tray icon and select **Reload** for changes to take effect.

---

## Customizing Tooltips

Strap uses a custom tooltip system that tracks your cursor. You can change how long these tooltips stay on screen, alter their text, or disable them entirely.

### Step 1: Open your Configuration file

- Combined script: Open `distribution/config.ahk`.
- Standalone modules: Open the specific file in `modules/`.

### Step 2: Find the `CONFIG: TOOLTIPS` section

```ahk
; =====================================================================================
; CONFIG: TOOLTIPS
; =====================================================================================
;
; >> Customize tooltip display duration and individual messages.
;
; INSTRUCTIONS:
;
; 1. EDIT THESE VALUES DIRECTLY:
;    - Change Config_TooltipDuration (milliseconds) to alter how long tooltips stay on screen.
;    - Change the message text inside the quotes "" to customize what each tooltip says.
;
; 2. ENABLE / DISABLE A TOOLTIP:
;    - To turn a tooltip OFF, put a semicolon (;) at the beginning of its line.
;    - To turn it ON, remove that semicolon.
;
; 3. Save the file and reload the script.
;
; =========================================================
;
; ------ Duration in milliseconds -------
;
Global Config_TooltipDuration := 2500   ; (default: 2500 ms)
;                                ^ <-- Edit this number (in milliseconds) to change how long tooltips stay visible   (1 sec = 1000 ms)


; --------- Color Picker tooltip --------
;
Global Msg_ColorPicker := "Copied to Clipboard"   ; (default-text: "Copied to Clipboard")
;                         ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip


; ------- Force Kill Task tooltip -------
;
Global Msg_EndTask := "EVAPORATED!"   ; (default-text: "EVAPORATED!")
;                     ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip



; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 3: Edit duration or text

- Change `2500` to your desired duration in milliseconds
- Change the text inside the quotes to change the message

### Step 4: Disable a tooltip (Optional)

If you don't want a tooltip to appear at all, simply add a semicolon (`;`) at the beginning of the message line:

```ahk
; --------- Color Picker tooltip --------
;
; Global Msg_ColorPicker := "Copied to Clipboard"   ; (default-text: "Copied to Clipboard")
;                         ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip

```

### Step 5: Save and Reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Changing the Default Tray Icon Visibility

By default, Strap hides the tray icon on startup.

### Step 1: Open the script in your text editor

- Combined script: Open `distribution/config.ahk`.
- Standalone modules: Open the specific file in `modules/`.

### Step 2: Find the `CONFIG: TRAY ICON VISIBILITY` section

```ahk
; =====================================================================================
; CONFIG: TRAY ICON VISIBILITY
; =====================================================================================
;
; >> Customize whether the tray icon is visible or hidden on script startup.
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line by adding a semicolon (;) at the beginning.
; 3. Save the file and reload the script.
;
;   A_IconHidden := 1   → Tray icon is HIDDEN on startup (default)
;   A_IconHidden := 0   → Tray icon is VISIBLE on startup
;
; =========================================================
;
A_IconHidden := 1    ; Un-comment for the tray icon to be Hidden (default)
; A_IconHidden := 0  ; Un-comment for the tray icon to be Visible
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 3: Choose the active Line

- `A_IconHidden := 1` keeps the tray icon hidden on startup.
- `A_IconHidden := 0` makes it visible on startup.

Only one line should stay active.

- **To make the tray icon visible on startup:**

```ahk
; =========================================================
;
; A_IconHidden := 1    ; Un-comment for the tray icon to be Hidden (default)
A_IconHidden := 0  ; Un-comment for the tray icon to be Visible
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

- **To go back to hidden on startup:**

```ahk
; =========================================================
;
A_IconHidden := 1    ; Un-comment for the tray icon to be Hidden (default)
; A_IconHidden := 0  ; Un-comment for the tray icon to be Visible
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 4: Save and Reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Changing CapsLock Numpad Shift Behavior

> By default, when CapsLock is on and you hold Shift, the number row keeps the usual shifted symbols: `! @ # $ % ^ & * ( )`.

### Step 1: Open your configuration File

- Combined script: Open `distribution/config.ahk`.
- Standalone modules: Open the specific file in `modules/`.

### Step 2: Find the `CONFIG: NUMPAD SHIFT SYMBOLS` section

```ahk
; =====================================================================================
; CONFIG: NUMPAD SHIFT SYMBOLS
; =====================================================================================
;
; >> What happens when Shift is held with CapsLock ON and a number key is pressed.
;
;   Enabled  →  Shift+numrow types symbols normally: "! @ # $ % ^ & * ( )"  (default)
;   Disabled →  Shift+numrow does nothing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
; NumpadShiftSymbols := false  ; Disabled: Shift does nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 3: Choose the Active line

- `numpadShiftSymbols := true` → shifted symbols work normally (default)
- `numpadShiftSymbols := false` → shifted symbols do nothing while CapsLock is on

Only one line should stay active.

- **To keep shifted symbols enabled (default):**

```ahk
; =========================================================
;
NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
; NumpadShiftSymbols := false  ; Disabled: Shift does nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

- **To disable shifted symbols:**

```ahk
; =========================================================
;
; NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
NumpadShiftSymbols := false  ; Disabled: Shift does nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 4: save and reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Configuring the Color Picker Summary MsgBox

By default, the Color Picker copies data silently to your clipboard. You can optionally have it pop up a Summary Message Box containing the Hex, RGB, and Coordinates.

### Step 1: Open Your configuration file

- Combined script: Open `distribution/config.ahk`.
- Standalone modules: Open the specific file in `modules/`.

### Step 2: Find the `CONFIG: COLOR PICKER SUMMARY MSGBOX` section

```ahk
; =====================================================================================
; CONFIG: COLOR PICKER SUMMARY MSGBOX
; =====================================================================================
;
; >> Controls whether a summary MsgBox appears after closing the picker.
; >> Clipboard copy always happens regardless of this setting.
;
;   Disabled →  Picker closes silently, values are copied to clipboard (default)
;   Enabled  →  MsgBox shows Hex, RGB, and coordinates after closing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
ColorPickerMsgBox := false  ; Disabled: close silently (default)
; ColorPickerMsgBox := true   ; Enabled: show summary MsgBox
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 3: choose the active line

- ColorPickerMsgBox := false  ; Disabled: close silently (default)
- ColorPickerMsgBox := true   ; Enabled: show summary MsgBox

Only one line should stay active.

- **To hide the summary MsgBox: (default):**

```ahk
; =========================================================
;
ColorPickerMsgBox := false  ; Disabled: close silently (default)
; ColorPickerMsgBox := true   ; Enabled: show summary MsgBox
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

- **To show the summary MsgBox:**

```ahk
; =========================================================
;
; ColorPickerMsgBox := false  ; Disabled: close silently (default)
ColorPickerMsgBox := true   ; Enabled: show summary MsgBox
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 4: Save And Reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Adding a Timezone Not in the List

If the timezone you want is not already in the script, add it to the **ADD CUSTOM TIMEZONES** section.

### Step 1: Find the Windows timezone ID

Open Command Prompt and run:

```cmd
tzutil /l
```

This prints all timezones Windows knows about. Each entry looks like this:

```cmd
(UTC+09:00) Osaka, Sapporo, Tokyo
Tokyo Standard Time
```

The second line of each entry is the Windows ID (e.g., `Tokyo Standard Time`).

### Step 2: Open the script in a text editor

- Combined script: `distribution/source.ahk`
- Timezone module: `modules/timezone-switcher.ahk`

### Step 3: Find the `ADD CUSTOM TIMEZONES` section

```ahk
; =====================================================================================
; CONFIG: ADD CUSTOM TIMEZONES
; =====================================================================================
;
; Add your own timezones here. Each entry takes two lines.
;
; FORMAT:
;   TZData["Windows ID"] := "(UTC +X) `"Your Label`""
;   TZOrder.Push("Windows ID")
;
; HOW TO FIND YOUR WINDOWS TIMEZONE ID:
;   1. Open Command Prompt and run:  tzutil /l
;   2. Find your timezone (e.g., "Tokyo Standard Time").
;   3. Copy the exact ID.
;
; INSTRUCTIONS:
;   1. Replace "Your Windows ID Here" with the actual ID.
;   2. Replace "Your Label" with any name you like.
;   3. Remove the semicolon (;) from the start of BOTH lines to enable.
;   4. Place your entry ABOVE the "^ ADD ABOVE HERE ^" line.
;
; ======= Your Custom Timezone SHOULD LOOK LIKE THIS ======
;
; EXAMPLE:
;   TZData["Vladivostok Standard Time"] := "(UTC +10) `"Vladivostok`""
;   TZOrder.Push("Vladivostok Standard Time")
;
; =========================================================
;
;
;
;
; ^^^^^^^^^^^^^^^^^^^^ ADD ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^
;
```

### Step 4: Add your entry

Each timezone takes two lines. Place them **above** the `ADD ABOVE HERE` line.

```ahk
; Your City or Label
TZData["Windows ID Here"] := "(UTC +X) `"Your Label`""
TZOrder.Push("Windows ID Here")
```

**Example:**

```ahk
; Vladivostok
TZData["Vladivostok Standard Time"] := "(UTC +10) `"Vladivostok`""
TZOrder.Push("Vladivostok Standard Time")
```

> [!NOTE]
> The order of enabled entries controls the cycle order. Put the new timezone where you want it to appear in the cycle.

**An example of how a newly added timezones might look like:**

```ahk
; =====================================================================================
; CONFIG: ADD CUSTOM TIMEZONES
; =====================================================================================
;
; Add your own timezones here. Each entry takes two lines.
;
; FORMAT:
;   TZData["Windows ID"] := "(UTC +X) `"Your Label`""
;   TZOrder.Push("Windows ID")
;
; HOW TO FIND YOUR WINDOWS TIMEZONE ID:
;   1. Open Command Prompt and run:  tzutil /l
;   2. Find your timezone (e.g., "Tokyo Standard Time").
;   3. Copy the exact ID.
;
; INSTRUCTIONS:
;   1. Replace "Your Windows ID Here" with the actual ID.
;   2. Replace "Your Label" with any name you like.
;   3. Remove the semicolon (;) from the start of BOTH lines to enable.
;   4. Place your entry ABOVE the "^ ADD ABOVE HERE ^" line.
;
; ======= Your Custom Timezone SHOULD LOOK LIKE THIS ======
;
; EXAMPLE:
;   TZData["Vladivostok Standard Time"] := "(UTC +10) `"Vladivostok`""
;   TZOrder.Push("Vladivostok Standard Time")
;
; =========================================================
;
;
; Vladivostok
TZData["Vladivostok Standard Time"] := "(UTC +10) `"Vladivostok`""
TZOrder.Push("Vladivostok Standard Time")

; Yakutsk
TZData["Yakutsk Standard Time"] := "(UTC +9) `"Yakutsk`""
TZOrder.Push("Yakutsk Standard Time")

; Newfoundland
TZData["Newfoundland Standard Time"] := "(UTC -3:30) `"Newfoundland`""
TZOrder.Push("Newfoundland Standard Time")
;
; ^^^^^^^^^^^^^^^^^^^^ ADD ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^
;
```

### Step_5: Save and Reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Setting a Startup Timezone

This controls what timezone Strap applies when it launches.

- By default, Strap does not change your Windows timezone on startup.
- Windows keeps whatever timezone was already active before the script launched.
- You can optionally force Strap to apply a specific timezone every time it starts.

### Step 1: Open the script in a text editor

- Combined script: `distribution/source.ahk`
- Timezone module: `modules/timezone-switcher.ahk`

### Step 2: Find the `STARTUP TIMEZONE` block

```ahk
; =====================================================================================
; CONFIG: STARTUP TIMEZONE
; =====================================================================================
;
; INSTRUCTIONS:
;   - Leave EVERY line commented → keep current Windows timezone.
;   - Uncomment EXACTLY ONE line → force that timezone on script startup.
;
; If you need a timezone not listed below, use the "ADD CUSTOM TIMEZONE FOR STARTUP" section.
;
; =========================================================
;
; StartupTZID := "UTC"
; StartupTZID := "GMT Standard Time"
; StartupTZID := "W. Europe Standard Time"
; StartupTZID := "Egypt Standard Time"
; StartupTZID := "Arab Standard Time"
; StartupTZID := "Russian Standard Time"
; StartupTZID := "Iran Standard Time"
; StartupTZID := "Arabian Standard Time"
; StartupTZID := "Afghanistan Standard Time"
; StartupTZID := "Pakistan Standard Time"
; StartupTZID := "India Standard Time"
; StartupTZID := "Bangladesh Standard Time"
; StartupTZID := "SE Asia Standard Time"
; StartupTZID := "China Standard Time"
; StartupTZID := "Singapore Standard Time"
; StartupTZID := "Tokyo Standard Time"
; StartupTZID := "AUS Eastern Standard Time"
; StartupTZID := "New Zealand Standard Time"
; StartupTZID := "Azores Standard Time"
; StartupTZID := "Cape Verde Standard Time"
; StartupTZID := "SA Eastern Standard Time"
; StartupTZID := "E. South America Standard Time"
; StartupTZID := "Venezuela Standard Time"
; StartupTZID := "SA Western Standard Time"
; StartupTZID := "Eastern Standard Time"
; StartupTZID := "Central Standard Time"
; StartupTZID := "Mountain Standard Time"
; StartupTZID := "Pacific Standard Time"
; StartupTZID := "Alaskan Standard Time"
; StartupTZID := "Hawaiian Standard Time"
;
```

### Step 3: Choose the timezone and uncomment it

- Leave every line commented to keep whatever timezone Windows already had.
- Uncomment exactly one line to force that timezone on startup.

> [!NOTE]
> If more than one line is uncommented, the bottom-most uncommented timezone is applied on startup.

**An example may look like this:**

```ahk
; =====================================================================================
; CONFIG: STARTUP TIMEZONE
; =====================================================================================
;
; INSTRUCTIONS:
;   - Leave EVERY line commented → keep current Windows timezone.
;   - Uncomment EXACTLY ONE line → force that timezone on script startup.
;
; If you need a timezone not listed below, use the "ADD CUSTOM TIMEZONE FOR STARTUP" section.
;
; =========================================================
;
; StartupTZID := "UTC"
; StartupTZID := "GMT Standard Time"
; StartupTZID := "W. Europe Standard Time"
; StartupTZID := "Egypt Standard Time"
; StartupTZID := "Arab Standard Time"
; StartupTZID := "Russian Standard Time"
; StartupTZID := "Iran Standard Time"
; StartupTZID := "Arabian Standard Time"
; StartupTZID := "Afghanistan Standard Time"
; StartupTZID := "Pakistan Standard Time"
; StartupTZID := "India Standard Time"
; StartupTZID := "Bangladesh Standard Time"
; StartupTZID := "SE Asia Standard Time"
; StartupTZID := "China Standard Time"
; StartupTZID := "Singapore Standard Time"
; StartupTZID := "Tokyo Standard Time"
; StartupTZID := "AUS Eastern Standard Time"
StartupTZID := "New Zealand Standard Time"
; StartupTZID := "Azores Standard Time"
; StartupTZID := "Cape Verde Standard Time"
; StartupTZID := "SA Eastern Standard Time"
; StartupTZID := "E. South America Standard Time"
; StartupTZID := "Venezuela Standard Time"
; StartupTZID := "SA Western Standard Time"
; StartupTZID := "Eastern Standard Time"
; StartupTZID := "Central Standard Time"
; StartupTZID := "Mountain Standard Time"
; StartupTZID := "Pacific Standard Time"
; StartupTZID := "Alaskan Standard Time"
; StartupTZID := "Hawaiian Standard Time"
;
```

### Step 4: Save and restart

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Adding a Custom Timezone to Startup (not in the list)

If your desired startup timezone is not in the pre‑defined list, use the `ADD CUSTOM TIMEZONE FOR STARTUP` section.

### Step 1: Find the Windows Timezone ID

Open Command Prompt and run:

```cmd
tzutil /l
```

This prints all timezones Windows knows about. Each entry looks like this:

```cmd
(UTC+09:00) Osaka, Sapporo, Tokyo
Tokyo Standard Time
```

The second line of each entry is the Windows ID (e.g., `Tokyo Standard Time`).

### Step 2: Open the script in your text editor

- Combined script: `distribution/source.ahk`
- Timezone module: `modules/timezone-switcher.ahk`

### Step 3: Find the `ADD CUSTOM TIMEZONE FOR STARTUP` section

```ahk
; =====================================================================================
; CONFIG: ADD CUSTOM TIMEZONE FOR STARTUP
; =====================================================================================
;
; Use this section if the timezone you want is NOT in the list above.
;
; INSTRUCTIONS:
; 1. Open Command Prompt and run:  tzutil /l
; 2. Find your timezone ID (e.g., "Pacific Standard Time").
; 3. Delete the semicolon (;) from the start of the line below.
; 4. Replace "Your_Custom_Windows_ID_Here" with your exact Windows ID.
;
; IMPORTANT:
;    Make sure ALL "StartupTZID" lines in the section above stay commented out (with a semicolon) if you use this option.
;
; =========================================================
;
; StartupTZID := "Your_Custom_Windows_ID_Here"
;
; ^^^^^^^^^^^^^^^^^^^^^^ ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^^^
;
```

### Step 4: Add the Timezone you want

In the space marked with `ABOVE HERE`

```ahk
; =========================================================
;
; StartupTZID := "Your_Custom_Windows_ID_Here"
;
; ^^^^^^^^^^^^^^^^^^^^^^ ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^^^
;
```

- Delete the semicolon (`;`) at the beginning of the line `; StartupTZID := "Your_Custom_Windows_ID_Here"`.
- Replace `Your_Custom_Windows_ID_Here` with the actual Windows timezone ID.

> Make sure all other `StartupTZID` lines in the **CONFIG: STARTUP TIMEZONE** section remain commented out.

**An example of how it might look like:**

```ahk
; =========================================================
;
StartupTZID := "Tokyo Standard Time"
;
; ^^^^^^^^^^^^^^^^^^^^^^ ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^^^
;
```

### Step 5: Save and reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

~*[@H-int0](https://github.com/H-int0)*
