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

~*[@H-int0](https://github.com/H-int0)*
