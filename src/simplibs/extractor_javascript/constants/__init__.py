from .JS_ASSET_DIR_NAMES import JS_ASSET_DIR_NAMES
from .JS_CLOSING_TAG import JS_CLOSING_TAG
from .JS_CONFIG_NAMES import JS_CONFIG_NAMES
from .JS_DEPENDENCY_DIR_NAMES import JS_DEPENDENCY_DIR_NAMES
from .JS_EXPORT_DEFAULT_NAME_PATTERN import JS_EXPORT_DEFAULT_NAME_PATTERN
from .JS_EXPORT_KEYWORD_PATTERN import JS_EXPORT_KEYWORD_PATTERN
from .JS_EXPORT_LIST_PATTERN import JS_EXPORT_LIST_PATTERN
from .JS_IMPORT_PATTERN import JS_IMPORT_PATTERN
from .JS_OUTPUT_DIR_NAMES import JS_OUTPUT_DIR_NAMES
from .JS_REGEX_KEYWORDS import JS_REGEX_KEYWORDS
from .JS_REQUIRE_PATTERN import JS_REQUIRE_PATTERN
from .JS_SEPARATORS import JS_SEPARATORS
from .JS_SUFFIXES import JS_SUFFIXES
from .JS_TEST_DIR_NAMES import JS_TEST_DIR_NAMES


_DESIGN_NOTES = """
# constants — Fixed Values of simplibs-extractor-javascript

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component                        | Type     | Description                                             |
| :------------------------------- | :------- | :------------------------------------------------------ |
| `JS_ASSET_DIR_NAMES`             | Constant | Folders of files served as they are.                    |
| `JS_CLOSING_TAG`                 | Pattern  | What follows the `<` of a JSX closing tag.              |
| `JS_CONFIG_NAMES`                | Constant | File names of JavaScript tooling configuration.         |
| `JS_DEPENDENCY_DIR_NAMES`        | Constant | Folders of installed packages.                          |
| `JS_EXPORT_DEFAULT_NAME_PATTERN` | Pattern  | `export default Name;`.                                 |
| `JS_EXPORT_KEYWORD_PATTERN`      | Pattern  | `export` / `export default` before a named declaration. |
| `JS_EXPORT_LIST_PATTERN`         | Pattern  | `export { a }`, `export * from "m"`.                    |
| `JS_IMPORT_PATTERN`              | Pattern  | An ES `import` statement.                               |
| `JS_OUTPUT_DIR_NAMES`            | Constant | Folders of generated build output.                      |
| `JS_REGEX_KEYWORDS`              | Constant | Words after which a slash starts a regular expression.  |
| `JS_REQUIRE_PATTERN`             | Pattern  | A CommonJS `const x = require("m")`.                    |
| `JS_SEPARATORS`                  | Constant | Characters that keep two tokens apart.                  |
| `JS_SUFFIXES`                    | Constant | Suffixes of JavaScript and TypeScript files.            |
| `JS_TEST_DIR_NAMES`              | Constant | Folders of JavaScript tests, mocks and coverage.        |

## Layering & Design
- Every value is a tuple, a set, a plain string or a compiled pattern: the rules and the steps are built from them.
- The names of version-control folders are not here: they come from `IGNORE_VCS` of `simplibs-path`.
"""
