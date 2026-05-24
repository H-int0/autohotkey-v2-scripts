# Configure Strap

This guide covers how to configure and customize Strap beyond its default behavior.

- It focuses primarily on the combined `source/source.ahk` build, since that is the main version of the script.
- Standalone scripts follow the same configuration principles whenever the feature exists in those files as well.

---

## Table of Contents

- [Changing the Default Tray Icon Visibility](#changing-the-default-tray-icon-visibility)
- [Changing CapsLock Numpad Shift Behavior](#changing-capslock-numpad-shift-behavior)
- [Adding a Timezone Not in the List](#adding-a-timezone-not-in-the-list)
- [Setting a Startup Timezone](#setting-a-startup-timezone)
- [Adding a Timezone Not in the List for Startup](#adding-a-custom-timezone-to-startup-not-in-the-list)

---

## Changing the Default Tray Icon Visibility

By default, Strap hides the tray icon on startup. To make it visible instead, switch which startup option is uncommented in the configuration block near the top of the script.

**To configure this behavior follow the steps below:**

### Step 1: Open the script in your text editor

### Step 2: Find the tray icon block

It looks like this:

```ahk
; =========================================================
; CONFIG: TRAY ICON VISIBILITY
; =========================================================
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
A_IconHidden := 1    ; Un-comment for the behavior to be = Hidden (default)
; A_IconHidden := 0  ; Un-comment for the behavior to be = Visible
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;
```

### Step 3: Choose the active line

- `A_IconHidden := 1` keeps the tray icon hidden on startup.
- `A_IconHidden := 0` makes it visible on startup.

Only one line should stay active.

**To make the tray icon visible on startup:**

```ahk
; A_IconHidden := 1  ; Un-comment for the behavior to be = Hidden (default)
A_IconHidden := 0    ; Un-comment for the behavior to be = Visible
```

**To go back to hidden on startup:**

```ahk
A_IconHidden := 1    ; Un-comment for the behavior to be = Hidden (default)
; A_IconHidden := 0  ; Un-comment for the behavior to be = Visible
```

### Step 4: Save and reload

The change does not take effect until the script is restarted.

- If the tray icon is visible, right-click it and choose **Reload**.
- If it is hidden, show it with `Win + Ctrl + \`, then reload it.
- Or exit the script and run it again.

---

## Changing CapsLock Numpad Shift Behavior

This applies to the numpad emulator.

- By default, when CapsLock is on and you hold Shift, the number row keeps the usual shifted symbols: `! @ # $ % ^ & * ( )`.

**To configure this behavior follow the steps below:**

### Step 1: Open the numpad script

Open `standalone-scripts/numpad-emulator.ahk` if you are using the standalone version, or edit the CapsLock numpad section in `source/source.ahk` if you are using the combined build.

### Step 2: Find the Shift setting

It looks like this:

```ahk
; =========================================================
; CONFIG: NUMPAD SHIFT SYMBOLS
; =========================================================
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

- `NumpadShiftSymbols := true` keeps shifted symbols working normally while CapsLock is active.
- `NumpadShiftSymbols := false` disables those shifted symbols while CapsLock is active.

Only one line should stay active.

**To keep shifted symbols enabled (default):**

```ahk
NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
; NumpadShiftSymbols := false  ; Disabled: Shift does nothing
```

**To disable shifted symbols:**

```ahk
; NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
NumpadShiftSymbols := false  ; Disabled: Shift does nothing
```

### Step 4: Save and Reload

Reload the script after saving your change. The new behavior applies immediately after restart or reload.

---

## Adding a Timezone Not in the List

If the timezone you want is not already in the script, add it to the **CUSTOM TIMEZONES** section.

### Step 1: Find the Windows timezone ID

Timezone changes go through `tzutil`, Windows' built-in timezone utility. Open Command Prompt and run:

```cmd
tzutil /l
```

This prints all timezones Windows knows about. Each entry looks like this:

```cmd
(UTC+09:00) Osaka, Sapporo, Tokyo
Tokyo Standard Time
```

The second line is the Windows ID. That is what the script needs.

### Step 2: Open the script in a text editor

Open `source/source.ahk` for the combined build, or `standalone-scripts/timezone-switcher.ahk` if you are only using the timezone feature.

### Step 3: Find the CUSTOM TIMEZONES section

It looks like this:

```ahk
; =========================================================
; CONFIG: CUSTOM TIMEZONES
; =========================================================
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

Each timezone takes two lines. Both lines must be uncommented:

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

Place your entry **above** the `; ^^^^^^^^^^^^^^^^^^^^ ADD ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^` line.

The order of enabled entries controls the cycle order. Put the new timezone where you want it to appear in the cycle.

**An example of newly added timezones may look like:**

```ahk
; =========================================================
; CONFIG: CUSTOM TIMEZONES
; =========================================================
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

### Step 5: Save and reload

After saving, reload the script so the updated timezone list is loaded.

---

## Setting a Startup Timezone

This controls what timezone Strap applies when it launches.

- By default, Strap does not change your Windows timezone on startup.
- Windows keeps whatever timezone was already active before the script launched.
- You can optionally force Strap to apply a specific timezone every time it starts.

### Step 1: Open the script in a text editor

Open `source/source.ahk` for the combined build, or `standalone-scripts/timezone-switcher.ahk` for the timezone-only version.

### Step 2: Find the startup timezone block

It looks like this:

```ahk
; =========================================================
; CONFIG: STARTUP TIMEZONE
; =========================================================
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

### Step 3: Choose the timezone

- Leave every line commented to keep whatever timezone Windows already had.
- Uncomment exactly one line to force that timezone on startup.

If more than one line is uncommented, the most bottom uncommented timezone is applied on startup.

**An example may look like this:**

```ahk
; =========================================================
; CONFIG: STARTUP TIMEZONE
; =========================================================
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

Save the file and restart the script. The selected timezone will be applied at launch.

---

## Adding a Custom Timezone to Startup not in the list

If the timezone you want is not already in the list of timezones available for startup, add it to the `ADD CUSTOM TIMEZONE FOR STARTUP` section under the `CONFIG: STARTUP TIMEZONE` section.

### Step 1: Find the Windows Timezone ID

Timezone changes go through `tzutil`, Windows' built-in timezone utility. Open Command Prompt and run:

```cmd
tzutil /l
```

This prints all timezones Windows knows about. Each entry looks like this:

```cmd
(UTC+09:00) Osaka, Sapporo, Tokyo
Tokyo Standard Time
```

**The second line is the Windows ID. That is what we need.**

### Step 2: Open the script in your text editor

Open `source/source.ahk` for the combined build, or `standalone-scripts/timezone-switcher.ahk` if you are only using the timezone feature.

### Step 3: Find the `ADD CUSTOM TIMEZONE FOR STARTUP` section

It looks like this:

```ahk
; =========================================================
; ADD CUSTOM TIMEZONE FOR STARTUP
; =========================================================
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

Make sure all other `StartupTZID` lines in the **CONFIG: STARTUP TIMEZONE** section remain commented out.

**An example of it may look like:**

```ahk
; =========================================================
;
StartupTZID := "Tokyo Standard Time"
;
; ^^^^^^^^^^^^^^^^^^^^^^ ABOVE HERE: ^^^^^^^^^^^^^^^^^^^^^^
;
```

### Step 5: Save and Reload

After saving, reload the script so the updated timezone list is loaded.

---

~*H-int*
