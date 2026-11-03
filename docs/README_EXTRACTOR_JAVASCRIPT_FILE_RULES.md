# 📐 `file_rules` — Which Files Are Worth Reading

The `file_rules` package holds **rules on the path of a file** — the path **inside** the source folder, not the
absolute one. The profiles use them as `include` and `exclude`; they are ordinary `Rule` objects of
[`simplibs-rules`](https://pypi.org/project/simplibs-rules/), so a program can compose its own selection from them with
`&`, `|` and `~`.

```python
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_TESTS

only_tests = JS_BASE & JS_TESTS                         # JavaScript and TypeScript files that are tests
no_tests = JS_BASE & ~JS_TESTS                          # those that are not
```

The package has its own `__all__` and is **not** re-exported from the package root — a rule and a step are different
kinds of thing and stay visibly different at the import line.

## Two groups

| Group        | What it holds                                                                                              |
|--------------|------------------------------------------------------------------------------------------------------------|
| `atomic`     | The shared pieces — **one rule, one idea**: a dot name, `index.*`, a `_` name, version control, installed packages, build output. |
| `javascript` | The rules of a JavaScript or TypeScript project, **combined** from the atomic ones: the base choice, tests, configuration, assets, the strict exclusion. |

`atomic` ← `javascript`: the second only combines what the first defines.

## One set of rules for JavaScript, TypeScript and React

The rules take every JavaScript and TypeScript file — `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs` — so a React
application, a Node project and a TypeScript library belong here alike. There is no separate "React" system.

## How a rule is used

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_STRICT_EXCLUDE

JS_BASE.is_valid(Path("src/App.tsx"))                   # -> True
JS_BASE.is_valid(Path("src/.hidden.js"))                # -> False
JS_STRICT_EXCLUDE.is_valid(Path("src/App.test.tsx"))    # -> True    "this file is one of those"
```

In a profile the pair works like this: `include=JS_BASE` says what **may** enter, `exclude=JS_STRICT_EXCLUDE` says what
**may not**. The extractor judges the path relative to the source, so a project that merely lies inside a folder called
`tests` is not dropped as "a test".

## Which path passes

The two ends of the scale — the base choice (`javascript/code-clean`) and the strict one (`javascript/src-clean`):

| Path                       | `JS_BASE` | `JS_TESTS` | `JS_STRICT_EXCLUDE` | Taken by `src-clean`? |
|----------------------------|:---------:|:----------:|:-------------------:|:---------------------:|
| `src/App.tsx`              | ✅        |            |                     | ✅                    |
| `src/index.js`             | ✅        |            |                     | ✅                    |
| `pages/_app.tsx`           | ✅        |            |                     | ✅                    |
| `src/latest.js`            | ✅        |            |                     | ✅                    |
| `src/App.test.tsx`         | ✅        | ✅         | ✅                  |                       |
| `src/__tests__/App.js`     | ✅        | ✅         | ✅                  |                       |
| `src/types.d.ts`           | ✅        |            | ✅                  |                       |
| `vite.config.ts`           | ✅        |            | ✅                  |                       |
| `public/sw.js`             | ✅        |            | ✅                  |                       |
| `build/main.js`            | ✅        |            | ✅                  |                       |
| `node_modules/a/b.js`      | ✅        |            | ✅                  |                       |
| `src/.hidden.js`           |           |            |                     |                       |
| `README.md`, `src/a.json`  |           |            |                     |                       |

The extractor's scan normally skips housekeeping folders (version control, `node_modules`, ...) before a rule sees them.
The strict rules are a second fence for the case that the scan was told otherwise.

---

## 🧭 Table of Contents

**`atomic/` — the shared pieces**

* [`DOT_NAME`](#dot_name)
* [`INDEX_NAME`](#index_name)
* [`UNDERSCORE_NAME`](#underscore_name)
* [`DEPENDENCY_DIRS`](#dependency_dirs)
* [`OUTPUT_DIRS`](#output_dirs)
* [`VCS_DIRS`](#vcs_dirs)

**`javascript/` — the rules of a JavaScript or TypeScript project**

* [`JS_FILES`](#js_files)
* [`JS_BASE`](#js_base)
* [`build_js_base`](#build_js_base)
* [`JS_TESTS`](#js_tests)
* [`JS_CONFIG`](#js_config)
* [`JS_ASSET_DIRS`](#js_asset_dirs)
* [`JS_STRICT_EXCLUDE`](#js_strict_exclude)

[⬅️ Back to main README](../README.md#-file_rules--which-files-are-worth-reading)

---

## `atomic/` — the shared pieces

Every piece is **one rule of one idea**. The rules about folders use `AnyParentNameIs` of
[`simplibs-path`](https://pypi.org/project/simplibs-path/) (some folder **above** the file satisfies a rule) and `IsIn`
of `simplibs-rules` (a name is one of a set, compared as a whole).

### `DOT_NAME`

**The file name starts with a dot** (`.env`, `.eslintrc.js`).

Dot files are settings and tool state, not source. Used by the base rule.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import DOT_NAME

DOT_NAME.is_valid(Path(".eslintrc.js"))                  # -> True
DOT_NAME.is_valid(Path("src/.hidden.js"))                # -> True
DOT_NAME.is_valid(Path("src/App.js"))                    # -> False
DOT_NAME.is_valid(Path(".cache/App.js"))                 # -> False    only the NAME is judged
```

**Name only.** A visible file inside a `.cache` folder is not hidden by this rule; the strict exclusions look at folders.

<details>
<summary>🔍 Under the hood</summary>

```python
DOT_NAME: Final[Rule] = NameIs(StartsWith("."))
```

`NameIs` points a string rule (`StartsWith`) at the final name of the path.

</details>

[▲ Back to top](#-table-of-contents)

---

### `INDEX_NAME`

**The file name is `index` with any suffix** (`index.js`, `index.tsx`).

`index.*` usually only re-exports, but a root `index.js` is often the entry of the whole application.
[`build_js_base`](#build_js_base) decides by its `include_index` option.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import INDEX_NAME

INDEX_NAME.is_valid(Path("src/index.js"))                # -> True
INDEX_NAME.is_valid(Path("index.tsx"))                   # -> True
INDEX_NAME.is_valid(Path("src/indexer.js"))              # -> False
INDEX_NAME.is_valid(Path("src/index-utils.ts"))          # -> False
```

**The dot is part of the prefix.** `index.` and not `index`, so `indexer.js` and `index-utils.ts` are not index files.

<details>
<summary>🔍 Under the hood</summary>

```python
INDEX_NAME: Final[Rule] = NameIs(StartsWith("index."))
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `UNDERSCORE_NAME`

**The file name starts with an underscore** (`_app.tsx`, `_helpers.js`).

In JavaScript projects a leading underscore marks a private helper, and in Next.js `_app.tsx` and `_document.tsx` are
central. [`build_js_base`](#build_js_base) decides by its `include_underscore` option whether they are taken.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import UNDERSCORE_NAME

UNDERSCORE_NAME.is_valid(Path("pages/_app.tsx"))         # -> True
UNDERSCORE_NAME.is_valid(Path("src/_helpers.js"))        # -> True
UNDERSCORE_NAME.is_valid(Path("src/a_b.js"))             # -> False    only the START of the name
```

<details>
<summary>🔍 Under the hood</summary>

```python
UNDERSCORE_NAME: Final[Rule] = NameIs(StartsWith("_"))
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `DEPENDENCY_DIRS`

**The file lies inside a folder of installed packages** (`node_modules`).

Part of the strict exclusion. The names are
[`JS_DEPENDENCY_DIR_NAMES`](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_dependency_dir_names).

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import DEPENDENCY_DIRS

DEPENDENCY_DIRS.is_valid(Path("node_modules/react/index.js"))      # -> True
DEPENDENCY_DIRS.is_valid(Path("web/node_modules/a/b.js"))          # -> True     at any depth
DEPENDENCY_DIRS.is_valid(Path("src/modules/a.js"))                 # -> False    whole names only
```

<details>
<summary>🔍 Under the hood</summary>

```python
DEPENDENCY_DIRS: Final[Rule] = AnyParentNameIs(IsIn(JS_DEPENDENCY_DIR_NAMES))
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `OUTPUT_DIRS`

**The file lies inside a build-output folder** (`build`, `dist`, `out`, `.next`).

Part of the strict exclusion. The names are
[`JS_OUTPUT_DIR_NAMES`](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_output_dir_names).

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import OUTPUT_DIRS

OUTPUT_DIRS.is_valid(Path("build/main.js"))              # -> True
OUTPUT_DIRS.is_valid(Path(".next/server/page.js"))       # -> True     a Next.js build: a dot FOLDER
OUTPUT_DIRS.is_valid(Path("src/distribution/a.js"))      # -> False
```

<details>
<summary>🔍 Under the hood</summary>

```python
OUTPUT_DIRS: Final[Rule] = AnyParentNameIs(IsIn(JS_OUTPUT_DIR_NAMES))
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `VCS_DIRS`

**The file lies inside a version-control folder** (`.git`, `.svn`, `.hg`, `.bzr`).

Part of the strict exclusion. The names are `IGNORE_VCS` of `simplibs-path`: version control is the same for every
language, so the library borrows the list instead of keeping its own.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import VCS_DIRS

VCS_DIRS.is_valid(Path(".git/hooks/pre-commit.js"))      # -> True
VCS_DIRS.is_valid(Path(".github/workflows/ci.js"))       # -> False   `.github` is not `.git`
VCS_DIRS.is_valid(Path("src/app.js"))                    # -> False
```

**What changed from the old code.** The old list also held `node_modules` and `tmp`. Neither is version control:
`node_modules` has its own rule ([`DEPENDENCY_DIRS`](#dependency_dirs)), and `tmp` is dropped.

<details>
<summary>🔍 Under the hood</summary>

```python
VCS_DIRS: Final[Rule] = AnyParentNameIs(IsIn(IGNORE_VCS))
```

`IsIn` compares a folder name as a whole.

</details>

[▲ Back to top](#-table-of-contents)

---

## `javascript/` — the rules of a JavaScript or TypeScript project

### `JS_FILES`

**The file is JavaScript or TypeScript** (`.js .jsx .ts .tsx .mjs .cjs`).

The core of [`build_js_base`](#build_js_base): files by suffix alone. `HasSuffix` compares case-insensitively and takes
several suffixes at once.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_FILES

JS_FILES.is_valid(Path("a.js"))                          # -> True
JS_FILES.is_valid(Path("a.tsx"))                         # -> True
JS_FILES.is_valid(Path("a.mjs"))                         # -> True
JS_FILES.is_valid(Path("A.JS"))                          # -> True     case does not matter
JS_FILES.is_valid(Path("a.d.ts"))                        # -> True     a declaration file is a TypeScript file
JS_FILES.is_valid(Path("a.json"))                        # -> False
JS_FILES.is_valid(Path("a.vue"))                         # -> False
```

<details>
<summary>🔍 Under the hood</summary>

```python
JS_FILES: Final[Rule] = HasSuffix(*JS_SUFFIXES)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_BASE`

**The default choice of JavaScript and TypeScript files worth reading.**

`build_js_base()` with its defaults, built once. Every JavaScript profile of this library uses it as `include`:
JavaScript and TypeScript files, **with** `index.*` and `_*` files, without dot files.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_BASE

JS_BASE.is_valid(Path("src/App.tsx"))  # -> True
JS_BASE.is_valid(Path("src/index.js"))  # -> True     the entry of an application
JS_BASE.is_valid(Path("pages/_app.tsx"))  # -> True     the heart of a Next.js app
JS_BASE.is_valid(Path("src/types.d.ts"))  # -> True     in the base choice; the strict one leaves it out
JS_BASE.is_valid(Path("src/.hidden.js"))  # -> False    a dot file
JS_BASE.is_valid(Path("../README.md"))  # -> False    not JavaScript
```

**It does not look at tests, configuration or packages.** That is the job of
[`JS_STRICT_EXCLUDE`](#js_strict_exclude), and a profile chooses whether to use it.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_BASE: Final[Rule] = build_js_base()
```

The constant has a file of its own, and the function a name that differs from it by more than the case — see
[`build_js_base`](#build_js_base).

</details>

[▲ Back to top](#-table-of-contents)

---

### `build_js_base`

**Builds the rule that picks the JavaScript and TypeScript files worth reading.**

JavaScript and TypeScript files without dot files. Two switches decide the two kinds of file the old code always dropped.

**Parameters:**

| Name                 | Type   | Default | Description                                                                                |
|----------------------|--------|---------|--------------------------------------------------------------------------------------------|
| `include_index`      | `bool` | `True`  | Take `index.*` files. Switch off to leave out the files that only re-export. *(keyword-only)* |
| `include_underscore` | `bool` | `True`  | Take files whose name starts with `_` (`_app.tsx`). Switch off for private helpers only. *(keyword-only)* |

**Returns:** a `Rule` on the path relative to the source folder.

**Raises:** `ValidationError` — an option is not a `bool`.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import build_js_base

components = build_js_base(include_index=False, include_underscore=False)

components.is_valid(Path("src/App.tsx"))                 # -> True
components.is_valid(Path("src/index.js"))                # -> False
components.is_valid(Path("pages/_app.tsx"))              # -> False

build_js_base(include_index=False).is_valid(Path("pages/_app.tsx"))        # -> True    each switch alone
build_js_base(include_underscore=False).is_valid(Path("src/index.js"))     # -> True
```

**What changed from the old `ReactBase`.** The old rule dropped every `index.*` and every `_*` file. In a real project
that loses the root `index.js` (the entry of the application) and Next.js `pages/_app.tsx`. Both are taken by default
now; the switches bring the old behaviour back.

**Why the name starts with `build_`.** The constant [`JS_BASE`](#js_base) has a file of its own. On Windows and macOS two
files whose names differ only by case (`js_base.py`, `JS_BASE.py`) are the same file, so the function got a name that
differs by more than the case.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def build_js_base(*, include_index: bool = True, include_underscore: bool = True) -> Rule:

    # 1. The core: JavaScript and TypeScript files that are not hidden
    rule = JS_FILES & ~DOT_NAME

    # 2. The two kinds the old code always dropped, unless asked to leave them out
    if not include_underscore:
        rule = rule & ~UNDERSCORE_NAME
    if not include_index:
        rule = rule & ~INDEX_NAME

    return rule
```

The rule is a plain combination of the atomic pieces: a suffix, **and not** a dot name. The two switches only add one
more `& ~` each.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_TESTS`

**The file is a JavaScript test:** by its name (`a.test.js`, `a.spec.ts`) or by its folder (`__tests__/`).

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_TESTS

# by the name
JS_TESTS.is_valid(Path("src/App.test.tsx"))              # -> True
JS_TESTS.is_valid(Path("src/a.spec.ts"))                 # -> True
JS_TESTS.is_valid(Path("src/test-utils.js"))             # -> True
JS_TESTS.is_valid(Path("src/a_test.js"))                 # -> True
JS_TESTS.is_valid(Path("src/test.js"))                   # -> True
JS_TESTS.is_valid(Path("src/specs.js"))                  # -> True     `specs`, like `tests`, is allowed

# by the folder
JS_TESTS.is_valid(Path("src/__tests__/a.js"))            # -> True     a helper of the tests, whatever it is called
JS_TESTS.is_valid(Path("src/__mocks__/b.js"))            # -> True
JS_TESTS.is_valid(Path("e2e/login.ts"))                  # -> True
JS_TESTS.is_valid(Path("coverage/lcov.js"))              # -> True     generated from the tests

# not tests
JS_TESTS.is_valid(Path("src/latest.js"))                 # -> False
JS_TESTS.is_valid(Path("src/contest.tsx"))               # -> False
JS_TESTS.is_valid(Path("src/inspector.ts"))              # -> False
JS_TESTS.is_valid(Path("src/testing.js"))                # -> False
```

**A whole word.** `test` or `spec` (with an optional `s`) must stand **alone** in the name: at the start, or after `.`,
`-`, `_`, and be followed by one of them or by the end. `App.test.tsx`, `a.spec.ts` and `test-utils.js` are tests;
`latest.js`, `contest.tsx` and `inspector.ts` are not. The old rule asked whether the path *contained* `test` and threw
all of them away.

**Or anywhere inside a test folder.** `__tests__`, `__mocks__`, `e2e`, `tests`, `test` and `coverage`
([`JS_TEST_DIR_NAMES`](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_test_dir_names)). The rule looks at **every** folder
above the file.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_TESTS: Final[Rule] = (
    NameIs(Regex(r"(^|[._-])(test|spec)s?([._-]|$)"))
    | AnyParentNameIs(IsIn(JS_TEST_DIR_NAMES))
)
```

The first half judges the name, the second half the folders above it; `|` makes a file a test if **either** is true. The
pattern reads: the start of the name or one of `. _ -`, then `test` or `spec`, an optional `s`, then one of `. _ -` or
the end of the name.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_CONFIG`

**The file is JavaScript tooling configuration** (`package.json`, `tsconfig.json`, `vite.config.ts`, ...).

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_CONFIG

JS_CONFIG.is_valid(Path("package.json"))                 # -> True
JS_CONFIG.is_valid(Path("vite.config.ts"))               # -> True
JS_CONFIG.is_valid(Path("src/package.json"))             # -> True     only the NAME is judged, at any depth
JS_CONFIG.is_valid(Path("src/App.js"))                   # -> False
JS_CONFIG.is_valid(Path("eslint.config.js"))             # -> False    not on the list — see the note below
```

**Only the names on the list.** The list is
[`JS_CONFIG_NAMES`](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_config_names), and it is finite: a tool that names its
configuration differently is not recognised.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_CONFIG: Final[Rule] = NameIs(IsIn(JS_CONFIG_NAMES))
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_ASSET_DIRS`

**The file lies inside a folder of files served as they are** (`public`, `static`, `assets`).

A script in `public/` is copied to the site untouched; it is not part of the application's source. Part of the strict
exclusion.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_ASSET_DIRS

JS_ASSET_DIRS.is_valid(Path("public/sw.js"))             # -> True
JS_ASSET_DIRS.is_valid(Path("src/assets/c.js"))          # -> True     at any depth
JS_ASSET_DIRS.is_valid(Path("src/asset/a.js"))           # -> False    whole names only
JS_ASSET_DIRS.is_valid(Path("src/App.js"))               # -> False
```

<details>
<summary>🔍 Under the hood</summary>

```python
JS_ASSET_DIRS: Final[Rule] = AnyParentNameIs(IsIn(JS_ASSET_DIR_NAMES))
```

The names are [`JS_ASSET_DIR_NAMES`](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_asset_dir_names), including the known
limit: an `assets/` folder that holds real source is left out too.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_STRICT_EXCLUDE`

**Everything that is JavaScript-looking but not the application's own logic:** tests, configuration, type declarations,
assets, installed packages, build output and version control.

The `exclude` of the profile `javascript/src-clean`. The old code had a strict React filter like this, but no profile
ever used it — now one does.

**Kind:** `Rule` on a path.

**Example usage:**

```python
from pathlib import Path
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_STRICT_EXCLUDE

JS_STRICT_EXCLUDE.is_valid(Path("src/App.test.tsx"))     # -> True
JS_STRICT_EXCLUDE.is_valid(Path("src/types.d.ts"))       # -> True     a type declaration
JS_STRICT_EXCLUDE.is_valid(Path("vite.config.ts"))       # -> True
JS_STRICT_EXCLUDE.is_valid(Path("public/sw.js"))         # -> True
JS_STRICT_EXCLUDE.is_valid(Path("build/a.js"))           # -> True
JS_STRICT_EXCLUDE.is_valid(Path("node_modules/a/b.js"))  # -> True
JS_STRICT_EXCLUDE.is_valid(Path("src/App.tsx"))          # -> False
JS_STRICT_EXCLUDE.is_valid(Path("pages/_app.tsx"))       # -> False    underscore and index files are source

# the whole selection of `javascript/src-clean` as one rule
own_code = JS_BASE & ~JS_STRICT_EXCLUDE
own_code.is_valid(Path("src/App.tsx"))                   # -> True
own_code.is_valid(Path("src/App.test.tsx"))              # -> False
```

**Type declarations.** A `.d.ts` file only describes the types of code that exists elsewhere.

**How it combines.** Used together with `JS_BASE` as `include`: a file must be JavaScript or TypeScript **and** must not
be any of these. In a profile the two are given separately (`include=`, `exclude=`); a config you pass to one `extract`
call can only **narrow** them further.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_STRICT_EXCLUDE: Final[Rule] = (
    JS_TESTS
    | JS_CONFIG
    | NameIs(EndsWith(".d.ts"))
    | VCS_DIRS
    | DEPENDENCY_DIRS
    | OUTPUT_DIRS
    | JS_ASSET_DIRS
)
```

Seven rules joined by `|`: a file that matches **any** of them is excluded. The type-declaration rule is built in place:
the name ends with `.d.ts`.

</details>

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-file_rules--which-files-are-worth-reading)
