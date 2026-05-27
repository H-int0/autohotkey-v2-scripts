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

; ------- Force Kill Task tooltip -------
;
Global Msg_EndTask := "Evaporated"   ; (default-text: "Evaporated")
;                     ^ <-- Edit the text inside the quotes to change the message, or add a semicolon (;) at the beginning of the line to disable this tooltip



; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> FORCE KILL TASK:
    Win+Ctrl+K      →  kill
)")

; =====================================================================================
; CONFIG: FORCE KILL TASK
; =====================================================================================
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
; FEATURE: FORCE KILL TASK (Win + Ctrl + K)
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
        > FORCE KILL TASK:
            Win+Ctrl+K      →  kill
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
