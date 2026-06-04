# =============================================================================
# install.ps1
# Strap bootstrapper run with:
#    powershell -Command "irm https://raw.githubusercontent.com/H-int0/autohotkey-v2-scripts/main/install.ps1 | iex"
#
# What this does:
#   1. Checks for Python
#   2. Fetches the latest tag from GitHub
#   3. Creates .strap_versions\vX.X.X\ and downloads the release zip into it
#   4. Copies contents into %APPDATA%\Strap\ (excluding docs/git noise)
#   5. Installs Python dependencies
#   6. Hands off to Python: python cli/main.py /install --from-ps
# =============================================================================

$ErrorActionPreference = "Stop"

$GITHUB_API   = "https://api.github.com/repos/H-int0/autohotkey-v2-scripts/tags"
$VERSIONS_DIR = Join-Path $env:USERPROFILE ".strap_versions"
$INSTALL_DIR  = Join-Path $env:APPDATA "Strap"
$BIN_DIR      = Join-Path $INSTALL_DIR "bin"
$BAT_PATH     = Join-Path $BIN_DIR "strap.bat"

$SKIP = @(
    ".git", ".github", ".gitignore", "bin", "__pycache__",
    "CHANGELOG.md", "CONFIGURE.md", "CONTRIBUTING.md",
    "FEATURES.md", "INTEGRATION_GUIDE.md",
    "PULL_REQUEST_TEMPLATE.md"
)

Write-Host ""
Write-Host ">> STRAP INSTALLER" -ForegroundColor Cyan
Write-Host ""

# -----------------------------------------------------------------------------
# 1. Check Python
# -----------------------------------------------------------------------------
Write-Host "Checking for Python..."
try {
    $pyver = python --version 2>&1
    Write-Host "  Found: $pyver"
} catch {
    Write-Host "[X] Python not found. Please install Python 3.10+ and try again." -ForegroundColor Red
    Write-Host "    https://www.python.org/downloads/"
    exit 1
}

# -----------------------------------------------------------------------------
# 2. Fetch latest tag from GitHub
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
# 3. Create .strap_versions\vX.X.X\ and download zip
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
# 4. Copy into %APPDATA%\Strap\ (wipe everything except bin\ if reinstalling)
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
# 5. Create strap.bat if it doesn't exist
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
# 6. Add bin\ to user PATH if not already there
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
# 7. Install Python dependencies
# -----------------------------------------------------------------------------
$requirementsPath = Join-Path $INSTALL_DIR "cli\requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host "Installing Python dependencies..."
    python -m pip install -r $requirementsPath --quiet
} else {
    Write-Host "Warning: requirements.txt not found, skipping pip install." -ForegroundColor Yellow
}

# -----------------------------------------------------------------------------
# 8. Hand off to Python for profiles + startup prompt
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "Handing off to Python..." -ForegroundColor Cyan
python "$INSTALL_DIR\cli\main.py" /install --from-ps
