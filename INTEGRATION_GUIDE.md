# Strap Feature Integration Safety Guide

When adding features to `source.ahk`, you must be careful not to disrupt the single-threaded hook model that powers the Numpad Emulator.

If you overload the thread queue, the script will freeze or stop responding to inputs.

---

## Why This Matters

AHK v2 uses a single-threaded hook model. With `#UseHook True` and `#MaxThreadsBuffer True` active, all keyboard hooks share a buffered thread queue. Features that use timers or closures incorrectly can compete with that queue causing hotkeys to drop, mis-fire, or stop working entirely until the script is restarted.

The symptom is always the same: everything works fine in isolation, then breaks under specific input stress (rapid keypresses, held modifiers, simultaneous keys).

---

## The Golden Rules

* **No Nested Timers:** Any `SetTimer` callback must be a **top-level named function**. Nested functions (lambdas/closures) cause thread re-entrancy issues under load.
* **Encapsulate All Hotkeys:** Never define bare hotkeys. Always wrap them in a `#HotIf` / `#HotIf` block to prevent them from bleeding into the Numpad Emulator logic.
* **Use Global State:** Share data via global variables defined at the top of the script. Do not rely on closure-captured statics inside functions. Initialize all feature globals near the top of the script, after the config flags and before any `#HotIf` blocks.
* **Respect the Order:** Do not insert code between the Numpad Emulator’s `#HotIf` blocks. New features must be appended to the end of the file.

---

### Why the Numpad Emulator Is Fragile?

Its `#HotIf` condition is evaluated on every single keypress. Holding Shift and pressing multiple number-row keys rapidly floods the hook queue with simultaneous events. Any competing thread such as a misfired timer callback can corrupt the queue at exactly that moment.

---

## Checklist: Before Integrating

### 1. Timer Logic

Ensure your timer targets a top-level function.

```ahk
; CORRECT
SetTimer(MyTopLevelFunc, 50)

MyTopLevelFunc() {
    ; No scope capture here
}
```

### 2. Hotkey Structure

Wrap hotkeys in a clean `#HotIf` block.

```ahk
#HotIf FeatureEnabled
#^k::DoSomething()
#HotIf ; Always close the block
```

### 3. GUI and Logic Safety

If your feature uses `CoordMode`, `MouseGetPos`, or `PixelGetColor` inside a timer, wrap them in a `try` block. This prevents the script from crashing if the GUI is destroyed while the timer is firing.

---

## Quick Reference

| Pattern | Issue | Fix |
| --- | --- | --- |
| `SetTimer` targeting a nested function | Creates closure re-entrancy | Use a top-level function |
| Bare hotkeys | Intercepts keys globally | Wrap in `#HotIf` |
| Unclosed `#HotIf` | Bleeds context into other hotkeys | Always close with blank `#HotIf` |
| Statics in timer closures | Not thread-safe | Use global variables |
| Code inside Numpad block | Breaks condition routing | Move to end of file |

> **Summary:** If it uses a timer, use a top-level function. If it uses a hotkey, wrap it in a clean `#HotIf` block. Keep all new code after the Numpad Emulator block to ensure stability.

---

~*[@H-int0](https://github.com/H-int0)*
