import solutions.adv_2024_05 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(5, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b), {"small": (143, 123), "p": (5374, 4260)}
)
