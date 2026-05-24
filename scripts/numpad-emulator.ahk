#Requires AutoHotkey v2.0
#UseHook True
#MaxThreadsBuffer True
ProcessSetPriority "High"

; =========================================================
; CONFIGURATION
; =========================================================

; Tray icon visibility on startup. Uncomment one.
;
;
A_IconHidden := 1    ; Un-comment for the behaviour to be = Hidden (default)
; A_IconHidden := 0  ; Un-comment for the behaviour to be = Visible

; =========================================================
; FEATURE: CAPSLOCK NUMPAD
; =========================================================

#HotIf GetKeyState("CapsLock", "T")

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
