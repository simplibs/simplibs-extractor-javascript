# 🔧 `logic` — The Steps That Read JavaScript and TypeScript

The `logic` package holds the **steps**: plain functions that take a JavaScript or TypeScript source as text and give
back a text (or, for one of them, the positions of the comments). One scanner reads every kind of source — JavaScript,
TypeScript, JSX and TSX alike — so a `//` inside `"http://x"` is not a comment, an `import` in a template literal is not
an import, and `/` in `a / b` is not the start of a regular expression.

```python
from simplibs.extractor_javascript import (
    js_comment_spans,
    remove_js_imports,
    remove_js_requires,
    strip_js_comments,
    strip_js_exports,
)
```

All five are exported from the package root. The same steps as pipeline actions live in
[`actions`](../README_EXTRACTOR_JAVASCRIPT_ACTIONS.md).

## A scanner, not a parser

The Python add-on has `ast` to lean on; JavaScript has nothing like it in the standard library, and a real parser for
JavaScript **plus** TypeScript **plus** JSX is a project of its own. This library takes the honest middle way:

| The scanner **knows**                                                       | The scanner **does not know**                       |
|-----------------------------------------------------------------------------|-----------------------------------------------------|
| strings (`'…'`, `"…"`) with their escapes                                   | types, generics, decorators                         |
| template literals, with the **code inside `${ … }`** (nested ones too)      | JSX tags and what is inside them                    |
| regular expression literals (a `/` inside `[ … ]` does not close them)       | which `/` after `)` or `}` is a division           |
| `//` and `/* … */` comments, JSDoc included                                 | whether the file is valid at all                    |
| whether a `/` is a division or the start of a regular expression (a rule of thumb, see below) | |

It is **not** a parser and it **cannot fail**: there is no syntax it refuses, so none of the steps raises on a strange
file. The worst a surprising source can do is spoil **the line it is on** — an unclosed string ends at its line, an
unclosed regular expression is dropped at its line. That is the design: a file that is a little wrong must not stop a
run over a thousand files.

On top of the scanner the statements are found by **line patterns** (`import … from "m"`, `export { … }`, …), and only
matches that **start in code** count — a line that merely looks like an import inside a string, a template literal or a
block comment is left alone.

## What each step takes away

One source, five steps:

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

| Step                 | Takes away                                                                  | Leaves                                                      |
|----------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|
| `strip_js_comments`  | the JSDoc block, `// state`, `/* initial */`, `// a link`                   | the string `"http://example.com/#a"`, everything else       |
| `remove_js_imports`  | `import React, { useState } from "react";`, `import "./App.css";`           | the `require`, all comments, all exports                    |
| `remove_js_requires` | `const fs = require("fs");`                                                 | the `import` lines                                          |
| `strip_js_exports`   | `export { Counter as C };` — and the word `export default` / `export` in front of a declaration | `function Counter(…)`, `const LIMIT = 10;`     |
| `js_comment_spans`   | nothing — it only **reports** where the four comments are                   | the text                                                    |

## The contract all of them share

| Rule                                  | What it means                                                                                         |
|---------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Text in, text out**                 | `str` → `str`. `js_comment_spans` returns the positions of the comments, `list[Span]`.                |
| **Never raises on a source**          | There is no `on_error` and no error card: the scanner has no syntax it refuses. A wrong **type** of the argument (`text=5`) is a `ValidationError` from `simplibs-validate`. |
| **Cut by position, nothing else**     | A removal cuts exactly the characters it found; the rest of the file stays as it was written — quotes, spacing, line breaks. |
| **Whole statements, or the keyword**  | `import`, `require` and list exports are removed **with their whole line(s)**; `export` in front of a declaration removes **only the keyword**. |
| **Nothing to do, nothing changed**    | A text without anything to remove comes back as the very same text.                                   |
| **Idempotent**                        | A second run finds nothing and returns the same text.                                                 |
| **Whatever the type, one scanner**    | `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`: the same steps. Nothing has to know types or tags to find a comment or an import line. |
| **`\n` only**                         | The line patterns end at `\n`. The extractor's reader hands over `\n` only; for a text you read yourself, normalise `\r\n` first. |

The output of a removal is **for reading, not for running**: the names that were imported are still used, the
`export` that made a function visible is gone. That is the point of the profiles that use them.

## Known limits

The scanner is honest about what it is. These are the places where a source can fool it — each costs at most **one
line**, and each is listed with what the user then sees:

| Source                                           | What happens                                                                                  |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `{/* note */}` in JSX                            | The comment goes, the brackets stay: `{}`. Removing them needs a JSX parser.                  |
| `<p>Don't</p> // c`                              | The apostrophe opens a "string" that ends at the end of the line, so the **comment on that line stays**. The next line is read correctly. |
| `if (x) /re'/.test(y); // c`                     | A slash after `)` or `}` is taken for a division, where it starts a regular expression: a quote in it can hide **one comment on that line**. |
| `case 1://note`                                  | A `//` right after a colon is taken as part of a URL in JSX text, so this comment stays.      |
| `return /* \n */ x`                              | A block comment with a line break between two tokens on one line changes what the line-ending rules of JavaScript see. |
| `import a from "m"; // why`                      | A statement that shares its line with a comment or with other code is **left**; run `strip_js_comments` first (the presets do). A minified bundle on one line is therefore left as it is. |
| `const a = require("a"), b = require("b");`      | One declarator per statement is taken; several in one are code and stay. See [`remove_js_requires`](#remove_js_requires). |
| a `/* … ` that is never closed                   | It runs to the end of the text, like in JavaScript.                                           |

## Order in a chain

The steps do not need each other — comments and strings are known to the scanner, so an import inside a block comment is
left either way — but this is the order the presets use:

```
comments  →  imports  →  requires  →  exports  →  whitespace
```

Comments first, because an `import … ;` followed by a comment on the same line is a whole line only once the comment is
gone. Whitespace last, to tidy the holes the others leave.

## The private parts

The scanner and what it is made of live in `logic/_helpers/`. They are not part of the interface and have no cards, but
they are the reason the steps behave as they do:

| Helper                 | What it does                                                                                              |
|------------------------|-----------------------------------------------------------------------------------------------------------|
| `scan_js`              | One pass over the source: finds the comments, the comments that sit **glued** between two tokens, and the literals. Returns a `JsScan`. |
| `JsScan`               | A frozen record of the three lists: `comments`, `glued`, `literals`.                                      |
| `regex_allowed`        | Decides whether a `/` starts a regular expression or is a division.                                       |
| `skip_string`          | The end of a quoted string (or of its line).                                                              |
| `skip_regex`           | The end of a regular expression literal, flags included.                                                  |
| `skip_template`        | The end of a template literal, **expressions included**.                                                  |
| `is_word_char`         | A character of an identifier, a number or regex flags.                                                    |
| `find_matches_outside` | The matches of a line pattern that start in code and not in a literal or a comment.                       |
| `remove_with_gaps`     | `remove_spans` that leaves **one space** where a comment sat between two tokens (`a/**/b` → `a b`).        |

<details>
<summary>🔍 Under the hood — how the scanner decides</summary>

The one ambiguity of JavaScript that a scanner cannot avoid is `/`: it divides (`a / b`) and it starts a regular
expression (`return /b/.test(x)`), and the only difference is **what stands in front of it**. `regex_allowed` decides by
the last significant token — comments and blanks do not count:

```python
def regex_allowed(last: str, word: str, before_last: str = "", closing_tag: bool = False) -> bool:

    # 1. `=> /re/` is a regex; a `>` that closes a type (`Array<T> / 2`) is not
    if last == ">":
        return before_last == "="

    # 2. After `<`: `</div>` opens a JSX closing tag, anything else (`n </x/.test(s)`) is a regex
    if last == "<":
        return not closing_tag

    # 3. Nothing before it, or an operator or opening bracket: an expression begins here
    if last == "" or last in "(,=:[!&|?{;+-*%~^":
        return True

    # 4. After a word it depends on the word
    if is_word_char(last):
        return word in JS_REGEX_KEYWORDS

    # 5. After `)`, `]`, `}`, a literal or another slash: a division
    return False
```

A heuristic, not a parser: after `)` it says "division" (right for `f(x) / 2`, wrong for `if (x) /re/.test(y)`), after `}`
"division" (right for the end of a JSX expression, wrong for a regular expression that starts a statement). The mistakes
are bearable: a slash taken for a division only means a regular expression is scanned as code — a quote in it opens a
"string" that **ends at the end of the line**.

The scanner itself is one loop over the text:

```python
def scan_js(text: str) -> JsScan:

    # 1. State: where we are, and the last significant token (comments and blanks do not count)
    length = len(text)
    position = 0
    comments: list[Span] = []
    glued: list[Span] = []
    literals: list[Span] = []
    last = before_last = word = ""
    in_word = False

    while position < length:
        character = text[position]

        # 2. Blanks
        if character in " \t\r\n":
            position += 1
            in_word = False

        # 3. A string
        elif character in "'\"":
            end = skip_string(text, position)
            literals.append((position, end))
            position, before_last, last, word, in_word = end, last, '"', "", False

        # 4. A template literal
        elif character == "`":
            end = skip_template(text, position)
            literals.append((position, end))
            position, before_last, last, word, in_word = end, last, "`", "", False

        # 5. Anything but a slash: follow the word it belongs to
        elif character != "/":
            word = (word + character if in_word else character) if is_word_char(character) else ""
            in_word = is_word_char(character)
            before_last, last, position = last, character, position + 1

        # 6. `//`: a comment to the end of the line, unless it follows a colon (`http://` in JSX text)
        elif text.startswith("//", position):
            if position > 0 and text[position - 1] == ":":
                position, before_last, last, word, in_word = position + 2, last, "/", "", False
                continue
            newline = text.find("\n", position)
            end = length if newline == -1 else newline
            start = position
            while start > 0 and text[start - 1] in " \t":
                start -= 1
            comments.append((start, end))
            position, in_word = end, False

        # 7. `/* ... */`
        elif text.startswith("/*", position):
            close = text.find("*/", position + 2)
            end = length if close == -1 else close + 2
            start = position
            after = text[end] if end < length else "\n"
            before = text[start - 1] if start > 0 else "\n"
            if after in " \t\r\n":
                while start > 0 and text[start - 1] in " \t":
                    start -= 1
                comments.append((start, end))
            elif before not in JS_SEPARATORS and after not in JS_SEPARATORS:
                comments.append((start, end))
                glued.append((start, end))
            else:
                comments.append((start, end))
            position, in_word = end, False

        # 8. A regular expression, or a division
        elif regex_allowed(last, word, before_last, closing_tag=JS_CLOSING_TAG.match(text, position) is not None):
            position, before_last, last, word, in_word = skip_regex(text, position), last, "x", "", False
        else:
            position, before_last, last, word, in_word = position + 1, last, "/", "", False

    return JsScan(tuple(comments), tuple(glued), tuple(literals))
```

Two details are worth the look. **The blanks in front:** a comment is cut together with the blanks before it
(`x = 1; // note` → `x = 1;`), but only when something blank or a line end follows it. **A glued comment:** `a/**/b` has
no separator on either side; it is reported in `glued`, and `remove_with_gaps` leaves one space in its place, so the two
names do not grow together into `ab`.

The three skippers each end where JavaScript itself would — or at the end of the line when the source is wrong:

```python
def skip_string(text: str, start: int) -> int:

    # 1. Walk to the matching quote; a backslash takes the next character with it
    quote = text[start]
    position = start + 1
    length = len(text)
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == quote:
            return position + 1
        elif character == "\n":
            return position
        else:
            position += 1

    return length
```

```python
def skip_regex(text: str, start: int) -> int:

    # 1. Walk to the closing slash; one inside a `[...]` class does not close it
    position = start + 1
    length = len(text)
    in_class = False
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == "\n":
            return start + 1
        elif character == "[":
            in_class, position = True, position + 1
        elif character == "]":
            in_class, position = False, position + 1
        elif character == "/" and not in_class:

            # 2. The flags are a run of letters
            position += 1
            while position < length and is_word_char(text[position]):
                position += 1
            return position
        else:
            position += 1

    return length
```

A string that is not closed on its line is not a string (an apostrophe in JSX text); a regular expression that is not
closed on its line was not a regular expression, and only its first slash is consumed. A template literal may span lines
and may hold **code**, which may hold templates — so `skip_template` and its private `_skip_braces` call each other
(which is why they share one file):

```python
def skip_template(text: str, start: int) -> int:

    # 1. Walk to the closing backtick; a `${` opens an expression that may hold anything
    position = start + 1
    length = len(text)
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == "`":
            return position + 1
        elif character == "$" and text.startswith("{", position + 1):
            position = _skip_braces(text, position + 2)
        else:
            position += 1

    return length
```

`_skip_braces` follows the expression with the same last-token rule as the scanner (so `${ s.replace(/'|"/g, "") }` does
not open a "string" at the quote inside the regular expression), skips strings, nested templates and comments, and counts
the braces until the one that closes the `${`.

</details>

---

## 🧭 Table of Contents

* [`js_comment_spans`](#js_comment_spans)
* [`strip_js_comments`](#strip_js_comments)
* [`remove_js_imports`](#remove_js_imports)
* [`remove_js_requires`](#remove_js_requires)
* [`strip_js_exports`](#strip_js_exports)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logic--the-steps-that-read-javascript-and-typescript)

---

### `js_comment_spans`

**Finds the comments of a JavaScript or TypeScript source** — where they are, as spans that `remove_spans` can cut.

`//` and `/* … */` comments, JSDoc included. The span of a comment runs from the **blanks in front of it** to its end.

**Parameters:**

| Name   | Type  | Default      | Description                       |
|--------|-------|--------------|-----------------------------------|
| `text` | `str` | *(required)* | The JavaScript or TypeScript source. |

**Returns:** `list[Span]` — a half-open `(start, end)` for each comment, in the order of the file; `[]` for a text with
no comment.

**Raises:** `ValidationError` — `text` is not a `str`. A source it cannot read does not exist for the scanner.

**Example usage:**

```python
from simplibs.extractor_javascript import js_comment_spans
from simplibs.text import remove_spans

text = "const a = 1; // note\n// alone\nconst u = 'http://x'; /* b */\nconst re = /[/*]/g; const s = \"// not\";\n"

spans = js_comment_spans(text)
spans                                                    # -> [(12, 20), (21, 29), (51, 59)]
[text[start:end] for start, end in spans]                # -> [' // note', '// alone', ' /* b */']     the blanks in front are part of the span

js_comment_spans("const a = 1;\n")                       # -> []
js_comment_spans("a(); /* x\ny */ b();\n")               # -> [(4, 14)]      a block comment over two lines is one span
```

The regular expression `/[/*]/g` and the string `"// not"` hold what looks like comment markers and are not
reported.

**Every comment, glued or not.** `strip_js_comments` also knows which comments sit **between two tokens** (`a/**/b`) and
need a space left in their place; this function reports all of them, and it is for anything that wants to *look at*
the comments or cut them its own way.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def js_comment_spans(text: str) -> list[Span]:

    # 1. The comments the scanner found
    return list(scan_js(text).comments)
```

Everything is in `scan_js` — see [how the scanner decides](#the-private-parts). The function only hands the
`comments` of the scan over as a list.

</details>

[▲ Back to top](#-table-of-contents)

---

### `strip_js_comments`

**Removes all comments from a JavaScript or TypeScript source, JSDoc included.**

A step of the profiles `javascript/code-clean`, `javascript/code-no-imports` and `javascript/src-clean`. Works for
JavaScript, TypeScript, JSX and TSX alike.

**Parameters:**

| Name   | Type  | Default      | Description                          |
|--------|-------|--------------|--------------------------------------|
| `text` | `str` | *(required)* | The JavaScript or TypeScript source. |

**Returns:** `str` — the text without comments. A line that held only a comment disappears.

**Raises:** `ValidationError` — `text` is not a `str`.

**Example usage:**

```python
from simplibs.extractor_javascript import strip_js_comments

strip_js_comments("const a = 1; // note\n// alone\nconst u = 'http://x'; /* b */\n")
# -> "const a = 1;\nconst u = 'http://x';\n"

strip_js_comments("/**\n * Doc\n * @param {string} a\n */\nfunction f(a) {}\n")          # -> 'function f(a) {}\n'     JSDoc is a comment

strip_js_comments("a/**/b\nlet x = a /* c */ + b;\n")      # -> 'a b\nlet x = a + b;\n'        a comment between two tokens leaves a space

strip_js_comments("<p>{/* note */}</p>\n")                 # -> '<p>{}</p>\n'                  the brackets stay

strip_js_comments("s.replace(/'|\"/g, \"\"); // c\n")       # -> 's.replace(/\'|"/g, "");\n'    quotes in a regular expression are not strings
strip_js_comments("const t = `a // ${ \"}\" + `inner` } /* c */ b`; // end\n")
# -> 'const t = `a // ${ "}" + `inner` } /* c */ b`;\n'                                   the template is text, even with code inside

strip_js_comments("a(); // c")                             # -> 'a();'
strip_js_comments("// a\n/* b */\n")                       # -> ''
strip_js_comments("const a = 1;\n")                        # -> 'const a = 1;\n'      the very same text
```

**The guarantee.** For a source that parses, the syntax tree of the result equals the tree of the original, apart from
positions — within the [known limits](#known-limits) of the scanner.

**A space where two tokens would touch.** `a/**/b` must not become `ab` — a different name. A comment that sits between
two tokens with no separator on either side leaves **one space**; anywhere else the comment (and the blanks before it)
simply goes. The separators are [`JS_SEPARATORS`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_separators).

**A space can stay.** `/* d */ b();` becomes ` b();` — the space after the
comment stays. The presets that use this step finish with a whitespace pass.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def strip_js_comments(text: str) -> str:

    # 1. One pass finds the comments and which of them sit between two tokens
    scan = scan_js(text)

    # 2. Cut them; a comment between two tokens leaves a space
    return remove_with_gaps(text, scan.comments, scan.glued)
```

`remove_spans` of [`simplibs-text`](https://pypi.org/project/simplibs-text/) only removes, and a comment between two
tokens needs a space instead. `remove_with_gaps` puts the space in **first** and cuts **after**, so one primitive does
both:

```python
def remove_with_gaps(text: str, spans: Sequence[Span], gaps: Collection[Span]) -> str:

    # 1. A space goes in front of every gap; the cut then removes the span and leaves the space
    positions = sorted({start for start, _ in gaps})
    pieces: list[str] = []
    previous = 0
    for position in positions:
        pieces.append(text[previous:position])
        pieces.append(" ")
        previous = position
    pieces.append(text[previous:])
    padded = "".join(pieces)

    # 2. The spans move with the text: each space inserted at or before an offset pushes it by one
    shifted = [
        (start + bisect_right(positions, start), end + bisect_right(positions, end))
        for start, end in spans
    ]

    # 3. Cut; a line that held only a removed span disappears whole
    return remove_spans(padded, shifted)
```

Every inserted space moves all later offsets by one, so each span is shifted by the number of spaces at or before it.

</details>

[▲ Back to top](#-table-of-contents)

---

### `remove_js_imports`

**Removes the ES `import` statements of a JavaScript or TypeScript source.**

The step of `javascript/code-no-imports` for modules: the logic without its dependencies. `import type` included; the lines
the statements stood on disappear.

**Parameters:**

| Name   | Type  | Default      | Description                          |
|--------|-------|--------------|--------------------------------------|
| `text` | `str` | *(required)* | The JavaScript or TypeScript source. |

**Returns:** `str` — the text without `import` statements. A dynamic `import("m")` stays.

**Raises:** `ValidationError` — `text` is not a `str`.

**Example usage:**

```python
from simplibs.extractor_javascript import remove_js_imports

remove_js_imports('import a from "m";\nx();\n')                          # -> 'x();\n'
remove_js_imports('import { a, b as c } from "m"\nx()\n')                # -> 'x()\n'          no semicolon
remove_js_imports("import * as ns from 'm';\nx()\n")                     # -> 'x()\n'
remove_js_imports('import "./side-effect";\nx()\n')                      # -> 'x()\n'          a side-effect import
remove_js_imports('import type { T } from "m";\nx()\n')                  # -> 'x()\n'          TypeScript
remove_js_imports('import { "name" as x } from "m";\nx()\n')             # -> 'x()\n'
remove_js_imports('import {\n  a,\n  b,\n} from "m";\nx()\n')            # -> 'x()\n'          over several lines
remove_js_imports('import a, { b } from "m";\nimport c from "n";\n')     # -> ''

# what stays
remove_js_imports('const m = await import("m");\nx()\n')                 # -> 'const m = await import("m");\nx()\n'   dynamic: an expression, not a statement
remove_js_imports('import a from "m"; // why\nx()\n')                    # -> 'import a from "m"; // why\nx()\n'     shares its line with a comment
remove_js_imports('import a from "m"; x();\n')                          # -> 'import a from "m"; x();\n'              shares its line with code
remove_js_imports('const s = `\nimport a from "m";\n`;\n')               # -> 'const s = `\nimport a from "m";\n`;\n'   a line in a template literal
remove_js_imports('/*\nimport a from "m";\n*/\nx()\n')                   # -> '/*\nimport a from "m";\n*/\nx()\n'     a line in a block comment
```

**A pattern, not a parser.** An import is found by a line pattern; the scanner only tells which matches are real code.
That is what makes the step work for JSX and TypeScript with no parser for either — and why a statement that shares its
line with other code (a minified bundle) is left.

**Needs no order.** Strings, templates and comments are known to the scan, so the step gives the same result before or
after `strip_js_comments`. Only an import **followed by a comment on the same line** needs the comments gone first, which
is what the presets do.

**A `;` on the next line.** It belongs to the statement and goes with it.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def remove_js_imports(text: str) -> str:

    # 1. The statements that start in code
    matches = find_matches_outside(text, JS_IMPORT_PATTERN, scan_js(text))

    # 2. Each match is a whole line (or lines): cut it, the emptied line goes with it
    return remove_spans(text, [match.span() for match in matches])
```

The pattern is [`JS_IMPORT_PATTERN`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_import_pattern). It starts at the
beginning of a line (indentation included) and ends at the end of the statement, so the line disappears whole.
`find_matches_outside` keeps only the matches that do not start inside a string, a template literal or a comment:

```python
def find_matches_outside(text: str, pattern: re.Pattern[str], scan: JsScan) -> list[re.Match[str]]:

    # 1. The places the pattern must not start in: strings, templates, comments
    protected = sorted(scan.literals + scan.comments)
    starts = [start for start, _ in protected]

    # 2. A match that begins inside one is text of that string or comment, not a statement
    found: list[re.Match[str]] = []
    for match in pattern.finditer(text):
        index = bisect_right(starts, match.start()) - 1
        if index >= 0 and match.start() < protected[index][1]:
            continue
        found.append(match)

    return found
```

The protected spans are sorted, so one binary search (`bisect_right`) tells for each match which span, if any, it
starts in.

</details>

[▲ Back to top](#-table-of-contents)

---

### `remove_js_requires`

**Removes the CommonJS `const x = require("m")` declarations of a JavaScript source.**

The step of `javascript/code-no-imports` for the files that never moved to `import`.

**Parameters:**

| Name   | Type  | Default      | Description                          |
|--------|-------|--------------|--------------------------------------|
| `text` | `str` | *(required)* | The JavaScript or TypeScript source. |

**Returns:** `str` — the text without them; the lines they stood on disappear.

**Raises:** `ValidationError` — `text` is not a `str`.

**Example usage:**

```python
from simplibs.extractor_javascript import remove_js_requires

remove_js_requires('const fs = require("fs");\nx()\n')                         # -> 'x()\n'
remove_js_requires('const { a, b: { c } } = require("m");\nx()\n')           # -> 'x()\n'     destructuring, two levels
remove_js_requires('const [x] = require("m");\nx()\n')                        # -> 'x()\n'
remove_js_requires('var get = require("m").get;\nx()\n')                      # -> 'x()\n'     with a member
remove_js_requires("let z = require('z');\nx()\n")                            # -> 'x()\n'
remove_js_requires('const a = require("a")\nx()\n')                           # -> 'x()\n'     no semicolon

# what stays — code, not a dependency
remove_js_requires('const a = require(name);\nx()\n')                         # -> 'const a = require(name);\nx()\n'
remove_js_requires('const a = require("a"), b = require("b");\nx()\n')        # -> 'const a = require("a"), b = require("b");\nx()\n'
remove_js_requires('const x = foo(require("m"));\n')                          # -> 'const x = foo(require("m"));\n'
remove_js_requires('var a = require("a")\n  , b = require("b");\nx()\n')      # -> 'var a = require("a")\n  , b = require("b");\nx()\n'
remove_js_requires('const a = require("a")\n  .call();\nx()\n')               # -> 'const a = require("a")\n  .call();\nx()\n'
```

**A statement that goes on.** Without a `;`, a statement ends at the end of its line only if the **next line cannot
continue it**. Comma-first style, a chained `.call()` or an operator at the start of the next line mean the declaration
is not finished, and removing the first line would leave a broken one. Such a statement is not taken.

**The limits.** One declarator per statement; destructuring nested **two levels** deep and without default values
(outside the innermost braces); and the argument must be a plain string — `require(name)` is code.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def remove_js_requires(text: str) -> str:

    # 1. The statements that start in code
    matches = find_matches_outside(text, JS_REQUIRE_PATTERN, scan_js(text))

    # 2. Cut each whole line
    return remove_spans(text, [match.span() for match in matches])
```

The same two lines as `remove_js_imports`, with another pattern:
[`JS_REQUIRE_PATTERN`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_require_pattern). The care is in the pattern — the
end of the statement and the "next line cannot continue it" look-ahead.

</details>

[▲ Back to top](#-table-of-contents)

---

### `strip_js_exports`

**Removes what only exports from a JavaScript or TypeScript source, and keeps the code.**

A step of `javascript/code-no-imports`: `export` says who may use a declaration, not what it does.

**Parameters:**

| Name   | Type  | Default      | Description                          |
|--------|-------|--------------|--------------------------------------|
| `text` | `str` | *(required)* | The JavaScript or TypeScript source. |

**Returns:** `str` — the text without `export { … }`, `export * from "m"` and `export default Name;`, and without the
`export` / `export default` keyword in front of a **named** declaration. An anonymous `export default …` stays.

**Raises:** `ValidationError` — `text` is not a `str`.

**Example usage:**

```python
from simplibs.extractor_javascript import strip_js_exports

# 1. Lists hold no code: removed whole
strip_js_exports('export { a, b };\nx()\n')                       # -> 'x()\n'
strip_js_exports('export * from "m";\nx()\n')                     # -> 'x()\n'
strip_js_exports('export * as ns from "m";\nx()\n')               # -> 'x()\n'
strip_js_exports('export type { T };\nx()\n')                     # -> 'x()\n'
strip_js_exports('export { a } from "m";\nx()\n')                 # -> 'x()\n'

# 2. A default export of a name: removed whole
strip_js_exports('export default App;\nx()\n')                    # -> 'x()\n'

# 3. A declaration: only the keyword goes, the indentation stays
strip_js_exports('export function f() {}\n')                      # -> 'function f() {}\n'
strip_js_exports('export async function f() {}\n')                # -> 'async function f() {}\n'
strip_js_exports('export const a = 1;\n')                         # -> 'const a = 1;\n'
strip_js_exports('  export const a = 1;\n')                       # -> '  const a = 1;\n'
strip_js_exports('export default function App() {}\n')            # -> 'function App() {}\n'
strip_js_exports('export default class App {}\n')                 # -> 'class App {}\n'
strip_js_exports('export interface Props { a: 1 }\n')             # -> 'interface Props { a: 1 }\n'
strip_js_exports('export type T = string;\n')                     # -> 'type T = string;\n'
strip_js_exports('export enum E { A }\n')                         # -> 'enum E { A }\n'
strip_js_exports('export abstract class A {}\n')                  # -> 'abstract class A {}\n'
strip_js_exports('export declare const x: number;\n')             # -> 'declare const x: number;\n'

# what stays
strip_js_exports('export default function () {}\n')               # -> 'export default function () {}\n'
strip_js_exports('export default () => {}\n')                     # -> 'export default () => {}\n'
strip_js_exports('export default class extends X {}\n')           # -> 'export default class extends X {}\n'
strip_js_exports('export default FILE\n  ? a : b;\n')             # -> 'export default FILE\n  ? a : b;\n'
strip_js_exports('module.exports = { a };\n')                     # -> 'module.exports = { a };\n'
```

**Three kinds of export.** (1) **Lists** declare nothing, they only say what is visible from outside: removed whole.
(2) **A default export of a name** (`export default App;` at the end of a component file) holds a name and no code:
removed whole. (3) **A declaration with `export` in front of it** *is* the code and `export` is only visibility: the
keyword goes, the declaration — indentation and all — stays.

**An anonymous default stays.** `export default function () {}`, `export default () => {}` and
`export default class extends X {}` have no name: without `export default` they would not be valid statements, so they
are not touched.

**A name that goes on.** `export default FILE` followed by `? a : b` on the next line is a conditional expression, not a
name: a line that the next one continues is not taken.

**`module.exports`.** It is an assignment — code — and stays.

<details>
<summary>🔍 Under the hood</summary>

```python
@validate_call
def strip_js_exports(text: str) -> str:

    # 1. One scan serves all three patterns: they never match the same line
    scan = scan_js(text)

    # 2. Lines that only export are cut whole
    spans = [
        match.span()
        for pattern in (JS_EXPORT_LIST_PATTERN, JS_EXPORT_DEFAULT_NAME_PATTERN)
        for match in find_matches_outside(text, pattern, scan)
    ]

    # 3. In front of a declaration only the keyword goes; the indentation (group 1) stays
    spans += [
        (match.end(1), match.end())
        for match in find_matches_outside(text, JS_EXPORT_KEYWORD_PATTERN, scan)
    ]

    return remove_spans(text, spans)
```

The three patterns are
[`JS_EXPORT_LIST_PATTERN`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_export_list_pattern),
[`JS_EXPORT_DEFAULT_NAME_PATTERN`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_export_default_name_pattern) and
[`JS_EXPORT_KEYWORD_PATTERN`](../README_EXTRACTOR_JAVASCRIPT_CONSTANTS.md#js_export_keyword_pattern). The first two give
**whole lines** to cut; the third gives only the keyword — the span runs from the **end of group 1** (the indentation)
to the end of the match (`export ` or `export default `), so the indentation stays and only the word goes.

</details>

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

The steps raise **no cards**. A source cannot be "invalid" for a scanner — it answers for whatever text it is given; the
worst case is a [known limit](#known-limits), one line spoiled.

A wrong **type** of the argument (`text=5`) is a `ValidationError` from
[`simplibs-validate`](https://pypi.org/project/simplibs-validate/), as everywhere in the family.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../../README.md#-logic--the-steps-that-read-javascript-and-typescript)
