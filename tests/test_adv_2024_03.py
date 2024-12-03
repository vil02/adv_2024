import solutions.adv_2024_03 as sol
from . import test_utils as tu


_INPUTS = tu.get_inputs(3, {"small_a", "small_b", "p"})

test_solve_a_single = _INPUTS.get_test(
    sol.solve_a, {"small_a": 161, "small_b": 161, "p": 174103751}
)
test_solve_b_single = _INPUTS.get_test(
    sol.solve_b, {"small_a": 161, "small_b": 48, "p": 100411201}
)
