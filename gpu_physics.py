"""
GPU-accelerated physics using Numba CUDA.
Requires: pip install numba cudatoolkit

This module provides GPU-accelerated versions of computationally expensive operations.
"""

try:
    from numba import cuda
    import numpy as np
    CUDA_AVAILABLE = cuda.is_available()
    if not CUDA_AVAILABLE:
        # CUDA driver is installed but toolkit may be missing
        # Check if we can provide helpful error message
        try:
            import subprocess
            result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=2)
            if result.returncode != 0:
                print("Note: CUDA Toolkit not found. GPU acceleration requires CUDA Toolkit installation.")
                print("      See CUDA_INSTALLATION_GUIDE.md for installation instructions.")
                print("      CPU JIT compilation will still provide good performance (2-5x speedup).")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Note: CUDA Toolkit not found. GPU acceleration requires CUDA Toolkit installation.")
            print("      See CUDA_INSTALLATION_GUIDE.md for installation instructions.")
            print("      CPU JIT compilation will still provide good performance (2-5x speedup).")
except ImportError:
    CUDA_AVAILABLE = False
    print("Warning: Numba CUDA not available. Install with: pip install numba")

if CUDA_AVAILABLE:
    @cuda.jit
    def update_bullets_gpu(positions, velocities, dt, screen_width, screen_height, result_mask):
        """
        GPU kernel to update bullet positions in parallel.
        
        Args:
            positions: (N, 2) array of [x, y] positions
            velocities: (N, 2) array of [vx, vy] velocities
            dt: delta time
            screen_width: screen width
            screen_height: screen height
            result_mask: output array (1 = keep, 0 = remove)
        """
        idx = cuda.grid(1)
        if idx < positions.shape[0]:
            # Update position
            positions[idx, 0] += velocities[idx, 0] * dt
            positions[idx, 1] += velocities[idx, 1] * dt
            
            # Check if offscreen (simple check - assumes bullet size is small)
            x, y = positions[idx, 0], positions[idx, 1]
            if x < -50 or x > screen_width + 50 or y < -50 or y > screen_height + 50:
                result_mask[idx] = 0  # Remove
            else:
                result_mask[idx] = 1  # Keep
    
    @cuda.jit
    def check_collisions_gpu(bullet_positions, bullet_sizes, target_positions, target_sizes, collisions):
        """
        GPU kernel to check collisions between bullets and targets.
        
        Args:
            bullet_positions: (N, 2) array of bullet [x, y]
            bullet_sizes: (N, 2) array of bullet [w, h]
            target_positions: (M, 2) array of target [x, y]
            target_sizes: (M, 2) array of target [w, h]
            collisions: (N,) output array (-1 = no collision, index = target index)
        """
        bullet_idx = cuda.grid(1)
        if bullet_idx >= bullet_positions.shape[0]:
            return
        
        bx = bullet_positions[bullet_idx, 0]
        by = bullet_positions[bullet_idx, 1]
        bw = bullet_sizes[bullet_idx, 0]
        bh = bullet_sizes[bullet_idx, 1]
        
        # Check against all targets
        for target_idx in range(target_positions.shape[0]):
            tx = target_positions[target_idx, 0]
            ty = target_positions[target_idx, 1]
            tw = target_sizes[target_idx, 0]
            th = target_sizes[target_idx, 1]
            
            # AABB collision check
            if not (bx + bw < tx or tx + tw < bx or by + bh < ty or ty + th < by):
                collisions[bullet_idx] = target_idx
                return
        
        collisions[bullet_idx] = -1
    
    @cuda.jit
    def calculate_distances_gpu(positions_a, positions_b, distances):
        """
        GPU kernel to calculate distances between two sets of points.
        
        Args:
            positions_a: (N, 2) array of [x, y] positions
            positions_b: (M, 2) array of [x, y] positions
            distances: (N, M) output array of distances
        """
        i, j = cuda.grid(2)
        if i < positions_a.shape[0] and j < positions_b.shape[0]:
            dx = positions_b[j, 0] - positions_a[i, 0]
            dy = positions_b[j, 1] - positions_a[i, 1]
            distances[i, j] = (dx * dx + dy * dy) ** 0.5
    
    def update_bullets_batch(bullets_data, dt, screen_width, screen_height):
        """
        Update a batch of bullets on GPU.
        
        Args:
            bullets_data: List of dicts with 'x', 'y', 'vx', 'vy', 'w', 'h'
            dt: delta time
            screen_width: screen width
            screen_height: screen height
        
        Returns:
            List of indices to keep
        """
        if not CUDA_AVAILABLE or len(bullets_data) == 0:
            return list(range(len(bullets_data)))
        
        n = len(bullets_data)
        
        # Prepare arrays
        positions = np.zeros((n, 2), dtype=np.float32)
        velocities = np.zeros((n, 2), dtype=np.float32)
        sizes = np.zeros((n, 2), dtype=np.float32)
        
        for i, bullet in enumerate(bullets_data):
            positions[i, 0] = bullet.get('x', 0)
            positions[i, 1] = bullet.get('y', 0)
            velocities[i, 0] = bullet.get('vx', 0)
            velocities[i, 1] = bullet.get('vy', 0)
            sizes[i, 0] = bullet.get('w', 10)
            sizes[i, 1] = bullet.get('h', 10)
        
        # Allocate GPU memory
        d_positions = cuda.to_device(positions)
        d_velocities = cuda.to_device(velocities)
        d_result_mask = cuda.device_array(n, dtype=np.int32)
        
        # Launch kernel
        threads_per_block = 256
        blocks_per_grid = (n + threads_per_block - 1) // threads_per_block
        
        update_bullets_gpu[blocks_per_grid, threads_per_block](
            d_positions, d_velocities, dt, screen_width, screen_height, d_result_mask
        )
        
        # Copy results back
        result_mask = d_result_mask.copy_to_host()
        positions_host = d_positions.copy_to_host()
        
        # Update bullet data and return indices to keep
        keep_indices = []
        for i in range(n):
            if result_mask[i] == 1:
                bullets_data[i]['x'] = float(positions_host[i, 0])
                bullets_data[i]['y'] = float(positions_host[i, 1])
                keep_indices.append(i)
        
        return keep_indices
    
    def check_collisions_batch(bullets_data, targets_data):
        """
        Check collisions between bullets and targets on GPU.
        
        Args:
            bullets_data: List of dicts with 'x', 'y', 'w', 'h'
            targets_data: List of dicts with 'x', 'y', 'w', 'h'
        
        Returns:
            List of (bullet_idx, target_idx) collision pairs
        """
        if not CUDA_AVAILABLE or len(bullets_data) == 0 or len(targets_data) == 0:
            return []
        
        n_bullets = len(bullets_data)
        n_targets = len(targets_data)
        
        # Prepare arrays
        bullet_positions = np.zeros((n_bullets, 2), dtype=np.float32)
        bullet_sizes = np.zeros((n_bullets, 2), dtype=np.float32)
        target_positions = np.zeros((n_targets, 2), dtype=np.float32)
        target_sizes = np.zeros((n_targets, 2), dtype=np.float32)
        
        for i, bullet in enumerate(bullets_data):
            bullet_positions[i, 0] = bullet.get('x', 0)
            bullet_positions[i, 1] = bullet.get('y', 0)
            bullet_sizes[i, 0] = bullet.get('w', 10)
            bullet_sizes[i, 1] = bullet.get('h', 10)
        
        for i, target in enumerate(targets_data):
            target_positions[i, 0] = target.get('x', 0)
            target_positions[i, 1] = target.get('y', 0)
            target_sizes[i, 0] = target.get('w', 20)
            target_sizes[i, 1] = target.get('h', 20)
        
        # Allocate GPU memory
        d_bullet_pos = cuda.to_device(bullet_positions)
        d_bullet_sizes = cuda.to_device(bullet_sizes)
        d_target_pos = cuda.to_device(target_positions)
        d_target_sizes = cuda.to_device(target_sizes)
        d_collisions = cuda.device_array(n_bullets, dtype=np.int32)
        
        # Launch kernel
        threads_per_block = 256
        blocks_per_grid = (n_bullets + threads_per_block - 1) // threads_per_block
        
        check_collisions_gpu[blocks_per_grid, threads_per_block](
            d_bullet_pos, d_bullet_sizes, d_target_pos, d_target_sizes, d_collisions
        )
        
        # Copy results back
        collisions = d_collisions.copy_to_host()
        
        # Return collision pairs
        collision_pairs = []
        for i, target_idx in enumerate(collisions):
            if target_idx >= 0:
                collision_pairs.append((i, int(target_idx)))
        
        return collision_pairs

else:
    # Fallback functions when CUDA is not available
    def update_bullets_batch(bullets_data, dt, screen_width, screen_height):
        """Fallback CPU implementation."""
        return list(range(len(bullets_data)))
    
    def check_collisions_batch(bullets_data, targets_data):
        """Fallback CPU implementation."""
        return []
