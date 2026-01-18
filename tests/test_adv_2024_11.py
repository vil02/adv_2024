import pytest

import solutions.adv_2024_11 as sol
from . import test_utils as tu

_SMALL = [125, 17]


@pytest.mark.parametrize(
    ("stones", "number_of_blinks", "expected"),
    [
        ([0, 1, 10, 99, 999], 1, 7),
        (_SMALL, 0, 2),
        (_SMALL, 1, 3),
        (_SMALL, 2, 4),
        (_SMALL, 3, 5),
        (_SMALL, 4, 9),
        (_SMALL, 5, 13),
        (_SMALL, 6, 22),
        (_SMALL, 25, 55312),
        (_SMALL, 75, 65601038650482),
    ],
)
def test_number_of_stones_produced(
    stones: list[int], number_of_blinks: int, expected: int
) -> None:
    assert sol.number_of_stones_produced(stones, number_of_blinks) == expected


_INPUTS = tu.get_inputs(11, {"p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"p": (183484, 218817038947400)}
)
