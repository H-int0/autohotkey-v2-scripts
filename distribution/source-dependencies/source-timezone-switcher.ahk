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

if !IsSet(TZData)
    TZData := Map()
if !IsSet(TZOrder)
    TZOrder := []

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> TIMEZONE SWITCHER:
    Win+Alt+``       →  cycle TZ
    Win+Ctrl+``      →  show current TZ
)")


; =========================================================
; LOGIC
; =========================================================

#!`::
{
    currentID := GetCurrentTimeZoneID()
    nextIndex := 1

    Loop TZOrder.Length {
        if (TZOrder[A_Index] = currentID) {
            nextIndex := A_Index + 1
            if (nextIndex > TZOrder.Length)
                nextIndex := 1
            break
        }
    }

    nextID := TZOrder[nextIndex]
    RunWait('tzutil /s "' nextID '"',, "Hide")

    msgLabel := TZData.Has(nextID) ? TZData[nextID] : nextID
    ShowToolTip("Switched TZ = " msgLabel)
}

#^`::
{
    currentID := GetCurrentTimeZoneID()
    msgLabel := TZData.Has(currentID) ? TZData[currentID] : currentID
    ShowToolTip("Current TZ = " msgLabel)
}
