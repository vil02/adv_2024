import solutions.adv_2024_16 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(16, {"small", "small_2", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small": (7036, 45), "small_2": (11048, 64), "p": (85432, 465)},
)
