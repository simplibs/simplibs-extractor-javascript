# 📋 `profiles` — The Four Profiles

A **profile** is a name for "which files, how to clean them, what the output is called": rules on the path plus steps
that transform each file's text. The `profiles` package holds the four profiles of the system `javascript` as ordinary
`Profile` objects of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/).

```bash
simplibs-extractor javascript src-clean my_project
simplibs-extractor javascript code-clean,data-all my_project     # two profiles -> two files, one run
```

One system for **JavaScript, TypeScript and React** alike: the profiles take `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs` and
`.cjs`, and the same steps clean them all.

Registering the profiles is the job of [`register_all`](README_EXTRACTOR_JAVASCRIPT_PLUGIN.md#register_all) — it runs by
itself when the extractor finds this add-on. Having them as **objects** lets a program use one directly or build its own
on top of it:

```python
from dataclasses import replace
from simplibs.extractor import extract, register_profile
from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN

mine = replace(JS_SRC_CLEAN, name="mine", output_name="mine.md")          # a changed copy; the original is untouched
register_profile(mine)

extract(source="my_project", profile="javascript/mine")
```

The package has its own `__all__` and is **not** re-exported from the package root.

## Which profile when

| Profile                      | Output                          | Files                                                        | What happens to the text                                      |
|------------------------------|---------------------------------|--------------------------------------------------------------|---------------------------------------------------------------|
| `javascript/data-all`        | `javascript_data_all.md`        | every relevant JavaScript and TypeScript file                | nothing — as it is                                            |
| `javascript/code-clean`      | `javascript_code_clean.md`      | every relevant file                                          | comments (JSDoc too) and extra blank lines out; imports and exports stay |
| `javascript/code-no-imports` | `javascript_code_no_imports.md` | every relevant file                                          | comments, imports, requires, exports and blank lines out      |
| `javascript/src-clean`       | `javascript_src_clean.md`       | like `code-clean`, **without** tests, configuration, type declarations, assets and build folders | as `code-clean` |

"Every relevant file" is [`JS_BASE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_base): JavaScript and TypeScript files,
with `index.*` and `_*` files, without dot files.

## One file, four profiles

The file `src/Counter.jsx` of a small project (380 bytes):

```jsx
import React, { useState } from "react";
import "./App.css";
const fs = require("fs");

/**
 * The counter.
 */
export default function Counter({ start }) {
  // state
  const [n, setN] = useState(start); /* initial */
  const url = "http://example.com/#a"; // a link
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}

export const LIMIT = 10;
export { Counter as C };
```

`javascript/code-clean` and `javascript/src-clean` (the same steps) — **321 bytes**:

```jsx
import React, { useState } from "react";
import "./App.css";
const fs = require("fs");

export default function Counter({ start }) {
  const [n, setN] = useState(start);
  const url = "http://example.com/#a";
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}

export const LIMIT = 10;
export { Counter as C };
```

`javascript/code-no-imports` — **185 bytes**:

```jsx
function Counter({ start }) {
  const [n, setN] = useState(start);
  const url = "http://example.com/#a";
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
const LIMIT = 10;
```

`javascript/data-all` gives the file back as it is (380 bytes). The report of a run shows the same numbers file by file
(`bytes_in` → `bytes_out` of each `FileReport`).

## A file the scanner does not like

The steps never refuse a source: there is no `error` line for "not valid JavaScript". A strange file costs at most **one
line** of imperfection (see the [known limits](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#known-limits)) — a comment left
behind after an apostrophe in JSX text, say. A minified bundle on one line passes through with its imports in place.

---

## 🧭 Table of Contents

* [`JS_CODE_CLEAN`](#js_code_clean)
* [`JS_CODE_NO_IMPORTS`](#js_code_no_imports)
* [`JS_DATA_ALL`](#js_data_all)
* [`JS_SRC_CLEAN`](#js_src_clean)
* [`JS_PROFILES`](#js_profiles)
* [A profile of your own](#a-profile-of-your-own)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-profiles--the-four-profiles)

---

### `JS_CODE_CLEAN`

**The profile `javascript/code-clean`:** the code with its comments taken away.

**Fields:**

| Field         | Value                                                                                          |
|---------------|------------------------------------------------------------------------------------------------|
| `system`      | `"javascript"`                                                                                 |
| `name`        | `"code-clean"`                                                                                 |
| `description` | `"JavaScript and TypeScript without comments and extra blank lines (imports and exports stay)"` |
| `include`     | [`JS_BASE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_base)                                 |
| `exclude`     | *(none)*                                                                                       |
| `steps`       | [`JS_CLEAN`](README_EXTRACTOR_JAVASCRIPT_PRESETS.md#js_clean) for every suffix of `JS_SUFFIXES` |
| `output_name` | `"javascript_code_clean.md"`                                                                   |

**Example usage:**

```python
from simplibs.extractor import extract

result = extract(source="my_project", profile="javascript/code-clean")
result.target                                            # -> my_project/javascript_code_clean.md
[(f.relative, f.bytes_in, f.bytes_out) for f in result.ok_files]       # what the profile saved, file by file
```

JSDoc goes with the other comments. The tests, the configuration and the build folders are **in** the output — see
[`JS_SRC_CLEAN`](#js_src_clean) for the strict one.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_CODE_CLEAN: Final[Profile] = Profile(
    system="javascript",
    name="code-clean",
    description="JavaScript and TypeScript without comments and extra blank lines (imports and exports stay)",
    include=JS_BASE,
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_code_clean.md",
)
```

`by_suffix` of `simplibs-extractor` gives the same pipeline to the files of all six suffixes — the extractor hands a step
the text only, never the path, so the step is chosen by the file type.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_CODE_NO_IMPORTS`

**The profile `javascript/code-no-imports`:** pure logic — what the code does, not what it is wired to.

**Fields:**

| Field         | Value                                                                                          |
|---------------|------------------------------------------------------------------------------------------------|
| `system`      | `"javascript"`                                                                                 |
| `name`        | `"code-no-imports"`                                                                            |
| `description` | `"Pure logic: no imports, requires, exports, comments or blank lines"`                         |
| `include`     | [`JS_BASE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_base)                                 |
| `exclude`     | *(none)*                                                                                       |
| `steps`       | [`JS_NO_IMPORTS`](README_EXTRACTOR_JAVASCRIPT_PRESETS.md#js_no_imports) for every suffix of `JS_SUFFIXES` |
| `output_name` | `"javascript_code_no_imports.md"`                                                              |

**Example usage:**

```bash
simplibs-extractor javascript code-no-imports my_project       # -> my_project/javascript_code_no_imports.md
```

The output is **for reading, not for running**: the names that were imported are still used further down, and the
`export` that made a function visible is gone.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_CODE_NO_IMPORTS: Final[Profile] = Profile(
    system="javascript",
    name="code-no-imports",
    description="Pure logic: no imports, requires, exports, comments or blank lines",
    include=JS_BASE,
    steps=by_suffix(JS_NO_IMPORTS, JS_SUFFIXES),
    output_name="javascript_code_no_imports.md",
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_DATA_ALL`

**The profile `javascript/data-all`:** every relevant JavaScript and TypeScript file, as it is.

The files selected by `JS_BASE` and **no transformation**.

**Fields:**

| Field         | Value                                                                  |
|---------------|------------------------------------------------------------------------|
| `system`      | `"javascript"`                                                         |
| `name`        | `"data-all"`                                                           |
| `description` | `"Every relevant JavaScript and TypeScript file, as it is"`            |
| `include`     | [`JS_BASE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_base)         |
| `exclude`     | *(none)*                                                               |
| `steps`       | *(none)*                                                               |
| `output_name` | `"javascript_data_all.md"`                                             |

**Example usage:**

```bash
simplibs-extractor javascript data-all my_project --dry-run    # plan and report, write nothing
```

<details>
<summary>🔍 Under the hood</summary>

```python
JS_DATA_ALL: Final[Profile] = Profile(
    system="javascript",
    name="data-all",
    description="Every relevant JavaScript and TypeScript file, as it is",
    include=JS_BASE,
    output_name="javascript_data_all.md",
)
```

No `steps`: the extractor takes the text of each file and changes nothing.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_SRC_CLEAN`

**The profile `javascript/src-clean`:** like `code-clean`, without tests, configuration, type declarations, assets and
build folders — only what the application does.

The old strict React filter made visible: the old code defined it and no profile ever used it.

**Fields:**

| Field         | Value                                                                                                  |
|---------------|--------------------------------------------------------------------------------------------------------|
| `system`      | `"javascript"`                                                                                         |
| `name`        | `"src-clean"`                                                                                          |
| `description` | `"Like code-clean, without tests, configuration, type declarations, assets and build folders"`         |
| `include`     | [`JS_BASE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_base)                                         |
| `exclude`     | [`JS_STRICT_EXCLUDE`](README_EXTRACTOR_JAVASCRIPT_FILE_RULES.md#js_strict_exclude)                     |
| `steps`       | [`JS_CLEAN`](README_EXTRACTOR_JAVASCRIPT_PRESETS.md#js_clean) for every suffix of `JS_SUFFIXES`        |
| `output_name` | `"javascript_src_clean.md"`                                                                            |

**Example usage:**

```python
from simplibs.extractor import extract

result = extract(source="my_project", profile="javascript/src-clean")
[f.relative for f in result.ok_files]                    # -> ['src/App.tsx', 'src/index.tsx']     no *.test.tsx, no vite.config.ts, no .d.ts
```

A folder called `assets` or `static` that holds real source is left out too — see the
[known limit](README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_asset_dir_names).

<details>
<summary>🔍 Under the hood</summary>

```python
JS_SRC_CLEAN: Final[Profile] = Profile(
    system="javascript",
    name="src-clean",
    description="Like code-clean, without tests, configuration, type declarations, assets and build folders",
    include=JS_BASE,
    exclude=JS_STRICT_EXCLUDE,
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_src_clean.md",
)
```

The only difference from `JS_CODE_CLEAN` is the `exclude` and the output name. A `config` of one `extract` call can only
narrow these rules further (`include` by AND, `exclude` by OR), never widen them.

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_PROFILES`

**The profiles of the system `javascript`**, in the order the listing commands show them.

**Kind:** `tuple[Profile, ...]`.

**Example usage:**

```python
from simplibs.extractor_javascript.profiles import JS_PROFILES

[profile.key for profile in JS_PROFILES]
# -> ['javascript/code-clean', 'javascript/code-no-imports', 'javascript/data-all', 'javascript/src-clean']
```

<details>
<summary>🔍 Under the hood</summary>

```python
JS_PROFILES: Final[tuple[Profile, ...]] = (
    JS_CODE_CLEAN,
    JS_CODE_NO_IMPORTS,
    JS_DATA_ALL,
    JS_SRC_CLEAN,
)
```

`register_all` walks this tuple and registers each profile; add a profile to the system by adding it here.

</details>

[▲ Back to top](#-table-of-contents)

---

## A profile of your own

A profile is built from the parts in this library. Rules combine with `&`, `|` and `~`; steps chain with `>>`.

```python
from simplibs.extractor import Profile, by_suffix, register_profile
from simplibs.extractor_javascript.actions import RemoveJsImports, StripJsComments
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_TESTS, build_js_base
from simplibs.extractor_javascript.presets import JS_CLEAN

# only the tests, cleaned
register_profile(Profile(
    system="javascript", name="tests-clean",
    description="The tests, without comments",
    include=JS_BASE & JS_TESTS,
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_tests_clean.md",
))

# components only (no index and no underscore files), with imports out but exports kept
register_profile(Profile(
    system="javascript", name="components",
    description="Components: comments and imports out, exports stay",
    include=build_js_base(include_index=False, include_underscore=False),
    steps=by_suffix(StripJsComments() >> RemoveJsImports(), JS_SUFFIXES),
    output_name="javascript_components.md",
))
```

---

## Errors of this package

This package raises **no cards of its own**: the profiles are plain objects, built when the package is imported. A
profile that cannot work is refused by `Profile` itself (`EXTRACTOR_PROFILE_INVALID`).

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-profiles--the-four-profiles)
