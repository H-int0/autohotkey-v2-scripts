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


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

; =========================================================
; CONFIG: END TASK
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
; FEATURE: END TASK
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

; ===========================================================================================================================================================================
; >> COPY ABOVE THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================


; =========================================================
; Accessibility: TOGGLE TRAY ICON (Win + Ctrl + \)
; =========================================================

#^\::
{
    if (A_IconHidden)
        A_IconHidden := 0
    else
        A_IconHidden := 1
}
