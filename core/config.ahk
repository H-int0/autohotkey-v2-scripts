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

A_IconHidden                        := 1
Global Config_TooltipDuration       := 2500

Global NumpadEmulatorEnabled        := 1
Global AltCodesEnabled              := 1
Global TimezoneSwitcherEnabled      := 1
Global ForceKillEnabled             := 1
Global ColorPickerEnabled           := 1
Global LineNavEnabled               := 1
Global VimNavigationEnabled         := 1
Global PowerPlanSwitcherEnabled     := 1
Global CharSwapEnabled              := 1

Global Msg_EndTask                  := "EVAPORATED!"
Global Msg_ColorPicker              := "Copied to Clipboard"

Global ColorPickerMsgBox            := 0

Global VimNavigationUseLeftAlt      := 1
Global VimNavigationUseRightAlt     := 1

#Include config-dependencies\timezones-variables.ahk
#Include config-dependencies\timezones-list.ahk

StartupTZID                         := ""
