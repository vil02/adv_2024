import pytest

import solutions.adv_2024_22 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("secret", "expected"),
    [
        (123, 15887950),
        (15887950, 16495136),
        (16495136, 527345),
        (527345, 704524),
        (704524, 1553684),
        (1553684, 12683156),
        (12683156, 11100544),
        (11100544, 12249484),
        (12249484, 7753432),
        (7753432, 5908254),
    ],
)
def test_next_secret(secret: int, expected: int) -> None:
    assert sol.next_secret(secret) == expected


_INPUTS = tu.get_inputs(22, {"small", "p"})

test_solve_a = _INPUTS.get_test(sol.solve_a, {"small": 37327623, "p": 17005483322})
test_solve_b = _INPUTS.get_test(sol.solve_b, {"p": 1910})
