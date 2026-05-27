# Contributing to STRAP

This document describes the end-to-end pipeline for adding a new feature to Strap, from writing the first line of code to merging into `main`.

---

> [!NOTE]
> Review the [Feature Integration Safety Guide](INTEGRATION_GUIDE.md) for rules on timer patterns, hotkey structure, and thread safety.

---

## Table of contents

- [The Module Template](#the-module-template)
- [Step-by-Step Pipeline](#step-by-step-pipeline)
  - [Step 1: Write the Standalone Module](#step-1-write-the-standalone-module)
  - [Step 2: Test the Standalone Module](#step-2-test-the-standalone-module)
  - [Step 3: Update `custom.ahk` (if needed)](#step-3-update-customahk-if-needed)
  - [Step 4: Test `custom.ahk` with Existing Modules Only](#step-4-test-customahk-with-existing-modules-only)
  - [Step 5: Test `custom.ahk` with the New Module Alone](#step-5-test-customahk-with-the-new-module-alone)
  - [Step 6: Test `custom.ahk` with New Module + All Existing Modules Together](#step-6-test-customahk-with-new-module--all-existing-modules-together)
  - [Step 7: Add New Config Entries to `config.ahk`](#step-7-add-new-config-entries-to-configahk)
  - [Step 8: Write the Source Dependency](#step-8-write-the-source-dependency)
  - [Step 9: Integrate into `source.ahk`](#step-9-integrate-into-sourceahk)
    - [9a. Add globals (if any)](#9a-add-globals-if-any)
    - [9b. Add the `#Include` line](#9b-add-the-include-line)
    - [9c. Update the help box (if `source.ahk` has a hardcoded help text)](#9c-update-the-help-box-if-sourceahk-has-a-hardcoded-help-text)
  - [Step 10: Test `source.ahk`](#step-10-test-sourceahk)
- [Merge the feature to `dev`](#merge-the-feature-to-dev)

## The Module Template

Every standalone module in `modules/` follows the same structure. Here it is as a skeleton use this when writing any new feature:

```ahk
; MIT License...
; ...

; ===========================================================================================================================================================================

#Requires AutoHotkey v2.0
#UseHook True
#MaxThreadsBuffer True
ProcessSetPriority "High"


; =====================================================================================
; CONFIG: TRAY ICON VISIBILITY
; =====================================================================================
; ...
A_IconHidden := 1
; A_IconHidden := 0...


; ===========================================================================================================================================================================
; >> COPY BELOW THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================

if !IsSet(HelpEntries)
    global HelpEntries := []
HelpEntries.Push("
(
> FEATURE NAME:
    Hotkey   →  description
)")

; =====================================================================================
; CONFIG: FEATURE NAME
; =====================================================================================
;
; ...
;
FeatureEnabled := true
; FeatureEnabled := false...


; =========================================================
; FEATURE: FEATURE NAME
; =========================================================

#HotIf FeatureEnabled

; ... hotkeys and logic here ...

#HotIf

; ===========================================================================================================================================================================
; >> COPY ABOVE THIS LINE INTO YOUR CUSTOM SCRIPT
; ===========================================================================================================================================================================


; =========================================================
; ACCESSIBILITY: TOGGLE TRAY ICON (Win + Ctrl + \)
; =========================================================

#HotIf
#^\::
{
    if (A_IconHidden)
        A_IconHidden := 0
    else
        A_IconHidden := 1
}
#HotIf

; ===========================================================================================================================================================================

; =========================================================
; STRAP HELP BOX (Win + /)
; =========================================================

; ... ToggleHelpBox / UpdateHelpBox boilerplate ...
```

Key rules extracted from existing modules:

- Everything between the two `COPY BELOW/ABOVE` delimiter comments is what gets pasted into `custom.ahk`.
- The `HelpEntries.Push(...)` block must always be the first thing after the delimiter, before any config or hotkeys.
- Config variables are declared directly in the module, not in a separate file.
- The tray icon toggle and help box boilerplate always appear below the `COPY ABOVE` delimiter they are standalone-only scaffolding and do **not** get copied into `custom.ahk`.

## Step-by-Step Pipeline

### Step 1: Write the Standalone Module

Create `modules/<feature-name>.ahk` following the module template above.

---

### Step 2: Test the Standalone Module

- Run `modules/<feature-name>.ahk` directly in AHK.

If any check fails: fix, re-run, and repeat until all pass. Then continue.

---

### Step 3: Update `custom.ahk` (if needed)

Check whether the new feature requires any changes to `distribution/custom.ahk`. This is needed when the feature introduces:

- New **global variables** that must be declared at the top of the script (e.g. the color picker required `cpGuiGlobal`, `cSwatchGlobal`, etc.).
- New **tooltip message globals** (e.g. `Msg_EndTask`, `Msg_ColorPicker`).
- New **config blocks** in the tooltips section or elsewhere in the preamble.

If no new globals or preamble changes are needed, skip to Step 7.

---

### Step 4: Test `custom.ahk` with Existing Modules Only

- Before touching anything new, verify that `custom.ahk` still works correctly with the existing modules pasted in.

This is your baseline. If this fails, something in Step 3 broke the file fix it before continuing.

---

### Step 5: Test `custom.ahk` with the New Module Alone

- If this fails, the issue is in the module itself or in the `custom.ahk` preamble changes from Step 3. Fix, re-test.

---

### Step 6: Test `custom.ahk` with New Module + All Existing Modules Together

- This is the critical integration test. If it fails, there is likely a variable naming conflict or a `#HotIf` context leak. Fix, re-test.

---

### Step 7: Add New Config Entries to `config.ahk`

- If the new feature introduces config variables that users should be able to control from `config.ahk` (in `distribution/`), add them now.

---

### Step 8: Write the Source Dependency

Create `distribution/source-dependencies/source-<feature-name>.ahk`.

The source dependency is a **stripped-down** version of the module it contains only what is needed when running inside `source.ahk`.

**What to keep:**

- MIT license header.
- `#Requires AutoHotkey v2.0` (no other directives `source.ahk` already sets them).
- `HelpEntries.Push(...)` block.
- The feature hotkeys and logic (wrapped in `#HotIf`).
- Any helper functions unique to this feature.

**What to remove:**

- `#UseHook`, `#MaxThreadsBuffer`, `ProcessSetPriority` (already in `source.ahk`).
- Tray icon config block.
- `COPY BELOW / COPY ABOVE` delimiter comments.
- Tray icon toggle hotkey.
- Help box boilerplate (`ToggleHelpBox`, `UpdateHelpBox`).
- Any config variable declarations those now live in `config.ahk`.

---

### Step 9: Integrate into `source.ahk`

Open `distribution/source.ahk` and make the following changes:

#### **9a. Add globals (if any)**

- If the feature requires module-level globals, declare them near the top of `source.ahk`, before the `#Include` directives. Follow the existing pattern:

#### **9b. Add the `#Include` line**

- Add a new `#Include` line in the include block, after the existing includes:

```ahk
#Include source-dependencies/source-<feature-name>.ahk
```

#### **9c. Update the help box (if `source.ahk` has a hardcoded help text)**

- If `source.ahk` contains a hardcoded `helpText` string (as opposed to building it dynamically from `HelpEntries`), add the new feature's entry to it manually, following the same separator style:

```ahk
───────────────────────────────────────
> MY FEATURE:
    Win+Ctrl+X      →  do the thing
```

---

### Step 10: Test `source.ahk`

- Run `distribution/source.ahk` directly.

If any check fails: fix, re-test, and do not proceed until the full suite passes.

---

## Merge the feature to `dev`

- Once all 10 steps pass, merge the feature into `dev`.

---

~*[@H-int0](https://github.com/H-int0)*
