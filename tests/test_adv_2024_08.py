import solutions.adv_2024_08 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(8, {"small", "small_2", "p"})


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (14, 34), "small_2": (3, 9), "p": (293, 934)}
)
