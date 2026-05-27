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
