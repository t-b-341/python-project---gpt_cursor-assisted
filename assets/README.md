# Assets

All loadable assets live under this directory. Use `asset_manager.py` in the project root to load them; do not call `pygame.image.load`, `mixer.Sound`, or `font.Font` directly on these paths.

| Directory | Purpose |
|-----------|--------|
| `images/` | Sprites, textures (e.g. `.png`, `.jpg`). Use `get_image("name")`. |
| `sfx/`    | Short sound effects (e.g. `.wav`, `.ogg`). Use `get_sound("name")`. |
| `music/`  | Background music. Use `get_music_path("name")` then `pygame.mixer.music.load(path)`. |
| `fonts/`  | TrueType/OpenType fonts (e.g. `main.ttf`). Use `get_font("main", size)`. |
| `data/`   | Optional JSON/config files. Use `get_data_path("name")` or read manually. |

Missing files are handled gracefully: the asset manager logs a clear message and returns a fallback when possible (e.g. system font for fonts, a small placeholder surface for images).
