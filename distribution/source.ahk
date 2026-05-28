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

SetWorkingDir A_ScriptDir
ProcessSetPriority "High"
#^/::Reload
#+/::ExitApp

; Color Picker globals
global cpGuiGlobal := ""
global cSwatchGlobal := "", cHexGlobal := "", cRgbGlobal := "", cXyGlobal := ""
global lastHexGlobal := "", lastRgbGlobal := "", lastXGlobal := 0, lastYGlobal := 0

; =====================================================================================
; SELECT FEATURES TO LOAD
; =====================================================================================
;
; >> Customize which features are loaded on script startup.
;
; INSTRUCTIONS:
; 1. Uncomment the lines of the features you want to enable.
; 2. Comment out any features you want to disable by adding a semicolon (;) at the beginning.
; 3. Save the file and reload the script.
;
; =========================================================
;
#Include source-dependencies/config.ahk                  ; Core settings (Required)

#Include source-dependencies/source-numpad-emulator.ahk    ; Numpad Emulator feature
#Include source-dependencies/source-timezone-switcher.ahk  ; Timezone Switcher feature
#Include source-dependencies/source-force-kill-task.ahk    ; Force Kill Task feature
#Include source-dependencies/source-color-picker.ahk       ; Color Picker feature
#Include source-dependencies/source-line-navigation.ahk    ; Line Navigation feature
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;

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
        
        helpText := ">> STRAP HELP`n"
        helpText .= "──────────────────────────────────────────`n"
        for entry in HelpEntries
        helpText .= entry . "`n──────────────────────────────────────────`n"
        helpText .= "> TRAY ICON:`n    Win+Ctrl+\      →  toggle tray icon`n"
        helpText .= "──────────────────────────────────────────`n"
        helpText .= "> RELOAD:`n    Win+Ctrl+/      →  reload script`n"
        helpText .= "──────────────────────────────────────────`n"
        helpText .= "> EXIT:`n    Win+Shift+/     →  exit script`n"
        helpText .= "──────────────────────────────────────────`n"
        helpText .= "> HELPER:`n    Win+/           →  toggle STRAP HELP"
        
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
