import solutions.adv_2024_13 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(13, {"small", "p"})

test_solve_a = _INPUTS.get_test(sol.solve_a, {"small": 480, "p": 29517})
test_solve_b = _INPUTS.get_test(sol.solve_b, {"p": 103570327981381})
