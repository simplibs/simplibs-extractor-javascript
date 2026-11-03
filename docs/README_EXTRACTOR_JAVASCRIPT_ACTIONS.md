# 🔗 `actions` — The Steps as Pipeline Actions

Every step of [`logic`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md) is also an `Action` of
[`simplibs-actions`](https://pypi.org/project/simplibs-actions/): configured once, called with the **text** as its main
input, and chainable with `>>`. That is the form a profile needs, because the `steps` of a profile are an action.

```python
from simplibs.extractor_javascript.actions import StripJsComments, RemoveJsImports

steps = StripJsComments() >> RemoveJsImports()

steps('import a from "m";\n// c\nx(); // n\n')           # -> 'x();\n'
```

## Where the actions are imported from

`actions/` is a **domain folder** with its own `__all__`; it is not re-exported from the package root. A function and an
action are different kinds of thing and should stay visibly different at the import line:

```python
from simplibs.extractor_javascript import strip_js_comments                # the function: text -> text
from simplibs.extractor_javascript.actions import StripJsComments          # the action: a step of a pipeline
```

## No options

The text flows through and there is **nothing to configure**: the steps have no options (a scanner has no `on_error` —
it cannot fail on a source). That is why every action is made with `StripJsComments()` — empty brackets.

## Thin wrappers

Each action is `create_action(function, main_param="text", class_name=...)` and nothing more — the logic lives once, in
the function.

| Action             | Over                 | Description                                                   |
|--------------------|----------------------|---------------------------------------------------------------|
| `StripJsComments`  | `strip_js_comments`  | Takes the comments out.                                       |
| `RemoveJsImports`  | `remove_js_imports`  | Takes the ES `import` statements out.                         |
| `RemoveJsRequires` | `remove_js_requires` | Takes the CommonJS `require` declarations out.                |
| `StripJsExports`   | `strip_js_exports`   | Takes what only exports out, and keeps the declarations.      |

`js_comment_spans` has no action: it does not turn a text into a text but into a list of positions, so it is not a step
of a pipeline.

---

## 🧭 Table of Contents

* [`StripJsComments`](#stripjscomments)
* [`RemoveJsImports`](#removejsimports)
* [`RemoveJsRequires`](#removejsrequires)
* [`StripJsExports`](#stripjsexports)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-actions--the-steps-as-pipeline-actions)

---

### `StripJsComments`

**Takes the comments out of the JavaScript or TypeScript text flowing in.** Action over
[`strip_js_comments`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#strip_js_comments).

**Main input:** the text (`str`). **Returns:** `str`. **Options:** none.

**Example usage:**

```python
from simplibs.extractor_javascript.actions import StripJsComments

StripJsComments()("const a = 1; // note\n// alone\n")    # -> 'const a = 1;\n'
StripJsComments()("a/**/b\n")                            # -> 'a b\n'          a comment between two tokens leaves a space
```

<details>
<summary>🔍 Under the hood</summary>

```python
StripJsComments = create_action(
    strip_js_comments,
    main_param="text",
    class_name="StripJsComments",
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `RemoveJsImports`

**Takes the ES import statements out of the JavaScript or TypeScript text flowing in.** Action over
[`remove_js_imports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#remove_js_imports).

**Main input:** the text (`str`). **Returns:** `str`. **Options:** none.

**Example usage:**

```python
from simplibs.extractor_javascript.actions import RemoveJsImports

RemoveJsImports()('import a from "m";\nx();\n')          # -> 'x();\n'
RemoveJsImports()('const m = await import("m");\n')      # -> 'const m = await import("m");\n'     a dynamic import stays
```

<details>
<summary>🔍 Under the hood</summary>

```python
RemoveJsImports = create_action(
    remove_js_imports,
    main_param="text",
    class_name="RemoveJsImports",
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `RemoveJsRequires`

**Takes the CommonJS `require` declarations out of the JavaScript text flowing in.** Action over
[`remove_js_requires`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#remove_js_requires).

**Main input:** the text (`str`). **Returns:** `str`. **Options:** none.

**Example usage:**

```python
from simplibs.extractor_javascript.actions import RemoveJsRequires

RemoveJsRequires()('const fs = require("fs");\nx();\n')   # -> 'x();\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
RemoveJsRequires = create_action(
    remove_js_requires,
    main_param="text",
    class_name="RemoveJsRequires",
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `StripJsExports`

**Takes the exports out of the JavaScript or TypeScript text flowing in, and keeps the declarations.** Action over
[`strip_js_exports`](logic/README_EXTRACTOR_JAVASCRIPT_LOGIC.md#strip_js_exports).

**Main input:** the text (`str`). **Returns:** `str`. **Options:** none.

**Example usage:**

```python
from simplibs.extractor_javascript.actions import StripJsExports

StripJsExports()("export const a = 1;\nexport { a };\n")  # -> 'const a = 1;\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
StripJsExports = create_action(
    strip_js_exports,
    main_param="text",
    class_name="StripJsExports",
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

This package raises **no cards of its own**, and the steps underneath raise none either — a scanner has no source it
refuses. A wrong type of the input (`5` instead of a text) is a `ValidationError` from
[`simplibs-validate`](https://pypi.org/project/simplibs-validate/), raised by the action that receives it.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-actions--the-steps-as-pipeline-actions)
