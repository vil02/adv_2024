import re
import typing


def _evaluate(in_str: str) -> int:
    _prefix = "mul("
    _suffix = ")"
    assert in_str.startswith(_prefix)
    assert in_str.endswith(_suffix)
    str_a, str_b = in_str.removeprefix(_prefix).removesuffix(_suffix).split(",")
    return int(str_a) * int(str_b)


def _sum_prods(in_str: str, is_enabled: typing.Callable[[int], bool]) -> int:
    return sum(
        _evaluate(_.group())
        for _ in re.finditer(r"mul\(\d{1,3},\d{1,3}\)", in_str)
        if is_enabled(_.start())
    )


def solve_a(in_str: str) -> int:
    return _sum_prods(in_str, lambda _: True)


def _find_all_starts(in_str: str, in_pattern: str) -> list[int]:
    return [_.start() for _ in re.finditer(in_pattern, in_str)]


def _pop_from_starts(
    cur_pos: int, cur_value: bool, starts: list[int], new_value: bool
) -> bool:
    if starts:
        assert cur_pos <= starts[0]
        if cur_pos == starts[0]:
            starts.pop(0)
            return new_value
    return cur_value


def _consume_starts(
    in_output_len: int, enabled_starts: list[int], disabled_starts: list[int]
) -> list[bool]:
    assert not set(enabled_starts) & set(disabled_starts)
    res = []
    is_enabled = True
    for _ in range(in_output_len):
        is_enabled = _pop_from_starts(_, is_enabled, enabled_starts, True)
        is_enabled = _pop_from_starts(_, is_enabled, disabled_starts, False)
        res.append(is_enabled)
    return res


def _compute_is_enabled(in_str: str) -> list[bool]:
    return _consume_starts(
        len(in_str),
        _find_all_starts(in_str, r"do\(\)"),
        _find_all_starts(in_str, r"don't\(\)"),
    )


def solve_b(in_str: str) -> int:
    is_enabled_list = _compute_is_enabled(in_str)
    return _sum_prods(in_str, lambda pos: is_enabled_list[pos])
