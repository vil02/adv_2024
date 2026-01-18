import solutions.adv_2024_24 as sol
from . import test_utils as tu

_INPUTS = tu.get_inputs(24, {"small", "small_2", "p"})

test_solve_a = _INPUTS.get_test(
    sol.solve_a, {"small": 4, "small_2": 2024, "p": 49520947122770}
)
test_solve_b = _INPUTS.get_test(
    sol.solve_b,
    {
        "p": "gjc,gvm,qjj,qsb,wmp,z17,z26,z39",
    },
)
