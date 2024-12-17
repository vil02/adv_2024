import pytest

import solutions.adv_2024_17 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("in_data", "expected"),
    [
        ((0, 0, 9, [2, 6]), (0, 1, 9, [])),
        ((10, 0, 0, [5, 0, 5, 1, 5, 4]), (10, 0, 0, [0, 1, 2])),
        (
            (2024, 0, 0, [0, 1, 5, 4, 3, 0]),
            (0, 0, 0, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]),
        ),
        ((0, 29, 0, [1, 7]), (0, 26, 0, [])),
        ((0, 2024, 43690, [4, 0]), (0, 44354, 43690, [])),
        ((256, 2, 0, [0, 5]), (64, 2, 0, [])),
        ((256, 0, 2, [0, 6]), (64, 0, 2, [])),
        ((256, 2, 0, [6, 5]), (256, 64, 0, [])),
        ((256, 0, 2, [6, 6]), (256, 64, 2, [])),
        ((256, 2, 0, [7, 5]), (256, 2, 64, [])),
        ((256, 0, 2, [7, 6]), (256, 0, 64, [])),
    ],
)
def test_compute_all(
    in_data: tuple[int, int, int, list[int]], expected: tuple[int, int, int, list[int]]
) -> None:
    reg_a, reg_b, reg_c, program = in_data
    computer = sol.Computer(reg_a, reg_b, reg_c, program)
    computer.compute_all()
    assert computer.get_state() == expected


_INPUTS = tu.get_inputs(17, {"small", "small_2", "p"})
test_solve_a = _INPUTS.get_test(
    sol.solve_a, {"small": "4,6,3,5,6,3,5,2,1,0", "p": "7,4,2,0,5,0,5,3,7"}
)

test_solve_b = _INPUTS.get_test(sol.solve_b, {"small_2": 117440, "p": 202991746427434})
