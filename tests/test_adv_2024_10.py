import solutions.adv_2024_10 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(10, {"small", "p", "r"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (36, 81), "p": (782, 1694), "r": (464, 16451)}
)
