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
; FEATURE 1: CAPSLOCK NUMPAD
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
; FEATURE 2: TIMEZONE SWITCHER
; =========================================================

TZData := Map()
TZOrder := []

; --- TIMEZONE LIST ---
; Uncomment both lines to add to cycle, comment both out to remove.

; UTC
TZData["UTC"] := "(UTC +0) `"UTC`""
TZOrder.Push("UTC")

; GMT / London
; TZData["GMT Standard Time"] := "(UTC +0) `"London`""
; TZOrder.Push("GMT Standard Time")

; Berlin / Paris
TZData["W. Europe Standard Time"] := "(UTC +1) `"Berlin / Paris`""
TZOrder.Push("W. Europe Standard Time")

; Cairo
; TZData["Egypt Standard Time"] := "(UTC +2) `"Cairo`""
; TZOrder.Push("Egypt Standard Time")

; Riyadh
; TZData["Arab Standard Time"] := "(UTC +3) `"Riyadh`""
; TZOrder.Push("Arab Standard Time")

; Moscow
TZData["Russian Standard Time"] := "(UTC +3) `"Moscow`""
TZOrder.Push("Russian Standard Time")

; Tehran
; TZData["Iran Standard Time"] := "(UTC +3:30) `"Tehran`""
; TZOrder.Push("Iran Standard Time")

; Dubai
; TZData["Arabian Standard Time"] := "(UTC +4) `"Dubai`""
; TZOrder.Push("Arabian Standard Time")

; Kabul
; TZData["Afghanistan Standard Time"] := "(UTC +4:30) `"Kabul`""
; TZOrder.Push("Afghanistan Standard Time")

; Karachi
; TZData["Pakistan Standard Time"] := "(UTC +5) `"Karachi`""
; TZOrder.Push("Pakistan Standard Time")

; India
; TZData["India Standard Time"] := "(UTC +5:30) `"India`""
; TZOrder.Push("India Standard Time")

; Dhaka
; TZData["Bangladesh Standard Time"] := "(UTC +6) `"Dhaka`""
; TZOrder.Push("Bangladesh Standard Time")

; Bangkok / Jakarta
; TZData["SE Asia Standard Time"] := "(UTC +7) `"Bangkok / Jakarta`""
; TZOrder.Push("SE Asia Standard Time")

; Beijing
; TZData["China Standard Time"] := "(UTC +8) `"Beijing`""
; TZOrder.Push("China Standard Time")

; Singapore
; TZData["Singapore Standard Time"] := "(UTC +8) `"Singapore`""
; TZOrder.Push("Singapore Standard Time")

; Tokyo
TZData["Tokyo Standard Time"] := "(UTC +9) `"Tokyo`""
TZOrder.Push("Tokyo Standard Time")

; Sydney
TZData["AUS Eastern Standard Time"] := "(UTC +10) `"Sydney`""
TZOrder.Push("AUS Eastern Standard Time")

; Auckland
; TZData["New Zealand Standard Time"] := "(UTC +12) `"Auckland`""
; TZOrder.Push("New Zealand Standard Time")

; Azores
; TZData["Azores Standard Time"] := "(UTC -1) `"Azores`""
; TZOrder.Push("Azores Standard Time")

; Cape Verde
; TZData["Cape Verde Standard Time"] := "(UTC -1) `"Cape Verde`""
; TZOrder.Push("Cape Verde Standard Time")

; Buenos Aires
; TZData["SA Eastern Standard Time"] := "(UTC -3) `"Buenos Aires`""
; TZOrder.Push("SA Eastern Standard Time")

; Brasilia
; TZData["E. South America Standard Time"] := "(UTC -3) `"Brasilia`""
; TZOrder.Push("E. South America Standard Time")

; Caracas
; TZData["Venezuela Standard Time"] := "(UTC -4) `"Caracas`""
; TZOrder.Push("Venezuela Standard Time")

; La Paz
; TZData["SA Western Standard Time"] := "(UTC -4) `"La Paz`""
; TZOrder.Push("SA Western Standard Time")

; Eastern Time
TZData["Eastern Standard Time"] := "(UTC -5) `"Eastern Time`""
TZOrder.Push("Eastern Standard Time")

; Central Time
; TZData["Central Standard Time"] := "(UTC -6) `"Central Time`""
; TZOrder.Push("Central Standard Time")

; Mountain Time
; TZData["Mountain Standard Time"] := "(UTC -7) `"Mountain Time`""
; TZOrder.Push("Mountain Standard Time")

; Pacific Time
; TZData["Pacific Standard Time"] := "(UTC -8) `"Pacific Time`""
; TZOrder.Push("Pacific Standard Time")

; Alaska
; TZData["Alaskan Standard Time"] := "(UTC -9) `"Alaska`""
; TZOrder.Push("Alaskan Standard Time")

; Hawaii
; TZData["Hawaiian Standard Time"] := "(UTC -10) `"Hawaii`""
; TZOrder.Push("Hawaiian Standard Time")

; =========================================================
; CUSTOM TIMEZONES
; =========================================================

; Add your own timezones here. Each entry takes two lines.
;
; Format:
;   TZData["Windows ID"] := "(UTC +X) `"Your Label`""
;   TZOrder.Push("Windows ID")
;
; To find a Windows timezone ID, open Command Prompt and run:
;   tzutil /l
;
; Remove the semicolons from both lines to enable an entry.
; =========================================================

; Your Custom Timezone
; TZData["Your Windows ID Here"] := "(UTC +X) `"Your Label`""
; TZOrder.Push("Your Windows ID Here")
;
; HERE:
;
;
;
;
;

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
; HELPER FUNCTIONS
; =========================================================

GetCurrentTimeZoneID()
{
    tempFile := A_Temp "\tzout.txt"
    if FileExist(tempFile)
        FileDelete(tempFile)

    RunWait(A_ComSpec ' /c "tzutil /g > ' tempFile '"',, "Hide")

    if FileExist(tempFile) {
        out := FileRead(tempFile)
        FileDelete(tempFile)
        return Trim(out, " `t`r`n")
    }
    return ""
}

ShowToolTip(text)
{
    ToolTip(text)
    SetTimer(RemoveToolTip, -3000)
}

RemoveToolTip()
{
    ToolTip()
}
