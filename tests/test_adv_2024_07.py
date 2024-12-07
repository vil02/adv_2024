import pytest

import solutions.adv_2024_07 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("equation", "expected"),
    [
        (sol.Equation(10, [10]), True),
        (sol.Equation(10, [11]), False),
        (sol.Equation(190, [10, 19]), True),
        (sol.Equation(3267, [81, 40, 27]), True),
        (sol.Equation(83, [17, 5]), False),
        (sol.Equation(156, [15, 6]), False),
        (sol.Equation(7290, [6, 8, 6, 15]), False),
        (sol.Equation(161011, [16, 10, 13]), False),
        (sol.Equation(192, [17, 8, 14]), False),
        (sol.Equation(21037, [9, 7, 18, 13]), False),
        (sol.Equation(292, [11, 6, 16, 20]), True),
    ],
)
def test_can_be_true_a(equation: sol.Equation, expected: bool) -> None:
    assert sol.can_be_true_a(equation) == expected


@pytest.mark.parametrize(
    ("equation", "expected"),
    [
        (sol.Equation(10, [10]), True),
        (sol.Equation(10, [11]), False),
        (sol.Equation(11, [1, 1]), True),
        (sol.Equation(190, [10, 19]), True),
        (sol.Equation(3267, [81, 40, 27]), True),
        (sol.Equation(83, [17, 5]), False),
        (sol.Equation(156, [15, 6]), True),
        (sol.Equation(7290, [6, 8, 6, 15]), True),
        (sol.Equation(161011, [16, 10, 13]), False),
        (sol.Equation(192, [17, 8, 14]), True),
        (sol.Equation(21037, [9, 7, 18, 13]), False),
        (sol.Equation(292, [11, 6, 16, 20]), True),
    ],
)
def test_can_be_true_b(equation: sol.Equation, expected: bool) -> None:
    assert sol.can_be_true_b(equation) == expected


_INPUTS = tu.get_inputs(7, {"small", "p"})


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small": (3749, 11387), "p": (20665830408335, 354060705047464)},
)
