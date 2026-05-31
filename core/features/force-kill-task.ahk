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

if !IsSet(HelpEntries)
    global HelpEntries := []
if (ForceKillEnabled)
    HelpEntries.Push("
(
> FORCE KILL TASK:
    Win+Ctrl+K      →  kill
)")

#HotIf ForceKillEnabled

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
    
    ; Check if the OS has already flagged it as hung
    if (DllCall("IsHungAppWindow", "Ptr", activeHwnd)) {
        isResponding := false
    } else {
        ; Ping the window to see if it's alive
        try {
            SendMessage(0x0, 0, 0,, "ahk_id " activeHwnd,,,, 250)
        } catch {
            isResponding := false
        }
    }

    if (!isResponding) {
        ; Window is frozen: use native ProcessClose to forcefully terminate
        try {
            ProcessClose(pid)
            ShowToolTip(Msg_EndTask)
        }
    } else {
        ; Window is healthy: ask it to close gracefully (Alt+F4 behavior)
        try {
            WinClose("ahk_id " activeHwnd)
            WinWaitClose("ahk_id " activeHwnd,, 5)
            ShowToolTip(Msg_EndTask)
        }
    }
}

#HotIf
