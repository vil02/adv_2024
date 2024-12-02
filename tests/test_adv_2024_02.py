import pytest

import solutions.adv_2024_02 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("in_list", "expected"),
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], False),
        ([8, 6, 4, 4, 1], False),
        ([1, 3, 6, 7, 9], True),
    ],
)
def test_is_safe_a(in_list: list[int], expected: int) -> None:
    assert sol.is_safe_a(in_list) == expected


@pytest.mark.parametrize(
    ("in_list", "expected"),
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([8, 6, 4, 4, 1], True),
        ([1, 3, 6, 7, 9], True),
    ],
)
def test_is_safe_b(in_list: list[int], expected: int) -> None:
    assert sol.is_safe_b(in_list) == expected


_INPUTS = tu.get_inputs(2, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (2, 4), "p": (686, 717)}
)
