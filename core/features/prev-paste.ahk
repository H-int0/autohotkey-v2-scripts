#Requires AutoHotkey v2.0

global ClipHistory := []
global IgnoreChange := false

OnClipboardChange ClipChanged

ClipChanged(DataType) {
    global ClipHistory, IgnoreChange
    if (IgnoreChange || DataType == 0)
        return
    ClipHistory.InsertAt(1, ClipboardAll())
    if (ClipHistory.Length > 10)
        ClipHistory.Pop()
}

Loop 9 {
    Hotkey "#^" A_Index, PasteHistory.Bind(A_Index)
}
Hotkey "#^v", PasteHistory.Bind(1)

PasteHistory(Index, *) {
    global ClipHistory, IgnoreChange
    TargetIndex := Index + 1
    if (ClipHistory.Length < TargetIndex)
        return
    IgnoreChange := true
    A_Clipboard := ClipHistory[TargetIndex]
    Sleep 50
    Send "^v"
    Sleep 100
    IgnoreChange := false
}
