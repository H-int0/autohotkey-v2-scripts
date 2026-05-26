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
; CONFIG: NUMPAD SHIFT SYMBOLS
; =========================================================
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
; FEATURE: CAPSLOCK NUMPAD
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
