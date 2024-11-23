import solutions.adv_2024_00 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(0, {"small", "p"})

test_solve_a_single = _INPUTS.get_test(sol.solve_a, {"small": 5, "p": 9})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (5, 10), "p": (9, 18)}
)
