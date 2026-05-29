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
HelpEntries.Push("
(
> LINE NAVIGATION:
    Shift+Alt+ ←/→  →  line start/end
    Shift+Win+ ←/→  →  select to edge
    Alt+Bksp/Del    →  delete to edge
)")

#HotIf true

+!Left::Send  "{Home}"
+!Right::Send "{End}"

+#Left::Send  "+{Home}"
+#Right::Send "+{End}"

!Backspace::Send "+{Home}{Backspace}"
!Delete::Send    "+{End}{Delete}"

#HotIf
