# Setting Up CUDA for Numba on Windows

## Your System
- GPU: NVIDIA GeForce RTX 4080 Super ✅
- Driver: 591.44 (CUDA 13.1) ✅
- Python: 3.12.10 ✅
- Numba: Installed ✅

## Issue
Numba can't detect CUDA even though your GPU and driver are installed.

## Solution Options

### Option 1: Install CUDA Toolkit (Recommended)
1. Download CUDA Toolkit 12.x from NVIDIA:
   - https://developer.nvidia.com/cuda-downloads
   - Choose Windows > x86_64 > 10/11 > exe (local)
   - Install with default options

2. After installation, verify:
   ```bash
   python -c "from numba import cuda; print(cuda.is_available())"
   ```

### Option 2: Use Conda (Alternative)
If you have conda installed:
```bash
conda install -c conda-forge cudatoolkit=11.8
```

### Option 3: Check Environment Variables
Make sure CUDA is in your PATH:
- CUDA_PATH should point to CUDA installation
- CUDA_PATH\bin should be in PATH

## Quick Test
After installing CUDA toolkit, run:
```bash
python test_gpu.py
```

Expected output:
```
Numba CUDA available: True
GPU device: <CUDA device 0>
```
