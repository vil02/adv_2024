import solutions.adv_2024_01 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(1, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (11, 31), "p": (1941353, 22539317)}
)
