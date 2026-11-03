# 🔢 `constants` — Fixed Values

The `constants` package holds the **names and patterns** the file rules, the scanner and the steps are built from: which
suffixes are JavaScript, which folders hold tests, packages and build output, which files configure a project — and the
compiled regular expressions that find an `import`, a `require` and an `export`.

```python
from simplibs.extractor_javascript.constants import JS_SUFFIXES, JS_IMPORT_PATTERN
```

The constants are importable from `simplibs.extractor_javascript.constants`; the package root does not export them.

Three kinds of value, three groups of cards:

| Group           | What it holds                                                                                          |
|-----------------|--------------------------------------------------------------------------------------------------------|
| **Names**       | Tuples of plain strings: suffixes, configuration files, folder names. The rules are built from them.   |
| **Patterns**    | Compiled `re.Pattern` objects that match **one statement on its own lines**. The steps use them.       |
| **The scanner** | A pattern, a set and a string that decide how the scanner reads a slash and keeps two tokens apart.    |

A few rules of the lists:

* **Names are compared as a whole.** A folder is `tests` or it is not; `contest` is not. A file is `package.json` — not
  `package.jsonc`.
* **The library keeps its own lists.** What counts as build output differs from language to language, so each add-on
  decides it for its own language instead of borrowing a list.
* **Version control is not here.** Its folder names are `IGNORE_VCS` of
  [`simplibs-path`](https://pypi.org/project/simplibs-path/), the same for every language.

---

## 🧭 Table of Contents

**Names**

* [`JS_SUFFIXES`](#js_suffixes)
* [`JS_CONFIG_NAMES`](#js_config_names)
* [`JS_TEST_DIR_NAMES`](#js_test_dir_names)
* [`JS_DEPENDENCY_DIR_NAMES`](#js_dependency_dir_names)
* [`JS_OUTPUT_DIR_NAMES`](#js_output_dir_names)
* [`JS_ASSET_DIR_NAMES`](#js_asset_dir_names)

**Patterns**

* [`JS_IMPORT_PATTERN`](#js_import_pattern)
* [`JS_REQUIRE_PATTERN`](#js_require_pattern)
* [`JS_EXPORT_LIST_PATTERN`](#js_export_list_pattern)
* [`JS_EXPORT_DEFAULT_NAME_PATTERN`](#js_export_default_name_pattern)
* [`JS_EXPORT_KEYWORD_PATTERN`](#js_export_keyword_pattern)

**The scanner**

* [`JS_CLOSING_TAG`](#js_closing_tag)
* [`JS_REGEX_KEYWORDS`](#js_regex_keywords)
* [`JS_SEPARATORS`](#js_separators)

[⬅️ Back to main README](../README.md#-constants)

---

## Names

### `JS_SUFFIXES`

**The suffixes of JavaScript and TypeScript source files.**

**Value:** `(".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")`

**Used by:** [`JS_FILES`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_files) (the rule that chooses files) and every
profile that has steps (`by_suffix(..., JS_SUFFIXES)` — the extractor gives a step the text only, never the path, so the
steps are chosen by the file type).

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_SUFFIXES

JS_SUFFIXES                                              # -> ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs')
".tsx" in JS_SUFFIXES                                    # -> True
".json" in JS_SUFFIXES                                   # -> False
```

**`.mjs` and `.cjs`.** ES modules and CommonJS files with an explicit module type. The old code did not know them.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_SUFFIXES: Final[tuple[str, ...]] = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")
```

A tuple: the rule is `HasSuffix(*JS_SUFFIXES)`, so adding a suffix is a change of one line here and nowhere else.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_CONFIG_NAMES`

**File names of JavaScript and TypeScript project configuration.**

**Value:** `("package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json", "next.config.js", "next.config.ts", "tailwind.config.js", "tailwind.config.ts", "postcss.config.js", "vite.config.ts", "webpack.config.js", "babel.config.js", "jest.config.js", "jest.config.ts", ".eslintrc.js", ".prettierrc")`

**Used by:** [`JS_CONFIG`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_config).

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_CONFIG_NAMES

"tsconfig.json" in JS_CONFIG_NAMES                       # -> True
"vite.config.ts" in JS_CONFIG_NAMES                      # -> True
"vite.config.js" in JS_CONFIG_NAMES                      # -> False     only the names on the list
```

**Tooling, not components.** These files describe how the project is built, linted and tested, not what it does. Most
are not source files and never get as far as the base rule; the list matters for the ones that **are**
(`vite.config.ts`, `jest.config.js`).

**The list is finite.** A configuration file that is not named here (`eslint.config.js`, `next.config.mjs`) is not
recognised as one: it is a source file to this library. A profile of your own can add names with
`NameIs(IsIn(...))`.

**The dot files.** `.eslintrc.js` and `.prettierrc` start with a dot, so `build_js_base()` already leaves them out; they
are named here so the strict exclusion is complete for a profile with an own, wider `include`.

<details>
<summary>🔍 Under the hood</summary>

```python
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
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_TEST_DIR_NAMES`

**Names of folders that hold JavaScript and TypeScript tests, mocks and coverage reports.**

**Value:** `("__tests__", "__mocks__", "e2e", "tests", "test", "coverage")`

**Used by:** [`JS_TESTS`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_tests): every file in a folder with one of these
names counts as a test, whatever the file is called.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_TEST_DIR_NAMES

"__tests__" in JS_TEST_DIR_NAMES                         # -> True
"coverage" in JS_TEST_DIR_NAMES                          # -> True
"contest" in JS_TEST_DIR_NAMES                           # -> False    whole names only
```

**`coverage` is not a test.** It is *generated from* the tests and has no place in a reading of the source, so it sits
with them.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_TEST_DIR_NAMES: Final[tuple[str, ...]] = ("__tests__", "__mocks__", "e2e", "tests", "test", "coverage")
```

The rule that uses it is `AnyParentNameIs(IsIn(JS_TEST_DIR_NAMES))`: `IsIn` compares a folder name as a whole.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_DEPENDENCY_DIR_NAMES`

**Names of folders that hold installed packages of a JavaScript project.**

**Value:** `("node_modules",)`

**Used by:** [`DEPENDENCY_DIRS`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#dependency_dirs). `node_modules` holds tens of
thousands of files that are not the project.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_DEPENDENCY_DIR_NAMES

JS_DEPENDENCY_DIR_NAMES                                  # -> ('node_modules',)
```

**Why its own constant.** The old code listed `node_modules` among the version-control folders. It is not version
control, and version control now comes from `simplibs-path`.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_DEPENDENCY_DIR_NAMES: Final[tuple[str, ...]] = ("node_modules",)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_OUTPUT_DIR_NAMES`

**Names of folders that hold generated build output of a JavaScript project.**

**Value:** `("build", "dist", "out", ".next")`

**Used by:** [`OUTPUT_DIRS`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#output_dirs). Build output repeats the source in
another shape; reading it twice only costs tokens.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_OUTPUT_DIR_NAMES

"dist" in JS_OUTPUT_DIR_NAMES                            # -> True
".next" in JS_OUTPUT_DIR_NAMES                           # -> True
"distribution" in JS_OUTPUT_DIR_NAMES                    # -> False
```

**`.next`.** The build folder of Next.js. It starts with a dot, but `build_js_base()` leaves out only dot **files**, so
without this name the compiled pages inside would be read as source.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_OUTPUT_DIR_NAMES: Final[tuple[str, ...]] = ("build", "dist", "out", ".next")
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_ASSET_DIR_NAMES`

**Names of folders that hold files served as they are** (images, fonts, static scripts).

**Value:** `("public", "static", "assets")`

**Used by:** [`JS_ASSET_DIRS`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_asset_dirs). A script in `public/` is copied to
the site untouched; it is not part of the application's source.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_ASSET_DIR_NAMES

JS_ASSET_DIR_NAMES                                       # -> ('public', 'static', 'assets')
```

**A known limit.** A folder with one of these names that holds **real source** (an `assets/` directory with code in it)
is left out by the strict rules. The **base** rule does not look at these names, so only the profile
`javascript/src-clean` is affected; use `javascript/code-clean`, or build your own `exclude`.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_ASSET_DIR_NAMES: Final[tuple[str, ...]] = ("public", "static", "assets")
```

</details>

[▲ Back to top](#-table-of-contents)

---

## Patterns

All five patterns are compiled with `re.MULTILINE`, start at the **beginning of a line** and end at the **end of a
statement**, so a match is a whole line (or lines) that can be cut out. They are tried **only** by
`find_matches_outside`, which drops every match that starts inside a string, a template literal or a comment.

### `JS_IMPORT_PATTERN`

**A whole ES `import` statement** on its own line(s).

**Used by:** [`remove_js_imports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#remove_js_imports).

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_IMPORT_PATTERN

def found(text):
    match = JS_IMPORT_PATTERN.search(text)
    return match.group(0) if match else None

found('import x from "m";')                             # -> 'import x from "m";'
found('import {a} from "m"')                             # -> 'import {a} from "m"'
found('import "m"')                                      # -> 'import "m"'
found('import type { T } from "m"')                      # -> 'import type { T } from "m"'
found("  import x from 'm'")                             # -> "  import x from 'm'"    the indentation is part of the match

found('import("m")')                                     # -> None      a dynamic import is an expression
found('const a = import("m")')                           # -> None
found('import a from "m"; run();')                       # -> None      the statement shares its line with code
```

**What it takes.** `import x from "m"`, `import { a, b as c } from "m"`, `import * as ns from "m"`, `import "m"`,
`import type { T } from "m"`, `import { "name" as x } from "m"`, and the same spread over several lines. A `;` on the
line after the statement belongs to it.

**What it leaves.** A dynamic `import("m")` — the `(` after `import` is excluded. A statement that shares its line with
other code or a comment; comments are removed first in the profiles.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_IMPORT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*import(?:\s+(?!\()|(?=[{*"']))(?:(?:[^'";{]|\{[^}]*\})*?\bfrom\s*)?"""
    r"""(["'])[^"'\n]+\1[ \t]*(?:\s*;)?[ \t]*$""",
    re.MULTILINE,
)
```

Read from the left: the start of a line and its indentation, the word `import` followed by whitespace that is **not** a `(`
(or directly by `{`, `*` or a quote, for `import{a}` and `import"m"`); an optional clause up to `from` that may contain
`{ … }`; the module in quotes; an optional `;`, possibly on the next line; the end of the line.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_REQUIRE_PATTERN`

**A CommonJS `const x = require("m")`** on its own line(s), with an optional `.member`; not one that goes on.

**Used by:** [`remove_js_requires`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#remove_js_requires).

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_REQUIRE_PATTERN

def found(text):
    match = JS_REQUIRE_PATTERN.search(text)
    return match.group(0) if match else None

found('const fs = require("fs");')                       # -> 'const fs = require("fs");'
found('var get = require("m").get;')                     # -> 'var get = require("m").get;'
found('const { a, b: { c } } = require("m")')            # -> 'const { a, b: { c } } = require("m")'

found('const a = require(name);')                        # -> None      not a plain string
found('const a = require("a"), b = require("b");')       # -> None      two declarators
found('var a = require("a")\n  , b = require("b");')      # -> None      comma-first: the statement goes on
```

**A statement that goes on.** Without a `;`, a statement ends at the end of its line only if the next line cannot
continue it. Comma-first style, a chained `.call()` or an operator at the start of the next line mean the declaration is
not finished, and removing the first line would leave a broken one.

**Limits.** One declarator per statement; destructuring nested two levels deep and without default values (outside the
innermost braces); the argument must be a plain string.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_REQUIRE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*(?:const|let|var)\s+(?:[\w$]+|\{(?:[^{}=;]|\{(?:[^{}=;]|\{[^{}]*\})*\})*\}|\[[^\[\]=;]*\])\s*=\s*"""
    r"""require\(\s*(["'])[^"'\n]+\1\s*\)(?:\.[A-Za-z_$][\w$]*)?"""
    r"""(?:\s*;[ \t]*$|[ \t]*$(?!\s*[,.(\[`+\-*/%<>=&|?:]))""",
    re.MULTILINE,
)
```

The end of the pattern has two ways out: a `;` (and the end of the line), **or** the end of the line when the next
non-blank character is **not** one that could continue the statement (`(?!\s*[,.(\[`+\-*/%<>=&|?:])`).

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_EXPORT_LIST_PATTERN`

**An export that only names things:** `export { a, b }`, `export * from "m"`, `export * as ns from "m"`,
`export type { T }`.

**Used by:** [`strip_js_exports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#strip_js_exports) — removed whole.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_EXPORT_LIST_PATTERN

def found(text):
    match = JS_EXPORT_LIST_PATTERN.search(text)
    return match.group(0) if match else None

found('export { a, b };')                                # -> 'export { a, b };'
found('export * from "m";')                              # -> 'export * from "m";'
found('export * as ns from "m"')                         # -> 'export * as ns from "m"'
found('export type { T };')                              # -> 'export type { T };'

found('export const a = 1;')                             # -> None      a declaration is code
```

`export { a, b }` and `export * from "./x"` declare nothing; for reading the code they are noise.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_EXPORT_LIST_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*export\s*(?:type\s+)?(?:\*(?:\s+as\s+[\w$]+)?|\{[^}]*\})\s*"""
    r"""(?:from\s*(["'])[^"'\n]+\1)?[ \t]*(?:\s*;)?[ \t]*$""",
    re.MULTILINE,
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_EXPORT_DEFAULT_NAME_PATTERN`

**`export default Name;`** — the default export of something declared elsewhere.

**Used by:** [`strip_js_exports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#strip_js_exports) — removed whole.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_EXPORT_DEFAULT_NAME_PATTERN

def found(text):
    match = JS_EXPORT_DEFAULT_NAME_PATTERN.search(text)
    return match.group(0) if match else None

found('export default App;')                             # -> 'export default App;'
found('export default App')                              # -> 'export default App'

found('export default function App() {}')                # -> None      carries code
found('export default FILE\n  ? a : b;')                 # -> None      a name that goes on is an expression
```

**A name that goes on.** `export default FILE` followed by `? a : b` on the next line is a conditional expression, not a
name: a line that the next one continues is not taken.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_EXPORT_DEFAULT_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*export\s+default\s+[A-Za-z_$][\w$]*"
    r"(?:\s*;[ \t]*$|[ \t]*$(?!\s*" + r"[,.(\[`+\-*/%<>=&|?:]" + r"))",
    re.MULTILINE,
)
```

The same "does the next line continue it?" look-ahead as `JS_REQUIRE_PATTERN`.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_EXPORT_KEYWORD_PATTERN`

**The keywords `export` or `export default` in front of a *named* declaration.** Group 1 is the indentation.

**Used by:** [`strip_js_exports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#strip_js_exports) — only the keyword is
cut.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_EXPORT_KEYWORD_PATTERN

def found(text):
    match = JS_EXPORT_KEYWORD_PATTERN.search(text)
    return (match.group(0), match.group(1)) if match else None

found('export function f() {}')                          # -> ('export ', '')
found('export default class App {}')                     # -> ('export default ', '')
found('  export const a = 1')                            # -> ('  export ', '  ')     group 1 is the indentation
found('export interface P {}')                           # -> ('export ', '')

found('export default function () {}')                   # -> None      anonymous: no name, no match
found('export default class extends X {}')               # -> None
found('export default () => {}')                         # -> None
```

**Only the keyword goes.** The match covers the keyword (and `default`) up to the declaration; the step cuts from the end
of group 1, so the indentation stays.

**An anonymous default stays.** `export default function () {}` and `export default class extends X {}` have no name:
without `export default` they would not be valid statements.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_EXPORT_KEYWORD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^([ \t]*)export\s+(?:default\s+(?=(?:async\s+)?function\s*\*?\s*[A-Za-z_$]"
    r"|class\s+(?!extends\b)[A-Za-z_$])"
    r"|(?=(?:declare\s+)?(?:async\s+)?(?:function|class|const|let|var|interface|type|enum|abstract)\b))",
    re.MULTILINE,
)
```

Two branches after `export`: **`default`** is taken only when a **name** follows (a look-ahead for `function Name`,
`async function Name`, `class Name`), and a plain declaration keyword (`function`, `class`, `const`, `let`, `var`,
`interface`, `type`, `enum`, `abstract`, with optional `declare` and `async`) is checked with a look-ahead and not
consumed.

</details>

[▲ Back to top](#-table-of-contents)

---

## The scanner

### `JS_CLOSING_TAG`

**What follows the `<` of a JSX closing tag:** `/div>`, `/Foo.Bar >`, `/>` of a fragment.

**Used by:** the scanner, through `regex_allowed`.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_CLOSING_TAG

bool(JS_CLOSING_TAG.match("/div>"))                      # -> True
bool(JS_CLOSING_TAG.match("/Foo.Bar >"))                 # -> True
bool(JS_CLOSING_TAG.match("/>"))                         # -> True       a fragment
bool(JS_CLOSING_TAG.match("/image\\/x/.test(s)"))        # -> False      a regular expression after `<`
bool(JS_CLOSING_TAG.match("/ 2"))                        # -> False
```

**`</div>` or `n </re/`?** After a `<`, a slash is either the start of a JSX closing tag or of a regular expression
(`n </image\/x/.test(s)`, a comparison with a literal). A closing tag is a slash, a tag name and `>`; anything else is a
regular expression. The pattern is tried **at the position of the slash**, with `Pattern.match`.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_CLOSING_TAG: Final[re.Pattern[str]] = re.compile(r"/[\w$.:\-]*\s*>")
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_REGEX_KEYWORDS`

**JavaScript words after which a `/` starts a regular expression and not a division.**

**Value:** `frozenset` of `await`, `case`, `delete`, `do`, `else`, `in`, `instanceof`, `new`, `of`, `return`, `throw`,
`typeof`, `void`, `yield`.

**Used by:** `regex_allowed`.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_REGEX_KEYWORDS

"return" in JS_REGEX_KEYWORDS                            # -> True      `return /b/.test(x)` — a regular expression
"a" in JS_REGEX_KEYWORDS                                 # -> False     `a / b` — a division
```

**Is this slash a division?** `a / b` divides and `return /b/.test(x)` starts a regular expression, and the only
difference is what stands in front of the slash. After a **word**, it is this list that decides: after `return`,
`typeof`, `case`… an expression begins, so a slash is a regex; after any other word (a variable, a number) it is a
division.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_REGEX_KEYWORDS: Final[frozenset[str]] = frozenset({
    "return", "typeof", "case", "do", "else", "in", "of", "void",
    "delete", "throw", "new", "yield", "await", "instanceof",
})
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_SEPARATORS`

**Characters that already keep two JavaScript tokens apart.**

**Value:** `" \t\r\n{}()[],;"`

**Used by:** the scanner, to decide whether a block comment is **glued** between two tokens.

**Example usage:**

```python
from simplibs.extractor_javascript.constants import JS_SEPARATORS

"(" in JS_SEPARATORS                                     # -> True
"a" in JS_SEPARATORS                                     # -> False

# a/**/b  -> `a` and `b` are not separators: the comment is glued, a space is left behind
# f(/**/x) -> `(` is a separator: the comment simply goes
```

When a block comment is cut out from between two tokens (`a/**/b`), the tokens must not touch afterwards: `ab` is a
different name. A character from this set on either side means they are separated anyway, and nothing has to be put in.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_SEPARATORS: Final[str] = " \t\r\n{}()[],;"
```

</details>

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-constants)
