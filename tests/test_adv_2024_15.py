import solutions.adv_2024_15 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(15, {"small", "small_2", "p"})

test_solve_a = _INPUTS.get_test(
    sol.solve_a, {"small": 2028, "small_2": 10092, "p": 1499739}
)

test_solve_b = _INPUTS.get_test(sol.solve_b, {"small_2": 9021, "p": 1522215})
