from simplibs.actions import create_action
# Outers
from ..logic import strip_js_comments


StripJsComments = create_action(
    strip_js_comments,
    main_param="text",
    class_name="StripJsComments",
)
"""Action wrapping `strip_js_comments` — takes the comments out of the JavaScript or TypeScript text flowing in."""


_DESIGN_NOTES = """
# StripJsComments — Action Over `strip_js_comments`

## Purpose
The comment step as a link of a pipeline.

## Shape
Main input: `text`. No options. Text in, text out.
"""
