import pytest
from simplibs.extractor_javascript.plugin import register_all

FILES = {
    "package.json": '{ "name": "demo" }\n',
    "src/index.ts": "import { run } from './app';\n// start\nrun();\n",
    "src/app.tsx": (
        "import React from 'react';\n"
        "\n"
        "/** The app. */\n"
        "export function run() {\n"
        "  // inner note\n"
        "  return <div>{/* note */}http://x.com</div>; // tail\n"
        "}\n"
        "\n"
        "export default run;\n"
    ),
    "src/util.js": "const fs = require('fs');\nmodule.exports = { read: (n) => fs.readFileSync(n) };\n",
    "src/app.test.ts": "import { run } from './app';\n\ntest('run', () => {\n  expect(run()).toBeDefined();\n});\n",
    "src/types.d.ts": "export interface Props {\n  name: string;\n}\n",
    "README.md": "# Readme\n",
    "notes.txt": "plain\n",
}


def write_project(folder) -> None:
    """Write the sample project into a folder."""
    for relative, text in FILES.items():
        path = folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


@pytest.fixture
def project(tmp_path):
    """A small JavaScript and TypeScript project in a temporary folder."""
    write_project(tmp_path)
    return tmp_path


@pytest.fixture
def registered():
    """The profiles of the add-on are in the registry of the extractor (the conftest of `tests/` restores it)."""
    register_all()


@pytest.fixture(autouse=True)
def no_terminal(monkeypatch):
    """Standard input is never a terminal here, so nothing stops to ask a question (even under `pytest -s`)."""

    class _NotATerminal:
        def isatty(self):
            return False

        def read(self, *args):
            return ""

        def readline(self, *args):
            return ""

    monkeypatch.setattr("sys.stdin", _NotATerminal())
