import pytest

import solutions.adv_2024_09 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("disc_map", "expected"),
    [
        ("12345", [0, -1, -1, 1, 1, 1, -1, -1, -1, -1, 2, 2, 2, 2, 2]),
        (
            "2333133121414131402",
            [
                0,
                0,
                -1,
                -1,
                -1,
                1,
                1,
                1,
                -1,
                -1,
                -1,
                2,
                -1,
                -1,
                -1,
                3,
                3,
                3,
                -1,
                4,
                4,
                -1,
                5,
                5,
                5,
                5,
                -1,
                6,
                6,
                6,
                6,
                -1,
                7,
                7,
                7,
                -1,
                8,
                8,
                8,
                8,
                9,
                9,
            ],
        ),
    ],
)
def test_to_blocks(disc_map: str, expected: list[int]) -> None:
    assert sol.to_blocks(disc_map) == expected


_INPUTS = tu.get_inputs(9, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small": (1928, 2858), "p": (6279058075753, 6301361958738)},
)
