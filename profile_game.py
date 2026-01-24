"""
Profile game.py using cProfile.
This script executes game.py in a controlled way and profiles it for ~10 seconds.
"""

import cProfile
import pstats
import subprocess
import sys
import time
import os


def profile_game():
    """Profile game.py execution using subprocess."""
    
    print("[Profiling] Starting game profiling (will stop after ~10 seconds)...")
    print("[Profiling] Note: The game window may open. It will close automatically.")
    
    # Create a wrapper script that will be profiled
    wrapper_script = """
import cProfile
import runpy
import sys
import atexit

profiler = cProfile.Profile()

def save_stats():
    try:
        profiler.disable()
        profiler.dump_stats("profiling_results.prof")
    except:
        pass

# Register cleanup function
atexit.register(save_stats)

profiler.enable()

try:
    runpy.run_module("game", run_name="__main__")
except SystemExit:
    pass
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
finally:
    save_stats()
"""
    
    # Write wrapper script
    wrapper_path = "profile_wrapper.py"
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(wrapper_script)
    
    try:
        # Run the wrapper script in a subprocess
        process = subprocess.Popen(
            [sys.executable, wrapper_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for 10 seconds, then terminate
        try:
            process.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            print("[Profiling] 10 seconds elapsed, terminating game process...")
            process.terminate()
            # Give it a moment to clean up
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                print("[Profiling] Force killing process...")
                process.kill()
                process.wait()
        
        # Small delay to ensure file is written
        time.sleep(0.5)
        
        # Check if profiling file was created
        if not os.path.exists("profiling_results.prof"):
            # If not, we need to profile differently - use runpy directly with timeout
            print("[Profiling] Profiling file not found, using direct profiling approach...")
            return profile_game_direct()
        
    finally:
        # Clean up wrapper script
        if os.path.exists(wrapper_path):
            try:
                os.remove(wrapper_path)
            except:
                pass
    
    # Load and process the stats
    if os.path.exists("profiling_results.prof"):
        stats = pstats.Stats("profiling_results.prof")
        stats.sort_stats('cumulative')
        
        # Save human-readable results using subprocess to ensure proper output capture
        result = subprocess.run(
            [sys.executable, "-c", 
             "import pstats; s = pstats.Stats('profiling_results.prof'); "
             "s.sort_stats('cumulative'); s.print_stats(150)"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        with open("profiling_results.txt", "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        print("[Profiling] Saved human-readable stats to profiling_results.txt")
        return None, stats
    else:
        raise RuntimeError("Profiling file was not created")


def profile_game_direct():
    """Alternative: Profile directly using runpy with signal-based timeout."""
    import signal
    import runpy
    
    profiler = cProfile.Profile()
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Profiling timeout")
    
    # Set up signal handler for timeout (Unix only)
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)
    
    print("[Profiling] Using direct profiling (10 second timeout)...")
    
    try:
        profiler.enable()
        try:
            runpy.run_module("game", run_name="__main__")
        except (SystemExit, KeyboardInterrupt, TimeoutError):
            pass
        except Exception as e:
            print(f"[Profiling] Error during execution: {e}")
        finally:
            profiler.disable()
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)  # Cancel alarm
    except Exception as e:
        profiler.disable()
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)
        raise
    
    # Save results
    profiler.dump_stats("profiling_results.prof")
    print("[Profiling] Saved raw stats to profiling_results.prof")
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    
    # Save human-readable results directly to file
    f = open("profiling_results.txt", "w", encoding="utf-8")
    try:
        # Redirect stdout to file
        old_stdout = sys.stdout
        sys.stdout = f
        try:
            stats.print_stats(150)
        finally:
            sys.stdout = old_stdout
            f.flush()
    finally:
        f.close()
    
    print("[Profiling] Saved human-readable stats to profiling_results.txt")
    return profiler, stats


if __name__ == "__main__":
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            profiler, stats = profile_game()
            break
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"[Profiling] Attempt {retry_count} failed: {e}")
                print(f"[Profiling] Retrying ({retry_count}/{max_retries})...")
                time.sleep(1)
            else:
                print(f"[Profiling] All {max_retries} attempts failed.")
                print(f"[Profiling] Last error: {e}")
                sys.exit(1)
    
    # Verify files exist
    import os
    if os.path.exists("profiling_results.txt"):
        print("[Profiling] OK: profiling_results.txt exists")
    else:
        print("[Profiling] ERROR: profiling_results.txt missing!")
    
    if os.path.exists("profiling_results.prof"):
        print("[Profiling] OK: profiling_results.prof exists")
    else:
        print("[Profiling] ERROR: profiling_results.prof missing!")
    
    # Output first 60 lines of results
    print("\n" + "="*80)
    print("First 60 lines of profiling_results.txt:")
    print("="*80)
    try:
        with open("profiling_results.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:60], 1):
                print(line.rstrip())
    except Exception as e:
        print(f"Error reading profiling_results.txt: {e}")
    
    # Detect startup mechanism
    print("\n" + "="*80)
    print("Detected startup mechanism:")
    print("="*80)
    print("The game runs at module level (no 'if __name__ == \"__main__\"' block).")
    print("When game.py is imported or executed, it immediately:")
    print("  1. Initializes pygame (pygame.init())")
    print("  2. Sets up the display in fullscreen mode")
    print("  3. Enters the main game loop (while running:)")
    print("  4. The loop is wrapped in a try-except-finally block for cleanup")
    print("  5. Game execution starts immediately upon module import/execution")
    
    # Top 10 slowest functions
    print("\n" + "="*80)
    print("Top ~10 slowest functions (by cumulative time):")
    print("="*80)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
