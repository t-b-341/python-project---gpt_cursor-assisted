"""
GPU-accelerated physics using Numba CUDA. Optional; fails soft to CPU when unavailable.

Single capability flag: CUDA_AVAILABLE — True only when the GPU path is usable.
Call sites should use the GPU path only when CUDA_AVAILABLE is True; otherwise use
the built-in CPU fallback (or the CPU helpers provided by this module when numba is
present but CUDA is not).

Requires for GPU: pip install numba cudatoolkit
"""

from __future__ import annotations

import sys

# Single capability flag: True only when GPU path is usable. Safe default.
CUDA_AVAILABLE = False


def _stub_update_bullets_batch(bullets_data, dt, screen_width, screen_height):
    """No-op fallback when GPU/JIT unavailable. Callers should use CPU path when CUDA_AVAILABLE is False."""
    return list(range(len(bullets_data)))


def _stub_check_collisions_batch(bullets_data, targets_data):
    """No-op fallback: no collisions (caller should use CPU path)."""
    return []


update_bullets_batch = _stub_update_bullets_batch
check_collisions_batch = _stub_check_collisions_batch


def _load_gpu_or_cpu():
    """Set CUDA_AVAILABLE and replace batch functions with GPU or CPU implementations. Never raises."""
    global CUDA_AVAILABLE, update_bullets_batch, check_collisions_batch
    try:
        from numba import cuda
        import numpy as np
        CUDA_AVAILABLE = bool(cuda.is_available())
    except Exception as e:
        print("gpu_physics: GPU/CUDA unavailable ({}). Using built-in CPU physics.".format(e), file=sys.stderr)
        return

    if CUDA_AVAILABLE:
        try:
            _define_gpu_path(cuda, np)
            return
        except Exception as e:
            print("gpu_physics: GPU path failed ({}). Falling back to CPU.".format(e), file=sys.stderr)
            CUDA_AVAILABLE = False

    try:
        from numba import njit
        _define_cpu_jit_path(np, njit)
    except Exception as e:
        print("gpu_physics: CPU JIT fallback unavailable ({}). Using no-op stubs.".format(e), file=sys.stderr)


def _define_gpu_path(cuda, np):
    """Define GPU implementations and assign to module-level names."""
    global update_bullets_batch, check_collisions_batch

    @cuda.jit
    def update_bullets_gpu(positions, velocities, dt, screen_width, screen_height, result_mask):
        idx = cuda.grid(1)
        if idx < positions.shape[0]:
            positions[idx, 0] += velocities[idx, 0] * dt
            positions[idx, 1] += velocities[idx, 1] * dt
            x, y = positions[idx, 0], positions[idx, 1]
            if x < -50 or x > screen_width + 50 or y < -50 or y > screen_height + 50:
                result_mask[idx] = 0
            else:
                result_mask[idx] = 1

    @cuda.jit
    def check_collisions_gpu(bullet_positions, bullet_sizes, target_positions, target_sizes, collisions):
        bullet_idx = cuda.grid(1)
        if bullet_idx >= bullet_positions.shape[0]:
            return
        bx = bullet_positions[bullet_idx, 0]
        by = bullet_positions[bullet_idx, 1]
        bw = bullet_sizes[bullet_idx, 0]
        bh = bullet_sizes[bullet_idx, 1]
        for target_idx in range(target_positions.shape[0]):
            tx = target_positions[target_idx, 0]
            ty = target_positions[target_idx, 1]
            tw = target_sizes[target_idx, 0]
            th = target_sizes[target_idx, 1]
            if not (bx + bw < tx or tx + tw < bx or by + bh < ty or ty + th < by):
                collisions[bullet_idx] = target_idx
                return
        collisions[bullet_idx] = -1

    def update_bullets_batch_impl(bullets_data, dt, screen_width, screen_height):
        if len(bullets_data) == 0:
            return []
        n = len(bullets_data)
        positions = np.zeros((n, 2), dtype=np.float32)
        velocities = np.zeros((n, 2), dtype=np.float32)
        for i, bullet in enumerate(bullets_data):
            positions[i, 0] = bullet.get("x", 0)
            positions[i, 1] = bullet.get("y", 0)
            velocities[i, 0] = bullet.get("vx", 0)
            velocities[i, 1] = bullet.get("vy", 0)
        d_positions = cuda.to_device(positions)
        d_velocities = cuda.to_device(velocities)
        d_result_mask = cuda.device_array(n, dtype=np.int32)
        threads_per_block = 256
        blocks_per_grid = (n + threads_per_block - 1) // threads_per_block
        update_bullets_gpu[blocks_per_grid, threads_per_block](
            d_positions, d_velocities, dt, screen_width, screen_height, d_result_mask
        )
        result_mask = d_result_mask.copy_to_host()
        positions_host = d_positions.copy_to_host()
        keep_indices = []
        for i in range(n):
            if result_mask[i] == 1:
                bullets_data[i]["x"] = float(positions_host[i, 0])
                bullets_data[i]["y"] = float(positions_host[i, 1])
                keep_indices.append(i)
        return keep_indices

    def check_collisions_batch_impl(bullets_data, targets_data):
        if len(bullets_data) == 0 or len(targets_data) == 0:
            return []
        n_bullets = len(bullets_data)
        n_targets = len(targets_data)
        bullet_positions = np.zeros((n_bullets, 2), dtype=np.float32)
        bullet_sizes = np.zeros((n_bullets, 2), dtype=np.float32)
        target_positions = np.zeros((n_targets, 2), dtype=np.float32)
        target_sizes = np.zeros((n_targets, 2), dtype=np.float32)
        for i, bullet in enumerate(bullets_data):
            bullet_positions[i, 0] = bullet.get("x", 0)
            bullet_positions[i, 1] = bullet.get("y", 0)
            bullet_sizes[i, 0] = bullet.get("w", 10)
            bullet_sizes[i, 1] = bullet.get("h", 10)
        for i, target in enumerate(targets_data):
            target_positions[i, 0] = target.get("x", 0)
            target_positions[i, 1] = target.get("y", 0)
            target_sizes[i, 0] = target.get("w", 20)
            target_sizes[i, 1] = target.get("h", 20)
        d_bullet_pos = cuda.to_device(bullet_positions)
        d_bullet_sizes = cuda.to_device(bullet_sizes)
        d_target_pos = cuda.to_device(target_positions)
        d_target_sizes = cuda.to_device(target_sizes)
        d_collisions = cuda.device_array(n_bullets, dtype=np.int32)
        threads_per_block = 256
        blocks_per_grid = (n_bullets + threads_per_block - 1) // threads_per_block
        check_collisions_gpu[blocks_per_grid, threads_per_block](
            d_bullet_pos, d_bullet_sizes, d_target_pos, d_target_sizes, d_collisions
        )
        collisions = d_collisions.copy_to_host()
        return [(i, int(t)) for i, t in enumerate(collisions) if t >= 0]

    update_bullets_batch = update_bullets_batch_impl
    check_collisions_batch = check_collisions_batch_impl


def _define_cpu_jit_path(np, njit):
    """Define CPU JIT implementations and assign to module-level names."""
    global update_bullets_batch, check_collisions_batch

    @njit
    def update_bullets_cpu_jit(positions, velocities, dt, screen_width, screen_height, result_mask):
        for i in range(positions.shape[0]):
            positions[i, 0] += velocities[i, 0] * dt
            positions[i, 1] += velocities[i, 1] * dt
            x, y = positions[i, 0], positions[i, 1]
            if x < -50 or x > screen_width + 50 or y < -50 or y > screen_height + 50:
                result_mask[i] = 0
            else:
                result_mask[i] = 1

    def update_bullets_batch_impl(bullets_data, dt, screen_width, screen_height):
        if len(bullets_data) == 0:
            return []
        n = len(bullets_data)
        positions = np.zeros((n, 2), dtype=np.float32)
        velocities = np.zeros((n, 2), dtype=np.float32)
        result_mask = np.ones(n, dtype=np.int32)
        for i, bullet in enumerate(bullets_data):
            positions[i, 0] = bullet.get("x", 0)
            positions[i, 1] = bullet.get("y", 0)
            velocities[i, 0] = bullet.get("vx", 0)
            velocities[i, 1] = bullet.get("vy", 0)
        update_bullets_cpu_jit(positions, velocities, dt, screen_width, screen_height, result_mask)
        keep_indices = []
        for i in range(n):
            if result_mask[i] == 1:
                bullets_data[i]["x"] = float(positions[i, 0])
                bullets_data[i]["y"] = float(positions[i, 1])
                keep_indices.append(i)
        return keep_indices

    def check_collisions_batch_impl(bullets_data, targets_data):
        return []

    update_bullets_batch = update_bullets_batch_impl
    check_collisions_batch = check_collisions_batch_impl


_load_gpu_or_cpu()
