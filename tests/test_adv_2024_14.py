import solutions.adv_2024_14 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(14, {"p"})

test_solve_a = _INPUTS.get_test(sol.solve_a, {"p": 224438715})
test_solve_b = _INPUTS.get_test(sol.solve_b, {"p": 7603})
