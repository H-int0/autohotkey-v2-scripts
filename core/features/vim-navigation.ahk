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

if (!VimNavigationUseLeftAlt && !VimNavigationUseRightAlt)
    VimNavigationEnabled := 0

if VimNavigationEnabled
{
    if (VimNavigationUseLeftAlt && VimNavigationUseRightAlt)
    {
        HelpEntries.Push("
(
> VIM ARROWS:
    Alt+H/J/K/L     → (← ↓ ↑ →)
)")
    }
    else if VimNavigationUseLeftAlt
    {
        HelpEntries.Push("
(
> VIM ARROWS:
    LAlt+H/J/K/L    → (← ↓ ↑ →)
)")
    }
    else if VimNavigationUseRightAlt
    {
        HelpEntries.Push("
(
> VIM ARROWS:
    RAlt+H/J/K/L    → (← ↓ ↑ →)
)")
    }
}

; ================================================================
; for LALT
; ================================================================

#HotIf VimNavigationEnabled && VimNavigationUseLeftAlt
; Standard Movement
<!h::Send "{Left}"
<!j::Send "{Down}"
<!k::Send "{Up}"
<!l::Send "{Right}"

; Shift + Movement (Highlight text)
+<!h::Send "+{Left}"
+<!j::Send "+{Down}"
+<!k::Send "+{Up}"
+<!l::Send "+{Right}"

; Ctrl + Movement (Jump words/paragraphs)
^<!h::Send "^{Left}"
^<!j::Send "^{Down}"
^<!k::Send "^{Up}"
^<!l::Send "^{Right}"

; Ctrl + Shift + Movement (Highlight while jumping words)
+^<!h::Send "+^{Left}"
+^<!j::Send "+^{Down}"
+^<!k::Send "+^{Up}"
+^<!l::Send "+^{Right}"
#HotIf

; ================================================================
; for RALT
; ================================================================

#HotIf VimNavigationEnabled && VimNavigationUseRightAlt
; Standard Movement
>!h::Send "{Left}"
>!j::Send "{Down}"
>!k::Send "{Up}"
>!l::Send "{Right}"

; Shift + Movement (Highlight text)
+>!h::Send "+{Left}"
+>!j::Send "+{Down}"
+>!k::Send "+{Up}"
+>!l::Send "+{Right}"

; Ctrl + Movement (Jump words/paragraphs)
^>!h::Send "^{Left}"
^>!j::Send "^{Down}"
^>!k::Send "^{Up}"
^>!l::Send "^{Right}"

; Ctrl + Shift + Movement (Highlight while jumping words)
+^>!h::Send "+^{Left}"
+^>!j::Send "+^{Down}"
+^>!k::Send "+^{Up}"
+^>!l::Send "+^{Right}"
#HotIf
