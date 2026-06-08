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
  - [4.2 Feature Types](#42-feature-types)
  - [4.3 What Updates Automatically](#43-what-updates-automatically)
  - [4.4 Files That Require MANUAL Updates](#44-files-that-require-manual-updates)
    - [Every feature (Type 1 and Type 2)](#every-feature-type-1-and-type-2)
    - [For Type 2 (only sub-settings)](#for-type-2-only-sub-settings)
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

- Every feature has a **toggle** (on/off switch).
- Some features also have **sub-settings** (additional configurable values beyond enable/disable).

Understanding this distinction is the most important thing in this step.

Here is the lifecycle of a feature toggle (`z`-flag):

1. **Definition** Registered in `cli/features.py`.

2. **Schema & Defaults** `cli/config/schema.py` reads the registry and automatically injects it into `DEFAULT_CONFIG["features"]`.

3. **Profile Creation/Update** `ops/updater.py` merges missing schema keys into existing user profiles.

4. **TUI Display** `tui/widgets/config_panel.py` dynamically builds the UI list by enumerating the registry.

5. **State Mutation (CLI)** `cli/headless.py` intercepts `strap /config -z 7`, mapping `7` to the feature key.

6. **State Mutation (TUI)** `tui/screens/config.py` intercepts UI interactions, mapping `7` to the feature key to open a `BooleanPopup`.

7. **Disk Write** `ops/file_editor.py` iterates over the registry, maps the JSON boolean to `0` or `1`, and replaces the value in `core/config.ahk` via regex.

Sub-settings (`y`-flag) follow a similar path but require additional manual work covered in [4.4](#44-files-that-require-manual-updates) below.

---

### 4.2 Feature Types

**Type 1: Toggle only:**

- A single on/off switch. Represented as a `z`-flag. The CLI/TUI integration is mostly automatic once you register it.

Examples: Numpad Emulator, ALT Codes, Line Navigation, Force Kill, Color Picker, etc.

**Type 2: Toggle + sub-settings:**

- Has a `z`-flag toggle AND a `y`-flag entry for additional configurable values.

Examples: Force Kill (`y1` tooltip text), Color Picker (`y2` msgbox toggle + tooltip text), Vim Navigation (`y3` Left Alt + Right Alt toggles), etc.

> Only add a `y`-flag entry if the feature has settings beyond a simple enable/disable.

---

### 4.3 What Updates Automatically

- For **Type 1 features only**, the following files require no changes they adapt automatically based on `FEATURE_REGISTRY`:

| File | What it does automatically |
| --- | --- |
| `cli/config/schema.py` | Injects the feature into `DEFAULT_CONFIG["features"]` |
| `cli/config/parser.py` | Parses the AHK var on first install |
| `ops/file_editor.py` | Writes the toggle value to `config.ahk` |
| `tui/widgets/config_panel.py` | Renders the `[z*]` row in the TUI list |
| `tui/constants.py` | Resolves the `[z*]` hint text in the config screen |

> For **Type 2 features**, all of these files except `cli/config/parser.py` require manual edits. See [4.4](#44-files-that-require-manual-updates) below.

---

### 4.4 Files That Require Manual Updates

| File | What to change |
| --- | --- |
| `cli/features.py` | Append entry to `FEATURE_REGISTRY` |
| `core/config.ahk` | Add `Global MyFeatureEnabled := 1` |
| `cli/headless.py` | Add index to `fk_map`; add `y` block if Type 2 |
| `tui/screens/config.py` | Add index to `fk_map` in `_apply_value` and both maps in `_open_popup`; add `y` blocks if Type 2 |
| `cli/config/schema.py` | *(Type 2 only)* Add sub-setting keys to `DEFAULT_CONFIG` |
| `ops/file_editor.py` | *(Type 2 only)* Add `re.sub` block for each sub-setting |
| `tui/popups/settings.py` | *(Type 2 only)* Create new popup class |
| `tui/constants.py` | *(Type 2 only)* Add `POPUP_*` help text constant |
| `tui/widgets/config_panel.py` | *(Type 2 only)* Add `y` row to `render_list`, `_mark_bool`, and `pending_summary` |

---

#### Every feature (Type 1 and Type 2)

<details>
  <summary> </summary>

##### 1. `cli/features.py`

- This is the single source of truth for all features. Append your feature to the end of `FEATURE_REGISTRY` everything else in the codebase that handles feature toggles automatically reads from this list at runtime.

  ```python
  {"key": "myFeature", "ahk_var": "MyFeatureEnabled", "label": "My Feature", "default": True},
  ```

- Insertion order strictly dictates the `z` index the 7th entry becomes `z7`. Try not to reorder existing entries unless it's absolutely necessary fr.

##### 2. `core/config.ahk`

- The Python side can only *update* values that already exist in this file it uses `re.sub` which finds and replaces, but never injects. So you have to add the variable here first before any CLI/TUI write will take effect.

  ```ahk2
  Global MyFeatureEnabled := 1
  ```

- The `ahk_var` string in `FEATURE_REGISTRY` must exactly match the left side of the `:=` assignment. A mismatch of course will cause a failure no error, but just that the file didn't update.

##### 3. `cli/headless.py`

- The headless path parses raw CLI arguments like `strap /config -z 7`. It has no way to know that `7` means `myFeature` without an explicit mapping `FEATURE_REGISTRY` isn't indexed by integer. Update `fk_map` inside `apply_headless_config`:

  ```python
  fk_map = {1:"numpadEmulator", ..., 7:"myFeature"}
  ```

##### 4. `tui/screens/config.py`

The TUI config screen has the same problem as `headless.py` it receives an integer and needs to resolve it to a feature key. Unlike the headless path though, it has two separate routing functions that both need updating.

- In `_apply_value` (handles typed commands inside the TUI):

  ```python
  fk_map = {1:"numpadEmulator", ..., 7:"myFeature"}
  ```

- In `_open_popup` (handles opening the settings popup), map the index to both the key and the display label:

  ```python
  f_map = {1: "numpadEmulator", ..., 7: "myFeature"}
  names = {1: "NumPad Emulator", ..., 7: "My Feature"}
  ```

</details>

#### For Type 2 (only sub-settings)

<details>
  <summary></summary>

##### 1. `cli/config/schema.py`

- `DEFAULT_CONFIG` is the canonical shape of a user profile. Any sub-setting key that isn't here won't exist in new profiles, and won't be added to existing profiles on upgrade. Add your keys with sensible defaults:

  ```python
  # --- [yN] My Feature settings ---
  "myFeatureOption1": True,
  "myFeatureOption2": "some default",
  ```

<!-- markdownlint-disable-next-line -->
##### 2. `core/config.ahk`

- Same rule as the feature toggle add the AHK variables here before any Python write can touch them:

  ```ahk2
  Global MyFeatureOption1 := 1
  ```

##### 3. `ops/file_editor.py`

- The file editor's automatic loop only covers `z`-flag feature toggles. Sub-settings live outside the `features` dict and have their own AHK variable names, so they need their own explicit `re.sub` blocks. Add a `[yN]` section inside `update_config_ahk`:

  ```python
  # --- [yN] My Feature settings ---
  if "myFeatureOption1" in config_data:
      val = 1 if config_data["myFeatureOption1"] else 0
      content = re.sub(
          r"(MyFeatureOption1\s*:=\s*)\d+",
          rf"\g<1>{val}",
          content, flags=re.IGNORECASE
      )
  ```

  > The `if key in config_data` guard is intentional it lets older profiles that are missing the key coexist with newer AHK files without overwriting anything.

##### 4. `cli/headless.py`

- The `z`-flag routing only handles feature toggles. Sub-settings come in as `y`-flag arguments (`strap /config -y -3--1 enable`), and the parser already splits them into `flag`, `no`, and `sub`. You just need to add a `no == N` branch that reads those parts and writes to `cfg`:

  ```python
  elif no == N:
      if sub == "1":
          if vl == "--!": cfg["myFeatureOption1"] = not cfg.get("myFeatureOption1", True)
          elif parse_bool(vl) is not None: cfg["myFeatureOption1"] = parse_bool(vl)
      elif sub == "2":
          ...
  ```

##### 5. `tui/screens/config.py`

The same `no == N` logic needs to exist in two places in the TUI screen for the same reason as with `z`-flags typed commands and popup interactions are handled separately.

- In `_apply_value`, mirror the headless block but write to `self.panel.pending` instead of `cfg` (pending changes aren't saved until the user explicitly saves):

  ```python
  elif no == N:
      if sub == "1":
          if vl == "--!": self.panel.pending["myFeatureOption1"] = not self.panel._effective("myFeatureOption1", True)
          elif parse_bool(vl) is not None: self.panel.pending["myFeatureOption1"] = parse_bool(vl)
  ```

- In `_open_popup`, push your new popup:

  ```python
  elif no == N:
      self.app.push_screen(
          MyFeaturePopup(cfg("myFeatureOption1", True), ...),
          lambda r: self._apply_route_result(None, r)
      )
  ```

##### 6. `tui/popups/settings.py`

- Each Type 2 feature gets its own popup class because the layout and inputs are unique to that feature there's no generic popup that works for all sub-setting combinations. Use `ColorPickerPopup` as a reference. Add your class after the existing ones:

  ```python
  class MyFeaturePopup(_BasePopup):
      def __init__(self, option1: bool, **kwargs):
          super().__init__(**kwargs)
          self._option1 = option1

      def popup_title(self) -> str: return "Configure - My Feature"
      def input_placeholder(self) -> str: return "/config -y -N--No. value"

      def compose_content(self):
          val = "enable" if self._option1 else "disable"
          yield Static(f"[1] Option Label                  \\[{val}]", id="mf-opt-1")

      def help_text(self) -> str:
          from tui.constants import POPUP_MY_FEATURE
          return POPUP_MY_FEATURE

      def process_cmd_input(self, raw: str) -> bool:
          return False
  ```

##### 7. `tui/constants.py`

- The popup's help text lives here rather than inline in the class so that all user-facing strings are in one place. Add a constant for your popup:

  ```python
  POPUP_MY_FEATURE = (
      "[b]CONFIG - [yN] My Feature[/b]\n"
      "─────────────────────────\n"
      "/config -y -N--1 --!       (Flip option)\n"
      "/config -y -N--1 value     (enable|disable)\n\n"
      "/back or Esc               (Close)\n\n"
  )
  ```

##### 8. `tui/widgets/config_panel.py`

Three small additions, all in service of making the panel aware that your sub-settings exist:

1. Add a `[yN]` row to `render_list` so it appears in the TUI list:

    ```python
    f"{'[bold yellow]*[/bold yellow]' if self._mark_bool('yN') else ' '}\\[yN] My Feature",
    ```

2. Add `yN` to `_mark_bool` so the panel knows which keys to watch for pending changes:

    ```python
    "yN": ["myFeatureOption1", "myFeatureOption2"]
    ```

3. Add entries to `label_map` in `pending_summary` so the save confirmation screen shows readable names instead of raw key names:

    ```python
    "myFeatureOption1": "My Feature - Option 1",
    ```

</details>

---

### 4.5 Some Non-Obvious Constraints

- **Index coupling** `fk_map` integers, `enumerate(registry, 1)` in `config_panel.py`, and `no - 1` lookups all depend on exact insertion order in `FEATURE_REGISTRY`. Never reorder existing entries.

- **Variable name sync** `ahk_var` in `FEATURE_REGISTRY` and every `re.sub` pattern in `file_editor.py` must exactly match the variable name in `config.ahk`. Mismatches fail silently.

- **Schema migration** Adding new keys to `DEFAULT_CONFIG["features"]` does not require a `MIGRATIONS` entry; `_add_missing_keys` handles it recursively. `MIGRATIONS` is only for renaming or removing existing top-level keys.

- **`re.sub` won't inject** `file_editor.py` can only update variables that already exist in `config.ahk`. Always add them manually first.

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

3. Fill out the [PR template].

> [!TIP]
> Don't worry if your pull request isn't perfect, no pull request ever is! The maintainers will work with you to fix any issues and get it merged! ^-^

 <!-- markdownlint-disable -->
  <details>
  <summary> </summary>
  <pre>
  <code>

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

  </code>
  </pre>
  </details>
<!-- markdownlint-enable -->

---

~*[@H-int0](https://github.com/H-int0)*
