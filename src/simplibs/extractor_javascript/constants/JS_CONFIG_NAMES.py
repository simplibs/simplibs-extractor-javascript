from typing import Final


JS_CONFIG_NAMES: Final[tuple[str, ...]] = (
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "tsconfig.json",
    "next.config.js",
    "next.config.ts",
    "tailwind.config.js",
    "tailwind.config.ts",
    "postcss.config.js",
    "vite.config.ts",
    "webpack.config.js",
    "babel.config.js",
    "jest.config.js",
    "jest.config.ts",
    ".eslintrc.js",
    ".prettierrc",
)
"""File names of JavaScript and TypeScript project configuration."""


_DESIGN_NOTES = """
# JS_CONFIG_NAMES — Tooling, Not Components

## Purpose
Used by `JS_CONFIG`. Build, lint and test tool settings.

## The Dot Files
`.eslintrc.js` and `.prettierrc` start with a dot, so `build_js_base()` already
leaves them out; they are named here so the strict exclusion is complete for
a profile with an own, wider `include`.
"""
