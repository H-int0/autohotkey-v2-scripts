# Changelog

All notable changes to Strap will be documented here.
Format: [version]: release date, followed by what changed.

---

## Unreleased

- Auto download python and other dependencies
- **Features**
  - Battery Plan Switcher
  - Vim Arrow Keys
  - Move the Selected Word/Line
  - System Temperatures & Fan Speed Monitor
  - Printscreen to Menu button
  - Select Multiple CLipboard
- CLI
  - Add new commands such as '/uninstall --hard', and much more
  - command history

---

## [v0.1.0] 2026-05-23

### Added in [v0.1.0]

- `numpad-emulator.ahk`: standalone CapsLock numpad emulator

- `timezone-switcher.ahk`: standalone timezone switcher

- `source.ahk`: combined script with both features

---

## [v0.2.0] 2026-05-24

### Added in [v0.2.0]

- **Inline configuration instructions** inside all scripts users can now edit settings directly in the file without leaving the editor.
- **Configurable tray icon visibility** choose between hidden (default) or visible on startup via a simple comment toggle.
- **Configurable CapsLock numpad Shift behavior** optionally disable shifted symbols (`! @ # $ % ^ & * ( )`) when CapsLock is on.
- **Custom timezone section** dedicated block with clear instructions to add any Windows timezone ID.
- **Startup timezone selection** force a specific timezone when the script launches, either from a predefined list or a custom ID.
- **Visual edit markers** (`^^^ Edit THE LINES HERE ABOVE ^^^`) to guide users to the exact lines they need to change.

### Changed in [v0.2.0]

- **Expanded inline help** every configurable setting now includes step by step comments.
- **Improved timezone list comments** clearer instructions for uncommenting/commenting entries.
- **Rearranged code structure** configuration blocks moved to the top for easier access.

---

## [v0.3.0] 2026-05-27

### Added in [v0.3.0]

- **Features:**
  1. Force Kill Task
      - closes the focused window and terminates frozen processes that won't exit gracefully.
  2. Color Picker
      - floating, always-on-top overlay that samples screen pixels in real time and displays Hex, RGB, and cursor coordinates.
  3. Line Navigation
      - keyboard shortcuts to jump to the start or end of a line, with selection and deletion variants.
- **Utilities:**
  1. STRAP HELP
      - built-in help reference for Strap shortcuts.
- **Docs:**
  1. CONTRIBUTING.md
  2. FEATURES.md
  3. INTEGRATION_GUIDE.md
  4. LICENSE
  5. ISSUE_TEMPLATE
      - bug-report.md
      - feature_request.md

### Changed in [v0.3.0]

- **Core**
  - All standalone scripts are now fully modular and self-contained.
  - `source.ahk` has been restructured supporting code is now split into `source-dependencies/`.
  - All feature configurations are now centralized in a single `config.ahk`.
  - Every script now includes the MIT License header (required in all scripts going this point in time forward).
- **Timezone Switcher**
  - UTC is no longer set as the active timezone by default.
  - Tooltip display duration is now user-configurable.
  - Tooltips are now screen-bound and will not render outside the visible display area.
- **Tooltips (Global)**
  - Tooltip behavior has been standardized across all features, existing tooltip timing and positioning may appear slightly different from v1.1.0.

---

## [v0.3.1] 2026-05-28

### Changed in [v0.3.1]

- Project license changed to GPL-3.0.
- Added GPL-3.0 license header to every script (required in all scripts as is, going this point in time forward).
- Restructured `distribution/` directory,
  - users can now configure features directly in the source code, eliminating the need for a separate `custom.ahk`.

### Fixed in [v0.3.1]

- Corrected command-line instructions for adding Strap to auto-start on boot.

---

## [v0.3.2] 2026-05-28

### Added in [v0.3.2]

- **Utilities:**
  1. Reload Script
      - reload the script with a single hotkey.
  2. Exit Script
      - exit the script with a single hotkey.
- `source.ahk` now includes inline instructions for selecting which features to load on startup.

### Changed in [v0.3.2]

- **Force Kill**
  - Switched to native `ProcessClose()` for closing the active window.
- **Color Picker**
  - Reduced CPU usage.
  - RGB values are now extracted using bitwise operators.
  - Cursor is now restored via a native `Win32 SPI_SETCURSORS` call.
- **Timezone Switcher**
  - Timezone ID is now read directly from the registry instead of relying on temp files, reducing latency on startup.
- Tooltips now position themselves beside the cursor automatically instead of using a fixed offset.
- Reduced the size of the `>> STRAP HELP` box.
- Removed unused config sections.

---

## [v0.4.0] 2026-06-06

### Added in [v0.4.0]

- **CLI/TUI alpha-v0.1.0 release**
  - Strap now ships with a full Python-based terminal interface for managing everything without touching config files directly.
    - `strap /run`, `/stop`, `/config`, `/profile`, `/install`, `/update`, `/switch`, `/version`, `/uninstall`, `/help`, etc.
    - Config screen with live feature toggles, sub-settings, and pending change tracking
    - Profile system `default`, `ghost`, and named profiles, all persisted across version switches
    - Version management install, archive, and switch between multiple versions locally
    - Startup shortcut management with `/run --cr shr` and `/run --d shr`
    - Command chaining with `^`
    - Auto-save flag (`-!`) for instant headless config changes
    - PowerShell one-liner bootstrapper (`install.ps1`) and `strap.bat` global command

### Changed in [v0.4.0]

- **Repo structure** `distribution/` and `modules/` replaced by `core/` (AHK) and `cli/` (Python).
- **Feature toggling** features are no longer enabled/disabled by commenting `#Include` lines in `source.ahk`. All toggling is now done through `config.ahk` boolean vars controlled with the CLI/TUI.
- **Configuration** Manual configuration is now replaced by the CLI/TUI config system. Settings are managed with `strap /config` instead of editing files directly.
- **ALT Codes** feature is now separated from the numpad-emulator feature for more stability.
- **Timezone list** expanded from 30 to 139 timezones.
- **Startup shortcut** now created and managed by the CLI (`/run --cr shr`) with PowerShell `WScript.Shell` instead of manual steps.
- **Installation** replaced manual clone + double-click setup with a PowerShell one-liner bootstrapper. ZIP fallback still available via `python cli/main.py /install`.

### Fixed in [v0.4.0]

- ALT codes are now more stable
- Fixed Numpad-Emulator breaking after smashing multiple Numrow keys at once.

### Removed in [v0.4.0]

- `distribution/` directory and `modules/` directory system.

### Known Bugs in [v0.4.0]

- Resizing the TUI window spawns multiple cursors
- Command chaining (`^`) does not work in the terminal TUI only
- Commands are whitespace-tolerant (extra spaces between arguments are ignored)

---

## [v0.4.1] 2026-06-06

### Changed in [v0.4.1]

- Reduce Timezone list down to 36.
- Improve Visuals of TUI.
- Change how the Timezone command work by simplifying it to the format `/config -{flag} -{Config No.} "{UTC_+/-OffSet}"`.

### Fixed in [v0.4.1]

- Fix timezone specific commands not working.

---

~*[@H-int0](https://github.com/H-int0)*
