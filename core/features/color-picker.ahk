; GNU GENERAL PUBLIC LICENSE
;
; Copyright (C) 2026 H-int0
; GitHub: <https://github.com/H-int0/>
; License: <https://github.com/H-int0/autohotkey-v2-scripts/blob/main/LICENSE/>
;
; This program is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with this program.  If not, see <https://www.gnu.org/licenses/>.

; ====================================================================================

#Requires AutoHotkey v2.0

if !IsSet(HelpEntries)
    global HelpEntries := []
if (ColorPickerEnabled)
    HelpEntries.Push("
(
> COLOR PICKER:
    Win+Ctrl+C      →  toggle picker
)")

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
        SetTimer(UpdateColorPicker, 20)
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

        colorNum := Integer(colorHexRaw)
        r := (colorNum >> 16) & 0xFF
        g := (colorNum >> 8) & 0xFF
        b := colorNum & 0xFF

        lastHexGlobal := "#" colorHex
        lastRgbGlobal := r ", " g ", " b
        lastXGlobal := mX
        lastYGlobal := mY

        cSwatchGlobal.Opt("Background" colorHex)
        cSwatchGlobal.Redraw()
        cHexGlobal.Value := "hex: " lastHexGlobal
        cRgbGlobal.Value := "rgb: " lastRgbGlobal
        cXyGlobal.Value  := "(x, y): (" lastXGlobal ", " lastYGlobal ")"

        WinGetPos(, , &guiW, &guiH, cpGuiGlobal)
        MonitorGetWorkArea(1, , , &screenW, &screenH)
        guiX := Min(mX + 5, screenW - guiW - 2)
        guiY := Min(mY + 5, screenH - guiH - 2)

        cpGuiGlobal.Show("NoActivate x" guiX " y" guiY)
    }
}

; COLOR PICKER HELPER FUNCTION
SetSystemCursor(mode) {
    static crosshairID := 32515
    static defaultCursors := Map()

    cursorList := [32512, 32513, 32514, 32515, 32516, 32631, 32640,
                   32641, 32642, 32643, 32644, 32645, 32646, 32648,
                   32649, 32650, 32651]

    if (mode = "restore") {
        DllCall("SystemParametersInfo", "UInt", 0x0057, "UInt", 0, "Ptr", 0, "UInt", 0)
        defaultCursors.Clear()
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
