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
#UseHook True
#MaxThreadsBuffer True
ProcessSetPriority "High"

; Color Picker globals
global cpGuiGlobal := ""
global cSwatchGlobal := "", cHexGlobal := "", cRgbGlobal := "", cXyGlobal := ""
global lastHexGlobal := "", lastRgbGlobal := "", lastXGlobal := 0, lastYGlobal := 0


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


; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> COLOR PICKER:
    Win+Ctrl+C      →  toggle picker
)")

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


; =========================================================
; FEATURE: COLOR PICKER (Win + Ctrl + C)
; =========================================================

#HotIf ColorPickerEnabled
#^c::ToggleColorPicker()
#HotIf

ToggleColorPicker() {
    global cpGuiGlobal, cSwatchGlobal, cHexGlobal, cRgbGlobal, cXyGlobal
    global lastHexGlobal, lastRgbGlobal, lastXGlobal, lastYGlobal
    static isPickerActive := false
    static resGui := ""

    if (isPickerActive) {
        SetTimer(UpdateColorPicker, 0)

        if (cpGuiGlobal) {
            cpGuiGlobal.Destroy()
            cpGuiGlobal := ""
        }
        isPickerActive := false

        SetSystemCursor("restore")

        clipText := "Hex: " lastHexGlobal "`nRGB: " lastRgbGlobal "`nX, Y: (" lastXGlobal ", " lastYGlobal ")"
        A_Clipboard := clipText

        if (ColorPickerMsgBox) {
            resGui := Gui("+AlwaysOnTop -MinimizeBox -MaximizeBox", "Color Picker Results")
            resGui.Add("Text", "w180", clipText)
            btn := resGui.Add("Button", "w80 x60 y+15 Default", "OK")

            closeGui := (*) => (
                resGui.Destroy(),
                resGui := "",
                ShowToolTip(Msg_ColorPicker)
            )

            btn.OnEvent("Click", closeGui)
            resGui.OnEvent("Close", closeGui)
            resGui.OnEvent("Escape", closeGui)

            resGui.Show("AutoSize")
        } else {
            ShowToolTip(Msg_ColorPicker)
        }

    } else {
        if (resGui) {
            try resGui.Destroy()
            resGui := ""
        }

        isPickerActive := true

        SetSystemCursor("crosshair")

        cpGuiGlobal := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20")
        cpGuiGlobal.BackColor := "202020"

        cpGuiGlobal.MarginX := 6
        cpGuiGlobal.MarginY := 6

        cSwatchGlobal := cpGuiGlobal.Add("Text", "x6 y6 w44 h44 Background000000")

        cpGuiGlobal.SetFont("cWhite s10", "Consolas")
        cHexGlobal := cpGuiGlobal.Add("Text", "x56 y5 w140 BackgroundTrans", "hex: #000000")
        cRgbGlobal := cpGuiGlobal.Add("Text", "x56 y20 w140 BackgroundTrans", "rgb: 0, 0, 0")
        cXyGlobal  := cpGuiGlobal.Add("Text", "x56 y35 w140 BackgroundTrans", "(x, y): (0, 0)")

        cpGuiGlobal.Show("NoActivate Hide")

        UpdateColorPicker()
        SetTimer(UpdateColorPicker, 5)
    }
}

UpdateColorPicker() {
    global cpGuiGlobal, cSwatchGlobal, cHexGlobal, cRgbGlobal, cXyGlobal
    global lastHexGlobal, lastRgbGlobal, lastXGlobal, lastYGlobal
    try {
        CoordMode("Mouse", "Screen")
        CoordMode("Pixel", "Screen")

        MouseGetPos(&mX, &mY)
        colorHexRaw := PixelGetColor(mX, mY)
        colorHex := StrLower(SubStr(colorHexRaw, 3))

        r := Integer("0x" SubStr(colorHex, 1, 2))
        g := Integer("0x" SubStr(colorHex, 3, 2))
        b := Integer("0x" SubStr(colorHex, 5, 2))

        lastHexGlobal := "#" colorHex
        lastRgbGlobal := r ", " g ", " b
        lastXGlobal := mX
        lastYGlobal := mY

        cSwatchGlobal.Opt("Background" colorHex)
        cSwatchGlobal.Redraw()
        cHexGlobal.Value := "hex: " lastHexGlobal
        cRgbGlobal.Value := "rgb: " lastRgbGlobal
        cXyGlobal.Value  := "(x, y): (" lastXGlobal ", " lastYGlobal ")"

        ; Clamp GUI position to stay within screen work area
        WinGetPos(, , &guiW, &guiH, cpGuiGlobal)
        MonitorGetWorkArea(1, , , &screenW, &screenH)
        guiX := Min(mX + 5, screenW - guiW - 2)
        guiY := Min(mY + 5, screenH - guiH - 2)

        cpGuiGlobal.Show("NoActivate x" guiX " y" guiY)
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

; ===========================================================================================================================================================================
; >> COPY ABOVE THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================


; =========================================================
; ACCESSIBILITY: TOGGLE TRAY ICON (Win + Ctrl + \)
; =========================================================

#HotIf
#^\::
{
    if (A_IconHidden)
        A_IconHidden := 0
    else
        A_IconHidden := 1
}
#HotIf

; ===========================================================================================================================================================================

; =========================================================
; STRAP HELP BOX (Win + /)
; =========================================================

global helpGuiGlobal := ""

#HotIf
#/::ToggleHelpBox()
#HotIf

ToggleHelpBox() {
    global helpGuiGlobal
    static isHelpActive := false

    if (isHelpActive) {
        SetTimer(UpdateHelpBox, 0)
        if (helpGuiGlobal) {
            helpGuiGlobal.Destroy()
            helpGuiGlobal := ""
        }
        isHelpActive := false
    } else {
        isHelpActive := true
        
        helpGuiGlobal := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20")
        helpGuiGlobal.BackColor := "000000"
        
        ; Set standard margins and crisp font matching the color picker
        helpGuiGlobal.MarginX := 12
        helpGuiGlobal.MarginY := 12
        helpGuiGlobal.SetFont("cWhite s10", "Consolas")
        
        helpText := "
        (
        >> STRAP HELP
        ───────────────────────────────────────
        > NUMPAD EMULATOR:
            CapsLock OFF    →  num-row keys
            CapsLock ON     →  numpad keys
        ───────────────────────────────────────
        > COLOR PICKER:
            Win+Ctrl+C      →  toggle picker
        ───────────────────────────────────────
        > HELPER:
            Win+/           →  toggle this box
        )"
        
        helpGuiGlobal.Add("Text", "", helpText)
        helpGuiGlobal.Show("NoActivate Hide")
        
        ; Set window transparency opacity (225 out of 255)
        WinSetTransparent(225, helpGuiGlobal.Hwnd)
        
        UpdateHelpBox()
        SetTimer(UpdateHelpBox, 10) ; Live updates every 10ms
    }
}

UpdateHelpBox() {
    global helpGuiGlobal
    try {
        CoordMode("Mouse", "Screen")
        MouseGetPos(&mX, &mY)
        
        ; Fetch UI size and screen boundaries for clamping
        WinGetPos(, , &guiW, &guiH, helpGuiGlobal.Hwnd)
        MonitorGetWorkArea(1, , , &screenW, &screenH)
        
        ; Position bottom-right of cursor, matching color picker logic
        guiX := Min(mX + 10, screenW - guiW - 2)
        guiY := Min(mY + 10, screenH - guiH - 2)
        
        helpGuiGlobal.Show("NoActivate x" guiX " y" guiY)
    }
}

; =========================================================
; GLOBAL HELPER FUNCTIONS
; =========================================================

Global ActiveToolTipText := ""

ShowToolTip(text)
{
    if (text = "")
        return
        
    Global ActiveToolTipText
    ActiveToolTipText := text
    
    SetTimer(TrackToolTipPos, 10)
    SetTimer(RemoveToolTip, -Config_TooltipDuration)
}

TrackToolTipPos()
{
    Global ActiveToolTipText
    static lastX := -1, lastY := -1, lastText := ""
    
    if (ActiveToolTipText = "")
    {
        SetTimer(TrackToolTipPos, 0)
        try ToolTip()
        lastX := -1, lastY := -1, lastText := ""
        return
    }

    try {
        CoordMode("Mouse", "Screen")
        CoordMode("ToolTip", "Screen")
        MouseGetPos(&mX, &mY)
        
        ; Only redraw if the mouse actually moved or the text changed
        if (mX != lastX || mY != lastY || ActiveToolTipText != lastText)
        {
            ToolTip(ActiveToolTipText, mX + 15, mY + 15)
            lastX := mX
            lastY := mY
            lastText := ActiveToolTipText
        }
    }
}

RemoveToolTip()
{
    Global ActiveToolTipText
    ActiveToolTipText := ""
    SetTimer(TrackToolTipPos, 0)
    try ToolTip()
}
