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
#SingleInstance Force

; Activate only when Caps Lock is ON.
#HotIf GetKeyState("CapsLock", "T") && NumpadEmulatorEnabled

1::Send "{Numpad1}"
2::Send "{Numpad2}"
3::Send "{Numpad3}"
4::Send "{Numpad4}"
5::Send "{Numpad5}"
6::Send "{Numpad6}"
7::Send "{Numpad7}"
8::Send "{Numpad8}"
9::Send "{Numpad9}"
0::Send "{Numpad0}"

#HotIf
