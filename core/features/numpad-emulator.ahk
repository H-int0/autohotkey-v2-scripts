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

; ====================================================================================

#Requires AutoHotkey v2.0
#SingleInstance Force
#MaxThreadsPerHotkey 1
#MaxThreadsBuffer True

if !IsSet(HelpEntries)
    global HelpEntries := []
if (NumpadEmulatorEnabled)
    HelpEntries.Push("
(
> NUMPAD EMULATOR:
    CapsLock OFF    →  num-row keys
    CapsLock ON     →  numpad keys
)")

global _numpadOn := false
_numpadOn := GetKeyState("CapsLock", "T")

~CapsLock:: {
    global _numpadOn
    _numpadOn := !_numpadOn
}

; Activate only when Caps Lock is ON.
#HotIf _numpadOn && NumpadEmulatorEnabled

1::SendEvent "{Blind}{Numpad1}"
2::SendEvent "{Blind}{Numpad2}"
3::SendEvent "{Blind}{Numpad3}"
4::SendEvent "{Blind}{Numpad4}"
5::SendEvent "{Blind}{Numpad5}"
6::SendEvent "{Blind}{Numpad6}"
7::SendEvent "{Blind}{Numpad7}"
8::SendEvent "{Blind}{Numpad8}"
9::SendEvent "{Blind}{Numpad9}"
0::SendEvent "{Blind}{Numpad0}"

#HotIf
