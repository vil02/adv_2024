import solutions.adv_2024_04 as sol
from . import test_utils as tu

_INPUTS = tu.get_inputs(4, {"small", "p"})


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (18, 9), "p": (2468, 1864)}
)
