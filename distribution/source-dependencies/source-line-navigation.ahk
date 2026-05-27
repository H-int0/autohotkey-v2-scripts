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

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> LINE NAVIGATION:
    Shift+Alt+ ←/→  →  line start/end
    Shift+Win+ ←/→  →  select to edge
    Alt+Bksp/Del    →  delete to edge
)")

; =====================================================================================
; CONFIG: LINE NAVIGATION
; =====================================================================================
;
; >> Ctrl+Alt+Left/Right moves to start/end of line.
; >> Shift+Alt+Left/Right selects to start/end of line.
; >> Shift+Alt+Backspace/Delete deletes to start/end of line.
;
;   Enabled  →  Line navigation hotkeys are active (default)
;   Disabled →  Line navigation hotkeys do nothing
;
; INSTRUCTIONS:
; 1. Uncomment ONLY ONE of the lines below.
; 2. Comment out the other line.
; 3. Save and reload the script.
;
; =========================================================
;
LineNavEnabled := true   ; Enabled: hotkeys are active (default)
; LineNavEnabled := false  ; Disabled: hotkeys do nothing
;
; ^^^^^^^^^^^^^^^ Edit THE LINES HERE ABOVE ^^^^^^^^^^^^^^^
;


; =========================================================
; FEATURE: LINE NAVIGATION
; =========================================================

#HotIf LineNavEnabled

; --- Move (shift+Alt) ---
+!Left::Send  "{Home}"
+!Right::Send "{End}"

; --- Select (Shift+Win) ---
+#Left::Send  "+{Home}"
+#Right::Send "+{End}"

; --- Delete (Alt) ---
!Backspace::Send "+{Home}{Backspace}"
!Delete::Send    "+{End}{Delete}"

#HotIf
