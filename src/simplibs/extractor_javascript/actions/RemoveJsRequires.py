from simplibs.actions import create_action
# Outers
from ..logic import remove_js_requires


RemoveJsRequires = create_action(
    remove_js_requires,
    main_param="text",
    class_name="RemoveJsRequires",
)
"""Action wrapping `remove_js_requires` — takes the CommonJS `require` declarations out of the JavaScript text flowing in."""


_DESIGN_NOTES = """
# RemoveJsRequires — Action Over `remove_js_requires`

## Purpose
The `require` step as a link of a pipeline.

## Shape
Main input: `text`. No options. Text in, text out.
"""
