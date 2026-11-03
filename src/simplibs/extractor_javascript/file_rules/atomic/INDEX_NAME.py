from typing import Final
from simplibs.path.rules import NameIs
from simplibs.rules import Rule, StartsWith


INDEX_NAME: Final[Rule] = NameIs(StartsWith("index."))
"""The file name is `index` with any suffix (`index.js`, `index.tsx`)."""


_DESIGN_NOTES = """
# INDEX_NAME — The Door of a Folder

## Purpose
`index.*` usually only re-exports, but a root `index.js` is often the entry
of the whole application. `build_js_base()` decides by its `include_index` option.

## The Dot Is Part of the Prefix
`index.` and not `index`, so `indexer.js` and `index-utils.ts` are not index
files.
"""
