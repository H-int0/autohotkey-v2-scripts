; MIT License
; 
; Copyright (c) 2026 H-int0
; 
; Permission is hereby granted, free of charge, to any person obtaining a copy
; of this software and associated documentation files (the "Software"), to deal
; in the Software without restriction, including without limitation the rights
; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
; copies of the Software, and to permit persons to whom the Software is
; furnished to do so, subject to the following conditions:
; 
; The above copyright notice and this permission notice shall be included in all
; copies or substantial portions of the Software.
; 
; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
; SOFTWARE.

; ===========================================================================================================================================================================

#Requires AutoHotkey v2.0

if !IsSet(TZData)
    TZData := Map()
if !IsSet(TZOrder)
    TZOrder := []

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
Global Msg_EndTask := "Evaporated"   ; (default-text: "Evaporated")
;                     ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip



; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


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


; =====================================================================================
; CONFIG: FORCE KILL TASK
; =====================================================================================
;
; >> Press Win+Ctrl+K to close the active window (like Alt+F4).
; >> If the window is frozen, it will force kill the process instead.
;
;   Enabled  →  Win+Ctrl+K closes/kills the active window (default)
;   Disabled →  Win+Ctrl+K does nothing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
EndTaskEnabled := true   ; Enabled: Win+Ctrl+K closes active window (default)
; EndTaskEnabled := false  ; Disabled: Win+Ctrl+K does nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; =====================================================================================
; CONFIG: COLOR PICKER
; =====================================================================================
;
; >> Press Win+Ctrl+C to toggle a live color picker under your mouse.
; >> Press it again to close it, copy Hex/RGB/coords to clipboard, and show a summary.
;
;   Enabled  →  Win+Ctrl+C toggles the color picker (default)
;   Disabled →  Win+Ctrl+C does nothing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
ColorPickerEnabled := true   ; Enabled: Win+Ctrl+C toggles color picker (default)
; ColorPickerEnabled := false  ; Disabled: Win+Ctrl+C does nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; =====================================================================================
; CONFIG: COLOR PICKER SUMMARY MSGBOX
; =====================================================================================
;
; >> Controls whether a summary MsgBox appears after closing the picker.
; >> Clipboard copy always happens regardless of this setting.
;
;   Enabled  →  MsgBox shows Hex, RGB, and coordinates after closing (default)
;   Disabled →  Picker closes silently, values are copied to clipboard
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
ColorPickerMsgBox := true   ; Enabled: show summary MsgBox (default)
; ColorPickerMsgBox := false  ; Disabled: close silently
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; =====================================================================================
; CONFIG: LINE NAVIGATION
; =====================================================================================
;
; >> Ctrl+Alt+Left/Right moves to start/end of line.
; >> Shift+Alt+Left/Right selects to start/end of line.
; >> Shift+Alt+Backspace/Delete deletes to start/end of line.
;
;   Enabled  →  Line navigation hotkeys are active (default)
;   Disabled →  Line navigation hotkeys do nothing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
LineNavEnabled := true   ; Enabled: hotkeys are active (default)
; LineNavEnabled := false  ; Disabled: hotkeys do nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; =========================================================
; CONFIG: TIMEZONE LIST
; =========================================================
;
; >> Uncomment both lines to add to cycle
; >> comment both out to remove.
;
;
; ========================================================= TIMEZONE LIST =========================================================


; -------------------- UTC --------------------
; TZData["UTC"] := "(UTC +0) `"UTC`""
; TZOrder.Push("UTC")

; -------------------- GMT/London --------------------
; TZData["GMT Standard Time"] := "(UTC +0) `"London`""
; TZOrder.Push("GMT Standard Time")

; -------------------- Berlin/Paris--------------------
TZData["W. Europe Standard Time"] := "(UTC +1) `"Berlin / Paris`""
TZOrder.Push("W. Europe Standard Time")

; -------------------- Cairo --------------------
; TZData["Egypt Standard Time"] := "(UTC +2) `"Cairo`""
; TZOrder.Push("Egypt Standard Time")

; -------------------- Riyadh --------------------
; TZData["Arab Standard Time"] := "(UTC +3) `"Riyadh`""
; TZOrder.Push("Arab Standard Time")

; -------------------- Moscow--------------------
TZData["Russian Standard Time"] := "(UTC +3) `"Moscow`""
TZOrder.Push("Russian Standard Time")

; -------------------- Tehran --------------------
; TZData["Iran Standard Time"] := "(UTC +3:30) `"Tehran`""
; TZOrder.Push("Iran Standard Time")

; -------------------- Dubai --------------------
; TZData["Arabian Standard Time"] := "(UTC +4) `"Dubai`""
; TZOrder.Push("Arabian Standard Time")

; -------------------- Kabul --------------------
; TZData["Afghanistan Standard Time"] := "(UTC +4:30) `"Kabul`""
; TZOrder.Push("Afghanistan Standard Time")

; -------------------- Karachi --------------------
; TZData["Pakistan Standard Time"] := "(UTC +5) `"Karachi`""
; TZOrder.Push("Pakistan Standard Time")

; -------------------- India --------------------
; TZData["India Standard Time"] := "(UTC +5:30) `"India`""
; TZOrder.Push("India Standard Time")

; -------------------- Dhaka --------------------
; TZData["Bangladesh Standard Time"] := "(UTC +6) `"Dhaka`""
; TZOrder.Push("Bangladesh Standard Time")

; -------------------- Bangkok/Jakarta --------------------
; TZData["SE Asia Standard Time"] := "(UTC +7) `"Bangkok / Jakarta`""
; TZOrder.Push("SE Asia Standard Time")

; -------------------- Beijing --------------------
; TZData["China Standard Time"] := "(UTC +8) `"Beijing`""
; TZOrder.Push("China Standard Time")

; -------------------- Singapore --------------------
; TZData["Singapore Standard Time"] := "(UTC +8) `"Singapore`""
; TZOrder.Push("Singapore Standard Time")

; -------------------- Tokyo--------------------
TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
TZOrder.Push("Tokyo Standard Time")

; -------------------- Sydney--------------------
TZData["AUS Eastern Standard Time"] := "(UTC +10) `"Sydney`""
TZOrder.Push("AUS Eastern Standard Time")

; -------------------- Auckland --------------------
; TZData["New Zealand Standard Time"] := "(UTC +12) `"Auckland`""
; TZOrder.Push("New Zealand Standard Time")

; -------------------- Azores --------------------
; TZData["Azores Standard Time"] := "(UTC -1) `"Azores`""
; TZOrder.Push("Azores Standard Time")

; -------------------- Cape Verde --------------------
; TZData["Cape Verde Standard Time"] := "(UTC -1) `"Cape Verde`""
; TZOrder.Push("Cape Verde Standard Time")

; -------------------- Buenos Aires --------------------
; TZData["SA Eastern Standard Time"] := "(UTC -3) `"Buenos Aires`""
; TZOrder.Push("SA Eastern Standard Time")

; -------------------- Brasilia --------------------
; TZData["E. South America Standard Time"] := "(UTC -3) `"Brasilia`""
; TZOrder.Push("E. South America Standard Time")

; -------------------- Caracas --------------------
; TZData["Venezuela Standard Time"] := "(UTC -4) `"Caracas`""
; TZOrder.Push("Venezuela Standard Time")

; -------------------- La Paz--------------------
; TZData["SA Western Standard Time"] := "(UTC -4) `"La Paz`""
; TZOrder.Push("SA Western Standard Time")

; -------------------- Eastern Time--------------------
TZData["Eastern Standard Time"] := "(UTC -5) `"Eastern Time`""
TZOrder.Push("Eastern Standard Time")

; -------------------- Central Time --------------------
; TZData["Central Standard Time"] := "(UTC -6) `"Central Time`""
; TZOrder.Push("Central Standard Time")

; -------------------- Mountain Time --------------------
; TZData["Mountain Standard Time"] := "(UTC -7) `"Mountain Time`""
; TZOrder.Push("Mountain Standard Time")

; -------------------- Pacific Time --------------------
; TZData["Pacific Standard Time"] := "(UTC -8) `"Pacific Time`""
; TZOrder.Push("Pacific Standard Time")

; -------------------- Alaska --------------------
; TZData["Alaskan Standard Time"] := "(UTC -9) `"Alaska`""
; TZOrder.Push("Alaskan Standard Time")

; -------------------- Hawaii --------------------
; TZData["Hawaiian Standard Time"] := "(UTC -10) `"Hawaii`""
; TZOrder.Push("Hawaiian Standard Time")


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

if IsSet(StartupTZID)
  RunWait('tzutil /s "' StartupTZID '"',, "Hide")
