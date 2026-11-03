from .js_comment_spans import js_comment_spans
from .remove_js_imports import remove_js_imports
from .remove_js_requires import remove_js_requires
from .strip_js_comments import strip_js_comments
from .strip_js_exports import strip_js_exports


_DESIGN_NOTES = """
# logic — The Steps That Read JavaScript and TypeScript

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component            | Type     | Description                                                       |
| :------------------- | :------- | :---------------------------------------------------------------- |
| `js_comment_spans`   | Function | The spans of the comments (by the scanner).                       |
| `remove_js_imports`  | Function | Removes ES `import` statements.                                   |
| `remove_js_requires` | Function | Removes CommonJS `require` declarations.                          |
| `strip_js_comments`  | Function | Removes the comments.                                             |
| `strip_js_exports`   | Function | Removes what only exports; keeps declarations.                    |
| `_helpers`           | Private  | The scanner and the parts it is made of.                          |

## Layering & Design
- JavaScript is read by a scanner that knows strings, templates and regular expressions; it is not a parser and cannot fail.
- Statements are found by line patterns, and only those that start in code count.
- Each step is a function of a text and returns a text; the `Action` wrappers come in `actions`.
- The steps import only `constants`; the ranges they find are `simplibs.text.Span`.
"""
