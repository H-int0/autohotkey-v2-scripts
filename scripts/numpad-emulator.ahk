#Requires AutoHotkey v2.0
#UseHook True
#MaxThreadsBuffer True
ProcessSetPriority "High"

; =========================================================
; CONFIG: TRAY ICON VISIBILITY
; =========================================================

; Tray icon visibility on startup. Uncomment one.
;
;
A_IconHidden := 1    ; Un-comment for the behaviour to be = Hidden (default)
; A_IconHidden := 0  ; Un-comment for the behaviour to be = Visible

; =========================================================
; CONFIG: NUMPAD SHIFT SYMBOLS
; =========================================================

; What happens when Shift is held with CapsLock ON and a number key is pressed.
;
;   Enabled  →  Shift+numrow types symbols normally:   ! @ # $ % ^ & * ( )
;   Disabled →  Shift+numrow does nothing
;
; Uncomment one.
;
NumpadShiftSymbols := true   ; Enabled: Shift types symbols (default)
; NumpadShiftSymbols := false  ; Disabled: Shift does nothing

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
