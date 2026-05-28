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

; ===========================================================================================================================================================================

#Requires AutoHotkey v2.0
#UseHook True
#MaxThreadsBuffer True

ProcessSetPriority "High"
#^/::Reload
#+/::ExitApp

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
; >> SECTION
; ===========================================================================================================================================================================

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> COLOR PICKER:
    Win+Ctrl+C      →  toggle picker
)")


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


; =========================================================
; FEATURE: COLOR PICKER (Win + Ctrl + C)
; =========================================================

#HotIf true
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
        DllCall("SystemParametersInfo", "UInt", 0x0057, "UInt", 0, "Ptr", 0, "UInt", 0) ; SPI_SETCURSORS
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

; ===========================================================================================================================================================================
; >> SECTION
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
        helpGuiGlobal.SetFont("cWhite s8", "Consolas")
        
        helpText := "
        (
        >> STRAP HELP
        ──────────────────────────────────────────
        > COLOR PICKER:
            Win+Ctrl+C      →  toggle picker
        ──────────────────────────────────────────
        > TRAY ICON:
            Win+Ctrl+\      →  toggle tray icon
        ──────────────────────────────────────────
        > RELOAD:
            Win+Ctrl+/      →  reload script
        ──────────────────────────────────────────
        > EXIT:
            Win+Shift+/     →  exit script
        ──────────────────────────────────────────
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
            ToolTip(ActiveToolTipText)
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
