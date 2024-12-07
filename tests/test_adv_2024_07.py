import solutions.adv_2024_07 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(7, {"small", "p"})


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small": (3749, 11387), "p": (20665830408335, 354060705047464)},
)
