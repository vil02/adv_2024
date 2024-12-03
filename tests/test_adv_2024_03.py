import solutions.adv_2024_03 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(3, {"small_a", "small_b", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small_a": (161, 161), "small_b": (161, 48), "p": (174103751, 100411201)},
)
