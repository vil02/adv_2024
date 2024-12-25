import pytest

import solutions.adv_2024_25 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("lock", "key", "expected"),
    [
        ([0, 5, 3, 4, 3], [5, 0, 2, 1, 3], False),
        ([0, 5, 3, 4, 3], [4, 3, 4, 0, 2], False),
        ([0, 5, 3, 4, 3], [3, 0, 2, 0, 1], True),
        ([1, 2, 0, 5, 3], [5, 0, 2, 1, 3], False),
        ([1, 2, 0, 5, 3], [4, 3, 4, 0, 2], True),
        ([1, 2, 0, 5, 3], [3, 0, 2, 0, 1], True),
    ],
)
def test_does_fit(lock: list[int], key: list[int], expected: bool) -> None:
    assert sol.does_fit(lock, key) == expected


_INPUTS = tu.get_inputs(25, {"small", "p"})

test_solve_a = _INPUTS.get_test(sol.solve_a, {"small": 3, "p": 3090})
