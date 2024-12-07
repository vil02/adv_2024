import typing


class _Equation(typing.NamedTuple):
    result: int
    numbers: list[int]


def _parse_equation(in_line: str) -> _Equation:
    result, numbers = in_line.split(": ")
    return _Equation(int(result), [int(_) for _ in numbers.split(" ")])


def _parse_input(in_str: str) -> list[_Equation]:
    return [_parse_equation(_) for _ in in_str.splitlines()]


def _simplify_eq_add(equation: _Equation) -> _Equation:
    return _Equation(equation.result - equation.numbers[-1], equation.numbers[:-1])


def _can_be_simplified_multip(equation: _Equation) -> bool:
    return equation.result % equation.numbers[-1] == 0


def _simplify_eq_multip(equation: _Equation) -> _Equation:
    return _Equation(equation.result // equation.numbers[-1], equation.numbers[:-1])


def _can_be_converted_to_int(in_str: str) -> bool:
    res = True
    try:
        int(in_str)
    except ValueError:
        res = False
    return res


def _can_be_simplified_concat(equation: _Equation) -> bool:
    str_res = str(equation.result)
    last_num_str = str(equation.numbers[-1])
    new_res_str = str_res.removesuffix(last_num_str)
    return str_res.endswith(last_num_str) and _can_be_converted_to_int(new_res_str)


def _simplify_eq_concat(equation: _Equation) -> _Equation:
    new_res = str(equation.result).removesuffix(str(equation.numbers[-1]))
    return _Equation(int(new_res), equation.numbers[:-1])


def _can_be_true_a(equation: _Equation) -> bool:
    assert len(equation.numbers) > 0
    if len(equation.numbers) == 1:
        return equation.result == equation.numbers[0]
    res = _can_be_true_a(_simplify_eq_add(equation))
    if not res and _can_be_simplified_multip(equation):
        res |= _can_be_true_a(_simplify_eq_multip(equation))
    return res


def _can_be_true_b(equation: _Equation) -> bool:
    assert len(equation.numbers) > 0
    if len(equation.numbers) == 1:
        return equation.result == equation.numbers[0]
    res = _can_be_true_b(_simplify_eq_add(equation))
    if not res and _can_be_simplified_multip(equation):
        res |= _can_be_true_b(_simplify_eq_multip(equation))
    if not res and _can_be_simplified_concat(equation):
        res |= _can_be_true_b(_simplify_eq_concat(equation))

    return res


def _get_solve(
    can_be_true: typing.Callable[[_Equation], bool]
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        return sum(_.result for _ in _parse_input(in_str) if can_be_true(_))

    return _solve


solve_a = _get_solve(_can_be_true_a)
solve_b = _get_solve(_can_be_true_b)
