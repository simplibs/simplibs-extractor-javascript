# 🧩 `presets` — Ready-Made Pipeline Steps

The `presets` package holds **chains of actions, built once**: the two cleanings that the profiles use, as objects you
can drop into a pipeline or give to a profile as `steps`.

```python
from simplibs.extractor_javascript.presets import JS_CLEAN, JS_NO_IMPORTS
```

A preset is a pipeline step: you **call** it with a text, or you chain it with `>>`.

```python
from simplibs.extractor_javascript.presets import JS_CLEAN

JS_CLEAN('import a from "m";\n\n\n\nx(); // n\n')        # -> 'import a from "m";\n\nx();\n'
```

The presets are **not** exported from the package root — they are a domain of their own, with their own `__all__`,
imported through `simplibs.extractor_javascript.presets`. They stand to the right of
[`actions`](README_EXTRACTOR_JAVASCRIPT_ACTIONS.md) (a preset is built **from actions**) and to the left of
[`profiles`](README_EXTRACTOR_JAVASCRIPT_PROFILES.md) (which use them).

## The two presets

| Preset          | Chain                                                                                                     | Used by                                      |
|-----------------|-----------------------------------------------------------------------------------------------------------|----------------------------------------------|
| `JS_CLEAN`      | `StripJsComments() >> CLEANUP_WHITESPACE`                                                                 | `javascript/code-clean`, `javascript/src-clean` |
| `JS_NO_IMPORTS` | `StripJsComments() >> RemoveJsImports() >> RemoveJsRequires() >> StripJsExports() >> COMPACT`             | `javascript/code-no-imports`                 |

`CLEANUP_WHITESPACE` and `COMPACT` are presets of [`simplibs-text`](https://pypi.org/project/simplibs-text/).

## The same source, two presets

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

`JS_CLEAN` — **321 bytes** of 380:

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

`JS_NO_IMPORTS` — **185 bytes**:

```jsx
function Counter({ start }) {
  const [n, setN] = useState(start);
  const url = "http://example.com/#a";
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
const LIMIT = 10;
```

## A note on the order

Comments go **first**: an `import … ;` followed by a comment on the same line is a whole line only once the comment is
gone. Whitespace comes **last**, to tidy the holes the first steps left — the usual "last pass" of a pipeline.

## A note on tidy and compact

The two presets end differently, on purpose:

* **`CLEANUP_WHITESPACE`** squeezes every run of blank lines to **one**; it does not remove them. Code stays in
  paragraphs a person can read.
* **`COMPACT`** removes **every** blank line — also those inside a template literal. This is the shortest form, meant for
  a reader (or a model) that needs the code and not its layout.

```python
text = "const s = `\n\nkeep\n`;\nx();\n"                  # a blank line inside a template literal

JS_CLEAN(text)                                           # -> 'const s = `\n\nkeep\n`;\nx();\n'      the literal is intact
JS_NO_IMPORTS(text)                                      # -> 'const s = `\nkeep\n`;\nx();\n'        the blank line is gone
```

If a blank line **in a template literal** matters, use `JS_CLEAN` or build a chain of your own that ends with
`CLEANUP_WHITESPACE`.

## A note on sharing one object

A preset is created **once**, at import, and used wherever it is needed. That is safe because an action holds only its
options and no state between calls, so the same object can serve any number of pipelines and profiles. Each is declared
`Final`, so a type checker stops an accidental reassignment.

---

## 🧭 Table of Contents

* [`JS_CLEAN`](#js_clean)
* [`JS_NO_IMPORTS`](#js_no_imports)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-presets--ready-made-chains)

---

### `JS_CLEAN`

**JavaScript and TypeScript without comments, whitespace tidied — imports and exports stay.**

The everyday clean read: the steps of `javascript/code-clean` and `javascript/src-clean` as one object.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**

```python
from simplibs.extractor_javascript.presets import JS_CLEAN
from simplibs.extractor_javascript.actions import StripJsExports

JS_CLEAN("import a from 'm';\n\n\n\nx(); // n\n")        # -> "import a from 'm';\n\nx();\n"      the blank run is squeezed to one line

# the usual way to extend it: one more step in front of the tidy-up
(StripJsExports() >> JS_CLEAN)("export const a = 1;\n")  # -> 'const a = 1;\n'
```

**Safe to run twice.** A text that was cleaned is not changed by a second pass — each step finds nothing.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_CLEAN: Final = (
    StripJsComments()
    >> CLEANUP_WHITESPACE
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `JS_NO_IMPORTS`

**JavaScript and TypeScript reduced to their logic:** no comments, imports, requires or exports, and no blank lines.

The steps of `javascript/code-no-imports`: what the code does, not what it is wired to.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**

```python
from simplibs.extractor_javascript.presets import JS_NO_IMPORTS

JS_NO_IMPORTS('import a from "m";\n// the limit\nconst LIMIT = 10; // max\n\n\nexport function load(name) {\n  /* read */\n  return name;\n}\n')
# -> 'const LIMIT = 10;\nfunction load(name) {\n  return name;\n}\n'
```

**Compact, not tidy.** See [the note above](#a-note-on-tidy-and-compact): `COMPACT` removes every blank line, also inside
a template literal.

**The output is for reading, not for running.** `export` is gone, so a module cannot be imported from it; the names that
were imported are still used.

<details>
<summary>🔍 Under the hood</summary>

```python
JS_NO_IMPORTS: Final = (
    StripJsComments()
    >> RemoveJsImports()
    >> RemoveJsRequires()
    >> StripJsExports()
    >> COMPACT
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

This package raises **no cards of its own** and takes no options: a preset accepts any text, and the steps underneath
never refuse a source. An argument that is not a `str` is a `ValidationError` from the action that receives it.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-presets--ready-made-chains)
