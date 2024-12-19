import pytest

import solutions.adv_2024_19 as sol
from . import test_utils as tu

_AVAILABLE = frozenset({"r", "wr", "b", "g", "bwu", "rb", "gb", "br"})


@pytest.mark.parametrize(
    ("available", "pattern", "expected"),
    [
        (_AVAILABLE, "brwrr", True),
        (_AVAILABLE, "bggr", True),
        (_AVAILABLE, "gbbr", True),
        (_AVAILABLE, "rrbgbr", True),
        (_AVAILABLE, "ubwu", False),
        (_AVAILABLE, "bwurrg", True),
        (_AVAILABLE, "brgr", True),
        (_AVAILABLE, "bbrgwb", False),
    ],
)
def test_is_possible(available: frozenset[str], pattern: str, expected: bool) -> None:
    assert sol.is_possible(available, pattern) == expected


@pytest.mark.parametrize(
    ("available", "pattern", "expected"),
    [
        (_AVAILABLE, "brwrr", 2),
        (_AVAILABLE, "bggr", 1),
        (_AVAILABLE, "gbbr", 4),
        (_AVAILABLE, "rrbgbr", 6),
        (_AVAILABLE, "ubwu", 0),
        (_AVAILABLE, "bwurrg", 1),
        (_AVAILABLE, "brgr", 2),
        (_AVAILABLE, "bbrgwb", 0),
    ],
)
def test_count_ways(available: frozenset[str], pattern: str, expected: bool) -> None:
    assert sol.count_ways(available, pattern) == expected


_INPUTS = tu.get_inputs(19, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (6, 16), "p": (300, 624802218898092)}
)
