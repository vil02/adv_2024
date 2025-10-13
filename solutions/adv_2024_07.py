import typing


class Equation(typing.NamedTuple):
    result: int
    numbers: list[int]


def _parse_equation(in_line: str) -> Equation:
    result, numbers = in_line.split(": ")
    return Equation(int(result), [int(_) for _ in numbers.split()])


def _parse_input(in_str: str) -> list[Equation]:
    return [_parse_equation(_) for _ in in_str.splitlines()]


def _can_be_simplified_add(_: Equation) -> bool:
    return True


def _simplify_eq_add(equation: Equation) -> Equation:
    return Equation(equation.result - equation.numbers[-1], equation.numbers[:-1])


def _can_be_simplified_multip(equation: Equation) -> bool:
    return equation.result % equation.numbers[-1] == 0


def _simplify_eq_multip(equation: Equation) -> Equation:
    return Equation(equation.result // equation.numbers[-1], equation.numbers[:-1])


def _can_be_converted_to_int(in_str: str) -> bool:
    res = True
    try:
        int(in_str)
    except ValueError:
        res = False
    return res


def _can_be_simplified_concat(equation: Equation) -> bool:
    str_res = str(equation.result)
    last_num_str = str(equation.numbers[-1])
    new_res_str = str_res.removesuffix(last_num_str)
    return str_res.endswith(last_num_str) and _can_be_converted_to_int(new_res_str)


def _simplify_eq_concat(equation: Equation) -> Equation:
    new_res = str(equation.result).removesuffix(str(equation.numbers[-1]))
    return Equation(int(new_res), equation.numbers[:-1])


class _Simplification(typing.NamedTuple):
    is_applicable: typing.Callable[[Equation], bool]
    simplify: typing.Callable[[Equation], Equation]


_PLUS = _Simplification(_can_be_simplified_add, _simplify_eq_add)
_MULTIP = _Simplification(_can_be_simplified_multip, _simplify_eq_multip)
_CONCAT = _Simplification(_can_be_simplified_concat, _simplify_eq_concat)


def _get_can_be_true(
    in_simplifications: list[_Simplification],
) -> typing.Callable[[Equation], bool]:
    def _can_be_true(equation: Equation) -> bool:
        assert len(equation.numbers) > 0
        if len(equation.numbers) == 1:
            return equation.result == equation.numbers[0]
        return any(
            _.is_applicable(equation) and _can_be_true(_.simplify(equation))
            for _ in in_simplifications
        )

    return _can_be_true


can_be_true_a = _get_can_be_true([_PLUS, _MULTIP])
can_be_true_b = _get_can_be_true([_PLUS, _MULTIP, _CONCAT])


def _get_solve(
    can_be_true: typing.Callable[[Equation], bool],
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        return sum(_.result for _ in _parse_input(in_str) if can_be_true(_))

    return _solve


solve_a = _get_solve(can_be_true_a)
solve_b = _get_solve(can_be_true_b)
