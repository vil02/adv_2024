import solutions.adv_2024_06 as sol
from . import test_utils as tu

_INPUTS = tu.get_inputs(6, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (41, 6), "p": (5312, 1748)}
)
