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
;


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
; CONFIG: TOOLTIPS
; =========================================================
;
; >> Customize tooltip display duration and individual messages.
;
; =========================================================
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
; Duration in milliseconds (1000 = 1 sec)
Global Config_TooltipDuration := 3000
;                                ^ <-- Edit this number (in milliseconds) to change how long tooltips stay visible
;
; ---------------------------------------------------------
;
;
; ----- Color Picker tooltip -----
Global Msg_ColorPicker := "Copied to Clipboard"
;                         ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip
;
; ----- Force Kill Task tooltip -----
Global Msg_EndTask := "Evaporated"
;                     ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

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
; FEATURE: COLOR PICKER
; =========================================================

#HotIf ColorPickerEnabled
#^c::ToggleColorPicker()
#HotIf

ToggleColorPicker() {
    static isPickerActive := false
    static cpGui := ""
    static resGui := ""  ; Added to track our custom MsgBox
    static cSwatch := "", cHex := "", cRgb := "", cXy := ""
    static lastHex := "", lastRgb := "", lastX := 0, lastY := 0

    if (isPickerActive) {
        ; --- Second Press: Turn off the picker ---
        SetTimer(UpdateColorPicker, 0)

        if (cpGui) {
            cpGui.Destroy()
            cpGui := ""
        }
        isPickerActive := false

        ; Restore default cursor
        SetSystemCursor("restore")

        ; Build clipboard string (always includes coords)
        clipText := "Hex: " lastHex "`nRGB: " lastRgb "`nX, Y: (" lastX ", " lastY ")"
        A_Clipboard := clipText

        ; Show tooltip — immediately if MsgBox is off, or after dismissal if on
        if (ColorPickerMsgBox) {
            
            ; Create a non-blocking custom GUI to replace the standard MsgBox
            resGui := Gui("+AlwaysOnTop -MinimizeBox -MaximizeBox", "Color Picker Results")
            resGui.Add("Text", "w180", clipText)
            btn := resGui.Add("Button", "w80 x60 y+15 Default", "OK")
            
            ; Function to run when the custom MsgBox is closed
            closeGui := (*) => (
                resGui.Destroy(),
                resGui := "",
                ShowToolTip(Msg_ColorPicker) ; Tooltip fires ONLY after closing
            )
            
            ; Bind the close function to the OK button, the 'X' button, and the Escape key
            btn.OnEvent("Click", closeGui)
            resGui.OnEvent("Close", closeGui)
            resGui.OnEvent("Escape", closeGui)
            
            resGui.Show("AutoSize")
            
        } else {
            ShowToolTip(Msg_ColorPicker) ; Tooltip fires immediately if MsgBox is disabled
        }

    } else {
        ; --- First Press: Turn on the picker ---
        
        ; Close the summary MsgBox if the user left it open from last time
        if (resGui) {
            try resGui.Destroy()
            resGui := ""
        }
        
        isPickerActive := true

        ; Switch cursor to crosshair
        SetSystemCursor("crosshair")

        ; Create GUI: Always on top, no title bar, tool window, click-through (+E0x20)
        cpGui := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20")
        cpGui.BackColor := "202020"
        
        ; Shrink the outer right/bottom margins of the UI
        cpGui.MarginX := 6
        cpGui.MarginY := 6

        ; Color swatch (tighter top/left padding, sized slightly taller to match text)
        cSwatch := cpGui.Add("Text", "x6 y6 w44 h44 Background000000")

        ; Text elements (moved closer to the swatch with tighter line spacing)
        cpGui.SetFont("cWhite s10", "Consolas")
        cHex := cpGui.Add("Text", "x56 y5 w140 BackgroundTrans", "hex: #000000")
        cRgb := cpGui.Add("Text", "x56 y20 w140 BackgroundTrans", "rgb: 0, 0, 0")
        cXy  := cpGui.Add("Text", "x56 y35 w140 BackgroundTrans", "(x, y): (0, 0)")

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

            cSwatch.Opt("Background" colorHex)
            cSwatch.Redraw()  ; <--- This forces the color to actually paint
            cHex.Value := "hex: " lastHex
            cRgb.Value := "rgb: " lastRgb
            cXy.Value  := "(x, y): (" lastX ", " lastY ")"
            
            ; Clamp GUI position to stay within screen work area
            WinGetPos(, , &guiW, &guiH, cpGui)
            MonitorGetWorkArea(1, , , &screenW, &screenH)
            guiX := Min(mX + 5, screenW - guiW - 2)
            guiY := Min(mY + 5, screenH - guiH - 2)

            cpGui.Show("NoActivate x" guiX " y" guiY)
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

; ===========================================================================================================================================================================
; >> COPY ABOVE THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================


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
; FEATURE: HELP BOX (Win + `)
; =========================================================


#`::ToggleHelpBox()

ToggleHelpBox() {
    static isHelpActive := false
    static helpGui := ""

    if (isHelpActive) {
        SetTimer(UpdateHelpBox, 0)
        if (helpGui) {
            helpGui.Destroy()
            helpGui := ""
        }
        isHelpActive := false
    } else {
        isHelpActive := true
        
        helpGui := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20")
        helpGui.BackColor := "000000"
        
        ; Set standard margins and crisp font matching the color picker
        helpGui.MarginX := 12
        helpGui.MarginY := 12
        helpGui.SetFont("cWhite s10", "Consolas")
        

        helpText := "
        (
        >> STRAP HELP
        ───────────────────────────────────────
        > NUMPAD EMULATOR:
            CapsLock OFF    →  num-row keys
            CapsLock ON     →  numpad keys
        ───────────────────────────────────────
        > TIMEZONE SWITCHER:
            Win+Alt+``       →  cycle TZ
            Win+Ctrl+``      →  show current TZ
        ───────────────────────────────────────
        > FORCE KILL TASK:
            Win+Ctrl+K      →  kill
        ───────────────────────────────────────
        > COLOR PICKER:
            Win+Ctrl+C      →  toggle picker
        ───────────────────────────────────────
        > LINE NAVIGATION:
            Ctrl+Alt+ ←/→   →  line start/end
            Shift+Alt+ ←/→  →  select to edge
            Alt+Bksp/Del    →  delete to edge
        ───────────────────────────────────────
        > HELPER:
            Win+``           →  toggle this box
        )"
        
        helpGui.Add("Text", "", helpText)
        helpGui.Show("NoActivate Hide")
        
        ; Set window transparency opacity (225 out of 255)
        WinSetTransparent(225, helpGui.Hwnd)
        
        UpdateHelpBox()
        SetTimer(UpdateHelpBox, 10) ; Live updates every 10ms
    }

    UpdateHelpBox() {
        try {
            CoordMode("Mouse", "Screen")
            MouseGetPos(&mX, &mY)
            
            ; Fetch UI size and screen boundaries for clamping
            WinGetPos(, , &guiW, &guiH, helpGui.Hwnd)
            MonitorGetWorkArea(1, , , &screenW, &screenH)
            
            ; Position bottom-right of cursor, matching color picker logic
            guiX := Min(mX + 10, screenW - guiW - 2)
            guiY := Min(mY + 10, screenH - guiH - 2)
            
            helpGui.Show("NoActivate x" guiX " y" guiY)
        }
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
