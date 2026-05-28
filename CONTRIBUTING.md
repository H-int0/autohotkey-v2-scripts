# Contributing to STRAP

This document describes the end-to-end pipeline for adding a new feature to Strap, from writing the first line of code to merging into `main`.

---

> [!NOTE]
> Review the [Feature Integration Safety Guide](INTEGRATION_GUIDE.md) for rules on timer patterns, hotkey structure, and thread safety.

---

## Table of contents

- [Commit Text](#commit-text)
- [The Module Template](#the-module-template)
- [Step-by-Step Pipeline](#step-by-step-pipeline)
  - [STEP 1: Write the Standalone Module](#step-1-write-the-standalone-module)
  - [STEP 2: Test the Standalone Module](#step-2-test-the-standalone-module)
  - [STEP 3: Update `source.ahk` (if needed)](#step-3-update-sourceahk-if-needed)
  - [STEP 4: Integration Testing in `source.ahk`](#step-4-integration-testing-in-sourceahk)
  - [STEP 5: Add New Config Entries to `source-dependencies/config.ahk`](#step-5-add-new-config-entries-to-source-dependenciesconfigahk)
  - [STEP 6: Write the Source Dependency](#step-6-write-the-source-dependency)
  - [STEP 7: Integrate into `source.ahk`](#step-7-integrate-into-sourceahk)
  - [STEP 8: Integration testing in `source.ahk`](#step-8-integration-testing-in-sourceahk)
  - [STEP 9: Merge the feature to `dev`](#step-9-merge-the-feature-to-dev)

---

## Commit Text

### Format

Every commit text follows this structure:

```cmd
type: short description in lowercase
```

### Types

| Type | Used for |
| --- | --- |
| `feat` | Adding something new like a new page, project, section, or file. |
| `fix` | Correcting a bug, broken link, typo, or anything that was wrong. |
| `docs` | Changes to documentation only. |
| `refactor` | Restructuring or reorganizing existing code without changing what it does. |
| `chore` | Maintenance work config changes, folder setup, `.gitignore` updates, perhaps adding files, etc. |
| `style` | Formatting, whitespace, or styling changes that do not affect logic or content. |

---

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

## Step-by-Step Pipeline

### STEP 1: Write the Standalone Module

Create `modules/<feature-name>.ahk` following the module template above.

---

### STEP 2: Test the Standalone Module

- Run `modules/<feature-name>.ahk` directly in AHK.

If any check fails: fix, re-run, and repeat until all pass. Then continue.

---

### STEP 3: Update `source.ahk` (if needed)

Check whether the new feature requires any changes to `distribution/source.ahk`. This is needed when the feature introduces:

- New **global variables** that must be declared at the top of the script (e.g. the color picker required `cpGuiGlobal`, `cSwatchGlobal`, etc.).
- New **tooltip message globals** (e.g. `Msg_EndTask`, `Msg_ColorPicker`).
- New **config blocks** in the tooltips section or elsewhere in the preamble.

> If no changes are needed, skip to [STEP 5](#step-5-add-new-config-entries-to-source-dependenciesconfigahk).

---

### STEP 4: Integration Testing in `source.ahk`

Before moving forward, you must verify that the new feature plays nicely with the rest of the ecosystem.

- Test `source.ahk` with Existing source-dependencies Only
  - Before touching anything new, verify that `source.ahk` still works correctly with the existing source-dependencies enabled.

> This is your baseline. If this fails, something in [STEP 3](#step-3-update-sourceahk-if-needed) broke the file fix it before continuing.

---

### STEP 5: Add New Config Entries to `source-dependencies/config.ahk`

- If the new feature introduces config variables that users should be able to control from `source-dependencies/config.ahk` (in `distribution/`), add them now.

---

### STEP 6: Write the Source Dependency

Create `distribution/source-dependencies/source-<feature-name>.ahk`.

The source dependency is a **stripped-down** version of the module it contains only what is needed when running inside `source.ahk`.

---

### STEP 7: Integrate into `source.ahk`

Open `distribution/source.ahk` and make the following changes:

- **Add globals (if any)**
  - If the feature requires module-level globals, declare them near the top of `source.ahk`, before the `#Include` directives. Follow the existing pattern:

- **Add the `#Include` line**
  - Add a new `#Include` line after the existing includes:

    ```ahk
    #Include source-dependencies/source-<feature-name>.ahk
    ```

---

### STEP 8: Integration testing in `source.ahk`

- **Test `source.ahk` with Existing source-dependencies Only**
  - Before touching anything new, verify that `source.ahk` still works correctly with the existing source-dependencies enabled.
  > This is your baseline. If this fails, something in [STEP 5](#step-5-add-new-config-entries-to-source-dependenciesconfigahk) or [STEP 7](#step-7-integrate-into-sourceahk) broke the `source.ahk`. Fix it before continuing.

- **Test `source.ahk` with the New `source-dependencies-*` Alone**
  - Disable the other features in `source.ahk` and test only the new feature.
  - If this fails, the issue is in the source-dependencies itself.
  > It means something in [STEP 6](#step-6-write-the-source-dependency) broke the `source.ahk`. Fix it before continuing.

- **Test `source.ahk` with New `source-dependencies-*` + All Existing source-dependencies Together**
  - Enable other features in `source.ahk` and test if the `source.ahk` works as intended with the new feature.
  - This is the critical integration test. If it fails, fix it before continuing.

---

### STEP 9: Merge the feature to `dev`

- Once all the 8 steps pass, the feature is now ready to be merged into `dev`.

---

~*[@H-int0](https://github.com/H-int0)*
