from typing import Final


JS_ASSET_DIR_NAMES: Final[tuple[str, ...]] = ("public", "static", "assets")
"""Names of folders that hold files served as they are (images, fonts, static scripts)."""


_DESIGN_NOTES = """
# JS_ASSET_DIR_NAMES — Served, Not Compiled

## Purpose
Used by `JS_STRICT_EXCLUDE`. A script in `public/` is copied to the site
untouched; it is not part of the application's source.
"""
