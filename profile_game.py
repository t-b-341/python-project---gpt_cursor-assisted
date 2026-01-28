"""
Profile game.py execution using cProfile.

This script executes game.py in a controlled way using runpy, wraps it in cProfile,
and automatically stops profiling after ~10 seconds to avoid infinite loops.
Results are saved to profiling_results.txt (human-readable) and profiling_results.prof (for SnakeViz).
"""
import cProfile
import os
import pstats
import runpy
import sys
import threading
import time
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


def timeout_handler():
    """Stop profiling after ~10 seconds by quitting pygame."""
    time.sleep(10.0)
    print("\n[Profiler] 10 seconds elapsed, stopping profiling...")
    try:
        import pygame
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    except:
        pass


def run_profiling():
    """Run the profiling session."""
    print("[Profiler] Starting profiling session...")
    print("[Profiler] Detected startup mechanism:", detect_startup_mechanism())
    print("[Profiler] Will profile for ~10 seconds...")
    
    # Start timeout thread
    timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
    timeout_thread.start()
    
    # Create profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    try:
        # Execute game.py as __main__ using runpy
        # This simulates: python game.py
        print("[Profiler] Executing game.py...")
        runpy.run_module("game", run_name="__main__")
    except KeyboardInterrupt:
        print("\n[Profiler] Interrupted by user")
    except SystemExit:
        print("\n[Profiler] Game exited")
    except Exception as e:
        print(f"\n[Profiler] Error during execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        profiler.disable()
        print("[Profiler] Profiling stopped, saving results...")
    
    return profiler


def save_results(profiler_instance):
    """Save profiling results to files."""
    # Save raw stats for SnakeViz
    profiler_instance.dump_stats("profiling_results.prof")
    print("[Profiler] Saved raw stats to profiling_results.prof")
    
    # Generate human-readable stats
    stats_stream = StringIO()
    stats = pstats.Stats(profiler_instance, stream=stats_stream)
    stats.sort_stats("cumulative")
    stats.print_stats()
    
    # Get all lines and limit to top 150
    all_lines = stats_stream.getvalue().splitlines()
    top_lines = all_lines[:150]
    
    # Save to file
    with open("profiling_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(top_lines))
    
    print("[Profiler] Saved human-readable stats to profiling_results.txt (top 150 lines)")
    
    return top_lines


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
    """Main profiling entry point."""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Run profiling
            profiler_instance = run_profiling()
            
            # Check if we got any stats
            try:
                stats = pstats.Stats(profiler_instance)
                total_calls = stats.total_calls
                if total_calls == 0:
                    raise ValueError("No profiling data collected")
            except Exception as e:
                if retry_count < max_retries - 1:
                    print(f"[Profiler] No profiling data collected: {e}")
                    retry_count += 1
                    print("[Profiler] Retrying...")
                    time.sleep(2)
                    continue
                else:
                    print(f"[Profiler] Failed to collect profiling data after {max_retries} attempts")
                    return 1
            
            # Save results
            stats_lines = save_results(profiler_instance)
            
            # Verify files exist
            if os.path.exists("profiling_results.txt") and os.path.exists("profiling_results.prof"):
                print("[Profiler] ✓ Both profiling files created successfully")
            else:
                print("[Profiler] ✗ Warning: Some profiling files are missing")
            
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
            
            print("\n[Profiler] Profiling complete!")
            return 0
            
        except Exception as e:
            retry_count += 1
            print(f"\n[Profiler] Error occurred (attempt {retry_count}/{max_retries}): {e}")
            import traceback
            traceback.print_exc()
            
            if retry_count < max_retries:
                print("[Profiler] Retrying...")
                time.sleep(2)
            else:
                print("[Profiler] Max retries reached. Exiting.")
                return 1
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
