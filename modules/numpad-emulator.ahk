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


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> NUMPAD EMULATOR:
    CapsLock OFF    →  num-row keys
    CapsLock ON     →  numpad keys
)")

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
