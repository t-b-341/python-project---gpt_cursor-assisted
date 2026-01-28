You are modifying my existing game repo to fix several issues and polish the shader tooling and build pipeline.

DO NOT change the overall structure of the project (game.py, shader_effects/, scenes/, gpu_gl_utils.py, rendering_shaders.py, assets/, etc.). Only apply the specific changes below.

High-level goals:
- Make ShaderSettings preview honest and ready for real shader previews.
- Centralize registry→pipeline category mapping.
- Make ShaderSettings parameter adjustment target a selected uniform instead of “first float”.
- Improve ShaderTest logging (use logging instead of print).
- Prepare PyInstaller builds to bundle assets and add a resource-path helper.
- Document moderngl as an optional dependency.

Apply all changes below as ONE coherent refactor.

================================================================================
1) CENTRALIZE REGISTRY→PIPELINE CATEGORY MAPPING
================================================================================

We currently map registry categories (CORE/ATMOSPHERE/etc.) to pipeline categories (EARLY/MID/LATE/LAST) inside ShaderTestScene. That logic should live in one place.

1. Open shader_effects/pipeline.py.

2. At the top, where imports live, ensure we can import the registry category:

   from shader_effects.registry import ShaderCategory as RegistryCategory

3. Near the top of the file (after enums and before ShaderEntry), add a small helper function:

   def pipeline_category_for_registry_category(cat: RegistryCategory) -> "ShaderCategory":
       """
       Map registry ShaderCategory (semantic categories) to pipeline ShaderCategory (ordering).
       """
       mapping = {
           RegistryCategory.CORE: ShaderCategory.EARLY,
           RegistryCategory.RETRO: ShaderCategory.EARLY,
           RegistryCategory.COMBAT: ShaderCategory.MID,
           RegistryCategory.WATER: ShaderCategory.MID,
           RegistryCategory.ATMOSPHERE: ShaderCategory.LATE,
           RegistryCategory.OUTLINES: ShaderCategory.MID,
           RegistryCategory.LIGHTING: ShaderCategory.LATE,
           RegistryCategory.DEBUG: ShaderCategory.LAST,
       }
       return mapping.get(cat, ShaderCategory.MID)

   Adjust the default return value if needed, but MID is fine as a fallback.

4. Open scenes/shader_test.py.

   - Replace any local category mapping dict with calls to this helper. For example, where we currently do:

       category_map = { ... }
       self.shader_list = [
           (name, category_map.get(SHADER_SPECS[name].category, ShaderCategory.MID), None)
           for name in test_shader_names
       ]

     change it to:

       from shader_effects.pipeline import pipeline_category_for_registry_category
       ...
       self.shader_list = [
           (name, pipeline_category_for_registry_category(SHADER_SPECS[name].category), None)
           for name in test_shader_names
       ]

   This ensures future changes to category ordering only happen in one place.

================================================================================
2) SHADERTESTSCENE: SWITCH FROM print TO LOGGER
================================================================================

1. Open scenes/shader_test.py.

2. At the top of the file, add:

   import logging
   logger = logging.getLogger(__name__)

3. Replace all uses of print for status messages with logger.info or logger.debug. For example:

   print(f"[ShaderTest] {message}")

   becomes:

   logger.info("[ShaderTest] %s", message)

   And:

   print(f"[ShaderTest] Active shaders: {', '.join(enabled)}")

   becomes:

   logger.info("[ShaderTest] Active shaders: %s", ", ".join(enabled))

4. Ensure there are no leftover plain print calls in ShaderTestScene.

================================================================================
3) SHADERSETTINGSSCREEN: HONEST PREVIEW + PARAMETER SELECTION
================================================================================

We’ll do two things:
- Make it clear that the preview is currently a visual demo (not yet running real GPU shaders).
- Allow per-uniform selection so +/- adjusts the selected uniform, not just the first numeric value.

--------------------------------
3A) Add “visual demo” label to preview
--------------------------------

1. Open scenes/shader_settings.py.

2. In the method that renders the preview (likely _render_preview), after drawing the preview panel but before returning, add a small text label indicating that shaders are not yet applied in the preview.

   For example, inside _render_preview:

   - After you blit the scaled preview surface to the panel area, draw a small text at the top that says something like:

       "Preview (no shaders applied yet)"

   Use the existing font system you’re using in this file (whatever font/rendering you already use for other labels). The goal is for a user (or future you) to immediately understand that this is a demo and not a real shader preview.

   - Add a TODO comment in that method, something like:

       # TODO: Wire this preview to the actual GPU shader pipeline so selected shader + uniforms are applied.

--------------------------------
3B) Track selected parameter name instead of “first float”
--------------------------------

1. In ShaderSettingsScreen.__init__ (or whatever init sets up the screen state), add:

   - self.selected_param_index: int = 0
   - self._param_keys: list[str] = []

   These will track which uniform is currently selected in the parameter panel.

2. In the method that renders the parameter list (likely _render_parameters), build a stable list of parameter keys for the currently selected shader:

   - At the start of _render_parameters, after determining the selected shader, do something like:

       uniforms = self.shader_uniforms.get(self.selected_shader, {})
       param_items = list(uniforms.items())
       self._param_keys = [key for key, _ in param_items]

   - When you loop to draw each parameter (key, value), use the index from enumerate to check if it is the selected one:

       for idx, (key, value) in enumerate(param_items):
           is_selected = (idx == self.selected_param_index)
           # If is_selected, draw this row highlighted (e.g., different color, underline, or prefix "▶").

   Use whatever existing drawing style you have; the important part is that visually you can see which param is “active”.

3. Add keyboard navigation for parameter selection:

   - In the input handling of ShaderSettingsScreen (where you already handle left/right/category navigation and +/-):

       - Add something like:
           - Up arrow: move self.selected_param_index -= 1 (clamped at 0)
           - Down arrow: move self.selected_param_index += 1 (clamped at len(self._param_keys)-1)

       Only do this when there is a selected shader and at least one parameter.

4. Update the _adjust_parameter (or equivalent) method:

   - Instead of “first numeric uniform”, adjust the selected uniform.

   Replace logic like:

       uniforms = self.shader_uniforms.get(self.selected_shader, {})
       for key, value in uniforms.items():
           if isinstance(value, (int, float)):
               uniforms[key] = max(0.0, min(10.0, value + delta))
               self._update_preview_pipeline()
               break

   with something like:

       uniforms = self.shader_uniforms.get(self.selected_shader, {})
       if not uniforms or not self._param_keys:
           return

       # Clamp index
       if self.selected_param_index < 0:
           self.selected_param_index = 0
       if self.selected_param_index >= len(self._param_keys):
           self.selected_param_index = len(self._param_keys) - 1

       key = self._param_keys[self.selected_param_index]
       value = uniforms.get(key)

       if isinstance(value, (int, float)):
           # Simple clamp; adjust if you want per-uniform ranges later
           new_value = value + delta
           new_value = max(0.0, min(10.0, new_value))
           uniforms[key] = new_value
           self._update_preview_pipeline()

       # If it’s a tuple (e.g. vec3), you can later extend this to adjust a specific component.

5. Ensure that when you change selected_shader (e.g., move between shaders or categories), you reset:

   - self.selected_param_index = 0
   - self._param_keys = []

   so you don’t carry a stale index into a different shader’s param list.

================================================================================
4) PYINSTALLER: BUNDLE ASSETS + ADD RESOURCE PATH HELPER
================================================================================

To move toward “real” distributable builds:

--------------------------------
4A) Add a resource-path helper
--------------------------------

1. Create a new file at the repo root called resource_paths.py.

2. In resource_paths.py, add:

   import os
   import sys
   from typing import Union

   PathLike = Union[str, "os.PathLike[str]"]

   def get_resource_path(relative_path: PathLike) -> str:
       """
       Get absolute path to resource, working both in development and in a PyInstaller bundle.
       """
       base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
       return os.path.join(base_path, relative_path)

3. In any place where you load assets via relative paths (for example, when loading images, sounds, shaders, configs, etc.), switch from:

   os.path.join("assets", "something", "file.png")

   to:

   from resource_paths import get_resource_path
   ...
   path = get_resource_path(os.path.join("assets", "something", "file.png"))

   You don’t need to convert everything at once right now, but at least add a TODO comment in a central place (where assets are loaded) reminding yourself to use get_resource_path for assets that must work in a frozen EXE.

--------------------------------
4B) Update build_game.bat to include assets
--------------------------------

1. Open build_game.bat at the repo root.

2. Update the PyInstaller call to include the assets directory. For example, change:

   pyinstaller --onefile --name MyGame --noconfirm game.py

   to something like:

   pyinstaller --onefile --name MyGame --noconfirm ^
       --add-data "assets;assets" ^
       --add-data "config;config" ^
       game.py

   - If you don’t have a config/ folder, you can omit that line.
   - The syntax "assets;assets" is for Windows: "source;destination_inside_bundle".

3. Add a short comment above the PyInstaller call explaining that assets are being bundled:

   REM Bundle assets folder into the EXE for use with get_resource_path.

================================================================================
5) REQUIREMENTS / README: MODERNGL AS OPTIONAL DEP
================================================================================

1. Open requirements.txt.

2. Add moderngl as an optional dependency with a comment, e.g.:

   pygame>=2.0.0
   pytest>=7.0.0
   # numba optional
   moderngl>=5.0.0  # optional, required for GPU shader pipeline and shader test/settings scenes

3. Open README_build.md.

   - In the section that explains dev environment or dependencies, add a short note:

     - “If you want to use the GPU shader pipeline, Shader Test Mode, or Shader Settings GPU preview, install moderngl: `pip install moderngl`.”
     - Mention that when moderngl is NOT installed, the game will fall back to CPU effects and hide/disable GPU-specific scenes.

================================================================================
6) SHADERSETTINGSSCREEN & SHADERTESTSCENE: ENSURE MODERNGL GATING
================================================================================

This is more of a sanity check than a new feature.

1. Open scenes/shader_settings.py and scenes/shader_test.py.

2. Confirm they both:

   - Import HAS_MODERNGL from gpu_gl_utils.
   - Gate their behavior accordingly:

     - If HAS_MODERNGL is False:
         - Either never show these screens in the menu, OR
         - Immediately return to the previous scene and log that moderngl is unavailable.

3. If any of this is missing or inconsistent between the two scenes, fix it so they behave the same way and don’t try to create GL contexts when moderngl is not present.

================================================================================
7) FINAL PASS: CONSISTENCY & COMMENTS
================================================================================

1. In shader_effects/registry.py and shader_effects/pipeline.py, add brief comments at the top clarifying the different ShaderCategory concepts:

   - In registry.py:

       # ShaderCategory here describes semantic shader groups (CORE, ATMOSPHERE, etc.)
       # It is used for UI grouping and metadata, not pipeline ordering.

   - In pipeline.py:

       # ShaderCategory here describes pipeline ordering (EARLY, MID, LATE, LAST).
       # See pipeline_category_for_registry_category() for mapping from semantic categories.

2. Do a quick search for “TODO” and “FIXME” related to shader preview, GPU wiring, and resource paths, and make sure they’re either:
   - Accurate and useful, or
   - Removed if they no longer apply.

3. Run the game in:
   - CPU mode (no moderngl or config.use_gpu_shader_pipeline = False)
   - GPU mode (moderngl installed + config.use_gpu_shader_pipeline = True)

   and verify:
   - Game runs without crashes.
   - ShaderSettings doesn’t pretend the preview is a real shader preview.
   - ShaderTest logging goes through the logger, not print.
   - build_game.bat still completes and builds dist\MyGame.exe.

================================================================================
END OF CHANGESET
================================================================================

Make all edits described above. Fix any small syntax or import errors that arise as part of this refactor so that the project runs cleanly in both CPU and GPU modes.

