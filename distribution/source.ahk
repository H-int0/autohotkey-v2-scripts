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
;
; ===========================================================================================================================================================================


#Requires AutoHotkey v2.0
#UseHook True
#MaxThreadsBuffer True
ProcessSetPriority "High"


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


; =========================================================
; FEATURE: NUMPAD EMULATOR
; =========================================================

#HotIf GetKeyState("CapsLock", "T") && NumpadShiftSymbols && GetKeyState("Shift", "P")

+1::SendText "!"
+2::SendText "@"
+3::SendText "#"
+4::SendText "$"
+5::SendText "%"
+6::SendText "^"
+7::SendText "&"
+8::SendText "*"
+9::SendText "("
+0::SendText ")"

#HotIf GetKeyState("CapsLock", "T") && (!NumpadShiftSymbols || !GetKeyState("Shift", "P"))

*1::Send '{Blind}{Numpad1}'
*2::Send '{Blind}{Numpad2}'
*3::Send '{Blind}{Numpad3}'
*4::Send '{Blind}{Numpad4}'
*5::Send '{Blind}{Numpad5}'
*6::Send '{Blind}{Numpad6}'
*7::Send '{Blind}{Numpad7}'
*8::Send '{Blind}{Numpad8}'
*9::Send '{Blind}{Numpad9}'
*0::Send '{Blind}{Numpad0}'

#HotIf

; =========================================================
; FEATURE: TIMEZONE SWITCHER
; =========================================================

TZData := Map()
TZOrder := []

; ===================== TIMEZONE LIST =====================
; >> Uncomment both lines to add to cycle
; >> comment both out to remove.
;


; UTC
TZData["UTC"] := "(UTC +0) `"UTC`""
TZOrder.Push("UTC")

; GMT / London
; TZData["GMT Standard Time"] := "(UTC +0) `"London`""
; TZOrder.Push("GMT Standard Time")

; Berlin / Paris
TZData["W. Europe Standard Time"] := "(UTC +1) `"Berlin / Paris`""
TZOrder.Push("W. Europe Standard Time")

; Cairo
; TZData["Egypt Standard Time"] := "(UTC +2) `"Cairo`""
; TZOrder.Push("Egypt Standard Time")

; Riyadh
; TZData["Arab Standard Time"] := "(UTC +3) `"Riyadh`""
; TZOrder.Push("Arab Standard Time")

; Moscow
TZData["Russian Standard Time"] := "(UTC +3) `"Moscow`""
TZOrder.Push("Russian Standard Time")

; Tehran
; TZData["Iran Standard Time"] := "(UTC +3:30) `"Tehran`""
; TZOrder.Push("Iran Standard Time")

; Dubai
; TZData["Arabian Standard Time"] := "(UTC +4) `"Dubai`""
; TZOrder.Push("Arabian Standard Time")

; Kabul
; TZData["Afghanistan Standard Time"] := "(UTC +4:30) `"Kabul`""
; TZOrder.Push("Afghanistan Standard Time")

; Karachi
; TZData["Pakistan Standard Time"] := "(UTC +5) `"Karachi`""
; TZOrder.Push("Pakistan Standard Time")

; India
; TZData["India Standard Time"] := "(UTC +5:30) `"India`""
; TZOrder.Push("India Standard Time")

; Dhaka
; TZData["Bangladesh Standard Time"] := "(UTC +6) `"Dhaka`""
; TZOrder.Push("Bangladesh Standard Time")

; Bangkok / Jakarta
; TZData["SE Asia Standard Time"] := "(UTC +7) `"Bangkok / Jakarta`""
; TZOrder.Push("SE Asia Standard Time")

; Beijing
; TZData["China Standard Time"] := "(UTC +8) `"Beijing`""
; TZOrder.Push("China Standard Time")

; Singapore
; TZData["Singapore Standard Time"] := "(UTC +8) `"Singapore`""
; TZOrder.Push("Singapore Standard Time")

; Tokyo
TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
TZOrder.Push("Tokyo Standard Time")

; Sydney
TZData["AUS Eastern Standard Time"] := "(UTC +10) `"Sydney`""
TZOrder.Push("AUS Eastern Standard Time")

; Auckland
; TZData["New Zealand Standard Time"] := "(UTC +12) `"Auckland`""
; TZOrder.Push("New Zealand Standard Time")

; Azores
; TZData["Azores Standard Time"] := "(UTC -1) `"Azores`""
; TZOrder.Push("Azores Standard Time")

; Cape Verde
; TZData["Cape Verde Standard Time"] := "(UTC -1) `"Cape Verde`""
; TZOrder.Push("Cape Verde Standard Time")

; Buenos Aires
; TZData["SA Eastern Standard Time"] := "(UTC -3) `"Buenos Aires`""
; TZOrder.Push("SA Eastern Standard Time")

; Brasilia
; TZData["E. South America Standard Time"] := "(UTC -3) `"Brasilia`""
; TZOrder.Push("E. South America Standard Time")

; Caracas
; TZData["Venezuela Standard Time"] := "(UTC -4) `"Caracas`""
; TZOrder.Push("Venezuela Standard Time")

; La Paz
; TZData["SA Western Standard Time"] := "(UTC -4) `"La Paz`""
; TZOrder.Push("SA Western Standard Time")

; Eastern Time
TZData["Eastern Standard Time"] := "(UTC -5) `"Eastern Time`""
TZOrder.Push("Eastern Standard Time")

; Central Time
; TZData["Central Standard Time"] := "(UTC -6) `"Central Time`""
; TZOrder.Push("Central Standard Time")

; Mountain Time
; TZData["Mountain Standard Time"] := "(UTC -7) `"Mountain Time`""
; TZOrder.Push("Mountain Standard Time")

; Pacific Time
; TZData["Pacific Standard Time"] := "(UTC -8) `"Pacific Time`""
; TZOrder.Push("Pacific Standard Time")

; Alaska
; TZData["Alaskan Standard Time"] := "(UTC -9) `"Alaska`""
; TZOrder.Push("Alaskan Standard Time")

; Hawaii
; TZData["Hawaiian Standard Time"] := "(UTC -10) `"Hawaii`""
; TZOrder.Push("Hawaiian Standard Time")


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


if IsSet(StartupTZID)
    RunWait('tzutil /s "' StartupTZID '"',, "Hide")


; =========================================================
; LOGIC
; =========================================================

#!`::
{
    currentID := GetCurrentTimeZoneID()
    nextIndex := 1

    Loop TZOrder.Length {
        if (TZOrder[A_Index] = currentID) {
            nextIndex := A_Index + 1
            if (nextIndex > TZOrder.Length)
                nextIndex := 1
            break
        }
    }

    nextID := TZOrder[nextIndex]
    RunWait('tzutil /s "' nextID '"',, "Hide")

    msgLabel := TZData.Has(nextID) ? TZData[nextID] : nextID
    ShowToolTip("Switched TZ = " msgLabel)
}

#^`::
{
    currentID := GetCurrentTimeZoneID()
    msgLabel := TZData.Has(currentID) ? TZData[currentID] : currentID
    ShowToolTip("Current TZ = " msgLabel)
}


; =========================================================
; CONFIG: FORCE KILL TASK
; =========================================================
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


; =========================================================
; CONFIG: COLOR PICKER
; =========================================================
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


; =========================================================
; CONFIG: COLOR PICKER SUMMARY MSGBOX
; =========================================================
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


; =========================================================
; FEATURE: FORCE KILL TASK
; =========================================================

#HotIf EndTaskEnabled
#^k:: {
    activeHwnd := 0
    try {
        activeHwnd := WinGetID("A")
    } catch {
        return
    }
    
    if (!activeHwnd) {
        return
    }
        
    cls := ""
    try {
        cls := WinGetClass("ahk_id " activeHwnd)
    } catch {
        return
    }
    
    if (cls = "Progman" || cls = "WorkerW" || cls = "Shell_TrayWnd") {
        return
    }

    pid := 0
    try {
        pid := WinGetPID("ahk_id " activeHwnd)
    } catch {
        return
    }
    
    if (!pid) {
        return
    }

    isResponding := true
    
    ; 1. Check if the OS has already flagged it as hung
    if (DllCall("IsHungAppWindow", "Ptr", activeHwnd)) {
        isResponding := false
    } else {
        ; 2. Ping the window to see if it's alive
        try {
            ; Send WM_NULL (0x0). If the app's thread is frozen, this will time out.
            SendMessage(0x0, 0, 0,, "ahk_id " activeHwnd,,,, 250)
        } catch {
            ; It failed to respond within 250ms (or closed unexpectedly)
            isResponding := false
        }
    }

    if (!isResponding) {
        ; Window is frozen: use taskkill to forcefully terminate the process
        try {
            RunWait("taskkill /PID " pid " /F",, "Hide")
            ToolTip("Evaporated")
            SetTimer(() => ToolTip(), -2000)
        }
    } else {
        ; Window is healthy: ask it to close gracefully (Alt+F4 behavior)
        try {
            WinClose("ahk_id " activeHwnd)
            WinWaitClose("ahk_id " activeHwnd,, 5)
            ToolTip("Evaporated")
            SetTimer(() => ToolTip(), -2000)
        }
    }
}
#HotIf


; =========================================================
; FEATURE: COLOR PICKER
; =========================================================

#HotIf ColorPickerEnabled
#^c::ToggleColorPicker()
#HotIf

ToggleColorPicker() {
    static isPickerActive := false
    static cpGui := ""
    static resGui := ""
    static cSwatch := "", cHex := "", cRgb := "", cXy := ""
    static lastHex := "", lastRgb := "", lastX := 0, lastY := 0

    if (isPickerActive) {
        SetTimer(UpdateColorPicker, 0)

        if (cpGui) {
            cpGui.Destroy()
            cpGui := ""
        }
        isPickerActive := false

        SetSystemCursor("restore")

        clipText := "Hex: " lastHex "`nRGB: " lastRgb "`nX, Y: (" lastX ", " lastY ")"
        A_Clipboard := clipText

        if (ColorPickerMsgBox) {
            resGui := Gui("+AlwaysOnTop -MinimizeBox -MaximizeBox", "Color Picker Results")
            resGui.Add("Text", "w180", clipText)
            btn := resGui.Add("Button", "w80 x60 y+15 Default", "OK")

            closeGui := (*) => (
                resGui.Destroy(),
                resGui := "",
                ShowToolTip("Copied to Clipboard")
            )

            btn.OnEvent("Click", closeGui)
            resGui.OnEvent("Close", closeGui)
            resGui.OnEvent("Escape", closeGui)

            resGui.Show("AutoSize")
        } else {
            ShowToolTip("Copied to Clipboard")
        }

    } else {
        if (resGui) {
            try resGui.Destroy()
            resGui := ""
        }

        isPickerActive := true

        SetSystemCursor("crosshair")

        cpGui := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20")
        cpGui.BackColor := "202020"

        cSwatch := cpGui.Add("Progress", "x10 y10 w40 h40 c000000", 100)

        cpGui.SetFont("cWhite s10", "Consolas")
        cHex := cpGui.Add("Text", "x60 y8 w150 BackgroundTrans", "hex: #000000")
        cRgb := cpGui.Add("Text", "x60 y23 w150 BackgroundTrans", "rgb: 0, 0, 0")
        cXy  := cpGui.Add("Text", "x60 y38 w150 BackgroundTrans", "(x, y): (0, 0)")

        cpGui.Show("NoActivate Hide")

        UpdateColorPicker()
        SetTimer(UpdateColorPicker, 5)
    }

    UpdateColorPicker() {
        try {
            CoordMode("Mouse", "Screen")
            CoordMode("Pixel", "Screen")

            MouseGetPos(&mX, &mY)
            colorHexRaw := PixelGetColor(mX, mY)
            colorHex := StrLower(SubStr(colorHexRaw, 3))

            r := Integer("0x" SubStr(colorHex, 1, 2))
            g := Integer("0x" SubStr(colorHex, 3, 2))
            b := Integer("0x" SubStr(colorHex, 5, 2))

            lastHex := "#" colorHex
            lastRgb := r ", " g ", " b
            lastX := mX
            lastY := mY

            cSwatch.Opt("c" colorHex)
            cHex.Value := "hex: " lastHex
            cRgb.Value := "rgb: " lastRgb
            cXy.Value  := "(x, y): (" lastX ", " lastY ")"

            cpGui.Show("NoActivate x" (mX + 5) " y" (mY + 5))
        }
    }
}

; =========================================================
; COLOR PICKER HELPER FUNCTION
; =========================================================

SetSystemCursor(mode) {
    static crosshairID := 32515
    static defaultCursors := Map()

    cursorList := [32512, 32513, 32514, 32515, 32516, 32631, 32640,
                   32641, 32642, 32643, 32644, 32645, 32646, 32648,
                   32649, 32650, 32651]

    if (mode = "restore") {
        for id in cursorList {
            if defaultCursors.Has(id) {
                DllCall("User32.dll\SetSystemCursor", "Ptr", defaultCursors[id], "UInt", id)
                defaultCursors.Delete(id)
            }
        }
        return
    }

    if (mode = "crosshair") {
        hCrosshair := DllCall("User32.dll\LoadCursor", "Ptr", 0, "Ptr", crosshairID, "Ptr")
        for id in cursorList {
            hCurrent := DllCall("User32.dll\CopyIcon", "Ptr",
                DllCall("User32.dll\LoadCursor", "Ptr", 0, "Ptr", id, "Ptr"), "Ptr")
            defaultCursors[id] := hCurrent
            DllCall("User32.dll\SetSystemCursor", "Ptr",
                DllCall("User32.dll\CopyIcon", "Ptr", hCrosshair, "Ptr"), "UInt", id)
        }
    }
}


; =========================================================
; ACCESSIBILITY: TOGGLE TRAY ICON (Win + Ctrl + \)
; =========================================================

#^\::
{
    if (A_IconHidden)
        A_IconHidden := 0
    else
        A_IconHidden := 1
}

; =========================================================
; HELPER FUNCTIONS
; =========================================================

GetCurrentTimeZoneID()
{
    tempFile := A_Temp "\tzout.txt"
    if FileExist(tempFile)
        FileDelete(tempFile)

    RunWait(A_ComSpec ' /c "tzutil /g > ' tempFile '"',, "Hide")

    if FileExist(tempFile) {
        out := FileRead(tempFile)
        FileDelete(tempFile)
        return Trim(out, " `t`r`n")
    }
    return ""
}

ShowToolTip(text)
{
    ToolTip(text)
    SetTimer(RemoveToolTip, -3000)
}

RemoveToolTip()
{
    ToolTip()
}
