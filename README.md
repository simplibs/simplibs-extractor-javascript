# 🟨 `simplibs-extractor-javascript`

[![PyPI](https://img.shields.io/pypi/v/simplibs-extractor-javascript)](https://pypi.org/project/simplibs-extractor-javascript/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/LICENSE)
[![tests](https://github.com/simplibs/simplibs-extractor-javascript/actions/workflows/tests.yml/badge.svg)](https://github.com/simplibs/simplibs-extractor-javascript/actions)

**A JavaScript, TypeScript or React project in one document — the code, with or without its paperwork.**

The JavaScript add-on of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/). The extractor gathers the
text files of a folder into one document and knows **no language**; this library teaches it JavaScript and TypeScript
(React, JSX and TSX included): which files are worth reading, how to take **comments, imports, requires and exports**
out of a source, and four ready **profiles** that put it together. The source is read by a small **scanner** that knows
strings, template literals, regular expressions and comments — so a `//` inside `"http://x"` is not a comment.

```bash
pip install simplibs-extractor-javascript
simplibs-extractor javascript src-clean my_project
```

```python
from simplibs.extractor_javascript import strip_js_comments, remove_js_imports

strip_js_comments("const a = 1; // note\nconst u = 'http://x'; // a link\n")   # -> "const a = 1;\nconst u = 'http://x';\n"
remove_js_imports('import a from "m";\nx();\n')                               # -> 'x();\n'
```

> `pip install` is the whole installation: the library announces itself to the extractor through an entry point, so the
> profiles show up in `simplibs-extractor --list-systems` with nothing to import. The same steps are plain functions
> (`str -> str`) you can use without the extractor at all.

---

## 🧭 The Core Philosophy

Cleaning JavaScript with a few regular expressions works until the first file where it does not: a URL in a string, a
quote inside a regular expression, a code sample in a template literal, `a/**/b`. And a real parser for JavaScript, plus
TypeScript, plus JSX is a project of its own. `simplibs-extractor-javascript` takes the honest middle way:

* **A scanner that knows what a comment is.** One pass over the source follows strings, template literals (with the code
  inside `${ … }`), regular expressions and comments. A `//` in `"http://x"`, a `/*` in `/[/*]/` and a quote in
  `` `a ${ s.replace(/'/g, "") } b` `` are never mistaken for the real thing.
* **It cannot fail.** There is no syntax the scanner refuses, so none of the steps raises on a strange file. The worst a
  surprising source can do is spoil **the line it is on** — an unclosed string ends at its line. A file that is a little
  wrong must not stop a run over a thousand files.
* **Honest about its limits.** It is a scanner, not a parser. The places where a source can fool it are listed, with what
  the user then sees, in the [known limits](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#known-limits).
* **One scanner for everything.** `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`: the same steps. Nothing has to know types
  or tags to find a comment or an import line — so there is no separate "React" system.
* **Statements by line patterns, but only in code.** An `import`, a `require` or an `export` is found by a pattern at the
  start of a line, and only a match that **starts in code** counts: a line that merely looks like an import inside a
  template literal or a block comment is left alone.
* **Cut by position, change nothing else.** A removal cuts exactly the characters it found; the rest of the file stays as
  it was written — quotes, spacing, line breaks. `export` in front of a declaration loses only the keyword.
* **A name is a whole name.** A test is `App.test.tsx`, `a.spec.ts`, `test-utils.js` or anything in `__tests__/` — not
  `latest.js`, `contest.tsx` or `inspector.ts`. A folder is `tests` or it is not.
* **`index.*` and `_*` are source.** A root `index.js` is often the entry of an application and Next.js `pages/_app.tsx`
  is central; both are taken by default. A `.next` build folder is output even though it starts with a dot.
* **For reading, not for running.** The output of a removal is built for a reader — a person or a model: the names that
  were imported are still used, the `export` that made a function visible is gone. The profiles say so.
* **Functions first, actions on top.** Every step is a plain function; the action is a thin wrapper over the function of
  the same name, and the presets and profiles are built from the actions. The logic lives once.
* **Layers that only look left.** `constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin` —
  every layer imports only from those before it.

```python
strip_js_comments("<p>Don't</p> // c\nconst a = 1; // d\n")   # -> "<p>Don't</p> // c\nconst a = 1;\n"
# the apostrophe spoils ONE line (its comment stays); the next line is read correctly
```

---

## 📦 Installation

```bash
pip install simplibs-extractor-javascript
```

Requires Python 3.11+. The package brings [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/) with it,
and the command `simplibs-extractor` is available at once. Runtime dependencies, all from the same family:
[`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/) (the profile, the registry),
[`simplibs-text`](https://pypi.org/project/simplibs-text/) (cutting the found ranges, the whitespace presets),
[`simplibs-actions`](https://pypi.org/project/simplibs-actions/) (the steps as actions),
[`simplibs-path`](https://pypi.org/project/simplibs-path/) and [`simplibs-rules`](https://pypi.org/project/simplibs-rules/)
(the file rules) and [`simplibs-validate`](https://pypi.org/project/simplibs-validate/) (the checks of the signatures).

> **It is a Python package that reads JavaScript.** The steps run in Python and need no Node.js; the files they read can
> be of any of the six JavaScript and TypeScript kinds, whatever the language version.

---

## 🚀 Quick Start in 60 Seconds

### Level 1: The command line

```bash
simplibs-extractor javascript src-clean my_project                 # the application's own code, cleaned -> my_project/javascript_src_clean.md
simplibs-extractor javascript code-no-imports my_project           # the logic only
simplibs-extractor javascript code-clean,data-all my_project       # two profiles -> two files, one run
simplibs-extractor javascript data-all my_project --dry-run        # plan and report, write nothing
simplibs-extractor --list-profiles javascript                      # the four profiles
```

Which one? `data-all` gives the files as they are, `code-clean` takes the comments away, `src-clean` does the same and
leaves out tests, configuration, type declarations, assets and build folders, and `code-no-imports` takes also the
imports, requires and exports away.

### Level 2: The steps as functions

```python
from simplibs.extractor_javascript import (
    js_comment_spans, remove_js_imports, remove_js_requires, strip_js_comments, strip_js_exports,
)

strip_js_comments("a/**/b\nlet x = a /* c */ + b;\n")                  # -> 'a b\nlet x = a + b;\n'      a comment between two tokens leaves a space
js_comment_spans("const a = 1; // note\n")                             # -> [(12, 20)]
remove_js_imports('import { a, b as c } from "m"\nx()\n')              # -> 'x()\n'
remove_js_imports('const m = await import("m");\n')                    # -> 'const m = await import("m");\n'    a dynamic import stays
remove_js_requires('const fs = require("fs");\nx()\n')                 # -> 'x()\n'
strip_js_exports("export function f() {}\nexport { f };\n")            # -> 'function f() {}\n'                 the keyword goes, the declaration stays
```

### Level 3: Actions and ready-made chains

```python
from simplibs.extractor_javascript.actions import RemoveJsImports, StripJsComments
from simplibs.extractor_javascript.presets import JS_CLEAN, JS_NO_IMPORTS

steps = StripJsComments() >> RemoveJsImports()
steps('import a from "m";\n// c\nx(); // n\n')            # -> 'x();\n'

JS_CLEAN('import a from "m";\n\n\n\nx(); // n\n')        # -> 'import a from "m";\n\nx();\n'
JS_NO_IMPORTS('import a from "m";\n// the limit\nconst LIMIT = 10; // max\n\n\nexport function load(name) {\n  /* read */\n  return name;\n}\n')
# -> 'const LIMIT = 10;\nfunction load(name) {\n  return name;\n}\n'
```

### Level 4: Your own profile from the parts

File rules combine with `&`, `|` and `~`; the steps chain with `>>`; a registered profile is a name for both.

```python
from simplibs.extractor import Profile, by_suffix, extract, register_profile
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_TESTS
from simplibs.extractor_javascript.presets import JS_CLEAN

register_profile(Profile(
    system="javascript", name="tests-clean",
    description="The tests, without comments",
    include=JS_BASE & JS_TESTS,                          # JavaScript and TypeScript files that are tests
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_tests_clean.md",
))

extract(source="my_project", profile="javascript/tests-clean")
```

A changed copy of a profile of this library is one `dataclasses.replace` away:

```python
from dataclasses import replace
from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN

mine = replace(JS_SRC_CLEAN, name="mine", output_name="mine.md")
```

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/extractor_javascript/
├── constants/            ◄── Names (suffixes, folders, configuration), patterns (import, require, export), scanner values
├── file_rules/           ◄── Rules on the path inside the source (domain folder)
│   ├── atomic/           ◄── DOT_NAME, INDEX_NAME, UNDERSCORE_NAME, DEPENDENCY_DIRS, OUTPUT_DIRS, VCS_DIRS
│   └── javascript/       ◄── JS_FILES, JS_BASE, build_js_base, JS_TESTS, JS_CONFIG, JS_ASSET_DIRS, JS_STRICT_EXCLUDE
├── logic/                ◄── The steps: plain functions over the scanner
│   ├── js_comment_spans.py  strip_js_comments.py  remove_js_imports.py  remove_js_requires.py  strip_js_exports.py
│   └── _helpers/                                         ◄── Private: the scanner (scan_js and its skippers), pattern matching, cutting with gaps
├── actions/              ◄── The steps as Action classes (domain folder)
├── presets/              ◄── Ready-made chains: JS_CLEAN, JS_NO_IMPORTS (domain folder)
├── profiles/             ◄── The four Profile objects and JS_PROFILES (domain folder)
├── plugin/               ◄── register_all: the target of the entry point
└── py.typed
```

The folder `_helpers/` is private: it holds the scanner and the small tools of the steps.

The package root exports **the steps** and `register_all`. The four domain folders have their own `__all__` and are
imported through their domain — a function and an action are different kinds of thing and should stay visibly different
at the import line:

```python
from simplibs.extractor_javascript import strip_js_comments, remove_js_imports                  # the steps
from simplibs.extractor_javascript.actions import StripJsComments                               # the steps as actions
from simplibs.extractor_javascript.file_rules import JS_BASE, build_js_base                     # the rules
from simplibs.extractor_javascript.presets import JS_CLEAN                                      # ready-made chains
from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN                                 # the profiles as objects
```

The ranges the steps find are `simplibs.text.Span`; the type is taken from `simplibs-text`, not defined here.

---

## 🔧 `logic/` — The steps that read JavaScript and TypeScript

Plain functions: a source as a text in, a text out (one of them gives the positions of the comments). None of them has an
option and none raises on a source.

| Function             | Description / Parameters                                                                                                  |
|----------------------|---------------------------------------------------------------------------------------------------------------------------|
| `js_comment_spans`   | Finds the comments (`//` and `/* */`, JSDoc included); returns a `Span` for each, from the blanks in front to the end (`text`). |
| `strip_js_comments`  | Removes every comment; a line that held only a comment disappears, a comment between two tokens leaves a space (`text`). |
| `remove_js_imports`  | Removes the ES `import` statements, `import type` included; a dynamic `import("m")` stays (`text`).                       |
| `remove_js_requires` | Removes the CommonJS `const x = require("m")` declarations (`text`).                                                      |
| `strip_js_exports`   | Removes `export { … }`, `export * from "m"` and `export default Name;`, and the `export` keyword in front of a named declaration (`text`). |

➡️ [README_EXTRACTOR_JAVASCRIPT_LOGIC](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md)

---

## 🔗 `actions/` — The steps as pipeline actions

Every step except `js_comment_spans` is also an `Action` of
[`simplibs-actions`](https://pypi.org/project/simplibs-actions/): called with the **text** as its main input, chainable
with `>>`. The steps have no options, so every action is made with empty brackets: `StripJsComments()`.

| Action             | Over                 | Description                                              |
|--------------------|----------------------|----------------------------------------------------------|
| `StripJsComments`  | `strip_js_comments`  | Takes the comments out of the text flowing in.           |
| `RemoveJsImports`  | `remove_js_imports`  | Takes the ES `import` statements out.                    |
| `RemoveJsRequires` | `remove_js_requires` | Takes the CommonJS `require` declarations out.           |
| `StripJsExports`   | `strip_js_exports`   | Takes what only exports out, and keeps the declarations. |

➡️ [README_EXTRACTOR_JAVASCRIPT_ACTIONS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_ACTIONS.md)

---

## 🧩 `presets/` — Ready-made chains

Chains of actions, built once, that the profiles use.

| Preset          | Chain                                                                                                  |
|-----------------|--------------------------------------------------------------------------------------------------------|
| `JS_CLEAN`      | `StripJsComments() >> CLEANUP_WHITESPACE` — imports and exports stay.                                  |
| `JS_NO_IMPORTS` | `StripJsComments() >> RemoveJsImports() >> RemoveJsRequires() >> StripJsExports() >> COMPACT` — the logic only. |

`CLEANUP_WHITESPACE` squeezes blank runs to one line, `COMPACT` removes every blank line (also inside a template literal).

➡️ [README_EXTRACTOR_JAVASCRIPT_PRESETS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PRESETS.md)

---

## 📋 `profiles/` — The four profiles

Registered in the system `javascript`; also importable as `Profile` objects.

| Profile                      | Output                          | Description                                                                                   |
|------------------------------|---------------------------------|-----------------------------------------------------------------------------------------------|
| `javascript/code-clean`      | `javascript_code_clean.md`      | JavaScript and TypeScript without comments and extra blank lines (imports and exports stay).  |
| `javascript/code-no-imports` | `javascript_code_no_imports.md` | Pure logic: no imports, requires, exports, comments or blank lines.                           |
| `javascript/data-all`        | `javascript_data_all.md`        | Every relevant JavaScript and TypeScript file, as it is.                                      |
| `javascript/src-clean`       | `javascript_src_clean.md`       | Like `code-clean`, without tests, configuration, type declarations, assets and build folders. |

`JS_PROFILES` is the tuple of all four, in the order the listings show them.

➡️ [README_EXTRACTOR_JAVASCRIPT_PROFILES](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PROFILES.md)

---

## 📐 `file_rules/` — Which files are worth reading

Rules on the path **inside** the source folder: `Rule` objects of
[`simplibs-rules`](https://pypi.org/project/simplibs-rules/), composable with `&`, `|` and `~`.

| Rule / function     | Description / Parameters                                                                                           |
|---------------------|--------------------------------------------------------------------------------------------------------------------|
| `JS_FILES`          | Files with a JavaScript or TypeScript suffix: `.js .jsx .ts .tsx .mjs .cjs`.                                       |
| `JS_BASE`           | The default choice: those files, with `index.*` and `_*` files, without dot files.                                 |
| `build_js_base`     | Builds that rule with switches (keyword-only: `include_index=True`, `include_underscore=True`).                    |
| `JS_TESTS`          | A test by its whole name (`a.test.js`, `a.spec.ts`, `test-utils.js`) or by its folder (`__tests__/`, `e2e/`, ...). |
| `JS_CONFIG`         | Tooling configuration: `package.json`, `tsconfig.json`, `vite.config.ts`, ...                                      |
| `JS_ASSET_DIRS`     | Inside `public/`, `static/` or `assets/`.                                                                          |
| `JS_STRICT_EXCLUDE` | Tests, configuration, type declarations (`.d.ts`), assets, installed packages, build output and version control.   |

The atomic pieces they are made of: `DOT_NAME`, `INDEX_NAME`, `UNDERSCORE_NAME`, `DEPENDENCY_DIRS`, `OUTPUT_DIRS`,
`VCS_DIRS`.

➡️ [README_EXTRACTOR_JAVASCRIPT_FILE_RULES](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md)

---

## 🔖 `constants/`

| Group           | Names                                                                                                                  |
|-----------------|------------------------------------------------------------------------------------------------------------------------|
| **Names**       | `JS_SUFFIXES`, `JS_CONFIG_NAMES`, `JS_TEST_DIR_NAMES`, `JS_DEPENDENCY_DIR_NAMES`, `JS_OUTPUT_DIR_NAMES`, `JS_ASSET_DIR_NAMES` |
| **Patterns**    | `JS_IMPORT_PATTERN`, `JS_REQUIRE_PATTERN`, `JS_EXPORT_LIST_PATTERN`, `JS_EXPORT_DEFAULT_NAME_PATTERN`, `JS_EXPORT_KEYWORD_PATTERN` |
| **The scanner** | `JS_CLOSING_TAG`, `JS_REGEX_KEYWORDS`, `JS_SEPARATORS`                                                                 |

Importable from `simplibs.extractor_javascript.constants`.

➡️ [README_EXTRACTOR_JAVASCRIPT_CONSTANTS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md)

---

## 🔌 `plugin/` — The meeting point with the extractor

| Function       | Description / Parameters                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| `register_all` | Registers the four profiles in the extractor's registry and returns their keys; the target of the entry point `simplibs.extractor.plugins` (keyword-only: `replace_existing=True`). |

The entry point lives in this library's `pyproject.toml`; the extractor's `load_plugins()` finds it, so nothing is
imported by name. From Python, call `load_plugins()` of the extractor once before a profile is looked up.

➡️ [README_EXTRACTOR_JAVASCRIPT_PLUGIN](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PLUGIN.md)

---

## ⚠️ Exceptions

The library defines **no exceptions of its own** and the steps raise **none on a source**: the scanner has no syntax it
refuses, so a file that is a little wrong is read as well as it can be (see the known limits).

| Situation                                                                   | How it is reported                                                       |
|-----------------------------------------------------------------------------|--------------------------------------------------------------------------|
| A step called on **any text**                                               | a text back — never an error                                             |
| A wrong **type** of an argument (`text=5`)                                  | a `ValidationError` from `simplibs-validate`                             |
| A profile key that is taken, with `register_all(replace_existing=False)`    | the card of the extractor's registry (`EXTRACTOR_PROFILE_EXISTS`)        |

---

## 📚 Documentation

The detailed references — every function, rule and profile with its parameters, return value, raised errors, an example
and a look under the hood:

| Reference | What it describes |
|-----------|-------------------|
| [LOGIC](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md) | the five steps, the scanner and its known limits |
| [ACTIONS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_ACTIONS.md) | the steps as pipeline actions |
| [PRESETS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PRESETS.md) | `JS_CLEAN`, `JS_NO_IMPORTS` |
| [PROFILES](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PROFILES.md) | the four profiles, one file through each, a profile of your own |
| [FILE_RULES](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md) | which files are worth reading: the atomic pieces and the rules of a JavaScript project |
| [CONSTANTS](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md) | the names, the patterns and the values of the scanner |
| [PLUGIN](https://github.com/simplibs/simplibs-extractor-javascript/blob/main/docs/README_EXTRACTOR_JAVASCRIPT_PLUGIN.md) | `register_all` and how the extractor finds this add-on |

---

## 🔗 Related libraries

* **[`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/)** — the extractor this library is an add-on of: the six phases, the profiles and the command.
* **[`simplibs-extractor-python`](https://pypi.org/project/simplibs-extractor-python/)** — the sister add-on for Python projects; both can be installed side by side.
* **[`simplibs-text`](https://pypi.org/project/simplibs-text/)** — `remove_spans` cuts the ranges the steps find; `CLEANUP_WHITESPACE` and `COMPACT` close the presets.
* **[`simplibs-actions`](https://pypi.org/project/simplibs-actions/)** — the `Action` the steps are wrapped in.
* **[`simplibs-path`](https://pypi.org/project/simplibs-path/)** — the path rules (`HasSuffix`, `NameIs`, `AnyParentNameIs`) and `IGNORE_VCS`.
* **[`simplibs-rules`](https://pypi.org/project/simplibs-rules/)** — the `Rule` object and its building blocks (`IsIn`, `StartsWith`, `EndsWith`, `Regex`).
* **[`simplibs-validate`](https://pypi.org/project/simplibs-validate/)** — the checks of every signature.

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---
