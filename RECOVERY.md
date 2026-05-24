# Recovery Guide

**These steps assume that your keyboard is not reliable/working and will only make use of your mouse.**

---

If your keyboard is behaving strangely after installing Strap like,

- sending wrong input
- number row acting odd
- or anything unexpected

Follow the steps below to safely remove the script from the Startup.

---

## Step 1: Open Task Manager

- Right-click anywhere on the **taskbar** (the bar usually at the bottom of your screen)
- click **Task Manager** from the menu that appears.

---

## Step 2: Find and Kill the Script

- In Task Manager, click the **Processes** tab from the top, if it isn't already selected.
- Look for a process named **AutoHotkey** or **strap.ahk** in the list.
- Click on it to select it.
- Click the **End Task** button inside the Task Manager
- or right click the **AutoHotkey** process and click **End Task** from the menu that appears.
  - If Task Manager looks tiny with no tabs, click More details at the bottom first.

Your keyboard should now return to normal immediately after this.

---

## Step 3: Remove the Startup Copy

If Strap was set to launch on startup, it will come back after the next restart and cause the same problem again unless you remove it from the startup folder too.

**If your keyboard is working again after Step 2**, the quickest way is:

- Press `Win + R`, type `shell:startup`, and press Enter.
- Find `strap.ahk` in the folder.
- Right-click it and select **Delete**.

---

**If your keyboard is still not reliable**, use the mouse-only method:

- Click the **Start** button (Windows logo) in the taskbar.
- Open **File Explorer** and go inside the following directory:

```cmd
C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

- Find `strap.ahk` in the folder.
- Right-click it and select **Delete**.

---

## Step 4: Verify

Restart your computer. This time your keyboard should behave completely normally. If Strap no longer appears in Task Manager after boot, the removal was successful.

---

## After Recovery

Once your system is stable, you can investigate what went wrong before re-adding the script.

Common causes of rogue behavior are conflicting hotkeys with other running software or an outdated version of AutoHotkey. Make sure you are running AutoHotkey v2.0 or later.

If you want to re-add the script to startup after fixing the issue, refer to the **Auto-Start on Boot** section in [README.md](README.md).

---

~*H-int*
