import solutions.adv_2024_12 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(12, {"small", "small_2", "small_3", "small_4", "small_5", "p"})

test_solve_a = _INPUTS.get_test(
    sol.solve_a, {"small": 140, "small_2": 772, "small_3": 1930, "p": 1452678}
)


test_solve_b = _INPUTS.get_test(
    sol.solve_b,
    {"small": 80, "small_3": 1206, "small_4": 236, "small_5": 368, "p": 873584},
)
