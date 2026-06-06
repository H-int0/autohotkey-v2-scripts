# Contributing to STRAP

This document covers the end-to-end pipeline for adding a new feature to Strap from writing the first line of AHK code to merging into `dev`, including how to register the feature in the CLI/TUI.

> [!TIP]
> Want to understand the codebase first? Try checking out [REFERENCE.md](REFERENCE.md). It breaks down how every part of the codebase works, from the AHK core to the CLI/TUI internals.

---

## Table of Contents

- [Commit Text](#commit-text)
- [Testing the PowerShell Installer](#testing-the-powershell-installer)
- [How do I make a Code Contribution?](#how-do-i-make-a-code-contribution)
- [STEP 1: Initial Setup](#step-1-initial-setup)
  - [1.1 Make a Fork](#11-make-a-fork)
  - [1.2 Clone your fork and Add the upstream Remote](#12-clone-your-fork-and-add-the-upstream-remote)
  - [1.3 Create a Branch](#13-create-a-branch)
- [STEP 2: Write the AHK Script](#step-2-write-the-ahk-script)
- [STEP 3: Test the AHK Script](#step-3-test-the-ahk-script)
- [STEP 4: Integrating the Feature in the CLI/TUI](#step-4-integrating-the-feature-in-the-clitui)
  - [4.1 How a Feature Flows Through the Codebase](#41-how-a-feature-flows-through-the-codebase)
  - [4.2 Feature types (from the perspective of CLI)](#42-feature-types-from-the-perspective-of-cli)
  - [4.3 Files that Update AUTOMATICALLY](#43-files-that-update-automatically)
  - [4.4 Files That Require MANUAL Updates](#44-files-that-require-manual-updates)
  - [4.5 Some Non-Obvious Constraints](#45-some-non-obvious-constraints)
- [STEP 5: Test the CLI Integration](#step-5-test-the-cli-integration)
- [STEP 6: Create Pull Request](#step-6-create-pull-request)

---

## Commit Text

### Format

```bash
type: short description in lowercase
```

### Types

| Type | Used for |
| --- | --- |
| `feat` | New features |
| `fix` | Fixing anything that was wrong |
| `docs` | Documentation |
| `refactor` | Code restructuring |
| `chore` | Maintenance work, folder setup, etc |
| `style` | Formatting, styling changes, etc |

---

## Testing the PowerShell Installer

To verify the full PowerShell install flow end-to-end without re-running `install.ps1`:

```bash
# Replace with your file path
cd C:\path_to_strap\autohotkey-v2-scripts-main
  
python cli/main.py /install --from-ps
```

> [!NOTE]
> `--from-ps` is an internal flag passed automatically by `install.ps1`. It tells the CLI that file copying and PATH setup are already done so it skips those and only handles profile creation and the startup prompt.

## How do I make a Code Contribution?

## STEP 1: Initial Setup

### 1.1 Make a Fork

- Fork the repo on GitHub

### 1.2 Clone your fork and Add the upstream Remote

```bash
git clone https://github.com/<your-username>/autohotkey-v2-scripts.git
cd autohotkey-v2-scripts

git remote add upstream https://github.com/H-int0/autohotkey-v2-scripts.git
```

### 1.3 Create a Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feat/<feature-name>
```

## STEP 2: Write the AHK Script

- Create `core/features/<feature-name>.ahk`.
- Only put what is unique to the feature in it, anything shared belongs in `source.ahk`.
- Add any new config variables to `core/config.ahk`.
- If the feature needs a large variable list (e.g. a timezone list), put it under `core/config-dependencies/`.

## STEP 3: Test the AHK Script

(Recommended) Test order:

1. New feature alone (hosted by `source.ahk`)
2. Each existing feature alone
3. New feature alongside all existing features

## STEP 4: Integrating the Feature in the CLI/TUI

### 4.1 How a Feature Flows Through the Codebase

- When a feature is defined, it is assigned an index (e.g., `z7`). Here is the lifecycle of a feature toggle:

  1. **Definition**: Registered in `cli/features.py`.

  2. **Schema & Defaults**: `cli/config/schema.py` reads the registry and automatically injects it into `DEFAULT_CONFIG["features"]`.

  3. **Profile Creation/Update**: `ops/updater.py` merges missing schema keys into existing user profiles.

  4. **TUI Display**: `tui/widgets/config_panel.py` dynamically builds the UI list and determines if a value changed by enumerating the registry.

  5. **State Mutation (CLI)**: `cli/headless.py` intercepts `strap /config -z 7`, mapping `7` to the feature key.

  6. **State Mutation (TUI)**: `tui/screens/config.py` intercepts UI interactions, mappings `7` to the feature key to open a `BooleanPopup`.

  7. **Disk Write**: `ops/file_editor.py` iterates over the registry, mapping the JSON boolean back to a `0` or `1`, and replaces the value in `core/config.ahk` via RegEx.

### 4.2 Feature types (from the perspective of CLI)

- **Type 1: toggle-only features**
  - A single on/off switch. Represented as a `z`-flag in the config UI.
  - Examples: Numpad Emulator, ALT Codes, Line Navigation, Timezone Switcher, Force Kill, Color Picker.
- **Type 2: features with sub-settings**
  - Has an on/off toggle plus additional configurable values. Represented as a `y`-flag.
  - Currently: Force Kill (`y1` tooltip text) and Color Picker (`y2` msgbox toggle + tooltip text).

  > Only add a `y`-flag entry if the feature has settings beyond a simple enable/disable.

### 4.3 Files that Update AUTOMATICALLY

- You **do not** need to edit the following files. They adapt automatically based on the central registry:

  - **`cli/config/schema.py`**: Automatically constructs the `"features"` dictionary.

  - **`cli/config/parser.py`**: Automatically parses initial installations using the registered `ahk_var`.

  - **`ops/file_editor.py`**: Automatically writes to `config.ahk`.

  - **`tui/widgets/config_panel.py`**: Automatically renders the TUI list and handles `[z*]` display tags.

  - **`tui/constants.py`**: Automatically resolves the UI hint text.

### 4.4 Files That Require MANUAL Updates

1. `cli/features.py`
    - Add your new feature to the end of the `FEATURE_REGISTRY`.
    - **Insertion order strictly dictates the `z` index.** Adding a feature as the 7th item makes it `z7`.

2. `cli/headless.py`
    - To support `strap /config -z 7`, you must map the new integer index (`7`) to your feature's `"key"`.
    - Find `apply_headless_config` and update `fk_map`:

      ```python
      # Before
      fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation"}

      # After
      fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation", 7:"NewFeature"}
      ```

3. `tui/screens/config.py`
    - The TUI screen has two separate routing maps that **must** be updated.
     1. **Update `_apply_value` routing:**

         ```python
         fk_map = {1:"numpadEmulator", 2:"altCodes", 3:"timezoneSwitcher", 4:"forceKillTask", 5:"colorPicker", 6:"lineNavigation", 7:"NewFeature"}
         ```

     2. **Update `_open_popup` routing:**
        - Here, you must map the index to the string `"key"`, AND the index to the UI Label.

          ```python
          f_map = {1: "numpadEmulator", 2: "altCodes", 3: "timezoneSwitcher", 4: "forceKillTask", 5: "colorPicker", 6: "lineNavigation", 7: "NewFeature"}

          names = {1: "NumPad Emulator", 2: "ALT Codes", 3: "TimeZone Switcher", 4: "Force Kill", 5: "Color Picker", 6: "Line Navigation", 7: "My New Feature"}
          ```

> [!NOTE]
> **`ops/file_editor.py`** updates the AHK file using a strict RegEx substitution:
>
> ```python
> content = re.sub(rf"({re.escape(ahk_var)}\s*:=\s*)\d+", rf"\g<1>{ahk_val}", content, flags=re.IGNORECASE)
> ```
>
> **Constraint:** `re.sub` *only* works if the text already exists. The Python script will NOT inject missing variables. You must manually add your variable to `core/config.ahk`.

### 4.5 Some Non-Obvious Constraints

- **Index coupling**
  - `no - 1` in `tui/constants.py`, `enumerate(registry, 1)` inside `config_panel.py`, and the `fk_map` integer keys, they all depend on exact insertion order in `FEATURE_REGISTRY`.
  - Try not to reorder existing entries if it's unnecessary.
- **Variable name sync**
  - The `ahk_var` string in `FEATURE_REGISTRY` (e.g. `"NewFeatureEnabled"`) must exactly match the left side of the `:=` assignment in `core/config.ahk`. A typo will of course cause a failure.
- **Schema migration**
  - Adding a new feature key to the nested `features` dict does NOT require a `MIGRATIONS` entry. `_add_missing_keys` handles it recursively.
  - `MIGRATIONS` is only for renaming or deleting existing keys.

## STEP 5: Test the CLI Integration

1. Run `strap /config` verify the new feature appears in the TUI list with the correct label and `z` index.
2. Toggle it via TUI confirm `core/config.ahk` updates correctly.
3. Toggle it via CLI (`strap /config -z <index>`) confirm same result.
4. Restart Strap verify the toggle state persists.
5. Switch profiles confirm the feature key exists in all profiles with the correct default.
6. Switch versions confirm the key is added to profiles missing it.
7. Run `python cli/main.py /install --from-ps` to verify profile creation and startup prompt behave correctly as if launched by `install.ps1`.

## STEP 6: Create Pull Request

Once all steps pass, the changes is ready to be merged.

1. Push your changes to your remote repository:

    ```bash
    git push origin <branch-name>
    ```

2. Open a PR on GitHub against `dev` (**not `main`**).

3. Fill out the PR template.

    > [!TIP]
    > Don't worry if your pull request isn't perfect, no pull request ever is! The maintainer will work with you to fix any issues and get it merged ^-^

    <!-- markdownlint-disable -->
    <details>
      <summary> </summary>
      <pre>

        ## What changed?
        <!--
        List the files you modified and what you did to each one.
        Example:
        - `cli/features.py` added new feature entry to FEATURE_REGISTRY
        - `cli/headless.py` updated fk_map with new index
        Reference any related issue:
        -->

        ## Why?
        <!--
        Explain the problem or gap this addresses.
        What was broken, missing, or could be improved?
        -->

        ## How to test it?
        <!--
        Walk the reviewer through verifying your change step by step.
        Example:
        1. Run `strap /config`
        2. Confirm the new feature appears at index z7
        3. Toggle it and check that config.ahk updates correctly
        -->

        ## Anything that could break?
        <!--
        List any side effects, edge cases, or areas you're unsure about.
        If you skipped any testing steps from CONTRIBUTING, explain why.
        Leave blank if none.
        -->

        ## Questions for the maintainer?
        <!--
        Anything you're unsure about or want feedback on before this gets merged.
        Leave blank if none.
        -->

        ## Anything else?
        <!--
        Screenshots, context, links, or anything else worth mentioning.
        Leave blank if none.
        -->

      </pre>
    </details>
    <!-- markdownlint-enable -->

---

~*[@H-int0](https://github.com/H-int0)*
