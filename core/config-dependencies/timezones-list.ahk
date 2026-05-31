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

if (TZ_Aleutian_Standard_Time)
    TZData["Aleutian Standard Time"]                := "(UTC -10) `"Aleutian Islands`"", TZOrder.Push("Aleutian Standard Time")

if (TZ_Hawaiian_Standard_Time)
    TZData["Hawaiian Standard Time"]                := "(UTC -10) `"Hawaii`"", TZOrder.Push("Hawaiian Standard Time")

if (TZ_Marquesas_Standard_Time)
    TZData["Marquesas Standard Time"]               := "(UTC -9:30) `"Marquesas Islands`"", TZOrder.Push("Marquesas Standard Time")

if (TZ_Alaskan_Standard_Time)
    TZData["Alaskan Standard Time"]                 := "(UTC -9) `"Alaska`"", TZOrder.Push("Alaskan Standard Time")

if (TZ_UTC_09)
    TZData["UTC-09"]                                := "(UTC -9) `"Coordinated Universal Time-09`"", TZOrder.Push("UTC-09")

if (TZ_Pacific_Standard_Time_Mexico)
    TZData["Pacific Standard Time (Mexico)"]        := "(UTC -8) `"Baja California`"", TZOrder.Push("Pacific Standard Time (Mexico)")

if (TZ_UTC_08)
    TZData["UTC-08"]                                := "(UTC -8) `"Coordinated Universal Time-08`"", TZOrder.Push("UTC-08")

if (TZ_Pacific_Standard_Time)
    TZData["Pacific Standard Time"]                 := "(UTC -8) `"Pacific Time (US & Canada)`"", TZOrder.Push("Pacific Standard Time")

if (TZ_US_Mountain_Standard_Time)
    TZData["US Mountain Standard Time"]             := "(UTC -7) `"Arizona`"", TZOrder.Push("US Mountain Standard Time")

if (TZ_Mountain_Standard_Time_Mexico)
    TZData["Mountain Standard Time (Mexico)"]       := "(UTC -7) `"La Paz, Mazatlan`"", TZOrder.Push("Mountain Standard Time (Mexico)")

if (TZ_Mountain_Standard_Time)
    TZData["Mountain Standard Time"]                := "(UTC -7) `"Mountain Time (US & Canada)`"", TZOrder.Push("Mountain Standard Time")

if (TZ_Yukon_Standard_Time)
    TZData["Yukon Standard Time"]                   := "(UTC -7) `"Yukon`"", TZOrder.Push("Yukon Standard Time")

if (TZ_Central_America_Standard_Time)
    TZData["Central America Standard Time"]         := "(UTC -6) `"Central America`"", TZOrder.Push("Central America Standard Time")

if (TZ_Central_Standard_Time)
    TZData["Central Standard Time"]                 := "(UTC -6) `"Central Time (US & Canada)`"", TZOrder.Push("Central Standard Time")

if (TZ_Easter_Island_Standard_Time)
    TZData["Easter Island Standard Time"]           := "(UTC -6) `"Easter Island`"", TZOrder.Push("Easter Island Standard Time")

if (TZ_Central_Standard_Time_Mexico)
    TZData["Central Standard Time (Mexico)"]        := "(UTC -6) `"Guadalajara, Mexico City, Monterrey`"", TZOrder.Push("Central Standard Time (Mexico)")

if (TZ_Canada_Central_Standard_Time)
    TZData["Canada Central Standard Time"]          := "(UTC -6) `"Saskatchewan`"", TZOrder.Push("Canada Central Standard Time")

if (TZ_SA_Pacific_Standard_Time)
    TZData["SA Pacific Standard Time"]              := "(UTC -5) `"Bogota, Lima, Quito, Rio Branco`"", TZOrder.Push("SA Pacific Standard Time")

if (TZ_Eastern_Standard_Time_Mexico)
    TZData["Eastern Standard Time (Mexico)"]        := "(UTC -5) `"Chetumal`"", TZOrder.Push("Eastern Standard Time (Mexico)")

if (TZ_Eastern_Standard_Time)
    TZData["Eastern Standard Time"]                 := "(UTC -5) `"Eastern Time (US & Canada)`"", TZOrder.Push("Eastern Standard Time")

if (TZ_Haiti_Standard_Time)
    TZData["Haiti Standard Time"]                   := "(UTC -5) `"Haiti`"", TZOrder.Push("Haiti Standard Time")

if (TZ_Cuba_Standard_Time)
    TZData["Cuba Standard Time"]                    := "(UTC -5) `"Havana`"", TZOrder.Push("Cuba Standard Time")

if (TZ_US_Eastern_Standard_Time)
    TZData["US Eastern Standard Time"]              := "(UTC -5) `"Indiana (East)`"", TZOrder.Push("US Eastern Standard Time")

if (TZ_Turks_And_Caicos_Standard_Time)
    TZData["Turks And Caicos Standard Time"]        := "(UTC -5) `"Turks and Caicos`"", TZOrder.Push("Turks And Caicos Standard Time")

if (TZ_Atlantic_Standard_Time)
    TZData["Atlantic Standard Time"]                := "(UTC -4) `"Atlantic Time (Canada)`"", TZOrder.Push("Atlantic Standard Time")

if (TZ_Venezuela_Standard_Time)
    TZData["Venezuela Standard Time"]               := "(UTC -4) `"Caracas`"", TZOrder.Push("Venezuela Standard Time")

if (TZ_Central_Brazilian_Standard_Time)
    TZData["Central Brazilian Standard Time"]       := "(UTC -4) `"Cuiaba`"", TZOrder.Push("Central Brazilian Standard Time")

if (TZ_SA_Western_Standard_Time)
    TZData["SA Western Standard Time"]              := "(UTC -4) `"Georgetown, La Paz, Manaus, San Juan`"", TZOrder.Push("SA Western Standard Time")

if (TZ_Pacific_SA_Standard_Time)
    TZData["Pacific SA Standard Time"]              := "(UTC -4) `"Santiago`"", TZOrder.Push("Pacific SA Standard Time")

if (TZ_Newfoundland_Standard_Time)
    TZData["Newfoundland Standard Time"]            := "(UTC -3:30) `"Newfoundland`"", TZOrder.Push("Newfoundland Standard Time")

if (TZ_Tocantins_Standard_Time)
    TZData["Tocantins Standard Time"]               := "(UTC -3) `"Araguaina`"", TZOrder.Push("Tocantins Standard Time")

if (TZ_Paraguay_Standard_Time)
    TZData["Paraguay Standard Time"]                := "(UTC -3) `"Asuncion`"", TZOrder.Push("Paraguay Standard Time")

if (TZ_E_South_America_Standard_Time)
    TZData["E. South America Standard Time"]        := "(UTC -3) `"Brasilia`"", TZOrder.Push("E. South America Standard Time")

if (TZ_SA_Eastern_Standard_Time)
    TZData["SA Eastern Standard Time"]              := "(UTC -3) `"Cayenne, Fortaleza`"", TZOrder.Push("SA Eastern Standard Time")

if (TZ_Argentina_Standard_Time)
    TZData["Argentina Standard Time"]               := "(UTC -3) `"City of Buenos Aires`"", TZOrder.Push("Argentina Standard Time")

if (TZ_Montevideo_Standard_Time)
    TZData["Montevideo Standard Time"]              := "(UTC -3) `"Montevideo`"", TZOrder.Push("Montevideo Standard Time")

if (TZ_Magallanes_Standard_Time)
    TZData["Magallanes Standard Time"]              := "(UTC -3) `"Punta Arenas`"", TZOrder.Push("Magallanes Standard Time")

if (TZ_Saint_Pierre_Standard_Time)
    TZData["Saint Pierre Standard Time"]            := "(UTC -3) `"Saint Pierre and Miquelon`"", TZOrder.Push("Saint Pierre Standard Time")

if (TZ_Bahia_Standard_Time)
    TZData["Bahia Standard Time"]                   := "(UTC -3) `"Salvador`"", TZOrder.Push("Bahia Standard Time")

if (TZ_UTC_02)
    TZData["UTC-02"]                                := "(UTC -2) `"Coordinated Universal Time-02`"", TZOrder.Push("UTC-02")

if (TZ_Greenland_Standard_Time)
    TZData["Greenland Standard Time"]               := "(UTC -2) `"Greenland`"", TZOrder.Push("Greenland Standard Time")

if (TZ_Azores_Standard_Time)
    TZData["Azores Standard Time"]                  := "(UTC -1) `"Azores`"", TZOrder.Push("Azores Standard Time")

if (TZ_Cape_Verde_Standard_Time)
    TZData["Cape Verde Standard Time"]              := "(UTC -1) `"Cabo Verde Is.`"", TZOrder.Push("Cape Verde Standard Time")

if (TZ_UTC)
    TZData["UTC"]                                   := "(UTC) `"Coordinated Universal Time`"", TZOrder.Push("UTC")

if (TZ_GMT_Standard_Time)
    TZData["GMT Standard Time"]                     := "(UTC +0) `"Dublin, Edinburgh, Lisbon, London`"", TZOrder.Push("GMT Standard Time")

if (TZ_Greenwich_Standard_Time)
    TZData["Greenwich Standard Time"]               := "(UTC +0) `"Monrovia, Reykjavik`"", TZOrder.Push("Greenwich Standard Time")

if (TZ_Sao_Tome_Standard_Time)
    TZData["Sao Tome Standard Time"]                := "(UTC +0) `"Sao Tome`"", TZOrder.Push("Sao Tome Standard Time")

if (TZ_Morocco_Standard_Time)
    TZData["Morocco Standard Time"]                 := "(UTC +1) `"Casablanca`"", TZOrder.Push("Morocco Standard Time")

if (TZ_W_Europe_Standard_Time)
    TZData["W. Europe Standard Time"]               := "(UTC +1) `"Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna`"", TZOrder.Push("W. Europe Standard Time")

if (TZ_Central_Europe_Standard_Time)
    TZData["Central Europe Standard Time"]          := "(UTC +1) `"Belgrade, Bratislava, Budapest, Ljubljana, Prague`"", TZOrder.Push("Central Europe Standard Time")

if (TZ_Romance_Standard_Time)
    TZData["Romance Standard Time"]                 := "(UTC +1) `"Brussels, Copenhagen, Madrid, Paris`"", TZOrder.Push("Romance Standard Time")

if (TZ_Central_European_Standard_Time)
    TZData["Central European Standard Time"]        := "(UTC +1) `"Sarajevo, Skopje, Warsaw, Zagreb`"", TZOrder.Push("Central European Standard Time")

if (TZ_W_Central_Africa_Standard_Time)
    TZData["W. Central Africa Standard Time"]       := "(UTC +1) `"West Central Africa`"", TZOrder.Push("W. Central Africa Standard Time")

if (TZ_GTB_Standard_Time)
    TZData["GTB Standard Time"]                     := "(UTC +2) `"Athens, Bucharest`"", TZOrder.Push("GTB Standard Time")

if (TZ_Middle_East_Standard_Time)
    TZData["Middle East Standard Time"]             := "(UTC +2) `"Beirut`"", TZOrder.Push("Middle East Standard Time")

if (TZ_Egypt_Standard_Time)
    TZData["Egypt Standard Time"]                   := "(UTC +2) `"Cairo`"", TZOrder.Push("Egypt Standard Time")

if (TZ_E_Europe_Standard_Time)
    TZData["E. Europe Standard Time"]               := "(UTC +2) `"Chisinau`"", TZOrder.Push("E. Europe Standard Time")

if (TZ_West_Bank_Standard_Time)
    TZData["West Bank Standard Time"]               := "(UTC +2) `"Gaza, Hebron`"", TZOrder.Push("West Bank Standard Time")

if (TZ_South_Africa_Standard_Time)
    TZData["South Africa Standard Time"]            := "(UTC +2) `"Harare, Pretoria`"", TZOrder.Push("South Africa Standard Time")

if (TZ_FLE_Standard_Time)
    TZData["FLE Standard Time"]                     := "(UTC +2) `"Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius`"", TZOrder.Push("FLE Standard Time")

if (TZ_Israel_Standard_Time)
    TZData["Israel Standard Time"]                  := "(UTC +2) `"Jerusalem`"", TZOrder.Push("Israel Standard Time")

if (TZ_South_Sudan_Standard_Time)
    TZData["South Sudan Standard Time"]             := "(UTC +2) `"Juba`"", TZOrder.Push("South Sudan Standard Time")

if (TZ_Kaliningrad_Standard_Time)
    TZData["Kaliningrad Standard Time"]             := "(UTC +2) `"Kaliningrad`"", TZOrder.Push("Kaliningrad Standard Time")

if (TZ_Sudan_Standard_Time)
    TZData["Sudan Standard Time"]                   := "(UTC +2) `"Khartoum`"", TZOrder.Push("Sudan Standard Time")

if (TZ_Libya_Standard_Time)
    TZData["Libya Standard Time"]                   := "(UTC +2) `"Tripoli`"", TZOrder.Push("Libya Standard Time")

if (TZ_Namibia_Standard_Time)
    TZData["Namibia Standard Time"]                 := "(UTC +2) `"Windhoek`"", TZOrder.Push("Namibia Standard Time")

if (TZ_Jordan_Standard_Time)
    TZData["Jordan Standard Time"]                  := "(UTC +3) `"Amman`"", TZOrder.Push("Jordan Standard Time")

if (TZ_Arabic_Standard_Time)
    TZData["Arabic Standard Time"]                  := "(UTC +3) `"Baghdad`"", TZOrder.Push("Arabic Standard Time")

if (TZ_Syria_Standard_Time)
    TZData["Syria Standard Time"]                   := "(UTC +3) `"Damascus`"", TZOrder.Push("Syria Standard Time")

if (TZ_Turkey_Standard_Time)
    TZData["Turkey Standard Time"]                  := "(UTC +3) `"Istanbul`"", TZOrder.Push("Turkey Standard Time")

if (TZ_Arab_Standard_Time)
    TZData["Arab Standard Time"]                    := "(UTC +3) `"Kuwait, Riyadh`"", TZOrder.Push("Arab Standard Time")

if (TZ_Belarus_Standard_Time)
    TZData["Belarus Standard Time"]                 := "(UTC +3) `"Minsk`"", TZOrder.Push("Belarus Standard Time")

if (TZ_Russian_Standard_Time)
    TZData["Russian Standard Time"]                 := "(UTC +3) `"Moscow, St. Petersburg`"", TZOrder.Push("Russian Standard Time")

if (TZ_E_Africa_Standard_Time)
    TZData["E. Africa Standard Time"]               := "(UTC +3) `"Nairobi`"", TZOrder.Push("E. Africa Standard Time")

if (TZ_Volgograd_Standard_Time)
    TZData["Volgograd Standard Time"]               := "(UTC +3) `"Volgograd`"", TZOrder.Push("Volgograd Standard Time")

if (TZ_Iran_Standard_Time)
    TZData["Iran Standard Time"]                    := "(UTC +3:30) `"Tehran`"", TZOrder.Push("Iran Standard Time")

if (TZ_Arabian_Standard_Time)
    TZData["Arabian Standard Time"]                 := "(UTC +4) `"Abu Dhabi, Muscat`"", TZOrder.Push("Arabian Standard Time")

if (TZ_Astrakhan_Standard_Time)
    TZData["Astrakhan Standard Time"]               := "(UTC +4) `"Astrakhan, Ulyanovsk`"", TZOrder.Push("Astrakhan Standard Time")

if (TZ_Azerbaijan_Standard_Time)
    TZData["Azerbaijan Standard Time"]              := "(UTC +4) `"Baku`"", TZOrder.Push("Azerbaijan Standard Time")

if (TZ_Russia_Time_Zone_3)
    TZData["Russia Time Zone 3"]                    := "(UTC +4) `"Izhevsk, Samara`"", TZOrder.Push("Russia Time Zone 3")

if (TZ_Mauritius_Standard_Time)
    TZData["Mauritius Standard Time"]               := "(UTC +4) `"Port Louis`"", TZOrder.Push("Mauritius Standard Time")

if (TZ_Saratov_Standard_Time)
    TZData["Saratov Standard Time"]                 := "(UTC +4) `"Saratov`"", TZOrder.Push("Saratov Standard Time")

if (TZ_Georgian_Standard_Time)
    TZData["Georgian Standard Time"]                := "(UTC +4) `"Tbilisi`"", TZOrder.Push("Georgian Standard Time")

if (TZ_Caucasus_Standard_Time)
    TZData["Caucasus Standard Time"]                := "(UTC +4) `"Yerevan`"", TZOrder.Push("Caucasus Standard Time")

if (TZ_Afghanistan_Standard_Time)
    TZData["Afghanistan Standard Time"]             := "(UTC +4:30) `"Kabul`"", TZOrder.Push("Afghanistan Standard Time")

if (TZ_West_Asia_Standard_Time)
    TZData["West Asia Standard Time"]               := "(UTC +5) `"Ashgabat, Tashkent`"", TZOrder.Push("West Asia Standard Time")

if (TZ_Qyzylorda_Standard_Time)
    TZData["Qyzylorda Standard Time"]               := "(UTC +5) `"Astana`"", TZOrder.Push("Qyzylorda Standard Time")

if (TZ_Ekaterinburg_Standard_Time)
    TZData["Ekaterinburg Standard Time"]            := "(UTC +5) `"Ekaterinburg`"", TZOrder.Push("Ekaterinburg Standard Time")

if (TZ_Pakistan_Standard_Time)
    TZData["Pakistan Standard Time"]                := "(UTC +5) `"Islamabad, Karachi`"", TZOrder.Push("Pakistan Standard Time")

if (TZ_India_Standard_Time)
    TZData["India Standard Time"]                   := "(UTC +5:30) `"Chennai, Kolkata, Mumbai, New Delhi`"", TZOrder.Push("India Standard Time")

if (TZ_Sri_Lanka_Standard_Time)
    TZData["Sri Lanka Standard Time"]               := "(UTC +5:30) `"Sri Jayawardenepura`"", TZOrder.Push("Sri Lanka Standard Time")

if (TZ_Nepal_Standard_Time)
    TZData["Nepal Standard Time"]                   := "(UTC +5:45) `"Kathmandu`"", TZOrder.Push("Nepal Standard Time")

if (TZ_Central_Asia_Standard_Time)
    TZData["Central Asia Standard Time"]            := "(UTC +6) `"Bishkek`"", TZOrder.Push("Central Asia Standard Time")

if (TZ_Bangladesh_Standard_Time)
    TZData["Bangladesh Standard Time"]              := "(UTC +6) `"Dhaka`"", TZOrder.Push("Bangladesh Standard Time")

if (TZ_Omsk_Standard_Time)
    TZData["Omsk Standard Time"]                    := "(UTC +6) `"Omsk`"", TZOrder.Push("Omsk Standard Time")

if (TZ_Myanmar_Standard_Time)
    TZData["Myanmar Standard Time"]                 := "(UTC +6:30) `"Yangon (Rangoon)`"", TZOrder.Push("Myanmar Standard Time")

if (TZ_SE_Asia_Standard_Time)
    TZData["SE Asia Standard Time"]                 := "(UTC +7) `"Bangkok, Hanoi, Jakarta`"", TZOrder.Push("SE Asia Standard Time")

if (TZ_Altai_Standard_Time)
    TZData["Altai Standard Time"]                   := "(UTC +7) `"Barnaul, Gorno-Altaysk`"", TZOrder.Push("Altai Standard Time")

if (TZ_W_Mongolia_Standard_Time)
    TZData["W. Mongolia Standard Time"]             := "(UTC +7) `"Hovd`"", TZOrder.Push("W. Mongolia Standard Time")

if (TZ_North_Asia_Standard_Time)
    TZData["North Asia Standard Time"]              := "(UTC +7) `"Krasnoyarsk`"", TZOrder.Push("North Asia Standard Time")

if (TZ_N_Central_Asia_Standard_Time)
    TZData["N. Central Asia Standard Time"]         := "(UTC +7) `"Novosibirsk`"", TZOrder.Push("N. Central Asia Standard Time")

if (TZ_Tomsk_Standard_Time)
    TZData["Tomsk Standard Time"]                   := "(UTC +7) `"Tomsk`"", TZOrder.Push("Tomsk Standard Time")

if (TZ_China_Standard_Time)
    TZData["China Standard Time"]                   := "(UTC +8) `"Beijing, Chongqing, Hong Kong, Urumqi`"", TZOrder.Push("China Standard Time")

if (TZ_North_Asia_East_Standard_Time)
    TZData["North Asia East Standard Time"]         := "(UTC +8) `"Irkutsk`"", TZOrder.Push("North Asia East Standard Time")

if (TZ_Singapore_Standard_Time)
    TZData["Singapore Standard Time"]               := "(UTC +8) `"Kuala Lumpur, Singapore`"", TZOrder.Push("Singapore Standard Time")

if (TZ_W_Australia_Standard_Time)
    TZData["W. Australia Standard Time"]            := "(UTC +8) `"Perth`"", TZOrder.Push("W. Australia Standard Time")

if (TZ_Taipei_Standard_Time)
    TZData["Taipei Standard Time"]                  := "(UTC +8) `"Taipei`"", TZOrder.Push("Taipei Standard Time")

if (TZ_Ulaanbaatar_Standard_Time)
    TZData["Ulaanbaatar Standard Time"]             := "(UTC +8) `"Ulaanbaatar`"", TZOrder.Push("Ulaanbaatar Standard Time")

if (TZ_Aus_Central_W_Standard_Time)
    TZData["Aus Central W. Standard Time"]          := "(UTC +8:45) `"Eucla`"", TZOrder.Push("Aus Central W. Standard Time")

if (TZ_Transbaikal_Standard_Time)
    TZData["Transbaikal Standard Time"]             := "(UTC +9) `"Chita`"", TZOrder.Push("Transbaikal Standard Time")

if (TZ_Tokyo_Standard_Time)
    TZData["Tokyo Standard Time"]                   := "(UTC +9) `"Osaka, Sapporo, Tokyo`"", TZOrder.Push("Tokyo Standard Time")

if (TZ_North_Korea_Standard_Time)
    TZData["North Korea Standard Time"]             := "(UTC +9) `"Pyongyang`"", TZOrder.Push("North Korea Standard Time")

if (TZ_Korea_Standard_Time)
    TZData["Korea Standard Time"]                   := "(UTC +9) `"Seoul`"", TZOrder.Push("Korea Standard Time")

if (TZ_Yakutsk_Standard_Time)
    TZData["Yakutsk Standard Time"]                 := "(UTC +9) `"Yakutsk`"", TZOrder.Push("Yakutsk Standard Time")

if (TZ_Cen_Australia_Standard_Time)
    TZData["Cen. Australia Standard Time"]          := "(UTC +9:30) `"Adelaide`"", TZOrder.Push("Cen. Australia Standard Time")

if (TZ_AUS_Central_Standard_Time)
    TZData["AUS Central Standard Time"]             := "(UTC +9:30) `"Darwin`"", TZOrder.Push("AUS Central Standard Time")

if (TZ_E_Australia_Standard_Time)
    TZData["E. Australia Standard Time"]            := "(UTC +10) `"Brisbane`"", TZOrder.Push("E. Australia Standard Time")

if (TZ_AUS_Eastern_Standard_Time)
    TZData["AUS Eastern Standard Time"]             := "(UTC +10) `"Canberra, Melbourne, Sydney`"", TZOrder.Push("AUS Eastern Standard Time")

if (TZ_West_Pacific_Standard_Time)
    TZData["West Pacific Standard Time"]            := "(UTC +10) `"Guam, Port Moresby`"", TZOrder.Push("West Pacific Standard Time")

if (TZ_Tasmania_Standard_Time)
    TZData["Tasmania Standard Time"]                := "(UTC +10) `"Hobart`"", TZOrder.Push("Tasmania Standard Time")

if (TZ_Vladivostok_Standard_Time)
    TZData["Vladivostok Standard Time"]             := "(UTC +10) `"Vladivostok`"", TZOrder.Push("Vladivostok Standard Time")

if (TZ_Lord_Howe_Standard_Time)
    TZData["Lord Howe Standard Time"]               := "(UTC +10:30) `"Lord Howe Island`"", TZOrder.Push("Lord Howe Standard Time")

if (TZ_Bougainville_Standard_Time)
    TZData["Bougainville Standard Time"]            := "(UTC +11) `"Bougainville Island`"", TZOrder.Push("Bougainville Standard Time")

if (TZ_Russia_Time_Zone_10)
    TZData["Russia Time Zone 10"]                   := "(UTC +11) `"Chokurdakh`"", TZOrder.Push("Russia Time Zone 10")

if (TZ_Magadan_Standard_Time)
    TZData["Magadan Standard Time"]                 := "(UTC +11) `"Magadan`"", TZOrder.Push("Magadan Standard Time")

if (TZ_Norfolk_Standard_Time)
    TZData["Norfolk Standard Time"]                 := "(UTC +11) `"Norfolk Island`"", TZOrder.Push("Norfolk Standard Time")

if (TZ_Sakhalin_Standard_Time)
    TZData["Sakhalin Standard Time"]                := "(UTC +11) `"Sakhalin`"", TZOrder.Push("Sakhalin Standard Time")

if (TZ_Central_Pacific_Standard_Time)
    TZData["Central Pacific Standard Time"]         := "(UTC +11) `"Solomon Is., New Caledonia`"", TZOrder.Push("Central Pacific Standard Time")

if (TZ_Russia_Time_Zone_11)
    TZData["Russia Time Zone 11"]                   := "(UTC +12) `"Anadyr, Petropavlovsk-Kamchatsky`"", TZOrder.Push("Russia Time Zone 11")

if (TZ_New_Zealand_Standard_Time)
    TZData["New Zealand Standard Time"]             := "(UTC +12) `"Auckland, Wellington`"", TZOrder.Push("New Zealand Standard Time")

if (TZ_UTC_12)
    TZData["UTC+12"]                                := "(UTC +12) `"Coordinated Universal Time+12`"", TZOrder.Push("UTC+12")

if (TZ_Fiji_Standard_Time)
    TZData["Fiji Standard Time"]                    := "(UTC +12) `"Fiji`"", TZOrder.Push("Fiji Standard Time")

if (TZ_Chatham_Islands_Standard_Time)
    TZData["Chatham Islands Standard Time"]         := "(UTC +12:45) `"Chatham Islands`"", TZOrder.Push("Chatham Islands Standard Time")

if (TZ_UTC_13)
    TZData["UTC+13"]                                := "(UTC +13) `"Coordinated Universal Time+13`"", TZOrder.Push("UTC+13")

if (TZ_Tonga_Standard_Time)
    TZData["Tonga Standard Time"]                   := "(UTC +13) `"Nuku'alofa`"", TZOrder.Push("Tonga Standard Time")

if (TZ_Samoa_Standard_Time)
    TZData["Samoa Standard Time"]                   := "(UTC +13) `"Samoa`"", TZOrder.Push("Samoa Standard Time")

if (TZ_Line_Islands_Standard_Time)
    TZData["Line Islands Standard Time"]            := "(UTC +14) `"Kiritimati Island`"", TZOrder.Push("Line Islands Standard Time")
