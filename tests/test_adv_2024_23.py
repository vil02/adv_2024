import solutions.adv_2024_23 as sol
from . import test_utils as tu

_INPUTS = tu.get_inputs(23, {"small", "p"})


test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {
        "small": (7, "co,de,ka,ta"),
        "p": (1423, "gt,ha,ir,jn,jq,kb,lr,lt,nl,oj,pp,qh,vy"),
    },
)
