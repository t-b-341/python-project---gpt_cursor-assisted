# PowerShell script to permanently add CUDA to PATH
# Run this script as Administrator

Write-Host "Adding CUDA Toolkit to PATH..." -ForegroundColor Cyan

$cudaPath = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.1"
$cudaBinPath = "$cudaPath\bin"
$cudaLibPath = "$cudaPath\lib\x64"

# Check if CUDA exists
if (Test-Path $cudaBinPath) {
    Write-Host "CUDA Toolkit found at: $cudaPath" -ForegroundColor Green
    
    # Get current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    # Check if already in PATH
    if ($currentPath -notlike "*$cudaBinPath*") {
        Write-Host "Adding CUDA to system PATH..." -ForegroundColor Yellow
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$cudaBinPath", "Machine")
        Write-Host "CUDA bin added to PATH" -ForegroundColor Green
    } else {
        Write-Host "CUDA bin already in PATH" -ForegroundColor Yellow
    }
    
    # Set CUDA_PATH environment variable
    [Environment]::SetEnvironmentVariable("CUDA_PATH", $cudaPath, "Machine")
    Write-Host "CUDA_PATH set to: $cudaPath" -ForegroundColor Green
    
    Write-Host "`nIMPORTANT: Restart your terminal/IDE for changes to take effect!" -ForegroundColor Yellow
    Write-Host "After restart, run: python test_gpu.py" -ForegroundColor Yellow
} else {
    Write-Host "CUDA Toolkit not found at expected location: $cudaPath" -ForegroundColor Red
    Write-Host "Please verify CUDA installation." -ForegroundColor Red
}
