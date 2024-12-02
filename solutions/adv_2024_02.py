import typing


def _parse_line(in_line: str) -> list[int]:
    return [int(_) for _ in in_line.split()]


def _parse_input(in_str: str) -> list[list[int]]:
    return [_parse_line(_) for _ in in_str.splitlines()]


def _get_diffs(in_list: list[int]) -> set[int]:
    return {in_list[_ + 1] - in_list[_] for _ in range(len(in_list) - 1)}


def is_safe_a(in_list: list[int]) -> bool:
    diffs = _get_diffs(in_list)
    return diffs <= {1, 2, 3} or diffs <= {-1, -2, -3}


def _count_safe(
    in_list: list[list[int]], is_safe: typing.Callable[[list[int]], bool]
) -> int:
    return sum(1 for _ in in_list if is_safe(_))


def _remove(in_list: list[int], in_pos: int) -> list[int]:
    assert 0 <= in_pos < len(in_list)
    return in_list[0:in_pos] + in_list[in_pos + 1 :]


def is_safe_b(in_list: list[int]) -> bool:
    return any(is_safe_a(_remove(in_list, _)) for _ in range(0, len(in_list)))


def _get_solve(
    is_safe: typing.Callable[[list[int]], bool]
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        return _count_safe(_parse_input(in_str), is_safe)

    return _solve


solve_a = _get_solve(is_safe_a)
solve_b = _get_solve(is_safe_b)
