#Requires AutoHotkey v2.0

if (PowerPlanSwitcherEnabled)
    HelpEntries.Push("
(
> POWER PLAN SWITCHER:
    Win+Alt+]       →  cycle power plan
    Win+Ctrl+]      →  show current plan
)")

; --- Hotkeys ---
#!]::CyclePowerPlan()        ; Win + Alt + ] -> Cycle to next power plan
^#]::ShowCurrentPowerPlan()   ; Win + Ctrl + ] -> Show current power plan

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
