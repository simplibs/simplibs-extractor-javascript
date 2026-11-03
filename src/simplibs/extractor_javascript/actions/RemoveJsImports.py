from simplibs.actions import create_action
# Outers
from ..logic import remove_js_imports


RemoveJsImports = create_action(
    remove_js_imports,
    main_param="text",
    class_name="RemoveJsImports",
)
"""Action wrapping `remove_js_imports` — takes the ES import statements out of the JavaScript or TypeScript text flowing in."""


_DESIGN_NOTES = """
# RemoveJsImports — Action Over `remove_js_imports`

## Purpose
The import step as a link of a pipeline.

## Shape
Main input: `text`. No options. Text in, text out.
"""
