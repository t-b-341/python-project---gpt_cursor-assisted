"""Pytest configuration. Prevent Pygame from opening a display during tests."""
import os

# Must run before any pygame import that might init display
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
