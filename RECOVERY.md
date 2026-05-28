# Recovery Guide

**These steps assume that your keyboard is not reliable/working and will primarily make use of your mouse.**

---

If your keyboard is behaving strangely after installing Strap like,

- sending wrong input
- number row acting odd
- or anything unexpected

Follow the steps below to safely remove the script from the Startup.

---

## Step 1: Open Task Manager

- Right-click anywhere on an empty space on your **taskbar** (the bar usually at the bottom of your screen).
- Click **Task Manager** from the menu that appears.
- *(If your keyboard is partially working, you can alternatively press `Ctrl + Shift + Esc` to open Task Manager instantly).*

---

## Step 2: Find and Kill the Script

- In Task Manager, click the **Processes** tab from the top (if it isn't already selected).
- Look for a process named **AutoHotkey** or **source.ahk** in the list.
- Click on it to select it.
- Click the **End Task** button inside the Task Manager (usually at the top right or bottom right depending on your Windows version).
- Alternatively, right-click the **AutoHotkey** process and click **End Task** from the menu that appears.

> [!Note]
> If Task Manager looks tiny with no tabs, click "More details" at the bottom left first.

Your keyboard should return to normal immediately after this process ends.

---

## Step 3: Remove the Startup Copy

If Strap was set to launch on startup, it will come back after the next restart and cause the same problem again unless you remove it from the startup folder too.

**If your keyboard is working again after Step 2**, the quickest way is:

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Find the shortcut named **Strap** (or `Strap.lnk`) in the folder.
3. Right-click it and select **Delete**.

---

**If your keyboard is still unreliable**, use the mouse-only method:

- Click the **Start** button (Windows logo) in the taskbar.
- Open **File Explorer** and go inside the following directory:

*(Be sure to replace `YourName` with your actual Windows username)*

```cmd
C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

- Find the shortcut named **Strap** (or `Strap.lnk`) in the folder.
- Right-click it and select **Delete**.

---

> If you don't see an `AppData` folder, it may be hidden. To show it:

- Open **File Explorer** and click the **View** tab from the top.
- Under **Show/hide**, check **Hidden items**.

---

## Step 4: Verify

Restart your computer. This time your keyboard should behave completely normally. If Strap no longer appears in Task Manager after boot, the removal was successful.

---

## After Recovery

Once your system is stable, you can investigate what went wrong before re-adding the script.

Common causes of rogue behavior are:

- Conflicting hotkeys with other running software.
- Violating the single-threaded hook model (e.g., running multiple separate AHK scripts that conflict with the CapsLock hook).
- Running an outdated version of AutoHotkey. Make sure you are running [AutoHotkey v2.0](https://www.autohotkey.com/) or later.

If you want to re-add the script to startup after fixing the issue, refer to the **Auto-Start on Boot** section in [README.md](README.md).

---

~*[@H-int0](https://github.com/H-int0)*
