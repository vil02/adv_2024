import numpy

Prize = tuple[int, int]
Button = tuple[int, int]
Machine = tuple[Button, Button, Prize]


def _parse_button_shift(button_shift: str) -> int:
    return int(button_shift[2:])


def _parse_button(in_line: str) -> Button:
    assert in_line.startswith("Button ")
    _, buttons = in_line.split(": ")
    shift_x, shift_y = buttons.split(", ")
    return _parse_button_shift(shift_x), _parse_button_shift(shift_y)


def _parse_coordinate(in_coodrinare: str) -> int:
    return int(in_coodrinare[2:])


def _parse_prize(in_line: str) -> Prize:
    assert in_line.startswith("Prize: X=")
    _, coordinates = in_line.split(": ")
    x_pos, y_pos = coordinates.split(", ")
    return _parse_coordinate(x_pos), _parse_coordinate(y_pos)


def _parse_machine(in_str: str) -> Machine:
    button_a, button_b, prize = in_str.splitlines()
    return _parse_button(button_a), _parse_button(button_b), _parse_prize(prize)


def _parse_input(in_str: str) -> list[Machine]:
    return [_parse_machine(_) for _ in in_str.split("\n\n")]


def _total_shift(in_button: Button, moves: int) -> tuple[int, int]:
    return tuple(moves * _ for _ in in_button)


def _add_shifts(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> tuple[int, int]:
    return pos_a[0] + pos_b[0], pos_a[1] + pos_b[1]


def _is_valid(in_machine: Machine, moves_a: int, moves_b: int) -> bool:
    button_a, button_b, prize = in_machine
    shift_a = _total_shift(button_a, moves_a)
    shift_b = _total_shift(button_b, moves_b)
    return prize == _add_shifts(shift_a, shift_b)


def _minimal_num_of_moves(in_machine: Machine) -> int | float:
    button_a, button_b, prize = in_machine
    button_matrix = numpy.array(
        [[button_a[0], button_b[0]], [button_a[1], button_b[1]]]
    )
    prize_matrix = numpy.array([[prize[0]], [prize[1]]])
    solution = numpy.linalg.solve(button_matrix, prize_matrix)

    moves_a = int(round(solution[0].item()))
    moves_b = int(round(solution[1].item()))
    if _is_valid(in_machine, moves_a, moves_b):
        return 3 * moves_a + moves_b
    return numpy.inf


def _update_prize(in_prize: Prize) -> Prize:
    shift = 10000000000000
    return _add_shifts(in_prize, (shift, shift))


def _update_machine(in_machine: Machine) -> Machine:
    button_a, button_b, prize = in_machine
    return button_a, button_b, _update_prize(prize)


def _find_minimal_cost_of_wining_all(machines: list[Machine]) -> int:
    costs = (_minimal_num_of_moves(_) for _ in machines)
    return sum(_ for _ in costs if _ < numpy.inf)


def solve_a(in_str: str) -> int:
    return _find_minimal_cost_of_wining_all(_parse_input(in_str))


def solve_b(in_str: str) -> int:
    return _find_minimal_cost_of_wining_all(
        [_update_machine(_) for _ in _parse_input(in_str)]
    )
