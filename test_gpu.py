"""Test script to check GPU availability"""
try:
    from numba import cuda
    print(f"Numba CUDA available: {cuda.is_available()}")
    if cuda.is_available():
        print(f"GPU device: {cuda.get_current_device()}")
except ImportError:
    print("Numba not installed. Install with: pip install numba")
