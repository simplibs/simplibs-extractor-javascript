from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.file_rules import INDEX_NAME

VALID = ["index.js", "src/index.tsx", "a/b/index.mjs", "index.d.ts", "index.test.js", "components/Button/index.ts"]
INVALID = ["indexer.js", "index-utils.ts", "index", "reindex.js", "myindex.js", "src/index/a.js", "indexjs", "a.js"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        INDEX_NAME,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("path", VALID)
def test_index_with_any_suffix_is_taken(path) -> None:
    assert INDEX_NAME(Path(path)) is True


@pytest.mark.parametrize("path", ["indexer.js", "index-utils.ts", "index"])
def test_the_dot_is_part_of_the_prefix(path) -> None:
    """`index.` and not `index`, so a name that only begins with the word is not an index file."""
    assert INDEX_NAME(Path(path)) is False


@pytest.mark.parametrize("path", ["index/a.js", "src/index/b.js"])
def test_a_folder_called_index_does_not_count(path) -> None:
    assert INDEX_NAME(Path(path)) is False
