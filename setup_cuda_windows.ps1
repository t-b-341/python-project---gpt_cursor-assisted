# PowerShell script to set up CUDA for Numba on Windows
# Run this script as Administrator for system-wide changes, or as user for user-level changes

Write-Host "=== CUDA Setup for Numba ===" -ForegroundColor Cyan
Write-Host ""

# Check for CUDA installations
$cudaVersions = @()
$cudaBasePath = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"

if (Test-Path $cudaBasePath) {
    $cudaVersions = Get-ChildItem $cudaBasePath -Directory | Where-Object { $_.Name -match "^v\d+\.\d+" } | Sort-Object Name -Descending
    Write-Host "Found CUDA installations:" -ForegroundColor Green
    foreach ($version in $cudaVersions) {
        Write-Host "  - $($version.Name)" -ForegroundColor Yellow
    }
} else {
    Write-Host "CUDA Toolkit not found at: $cudaBasePath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install CUDA Toolkit 12.x from:" -ForegroundColor Yellow
    Write-Host "https://developer.nvidia.com/cuda-12-6-0-download-archive" -ForegroundColor Cyan
    exit 1
}

# Prefer CUDA 12.x over 13.x for Numba compatibility
$selectedCuda = $null
foreach ($version in $cudaVersions) {
    if ($version.Name -match "^v12\.") {
        $selectedCuda = $version
        break
    }
}
if ($null -eq $selectedCuda -and $cudaVersions.Count -gt 0) {
    $selectedCuda = $cudaVersions[0]
    Write-Host "Warning: Using CUDA $($selectedCuda.Name) - Numba 0.63.1 works best with CUDA 12.x" -ForegroundColor Yellow
}

if ($null -eq $selectedCuda) {
    Write-Host "No CUDA version found!" -ForegroundColor Red
    exit 1
}

$cudaPath = $selectedCuda.FullName
$cudaBinPath = Join-Path $cudaPath "bin"
$cudaLibPath = Join-Path $cudaPath "lib\x64"

Write-Host ""
Write-Host "Selected CUDA: $($selectedCuda.Name) at $cudaPath" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "Running as Administrator - setting system-wide environment variables" -ForegroundColor Cyan
    
    # Get current system PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    # Add CUDA bin to PATH if not present
    if ($currentPath -notlike "*$cudaBinPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$cudaBinPath", "Machine")
        Write-Host "Added $cudaBinPath to system PATH" -ForegroundColor Green
    } else {
        Write-Host "$cudaBinPath already in system PATH" -ForegroundColor Yellow
    }
    
    # Set CUDA_PATH
    [Environment]::SetEnvironmentVariable("CUDA_PATH", $cudaPath, "Machine")
    Write-Host "Set CUDA_PATH = $cudaPath" -ForegroundColor Green
    
    # Set CUDA_HOME (some tools use this)
    [Environment]::SetEnvironmentVariable("CUDA_HOME", $cudaPath, "Machine")
    Write-Host "Set CUDA_HOME = $cudaPath" -ForegroundColor Green
} else {
    Write-Host "Running as regular user - setting user-level environment variables" -ForegroundColor Cyan
    Write-Host "Note: For system-wide changes, run as Administrator" -ForegroundColor Yellow
    
    # Get current user PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Add CUDA bin to PATH if not present
    if ($currentPath -notlike "*$cudaBinPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$cudaBinPath", "User")
        Write-Host "Added $cudaBinPath to user PATH" -ForegroundColor Green
    } else {
        Write-Host "$cudaBinPath already in user PATH" -ForegroundColor Yellow
    }
    
    # Set CUDA_PATH
    [Environment]::SetEnvironmentVariable("CUDA_PATH", $cudaPath, "User")
    Write-Host "Set CUDA_PATH = $cudaPath" -ForegroundColor Green
    
    # Set CUDA_HOME
    [Environment]::SetEnvironmentVariable("CUDA_HOME", $cudaPath, "User")
    Write-Host "Set CUDA_HOME = $cudaPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Restart your terminal/IDE for changes to take effect!" -ForegroundColor Yellow
Write-Host ""
Write-Host "After restart, test with:" -ForegroundColor Cyan
Write-Host "  python test_gpu.py" -ForegroundColor White
Write-Host ""
Write-Host "If CUDA is still not detected, you may need to:" -ForegroundColor Yellow
Write-Host "  1. Install CUDA Toolkit 12.x (recommended for Numba 0.63.1)" -ForegroundColor White
Write-Host "  2. Restart your computer" -ForegroundColor White
Write-Host "  3. Verify with: nvcc --version" -ForegroundColor White
