"""Diagnostic script to check CUDA and Numba compatibility"""
import os
import sys

print("=== CUDA & Numba Diagnostic ===\n")

# Check environment variables
print("1. Environment Variables:")
print(f"   CUDA_PATH: {os.environ.get('CUDA_PATH', 'Not set')}")
print(f"   CUDA_HOME: {os.environ.get('CUDA_HOME', 'Not set')}")
print(f"   PATH contains CUDA: {'CUDA' in os.environ.get('PATH', '')}")

# Check Numba
print("\n2. Numba Installation:")
try:
    import numba
    print(f"   Numba version: {numba.__version__}")
    
    from numba import cuda
    print(f"   CUDA available: {cuda.is_available()}")
    
    if not cuda.is_available():
        print("\n3. CUDA Detection Issues:")
        try:
            # Try to get more info
            import numba.cuda.cudadrv.driver as driver
            print(f"   Driver version: {driver.get_version() if hasattr(driver, 'get_version') else 'N/A'}")
        except Exception as e:
            print(f"   Error accessing driver: {e}")
        
        # Check if CUDA libraries are accessible
        cuda_path = os.environ.get('CUDA_PATH', '')
        if cuda_path:
            import os.path
            cudart_path = os.path.join(cuda_path, 'bin', 'cudart64_*.dll')
            print(f"   CUDA runtime DLL pattern: {cudart_path}")
            
            # List available CUDA DLLs
            import glob
            dlls = glob.glob(os.path.join(cuda_path, 'bin', 'cudart*.dll'))
            print(f"   Found CUDA runtime DLLs: {len(dlls)}")
            if dlls:
                for dll in dlls[:3]:  # Show first 3
                    print(f"     - {os.path.basename(dll)}")
    else:
        print(f"   GPU Device: {cuda.get_current_device()}")
        print(f"   Number of GPUs: {len(cuda.gpus)}")
        
except ImportError as e:
    print(f"   Error: {e}")
    print("   Install Numba: pip install numba")

# Check Python version
print(f"\n4. Python Version: {sys.version}")

# Check CUDA compiler
print("\n5. CUDA Compiler:")
import subprocess
try:
    result = subprocess.run(['nvcc', '--version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        for line in lines[:3]:
            if line.strip():
                print(f"   {line}")
    else:
        print("   nvcc not found or error running")
except Exception as e:
    print(f"   Error: {e}")

print("\n=== Recommendations ===")
if not cuda.is_available():
    print("CUDA is not detected by Numba. Possible solutions:")
    print("1. Install CUDA Toolkit 12.x (better compatibility with Numba 0.63.1)")
    print("2. Upgrade Numba: pip install --upgrade numba")
    print("3. Restart your computer after setting environment variables")
    print("4. Check Numba compatibility: https://numba.readthedocs.io/en/stable/cuda/overview.html")
else:
    print("CUDA is working! GPU acceleration is available.")
