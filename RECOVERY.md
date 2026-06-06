# Recovery Guide

Something went wrong with Strap and your keyboard is acting up? This guide will get you back to normal.

---

## Step 1: Kill the Script

- Open **Task Manager**:
- Right-click an empty spot on your taskbar → click **Task Manager**

> [!TIP]
> If your keyboard is partially working: `Ctrl + Shift + Esc` opens Task Manager instantly.

- Once open:
  1. Click the **Processes** tab
  2. Look for **AutoHotkey** or **source.ahk**
  3. Click it → click **End Task**
  > If Task Manager looks tiny with no tabs, click **More details** at the bottom left first.

Your keyboard should return to normal immediately.

> [!IMPORTANT]
> If Strap is set to auto-start on boot, complete **Step 2** before restarting. Otherwise the script will launch again and you'll be back to square one.

---

## Step 2: Remove Strap from Startup

Killing the script is temporary. it'll come back on the next restart unless you remove it from startup.

**If your keyboard is working again:**

1. Press `Win + R`
2. Type `shell:startup` → press Enter
3. Find **Strap** or `Strap.lnk` → right-click → **Delete**

**If your keyboard is still unreliable (mouse only):**

1. Click the **Start** button → open **File Explorer**
2. Navigate to:

    ```bash
    # Replace `USER_NAME` with your actual Windows username

    C:\Users\USER_NAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    ```

3. Find **Strap** or `Strap.lnk` → right-click → **Delete**

> [!TIP]
> Can't see the `AppData` folder? It's hidden. In File Explorer click **View** from the top ribbon → check **Hidden items**.

---

## Step 3: Verify

Restart your computer. If your keyboard is back to normal and Strap no longer appears in Task Manager you're good.

---

~*[@H-int0](https://github.com/H-int0)*
