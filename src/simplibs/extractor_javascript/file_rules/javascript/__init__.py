from .JS_ASSET_DIRS import JS_ASSET_DIRS
from .JS_BASE import JS_BASE
from .JS_CONFIG import JS_CONFIG
from .JS_FILES import JS_FILES
from .JS_STRICT_EXCLUDE import JS_STRICT_EXCLUDE
from .JS_TESTS import JS_TESTS
from .build_js_base import build_js_base


_DESIGN_NOTES = """
# javascript — File Rules for JavaScript and TypeScript Projects

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component           | Type     | Description                                                      |
| :------------------ | :------- | :--------------------------------------------------------------- |
| `JS_ASSET_DIRS`     | Rule     | Inside a folder of files served as they are.                     |
| `JS_BASE`           | Rule     | The default choice of JavaScript and TypeScript files.           |
| `JS_CONFIG`         | Rule     | Tooling configuration files.                                     |
| `JS_FILES`          | Rule     | Files with a JavaScript or TypeScript suffix.                    |
| `JS_STRICT_EXCLUDE` | Rule     | Tests, configuration, type declarations, assets, packages, build output. |
| `JS_TESTS`          | Rule     | Test files, by name or by folder.                                |
| `build_js_base`     | Function | Builds the base rule; switches for `index.*` and `_*` files.     |
"""
