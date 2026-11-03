from .JsScan import JsScan
from .find_matches_outside import find_matches_outside
from .is_word_char import is_word_char
from .regex_allowed import regex_allowed
from .remove_with_gaps import remove_with_gaps
from .scan_js import scan_js
from .skip_regex import skip_regex
from .skip_string import skip_string
from .skip_template import skip_template


_DESIGN_NOTES = """
# _helpers — The Scanner and Its Parts

Private. Plain imports, no `__all__`.

## Internal Components Registry

| Component              | Type     | Description                                                          |
| :--------------------- | :------- | :------------------------------------------------------------------- |
| `JsScan`               | Class    | Comments, glued comments and literals found in one pass.             |
| `find_matches_outside` | Function | Line-pattern matches that start in code, not in a string or comment. |
| `is_word_char`         | Function | A character of an identifier, a number or regex flags.               |
| `regex_allowed`        | Function | Is this slash the start of a regular expression?                     |
| `remove_with_gaps`     | Function | Removes spans, leaving a space where one was marked.                 |
| `scan_js`              | Function | One pass over a source: comments and literals.                       |
| `skip_regex`           | Function | The end of a regular expression literal.                             |
| `skip_string`          | Function | The end of a quoted string.                                          |
| `skip_template`        | Function | The end of a template literal, expressions included.                 |
"""
