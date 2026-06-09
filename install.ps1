# GNU GENERAL PUBLIC LICENSE
#
# Copyright (C) 2026 H-int0
# GitHub: <https://github.com/H-int0/>
# License: <https://github.com/H-int0/autohotkey-v2-scripts/blob/main/LICENSE/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ====================================================================================

# =============================================================================
# install.ps1
# Strap bootstrapper run with:
#    powershell -ExecutionPolicy Bypass -Command "irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex"
#    irm 'https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1' | iex
#
# What this does:
#   1. Checks for AutoHotkey v2 (installs via winget if missing)
#   2. Checks for Python 3.10+ (installs via official installer if missing)
#   3. Fetches the latest tag from GitHub
#   4. Creates .strap_versions\vX.X.X\ and downloads the release zip into it
#   5. Copies contents into %APPDATA%\Strap\ (excluding docs/git noise)
#   6. Creates strap.bat and adds bin\ to user PATH
#   7. Installs Python dependencies (pip)
#   8. Hands off to Python: python cli/main.py /install --from-ps
# =============================================================================

$ErrorActionPreference = "Stop"

$GITHUB_API   = "https://api.github.com/repos/H-int0/autohotkey-v2-scripts/tags"
$VERSIONS_DIR = Join-Path $env:USERPROFILE ".strap_versions"
$INSTALL_DIR  = Join-Path $env:APPDATA "Strap"
$BIN_DIR      = Join-Path $INSTALL_DIR "bin"
$BAT_PATH     = Join-Path $BIN_DIR "strap.bat"

$SKIP = @(
".git", ".github", "bin", "__pycache__"
)

Write-Host ""
Write-Host ">> STRAP INSTALLER" -ForegroundColor Cyan
Write-Host ""

# -----------------------------------------------------------------------------
# 1. Check for AutoHotkey v2 (install via winget if missing)
# -----------------------------------------------------------------------------
Write-Host "Checking for AutoHotkey v2..."
$ahkPath = "${env:ProgramFiles}\AutoHotkey\v2\AutoHotkey64.exe"
if (Test-Path $ahkPath) {
    Write-Host "  Found: $ahkPath"
} else {
    Write-Host "  AutoHotkey v2 not found. Installing via winget..."
    try {
        winget install --id AutoHotkey.AutoHotkey --silent --accept-package-agreements --accept-source-agreements | Out-Null
        Write-Host "  [OK] AutoHotkey v2 installed."
    } catch {
        Write-Host "[X] Failed to install AutoHotkey v2: $_" -ForegroundColor Red
        Write-Host "    Install manually: https://www.autohotkey.com/download/" -ForegroundColor Yellow
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 2. Check for Python 3.10+ (install via official installer if missing)
# -----------------------------------------------------------------------------
Write-Host "Checking for Python..."
$pyFound = $false
try {
    $pyver = python --version 2>&1
    if ($pyver -match "Python (\d+)\.(\d+)") {
        $pyMajor = [int]$Matches[1]
        $pyMinor = [int]$Matches[2]
        if ($pyMajor -gt 3 -or ($pyMajor -eq 3 -and $pyMinor -ge 10)) {
            Write-Host "  Found: $pyver"
            $pyFound = $true
        } else {
            Write-Host "  Found $pyver but Strap requires 3.10+. Installing a compatible version..." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "  Python not found. Installing..."
}

if (-not $pyFound) {
    $pyInstallerUrl = "https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
    $pyInstallerPath = Join-Path $env:TEMP "python-installer.exe"
    try {
        Write-Host "  Downloading Python 3.12.9..."
        Invoke-WebRequest -Uri $pyInstallerUrl -OutFile $pyInstallerPath -UseBasicParsing
        Write-Host "  Installing Python 3.12.9 (per-user, no UAC required)..."
        Start-Process -FilePath $pyInstallerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=0" -Wait -NoNewWindow
        Remove-Item $pyInstallerPath -Force -ErrorAction SilentlyContinue

        # Refresh PATH in current session so subsequent python calls work immediately
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + $env:Path

        $pyver = python --version 2>&1
        Write-Host "  [OK] $pyver installed."
    } catch {
        Write-Host "[X] Failed to install Python: $_" -ForegroundColor Red
        Write-Host "    Install manually: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 3. Fetch latest tag from GitHub
# -----------------------------------------------------------------------------
Write-Host "Fetching latest version from GitHub..."
try {
    $tags      = Invoke-RestMethod -Uri $GITHUB_API -UseBasicParsing
    $latestTag = $tags[0].name
    $zipUrl    = $tags[0].zipball_url
    $version   = $latestTag.TrimStart("v")
    $null = $version
} catch {
    Write-Host "[X] Failed to fetch tags from GitHub: $_" -ForegroundColor Red
    exit 1
}
Write-Host "  Latest version: $latestTag"

# -----------------------------------------------------------------------------
# 4. Create .strap_versions\vX.X.X\ and download zip
# -----------------------------------------------------------------------------
$versionDir = Join-Path $VERSIONS_DIR $latestTag

if (Test-Path $versionDir) {
    Write-Host "  $latestTag already archived in .strap_versions, skipping download."
} else {
    Write-Host "Downloading $latestTag..."
    New-Item -ItemType Directory -Force -Path $versionDir | Out-Null

    $tmpZip     = Join-Path $VERSIONS_DIR "tmp_download.zip"
    $tmpExtract = Join-Path $VERSIONS_DIR "tmp_extract"

    try {
        Invoke-WebRequest -Uri $zipUrl -OutFile $tmpZip -UseBasicParsing
    } catch {
        Write-Host "[X] Download failed: $_" -ForegroundColor Red
        Remove-Item $versionDir -Recurse -Force -ErrorAction SilentlyContinue
        exit 1
    }

    Write-Host "Extracting..."
    New-Item -ItemType Directory -Force -Path $tmpExtract | Out-Null
    Expand-Archive -Path $tmpZip -DestinationPath $tmpExtract -Force
    Remove-Item $tmpZip -Force

    # GitHub zips extract into a single root folder e.g., "H-int0-autohotkey-v2-scripts-abc1234/"
    $extractedRoot = Get-ChildItem -Path $tmpExtract -Directory | Select-Object -First 1

    if (-not $extractedRoot) {
        Write-Host "[X] Could not find extracted files." -ForegroundColor Red
        Remove-Item $tmpExtract -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item $versionDir -Recurse -Force -ErrorAction SilentlyContinue
        exit 1
    }

    # Copy into versionDir, skipping docs/git noise
    Get-ChildItem -Path $extractedRoot.FullName | ForEach-Object {
        if ($SKIP -notcontains $_.Name) {
            Copy-Item -Path $_.FullName -Destination $versionDir -Recurse -Force
        }
    }

    Remove-Item $tmpExtract -Recurse -Force
    Write-Host "  [OK] $latestTag archived to .strap_versions\$latestTag\"
}

# -----------------------------------------------------------------------------
# 5. Copy into %APPDATA%\Strap\ (wipe everything except bin\ if reinstalling)
# -----------------------------------------------------------------------------
if (Test-Path $INSTALL_DIR) {
    Write-Host "Existing installation found. Overwriting (keeping bin\)..."
    Get-ChildItem -Path $INSTALL_DIR | ForEach-Object {
        if ($_.Name -ne "bin") {
            Remove-Item $_.FullName -Recurse -Force
        }
    }
} else {
    New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
}

Write-Host "Copying $latestTag to %APPDATA%\Strap\..."
Get-ChildItem -Path $versionDir | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $INSTALL_DIR -Recurse -Force
}

# -----------------------------------------------------------------------------
# 6. Create strap.bat if it doesn't exist
# -----------------------------------------------------------------------------
if (-not (Test-Path $BAT_PATH)) {
    Write-Host "Creating strap.bat..."
    New-Item -ItemType Directory -Force -Path $BIN_DIR | Out-Null
    $batContent = "@echo off`npython `"$INSTALL_DIR\cli\main.py`" %*`n"
    Set-Content -Path $BAT_PATH -Value $batContent -Encoding ASCII
} else {
    Write-Host "strap.bat already exists, skipping."
}

# -----------------------------------------------------------------------------
# 7. Add bin\ to user PATH if not already there
# -----------------------------------------------------------------------------
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$BIN_DIR*") {
    Write-Host "Adding bin\ to PATH..."
    $newPath = $userPath.TrimEnd(";") + ";" + $BIN_DIR
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    # Broadcast the change so open Explorer windows pick it up
    $signature = @"
[DllImport("user32.dll", SetLastError=true)]
public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, string lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
"@
    $type   = Add-Type -MemberDefinition $signature -Name "Win32SendMessage" -Namespace "Win32" -PassThru
    $result = [UIntPtr]::Zero
    $type::SendMessageTimeout([IntPtr]0xffff, 0x001A, [UIntPtr]::Zero, "Environment", 2, 5000, [ref]$result) | Out-Null
} else {
    Write-Host "bin\ already in PATH, skipping."
}

# -----------------------------------------------------------------------------
# 8. Install Python dependencies
# -----------------------------------------------------------------------------
$requirementsPath = Join-Path $INSTALL_DIR "cli\requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host "Installing Python dependencies..."
    python -m pip install -r $requirementsPath --quiet
} else {
    Write-Host "Warning: requirements.txt not found, skipping pip install." -ForegroundColor Yellow
}

# -----------------------------------------------------------------------------
# 9. Hand off to Python for profiles + startup prompt
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "Handing off to Python..." -ForegroundColor Cyan
python "$INSTALL_DIR\cli\main.py" /install --from-ps
