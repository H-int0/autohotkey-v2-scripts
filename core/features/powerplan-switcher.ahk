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

if (PowerPlanSwitcherEnabled)
    HelpEntries.Push("
(
> POWER PLAN SWITCHER:
    Win+Alt+]       →  cycle power plan
    Win+Ctrl+]      →  show current plan
)")

#HotIf PowerPlanSwitcherEnabled

; --- Hotkeys ---
#!]::CyclePowerPlan()        ; Win + Alt + ] -> Cycle to next power plan
^#]::ShowCurrentPowerPlan()   ; Win + Ctrl + ] -> Show current power plan

#HotIf

; --- Core Functions ---

GetPowerCfgOutput(args) {
    tempFile := A_Temp "\ahk_powercfg_out.txt"
    if FileExist(tempFile) {
        FileDelete(tempFile)
    }
    
    RunWait(A_ComSpec ' /c powercfg ' args ' > "' tempFile '"', , "Hide")
    
    output := ""
    if FileExist(tempFile) {
        output := FileRead(tempFile)
        FileDelete(tempFile)
    }
    return output
}

GetPowerPlans(&plans, &activeIndex) {
    plans := []
    activeIndex := 0
    
    ; Get the active plan's GUID
    activeOutput := GetPowerCfgOutput("/getactivescheme")
    activeGuid := ""
    if RegExMatch(activeOutput, "i)GUID:\s+([a-f0-9-]+)", &activeMatch) {
        activeGuid := activeMatch[1]
    }
    
    ; Get all available power plans
    listOutput := GetPowerCfgOutput("/list")
    
    Loop parse listOutput, "`n", "`r" {
        if RegExMatch(A_LoopField, "i)GUID:\s+([a-f0-9-]+)\s+\((.+?)\)", &match) {
            plan := {guid: match[1], name: match[2]}
            plans.Push(plan)
            
            if (plan.guid = activeGuid) {
                activeIndex := plans.Length
            }
        }
    }
    return plans.Length > 0
}

CyclePowerPlan() {
    if !GetPowerPlans(&plans, &activeIndex) || plans.Length == 0 {
        ShowToolTip("Error: No power plans found.")
        return
    }
    
    nextIndex := Mod(activeIndex, plans.Length) + 1
    nextPlan := plans[nextIndex]
    
    GetPowerCfgOutput("/setactive " nextPlan.guid)
    
    ShowToolTip("Switched PowerPlan = " nextPlan.name)
}

ShowCurrentPowerPlan() {
    if !GetPowerPlans(&plans, &activeIndex) || activeIndex == 0 {
        ShowToolTip("Error: Could not determine current power plan.")
        return
    }
    
    currentPlan := plans[activeIndex]
    ShowToolTip("Current PowerPlan = " currentPlan.name)
}
