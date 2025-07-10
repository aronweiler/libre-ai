# Build the LibreOffice AI extension using LibreOffice's Python for binary compatibility
# Usage: .\build_libreai_oxt.ps1

$possiblePythons = @(
    "C:\Program Files\LibreOffice\program\python.exe",
    "C:\Program Files\LibreOffice\program\python-core-3.10.18\bin\python.exe"
)
$pythonExe = $null
foreach ($py in $possiblePythons) {
    if (Test-Path $py) {
        $pythonExe = $py
        break
    }
}

if (-not $pythonExe) {
    Write-Error "LibreOffice Python not found at any known location. Please check your LibreOffice installation."
    exit 1
}

$scriptPath = Join-Path $PSScriptRoot "package_oxt.py"
if (!(Test-Path $scriptPath)) {
    Write-Error "package_oxt.py not found in $PSScriptRoot."
    exit 1
}

Write-Host "[INFO] Building .oxt using LibreOffice's Python: $pythonExe"
# Ensure pip is available for LibreOffice's Python
$pipCheck = & $pythonExe -m pip --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[INFO] pip not found for LibreOffice's Python. Attempting to install pip with ensurepip..."
    & $pythonExe -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARN] ensurepip not available. This script will now download and run get-pip.py to install pip for LibreOffice's Python. This will execute a script from the internet with administrator privileges."
        $confirmation = Read-Host "Do you want to continue? (y/n)"
        if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
            Write-Host "Aborted by user."
            exit 1
        }
        $getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
        $getPipPath = Join-Path $env:TEMP "get-pip.py"
        try {
            Invoke-WebRequest -Uri $getPipUrl -OutFile $getPipPath -UseBasicParsing
        } catch {
            Write-Error "[ERROR] Failed to download get-pip.py. Please check your internet connection."
            exit 1
        }
        & $pythonExe $getPipPath
        if ($LASTEXITCODE -ne 0) {
            Write-Error "[ERROR] Failed to install pip using get-pip.py."
            exit 1
        }
        Remove-Item $getPipPath -ErrorAction SilentlyContinue
        Write-Host "[INFO] pip installed successfully using get-pip.py."
    } else {
        # Optionally upgrade pip to latest
        & $pythonExe -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) {
            Write-Error "[ERROR] Failed to upgrade pip for LibreOffice's Python."
            exit 1
        }
        Write-Host "[INFO] pip installed and upgraded successfully."
    }
}

# Run the packaging script with LibreOffice's Python
& $pythonExe $scriptPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "[INFO] Build completed successfully. Output: libreai.oxt"
} else {
    Write-Error "[ERROR] Build failed. See output above."
    exit $LASTEXITCODE
}
