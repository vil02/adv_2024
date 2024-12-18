import pytest

import solutions.adv_2024_18 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(18, {"small", "p"})


@pytest.mark.parametrize(
    ("walls", "limits", "start_pos", "end_pos", "expected"),
    [
        (
            set(sol.parse_input(_INPUTS.inputs["small"])[0:12]),
            (7, 7),
            (0, 0),
            (6, 6),
            22,
        ),
        (
            set(sol.parse_input(_INPUTS.inputs["p"])[0 : sol.TRUNC]),
            sol.LIMITS,
            sol.START_POS,
            sol.END_POS,
            344,
        ),
    ],
)
def test_find_shortest_path(
    walls: set[sol.Pair],
    limits: sol.Pair,
    start_pos: sol.Pair,
    end_pos: sol.Pair,
    expected: int,
) -> None:
    assert sol.find_shortest_path(walls, limits, start_pos, end_pos) == expected


@pytest.mark.parametrize(
    ("wall_list", "limits", "start_pos", "end_pos", "expected"),
    [
        (
            sol.parse_input(_INPUTS.inputs["small"]),
            (7, 7),
            (0, 0),
            (6, 6),
            (6, 1),
        ),
        (
            sol.parse_input(_INPUTS.inputs["p"]),
            sol.LIMITS,
            sol.START_POS,
            sol.END_POS,
            (46, 18),
        ),
    ],
)
def test_find_first_blocking(
    wall_list: list[sol.Pair],
    limits: sol.Pair,
    start_pos: sol.Pair,
    end_pos: sol.Pair,
    expected: sol.Pair,
) -> None:
    assert sol.find_first_blocking(wall_list, limits, start_pos, end_pos) == expected


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"p": (344, "46,18")}
)
