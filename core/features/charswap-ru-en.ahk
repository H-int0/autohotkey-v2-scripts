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

if !IsSet(HelpEntries)
    global HelpEntries := []
if (CharSwapEnabled)
    HelpEntries.Push("
(
> RU-EN CHARSWAP:
    Win+Ctrl+Space  →  swap character
)")

#HotIf CharSwapEnabled

; Hotkey: Win + Ctrl + Space
#^Space::
{
    SavedClip := ClipboardAll()

    A_Clipboard := ""
    Send "^c"

    if !ClipWait(0.5) {
        A_Clipboard := SavedClip
        return
    }

    OriginalText := A_Clipboard
    ConvertedText := Transliterate(OriginalText)

    if (ConvertedText == OriginalText) {
        A_Clipboard := SavedClip
        return
    }

    A_Clipboard := ConvertedText
    ClipWait(0.5)

    Send "^v"
    Sleep 150

    A_Clipboard := SavedClip
}

#HotIf

; --- Core Transliteration Logic ---
; TransMap stores all three case variants explicitly.
; Pattern is case-sensitive (no i flag); upper/lower/title tokens each have their own entry.

Transliterate(Text) {
    static TransMap := Map(
        ; --- Latin -> Cyrillic (multi-char) ---
        "shch", "щ",  "Shch", "Щ",  "SHCH", "Щ",
        "sh",   "ш",  "Sh",   "Ш",  "SH",   "Ш",
        "ch",   "ч",  "Ch",   "Ч",  "CH",   "Ч",
        "zh",   "ж",  "Zh",   "Ж",  "ZH",   "Ж",
        "ya",   "я",  "Ya",   "Я",  "YA",   "Я",
        "yu",   "ю",  "Yu",   "Ю",  "YU",   "Ю",
        "yo",   "ё",  "Yo",   "Ё",  "YO",   "Ё",
        "ts",   "ц",  "Ts",   "Ц",  "TS",   "Ц",
        "kh",   "х",  "Kh",   "Х",  "KH",   "Х",
        "eh",   "э",  "Eh",   "Э",  "EH",   "Э",

        ; --- Latin -> Cyrillic (single, lowercase) ---
        "a", "а",  "b", "б",  "v", "в",  "g", "г",  "d", "д",
        "e", "е",  "z", "з",  "i", "и",  "j", "й",  "k", "к",
        "l", "л",  "m", "м",  "n", "н",  "o", "о",  "p", "п",
        "r", "р",  "s", "с",  "t", "т",  "u", "у",  "f", "ф",
        "y", "ы",  "c", "ц",  "h", "х",
        "x", "х",  "w", "в",  "q", "к",

        ; --- Latin -> Cyrillic (single, uppercase) ---
        "A", "А",  "B", "Б",  "V", "В",  "G", "Г",  "D", "Д",
        "E", "Е",  "Z", "З",  "I", "И",  "J", "Й",  "K", "К",
        "L", "Л",  "M", "М",  "N", "Н",  "O", "О",  "P", "П",
        "R", "Р",  "S", "С",  "T", "Т",  "U", "У",  "F", "Ф",
        "Y", "Ы",  "C", "Ц",  "H", "Х",
        "X", "Х",  "W", "В",  "Q", "К",

        ; --- Cyrillic -> Latin (lowercase) ---
        "а", "a",  "б", "b",  "в", "v",  "г", "g",  "д", "d",
        "е", "e",  "ё", "yo", "ж", "zh", "з", "z",  "и", "i",
        "й", "j",  "к", "k",  "л", "l",  "м", "m",  "н", "n",
        "о", "o",  "п", "p",  "р", "r",  "с", "s",  "т", "t",
        "у", "u",  "ф", "f",  "х", "kh", "ц", "ts", "ч", "ch",
        "ш", "sh", "щ", "shch", "ы", "y", "э", "eh", "ю", "yu",
        "я", "ya", "ь", "",   "ъ", "",

        ; --- Cyrillic -> Latin (uppercase) ---
        "А", "A",  "Б", "B",  "В", "V",  "Г", "G",  "Д", "D",
        "Е", "E",  "Ё", "Yo", "Ж", "Zh", "З", "Z",  "И", "I",
        "Й", "J",  "К", "K",  "Л", "L",  "М", "M",  "Н", "N",
        "О", "O",  "П", "P",  "Р", "R",  "С", "S",  "Т", "T",
        "У", "U",  "Ф", "F",  "Х", "Kh", "Ц", "Ts", "Ч", "Ch",
        "Ш", "Sh", "Щ", "Shch", "Ы", "Y", "Э", "Eh", "Ю", "Yu",
        "Я", "Ya", "Ь", "",   "Ъ", ""
    )

    ; Case-sensitive pattern — no i flag.
    ; Multi-char sequences listed for all three case variants before single chars.
    static Pattern := "(*UCP)(shch|Shch|SHCH|sh|Sh|SH|ch|Ch|CH|zh|Zh|ZH|ya|Ya|YA|yu|Yu|YU|yo|Yo|YO|ts|Ts|TS|kh|Kh|KH|eh|Eh|EH|[a-zA-Z]|[А-ЯЁЪЬа-яёъь])"

    OutText     := ""
    StartingPos := 1

    Loop {
        FoundPos := RegExMatch(Text, Pattern, &Match, StartingPos)
        if !FoundPos
            break

        OutText .= SubStr(Text, StartingPos, FoundPos - StartingPos)

        token := Match[0]

        if TransMap.Has(token) {
            OutText .= TransMap[token]
        } else {
            OutText .= token
        }

        StartingPos := FoundPos + Match.Len
    }

    OutText .= SubStr(Text, StartingPos)
    return OutText
}
