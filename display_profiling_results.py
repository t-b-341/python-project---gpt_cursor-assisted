"""Display profiling results from existing files."""
import os
import pstats
from io import StringIO


def detect_startup_mechanism():
    """Detect how game.py starts."""
    try:
        with open("game.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if 'if __name__ == "__main__":' in content:
            if "main()" in content:
                return "if __name__ == '__main__': main()"
            else:
                return "if __name__ == '__main__': (direct execution)"
        elif "pygame.init()" in content:
            return "pygame.init() on import (runs immediately)"
        else:
            return "Unknown (likely runs on import)"
    except Exception as e:
        return f"Error detecting: {e}"


def summarize_slowest_functions(stats_lines):
    """Extract top ~10 slowest functions from stats."""
    slowest = []
    for line in stats_lines:
        # Skip header lines
        if not line.strip() or line.startswith("ncalls") or line.startswith("---"):
            continue
        
        # Parse pstats format: ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        parts = line.split()
        if len(parts) >= 5:
            try:
                # Try to extract cumulative time (usually 4th column)
                cumtime = float(parts[3])
                # Extract function name (last part after colon)
                func_part = parts[-1] if parts else ""
                if ":" in func_part:
                    func_name = func_part.split(":")[-1].strip("()")
                else:
                    func_name = func_part.strip("()")
                
                if func_name and cumtime > 0:
                    slowest.append((cumtime, func_name, line))
            except (ValueError, IndexError):
                continue
        
        # Stop after collecting ~10 meaningful entries
        if len(slowest) >= 10:
            break
    
    return slowest


def main():
    if not os.path.exists("profiling_results.prof"):
        print("Error: profiling_results.prof not found")
        return 1
    
    if not os.path.exists("profiling_results.txt"):
        print("Error: profiling_results.txt not found")
        return 1
    
    # Read the text file
    with open("profiling_results.txt", "r", encoding="utf-8") as f:
        stats_lines = f.read().splitlines()
    
    # Output results
    print("\n" + "="*80)
    print("PROFILING RESULTS - First 60 lines:")
    print("="*80)
    for i, line in enumerate(stats_lines[:60], 1):
        print(line)
    
    print("\n" + "="*80)
    print("DETECTED STARTUP MECHANISM:")
    print("="*80)
    print(detect_startup_mechanism())
    
    print("\n" + "="*80)
    print("TOP ~10 SLOWEST FUNCTIONS (by cumulative time):")
    print("="*80)
    slowest = summarize_slowest_functions(stats_lines)
    if slowest:
        for cumtime, func_name, full_line in slowest:
            print(f"  {cumtime:.4f}s - {func_name}")
            print(f"    {full_line[:100]}...")
    else:
        print("  (No function data available)")
    
    print("\n[Profiler] Display complete!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
