# Changelog

All notable changes to Strap will be documented here.
Format: [version]: release date, followed by what changed.

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

~*[@H-int0](https://github.com/H-int0)*
