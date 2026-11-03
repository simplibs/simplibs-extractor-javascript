# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-11-03

The first release: the JavaScript add-on of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/).
It carries over what the old code extractor knew about React and widens it to JavaScript and TypeScript as a whole.

### ✨ Added

#### Steps — plain functions, text in, text out

* `js_comment_spans(text)` — finds the comments with a scanner and returns them as `Span`s (from the blanks in front of a comment to its end); `//` and `/* */`, JSDoc included; a `//` inside a string, a template literal or a regular expression is never a comment
* `strip_js_comments(text)` — removes every comment; a line that held only a comment disappears, `x = 1; // note` becomes `x = 1;`, a block comment between two tokens leaves one space (`a/**/b` → `a b`)
* `remove_js_imports(text)` — removes the ES `import` statements, `import type` and imports over several lines included; a dynamic `import("m")` stays
* `remove_js_requires(text)` — removes the CommonJS `const x = require("m")` declarations, with destructuring (two levels) and an optional `.member`
* `strip_js_exports(text)` — removes `export { … }`, `export * from "m"` and `export default Name;`, and the `export` / `export default` keyword in front of a named declaration; an anonymous default export stays

#### The scanner

* One pass over the source that knows strings, template literals (with the code inside `${ … }`, nested ones too), regular expressions and comments, and decides by the last significant token whether a `/` is a division or a regular expression. It is not a parser and cannot fail: no step raises on a source, and a surprising one spoils at most the line it is on
* Statements are found by line patterns, and only matches that **start in code** count — a line that looks like an import inside a string, a template literal or a block comment is left alone

#### Actions — the steps as links of a pipeline

* `StripJsComments`, `RemoveJsImports`, `RemoveJsRequires`, `StripJsExports` — one `Action` over each step, made with `create_action`. Imported from `simplibs.extractor_javascript.actions`

#### Presets — ready-made chains

* `JS_CLEAN` — comments out, whitespace tidied; imports and exports stay
* `JS_NO_IMPORTS` — comments, imports, requires and exports out, no blank lines; the logic and nothing else

#### Profiles — registered in the system `javascript`

* `javascript/code-clean` — `javascript_code_clean.md`
* `javascript/code-no-imports` — `javascript_code_no_imports.md`
* `javascript/data-all` — `javascript_data_all.md`, every relevant file as it is
* `javascript/src-clean` — `javascript_src_clean.md`, with the strict exclusion (the old strict filter, which no profile ever used, is a profile now)
* `JS_PROFILES` — the four profile objects in the order the listings show them
* Imported from `simplibs.extractor_javascript.profiles`

#### File rules — judge the path inside the source

* `JS_FILES`, `JS_BASE`, `build_js_base(*, include_index=True, include_underscore=True)` — JavaScript and TypeScript files (`.js .jsx .ts .tsx .mjs .cjs`) that are not hidden
* `JS_TESTS` — a test by its whole name (`a.test.js`, `a.spec.ts`, `test-utils.js`) or by its folder (`__tests__/`, `__mocks__/`, `e2e/`, `tests/`, `test/`, `coverage/`)
* `JS_CONFIG`, `JS_ASSET_DIRS`, `JS_STRICT_EXCLUDE` — tooling configuration; assets; tests, configuration, type declarations, assets, installed packages, build output and version control together
* Atomic pieces: `DOT_NAME`, `INDEX_NAME`, `UNDERSCORE_NAME`, `DEPENDENCY_DIRS`, `OUTPUT_DIRS`, `VCS_DIRS`
* Imported from `simplibs.extractor_javascript.file_rules`

#### Constants and the add-on

* Names: `JS_SUFFIXES`, `JS_CONFIG_NAMES`, `JS_TEST_DIR_NAMES`, `JS_DEPENDENCY_DIR_NAMES`, `JS_OUTPUT_DIR_NAMES`, `JS_ASSET_DIR_NAMES`
* Patterns: `JS_IMPORT_PATTERN`, `JS_REQUIRE_PATTERN`, `JS_EXPORT_LIST_PATTERN`, `JS_EXPORT_DEFAULT_NAME_PATTERN`, `JS_EXPORT_KEYWORD_PATTERN`
* For the scanner: `JS_CLOSING_TAG`, `JS_REGEX_KEYWORDS`, `JS_SEPARATORS`
* `register_all(*, replace_existing=True)` — registers the four profiles; the target of the entry point `simplibs.extractor.plugins`, so `pip install` is the whole installation

#### Exceptions

* The library defines no exceptions of its own, and no step raises on a source: the scanner has no syntax it refuses
* The one thing a step refuses is a text that is not a `str`; `@validate_call` raises its `ValidationError`

#### Typing

* `py.typed` marker — the package ships its type information

#### Package Layout

* `simplibs.extractor_javascript` exports the five steps and `register_all`; the actions, presets, profiles and file rules are imported from their own folders (`actions`, `presets`, `profiles`, `file_rules`), each of which declares its own `__all__`, and the constants from `constants`
* Layers that only look left: `constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin`
* The add-on uses `simplibs.extractor` only through its public names (`Profile`, `register_profile`, `by_suffix`)
* Importing the package registers nothing; the extractor calls `register_all` through the entry point

#### Dependencies

* `simplibs-extractor` — `Profile`, `register_profile`, `by_suffix`
* `simplibs-text` — `remove_spans`, `Span`, `CLEANUP_WHITESPACE` and `COMPACT`
* `simplibs-actions` — `create_action`: the steps as pipeline actions
* `simplibs-path` — `IGNORE_VCS` and the path rules (`HasSuffix`, `NameIs`, `AnyParentNameIs`)
* `simplibs-rules` — `Rule`, `IsIn`, `StartsWith`, `EndsWith` and `Regex`
* `simplibs-validate` — `@validate_call` on every public function

### 🔄 Changed from the old code extractor

* **One system for JavaScript, TypeScript and React.** The old React profiles (`REACT_CODE_CLEAN`, `REACT_CODE_CLEAN_NO_IMPORTS`, `REACT_DATA_ALL` and the strict React filter) are the profiles of the system `javascript` now, and the rules and steps take every JavaScript and TypeScript file, `.mjs` and `.cjs` included
* **`index.*` and `_*` files are source.** The old base rule dropped every `index.*` and every `_*` file, which lost the root `index.js` (the entry of an application) and Next.js `pages/_app.tsx`. Both are taken by default; `build_js_base(include_index=False, include_underscore=False)` brings the old behaviour back
* **A test is recognised by its whole name.** The old rule asked whether the path *contained* `test` and threw away `latest.js`, `contest.tsx` and `inspector.ts`
* **`node_modules` has its own rule.** The old list of version-control folders held `node_modules` and `tmp`; version control is `IGNORE_VCS` of `simplibs-path` now, `node_modules` is `DEPENDENCY_DIRS`, and `tmp` is dropped
* **`.next` is build output.** It starts with a dot, but the base rule leaves out only dot *files*; without this name the compiled pages of a Next.js build would be read as source
* **Type declarations (`.d.ts`) are left out of the strict profile.** They only describe code that exists elsewhere
* **Comments are found by a scanner, not by a regex.** A `//` in a URL, a quote in a regular expression and a code sample in a template literal are left alone; JSDoc goes with the other comments

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)