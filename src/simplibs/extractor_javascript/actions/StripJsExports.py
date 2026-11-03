from simplibs.actions import create_action
# Outers
from ..logic import strip_js_exports


StripJsExports = create_action(
    strip_js_exports,
    main_param="text",
    class_name="StripJsExports",
)
"""Action wrapping `strip_js_exports` — takes the exports out of the JavaScript or TypeScript text flowing in, and keeps the declarations."""


_DESIGN_NOTES = """
# StripJsExports — Action Over `strip_js_exports`

## Purpose
The export step as a link of a pipeline.

## Shape
Main input: `text`. No options. Text in, text out.
"""
