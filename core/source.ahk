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

if !IsSet(TZData)
    TZData := Map()
if !IsSet(TZOrder)
    TZOrder := []

#Include config.ahk

if (IsSet(StartupTZID) && StartupTZID != "")
    SetTimer(() => RunWait('tzutil /s "' StartupTZID '"',, "Hide"), -1)

#Include features/numpad-emulator.ahk
#Include features/alt-codes.ahk
#Include features/timezone-switcher.ahk
#Include features/force-kill-task.ahk
#Include features/color-picker.ahk
#Include features/line-navigation.ahk

#HotIf
#^\::
{
    if (A_IconHidden)
        A_IconHidden := 0
    else
        A_IconHidden := 1
}
#HotIf

; STRAP HELP BOX (Win + /)
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
        
        WinSetTransparent(225, helpGuiGlobal.Hwnd)
        
        UpdateHelpBox()
        SetTimer(UpdateHelpBox, 10)
    }
}

UpdateHelpBox() {
    global helpGuiGlobal
    try {
        CoordMode("Mouse", "Screen")
        MouseGetPos(&mX, &mY)
        
        WinGetPos(, , &guiW, &guiH, helpGuiGlobal.Hwnd)
        MonitorGetWorkArea(1, , , &screenW, &screenH)
        
        guiX := Min(mX + 10, screenW - guiW - 2)
        guiY := Min(mY + 10, screenH - guiH - 2)
        
        helpGuiGlobal.Show("NoActivate x" guiX " y" guiY)
    }
}

; GLOBAL HELPER FUNCTIONS
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
    try {
        return RegRead("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation", "TimeZoneKeyName")
    } catch {
        return ""
    }
}
