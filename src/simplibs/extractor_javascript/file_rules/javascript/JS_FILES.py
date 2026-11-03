from typing import Final
from simplibs.path.rules import HasSuffix
from simplibs.rules import Rule
# Outers
from ...constants import JS_SUFFIXES


JS_FILES: Final[Rule] = HasSuffix(*JS_SUFFIXES)
"""The file is JavaScript or TypeScript (`.js .jsx .ts .tsx .mjs .cjs`)."""


_DESIGN_NOTES = """
# JS_FILES — By Suffix Alone

## Purpose
The core of `build_js_base()`. HasSuffix compares case-insensitively and takes
several suffixes at once.

## JavaScript, TypeScript and React
The rule takes every JavaScript and TypeScript file, JSX and TSX included: a
React application and a Node project belong here alike.
"""
