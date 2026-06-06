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

global altBuffer := ""

if (!AltCodesEnabled)
    return

; Clear the buffer whenever Alt is initially pressed
~*LAlt::
~*RAlt:: {
    global altBuffer := ""
}

; Capture digits while Alt is held ignore CapsLock state
*!1::AppendToBuffer("1")
*!2::AppendToBuffer("2")
*!3::AppendToBuffer("3")
*!4::AppendToBuffer("4")
*!5::AppendToBuffer("5")
*!6::AppendToBuffer("6")
*!7::AppendToBuffer("7")
*!8::AppendToBuffer("8")
*!9::AppendToBuffer("9")
*!0::AppendToBuffer("0")

AppendToBuffer(val) {
    ; Abort if other modifiers are held so we don't break native OS shortcuts
    if (GetKeyState("Shift", "P") || GetKeyState("Ctrl", "P")
     || GetKeyState("LWin", "P") || GetKeyState("RWin", "P"))
        return

    global altBuffer
    altBuffer .= val
}

; Execute when Alt is physically released
~*LAlt Up::
~*RAlt Up:: {
    global altBuffer
    if (altBuffer = "")
        return

    charToSend := ConvertAltCodeToChar(altBuffer)
    if (charToSend != "")
        Send("{Text}" charToSend)

    altBuffer := ""
}

; =========================================================
; CORE: ALT CODE → CHARACTER
;
; Two conventions Windows supports:
;
;   No leading zero  →  OEM / CP437 (classic DOS alt codes)
;                        1–31   : CP437 symbol glyphs (☺ ♥ ♦ ...)
;                        32–127 : standard ASCII (same in both)
;                        128–255: CP437 extended chars (Ç ü é â ...)
;                        256–1114111: Unicode codepoint via Chr()
;
;   Leading zero     →  ANSI / Windows-1252
;                        0128–0255: Windows-1252 chars (€ ™ © ...)
; =========================================================

ConvertAltCodeToChar(codeStr) {
    try {
        num := Integer(codeStr)
    } catch {
        return ""
    }

    ; Nothing to send for zero or negatives
    if (num <= 0)
        return ""

    hasLeadingZero := (SubStr(codeStr, 1, 1) = "0")

    ; ── No leading zero (OEM / CP437) ────────────────────

    if (!hasLeadingZero) {

        ; Unicode range: 256–1114111 (U+10FFFF max, UTF-16 surrogates excluded)
        if (num > 255) {
            if (num > 1114111 || (num >= 0xD800 && num <= 0xDFFF))
                return ""
            return Chr(num)
        }

        ; CP437 control range 1–31: graphical symbols, not control chars
        if (num <= 31) {
            static cp437 := [
                0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022, 0x25D8,
                0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C, 0x25BA,
                0x25C4, 0x2195, 0x203C, 0x00B6, 0x00A7, 0x25AC, 0x21A8, 0x2191,
                0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC
            ]
            return Chr(cp437[num])
        }

        ; CP437 printable range: 32–255
        buf := Buffer(2, 0)
        NumPut("UChar", num, buf, 0)
        return StrGet(buf, "CP437")
    }

    ; ── Leading zero (ANSI / Windows-1252) ───────────────

    if (num > 255)
        return ""

    buf := Buffer(2, 0)
    NumPut("UChar", num, buf, 0)
    return StrGet(buf, "CP0")
}
