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

if (TZ_Dateline_Standard_Time)
    TZData["Dateline Standard Time"]                := "(UTC -12) `"International Date Line West`"", TZOrder.Push("Dateline Standard Time")

if (TZ_UTC_11)
    TZData["UTC-11"]                                := "(UTC -11) `"Coordinated Universal Time-11`"", TZOrder.Push("UTC-11")

if (TZ_Hawaiian_Standard_Time)
    TZData["Hawaiian Standard Time"]                := "(UTC -10) `"Hawaii`"", TZOrder.Push("Hawaiian Standard Time")

if (TZ_Marquesas_Standard_Time)
    TZData["Marquesas Standard Time"]               := "(UTC -9:30) `"Marquesas Islands`"", TZOrder.Push("Marquesas Standard Time")

if (TZ_Alaskan_Standard_Time)
    TZData["Alaskan Standard Time"]                 := "(UTC -9) `"Alaska`"", TZOrder.Push("Alaskan Standard Time")

if (TZ_Pacific_Standard_Time)
    TZData["Pacific Standard Time"]                 := "(UTC -8) `"Pacific Time (US & Canada)`"", TZOrder.Push("Pacific Standard Time")

if (TZ_US_Mountain_Standard_Time)
    TZData["US Mountain Standard Time"]             := "(UTC -7) `"Arizona`"", TZOrder.Push("US Mountain Standard Time")

if (TZ_Central_Standard_Time)
    TZData["Central Standard Time"]                 := "(UTC -6) `"Central Time (US & Canada)`"", TZOrder.Push("Central Standard Time")

if (TZ_Eastern_Standard_Time)
    TZData["Eastern Standard Time"]                 := "(UTC -5) `"Eastern Time (US & Canada)`"", TZOrder.Push("Eastern Standard Time")

if (TZ_Atlantic_Standard_Time)
    TZData["Atlantic Standard Time"]                := "(UTC -4) `"Atlantic Time (Canada)`"", TZOrder.Push("Atlantic Standard Time")

if (TZ_Venezuela_Standard_Time)
    TZData["Venezuela Standard Time"]               := "(UTC -4) `"Caracas`"", TZOrder.Push("Venezuela Standard Time")

if (TZ_E_South_America_Standard_Time)
    TZData["E. South America Standard Time"]        := "(UTC -3) `"Brasilia`"", TZOrder.Push("E. South America Standard Time")

if (TZ_Argentina_Standard_Time)
    TZData["Argentina Standard Time"]               := "(UTC -3) `"City of Buenos Aires`"", TZOrder.Push("Argentina Standard Time")

if (TZ_UTC_02)
    TZData["UTC-02"]                                := "(UTC -2) `"Coordinated Universal Time-02`"", TZOrder.Push("UTC-02")

if (TZ_Azores_Standard_Time)
    TZData["Azores Standard Time"]                  := "(UTC -1) `"Azores`"", TZOrder.Push("Azores Standard Time")

if (TZ_GMT_Standard_Time)
    TZData["GMT Standard Time"]                     := "(UTC +0) `"Dublin, Edinburgh, Lisbon, London`"", TZOrder.Push("GMT Standard Time")

if (TZ_W_Europe_Standard_Time)
    TZData["W. Europe Standard Time"]               := "(UTC +1) `"Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna`"", TZOrder.Push("W. Europe Standard Time")

if (TZ_Israel_Standard_Time)
    TZData["Israel Standard Time"]                  := "(UTC +2) `"Jerusalem`"", TZOrder.Push("Israel Standard Time")

if (TZ_Russian_Standard_Time)
    TZData["Russian Standard Time"]                 := "(UTC +3) `"Moscow, St. Petersburg`"", TZOrder.Push("Russian Standard Time")

if (TZ_Iran_Standard_Time)
    TZData["Iran Standard Time"]                    := "(UTC +3:30) `"Tehran`"", TZOrder.Push("Iran Standard Time")

if (TZ_Arabian_Standard_Time)
    TZData["Arabian Standard Time"]                 := "(UTC +4) `"Abu Dhabi, Muscat`"", TZOrder.Push("Arabian Standard Time")

if (TZ_Afghanistan_Standard_Time)
    TZData["Afghanistan Standard Time"]             := "(UTC +4:30) `"Kabul`"", TZOrder.Push("Afghanistan Standard Time")

if (TZ_Pakistan_Standard_Time)
    TZData["Pakistan Standard Time"]                := "(UTC +5) `"Islamabad, Karachi`"", TZOrder.Push("Pakistan Standard Time")

if (TZ_India_Standard_Time)
    TZData["India Standard Time"]                   := "(UTC +5:30) `"Chennai, Mumbai, New Delhi`"", TZOrder.Push("India Standard Time")

if (TZ_Nepal_Standard_Time)
    TZData["Nepal Standard Time"]                   := "(UTC +5:45) `"Kathmandu`"", TZOrder.Push("Nepal Standard Time")

if (TZ_Central_Asia_Standard_Time)
    TZData["Central Asia Standard Time"]            := "(UTC +6) `"Bishkek`"", TZOrder.Push("Central Asia Standard Time")

if (TZ_Myanmar_Standard_Time)
    TZData["Myanmar Standard Time"]                 := "(UTC +6:30) `"Yangon (Rangoon)`"", TZOrder.Push("Myanmar Standard Time")

if (TZ_SE_Asia_Standard_Time)
    TZData["SE Asia Standard Time"]                 := "(UTC +7) `"Bangkok, Hanoi, Jakarta`"", TZOrder.Push("SE Asia Standard Time")

if (TZ_China_Standard_Time)
    TZData["China Standard Time"]                   := "(UTC +8) `"Beijing, Chongqing, Hong Kong, Urumqi`"", TZOrder.Push("China Standard Time")

if (TZ_Tokyo_Standard_Time)
    TZData["Tokyo Standard Time"]                   := "(UTC +9) `"Osaka, Sapporo, Tokyo`"", TZOrder.Push("Tokyo Standard Time")

if (TZ_Cen_Australia_Standard_Time)
    TZData["Cen. Australia Standard Time"]          := "(UTC +9:30) `"Adelaide`"", TZOrder.Push("Cen. Australia Standard Time")

if (TZ_AUS_Eastern_Standard_Time)
    TZData["AUS Eastern Standard Time"]             := "(UTC +10) `"Canberra, Melbourne, Sydney`"", TZOrder.Push("AUS Eastern Standard Time")

if (TZ_Central_Pacific_Standard_Time)
    TZData["Central Pacific Standard Time"]         := "(UTC +11) `"Solomon Is., New Caledonia`"", TZOrder.Push("Central Pacific Standard Time")

if (TZ_New_Zealand_Standard_Time)
    TZData["New Zealand Standard Time"]             := "(UTC +12) `"Auckland, Wellington`"", TZOrder.Push("New Zealand Standard Time")

if (TZ_Tonga_Standard_Time)
    TZData["Tonga Standard Time"]                   := "(UTC +13) `"Nuku'alofa`"", TZOrder.Push("Tonga Standard Time")

if (TZ_Line_Islands_Standard_Time)
    TZData["Line Islands Standard Time"]            := "(UTC +14) `"Kiritimati Island`"", TZOrder.Push("Line Islands Standard Time")
