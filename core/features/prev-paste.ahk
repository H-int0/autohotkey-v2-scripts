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

global ClipHistory := []
global IgnoreChange := false

if (PrevPasteEnabled)
    HelpEntries.Push("
(
> PREV PASTE:
    Win+Ctrl+V      →  paste prev item
    Ctrl+Alt+1-9    →  paste Nth prev item
)")

OnClipboardChange ClipChanged

ClipChanged(DataType) {
    global ClipHistory, IgnoreChange
    if (IgnoreChange || DataType == 0)
        return
    ClipHistory.InsertAt(1, ClipboardAll())
    if (ClipHistory.Length > 10)
        ClipHistory.Pop()
}

#HotIf PrevPasteEnabled

Loop 9 {
    Hotkey "^!" A_Index, PasteHistory.Bind(A_Index)
}
Hotkey "#^v", PasteHistory.Bind(1)

#HotIf 

PasteHistory(Index, *) {
    global ClipHistory, IgnoreChange
    TargetIndex := Index + 1
    if (ClipHistory.Length < TargetIndex)
        return
    SavedClip := ClipHistory[1]
    IgnoreChange := true
    A_Clipboard := ClipHistory[TargetIndex]
    Sleep 50
    Send "^v"
    Sleep 100
    A_Clipboard := SavedClip
    Sleep 50
    IgnoreChange := false
}
