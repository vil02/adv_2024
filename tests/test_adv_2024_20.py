import solutions.adv_2024_20 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(20, {"p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"p": (1311, 961364)}
)
