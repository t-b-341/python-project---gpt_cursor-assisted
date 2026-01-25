# PowerShell script to help set up CUDA for Numba on Windows
# Run this script as Administrator if needed

Write-Host "Checking CUDA installation..." -ForegroundColor Cyan

# Check if CUDA_PATH is set
$cudaPath = $env:CUDA_PATH
if ($cudaPath) {
    Write-Host "CUDA_PATH found: $cudaPath" -ForegroundColor Green
} else {
    Write-Host "CUDA_PATH not set. CUDA Toolkit may not be installed." -ForegroundColor Yellow
}

# Check for nvcc compiler
$nvcc = Get-Command nvcc -ErrorAction SilentlyContinue
if ($nvcc) {
    Write-Host "nvcc found: $($nvcc.Source)" -ForegroundColor Green
} else {
    Write-Host "nvcc not found. CUDA Toolkit not in PATH." -ForegroundColor Yellow
}

# Check for CUDA DLLs
$cudaDlls = @(
    "$env:ProgramFiles\NVIDIA GPU Computing Toolkit\CUDA\*\bin\cudart64_*.dll",
    "$env:ProgramFiles(x86)\NVIDIA GPU Computing Toolkit\CUDA\*\bin\cudart64_*.dll"
)

$found = $false
foreach ($pattern in $cudaDlls) {
    $dlls = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
    if ($dlls) {
        Write-Host "Found CUDA DLLs in: $($dlls[0].DirectoryName)" -ForegroundColor Green
        $found = $true
        break
    }
}

if (-not $found) {
    Write-Host "`nCUDA Toolkit not found. Installation required:" -ForegroundColor Red
    Write-Host "1. Download CUDA Toolkit 12.x from: https://developer.nvidia.com/cuda-downloads" -ForegroundColor Yellow
    Write-Host "2. Choose: Windows > x86_64 > 10/11 > exe (local)" -ForegroundColor Yellow
    Write-Host "3. Install with default options" -ForegroundColor Yellow
    Write-Host "4. Restart your terminal/IDE after installation" -ForegroundColor Yellow
    Write-Host "5. Run: python test_gpu.py" -ForegroundColor Yellow
} else {
    Write-Host "`nCUDA Toolkit appears to be installed. Testing Numba..." -ForegroundColor Cyan
    python -c "from numba import cuda; print('CUDA available:', cuda.is_available())"
}
